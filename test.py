import argparse
import csv
import json
import logging
import os
import random
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch
import torch.backends.cudnn as cudnn
import torch.nn as nn
from torch.utils.data import DataLoader
from tqdm import tqdm
from experiment_utils import (
    apply_attention_config,
    apply_reverse_attention_config,
    build_attention_suffix,
    build_reverse_attention_suffix,
    build_skip_indices_suffix,
    parse_attention_scales,
    parse_reverse_attention_scales,
    parse_skip_indices,
)

CLASS_NAMES = (
    "background",
    "aorta",
    "gallbladder",
    "kidney_left",
    "kidney_right",
    "liver",
    "pancreas",
    "spleen",
    "stomach",
)

parser = argparse.ArgumentParser()
parser.add_argument('--volume_path', type=str,
                    default='./data/Synapse/test_vol_h5', help='root dir for validation volume data')  # for acdc volume_path=root_dir
parser.add_argument('--dataset', type=str,
                    default='Synapse', help='experiment_name')
parser.add_argument('--num_classes', type=int,
                    default=9, help='output channel of network')
parser.add_argument('--list_dir', type=str,
                    default='./splits/synapse', help='split dir')
parser.add_argument('--batch_size', type=int, default=24,
                    help='batch_size per gpu')
parser.add_argument('--img_size', type=int, default=224, help='input patch size of network input')
parser.add_argument('--is_savenii', action="store_true", help='whether to save results during inference')

parser.add_argument('--n_skip', type=int, default=3, help='using number of skip-connect, default is num')
parser.add_argument('--skip_indices', type=str, default='',
                    help='comma-separated skip indices to use, e.g. "1,2"')
parser.add_argument('--vit_name', type=str, default='ViT-B_16', help='select one vit model')

parser.add_argument('--test_save_dir', type=str, default='../predictions', help='saving prediction as nii!')
parser.add_argument('--deterministic', type=int,  default=1, help='whether use deterministic training')
parser.add_argument('--base_lr', type=float,  default=0.01, help='segmentation network learning rate')
parser.add_argument('--seed', type=int, default=1234, help='random seed')
parser.add_argument('--vit_patches_size', type=int, default=16, help='vit_patches_size, default is 16')
parser.add_argument('--max_iterations', type=int, default=30000,
                    help='max iterations used to reconstruct the training snapshot name during evaluation')
parser.add_argument('--max_epochs', type=int, default=30,
                    help='max epochs used to reconstruct the training snapshot name during evaluation')
parser.add_argument('--attention_mode', type=str,
                    default='none', choices=['none', 'pre_hidden', 'cnn_fusion'],
                    help='where to inject CNN attention before the transformer')
parser.add_argument('--attention_scales', type=str,
                    default='',
                    help='comma-separated CNN scales, e.g. 1/8,1/4,1/2')
parser.add_argument('--attention_reduction', type=int,
                    default=16, help='channel reduction used by the CNN attention blocks')
parser.add_argument('--ra_mode', type=str, default='none',
                    choices=['none', 'ra_skip', 'ra_bridge', 'ra_fusion'],
                    help='reverse attention mode for decoder bridge, skip, or post-fusion features')
parser.add_argument('--ra_scales', type=str, default='0',
                    help='comma-separated skip or fusion block indices for RA, e.g. "0" or "0,1,2"')
parser.add_argument('--ra_reduction', type=int, default=4,
                    help='bottleneck reduction ratio for reverse attention')
parser.add_argument('--run_id', type=str, default='',
                    help='stable experiment id used for artifact export')
parser.add_argument('--artifact_root', type=str, default='./artifacts/runs',
                    help='root directory for per-run artifacts when --run_id is provided')
parser.add_argument('--drive_export_dir', type=str, default='',
                    help='optional Google Drive directory where the completed artifact folder and zip are mirrored')
parser.add_argument('--export_artifact_zip', action='store_true',
                    help='zip the per-run artifact directory after evaluation')
args = parser.parse_args()


def finite_or_none(value):
    if value is None:
        return None
    value = float(value)
    if np.isnan(value) or np.isinf(value):
        return None
    return value


def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding='utf-8')


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def summarize_per_class(metric_list, confusion, class_names):
    confusion = np.asarray(confusion, dtype=np.int64)
    true_counts = confusion.sum(axis=1)
    predicted_counts = confusion.sum(axis=0)
    diagonal = np.diag(confusion)
    rows = []
    for class_id in range(1, len(class_names)):
        metric_index = class_id - 1
        accuracy = (
            float(diagonal[class_id] / true_counts[class_id])
            if true_counts[class_id]
            else None
        )
        rows.append(
            {
                'class_id': class_id,
                'class_name': class_names[class_id],
                'mean_dice': finite_or_none(metric_list[metric_index][0]),
                'mean_hd95': finite_or_none(metric_list[metric_index][1]),
                'mean_jaccard': finite_or_none(metric_list[metric_index][2]),
                'accuracy': accuracy,
                'accuracy_percent': finite_or_none(accuracy * 100) if accuracy is not None else None,
                'true_voxels': int(true_counts[class_id]),
                'predicted_voxels': int(predicted_counts[class_id]),
                'correct_voxels': int(diagonal[class_id]),
            }
        )
    return rows


def per_case_rows(case_name, metric_i, confusion_i, class_names):
    confusion_i = np.asarray(confusion_i, dtype=np.int64)
    true_counts = confusion_i.sum(axis=1)
    predicted_counts = confusion_i.sum(axis=0)
    diagonal = np.diag(confusion_i)
    rows = []
    for class_id in range(1, len(class_names)):
        metric_index = class_id - 1
        true_voxels = int(true_counts[class_id])
        predicted_voxels = int(predicted_counts[class_id])
        if true_voxels == 0 and predicted_voxels == 0:
            presence_status = 'empty_true_negative'
        elif true_voxels == 0:
            presence_status = 'false_positive'
        elif predicted_voxels == 0:
            presence_status = 'false_negative'
        else:
            presence_status = 'present'
        accuracy = (
            float(diagonal[class_id] / true_voxels)
            if true_voxels
            else None
        )
        rows.append(
            {
                'case_name': case_name,
                'class_id': class_id,
                'class_name': class_names[class_id],
                'dice': finite_or_none(metric_i[metric_index][0]),
                'hd95': finite_or_none(metric_i[metric_index][1]),
                'jaccard': finite_or_none(metric_i[metric_index][2]),
                'accuracy': finite_or_none(accuracy),
                'accuracy_percent': finite_or_none(accuracy * 100) if accuracy is not None else None,
                'presence_status': presence_status,
                'true_voxels': true_voxels,
                'predicted_voxels': predicted_voxels,
                'correct_voxels': int(diagonal[class_id]),
            }
        )
    return rows


def serialize_args(args):
    payload = {}
    for key, value in vars(args).items():
        if key == 'Dataset':
            payload[key] = getattr(value, '__name__', str(value))
        elif isinstance(value, tuple):
            payload[key] = list(value)
        else:
            payload[key] = value
    return payload


def zip_directory(source_dir, zip_path):
    source_dir = Path(source_dir)
    zip_path = Path(zip_path)
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zip_file:
        for path in sorted(source_dir.rglob('*')):
            if not path.is_file() or path == zip_path:
                continue
            zip_file.write(path, path.relative_to(source_dir))
    return zip_path


def mirror_artifact_directory(source_dir, drive_dir):
    source_dir = Path(source_dir)
    drive_dir = Path(drive_dir)
    drive_dir.mkdir(parents=True, exist_ok=True)
    try:
        drive_resolved = drive_dir.resolve()
    except FileNotFoundError:
        drive_resolved = drive_dir

    for path in sorted(source_dir.rglob('*')):
        if not path.is_file():
            continue
        target = drive_dir / path.relative_to(source_dir)
        try:
            if path.resolve() == target.resolve():
                continue
        except FileNotFoundError:
            pass
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            if target.resolve().is_relative_to(source_dir.resolve()):
                continue
        except (AttributeError, FileNotFoundError):
            if str(drive_resolved).startswith(str(source_dir.resolve())):
                continue
        shutil.copy2(path, target)


def export_artifacts(args, snapshot_name, checkpoint_path, log_file, metrics, per_class, per_case, confusion):
    if not args.run_id:
        return None

    artifact_dir = Path(args.artifact_root) / args.run_id
    artifact_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_dir = artifact_dir / 'checkpoints'
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    copied_checkpoint = None
    if checkpoint_path and Path(checkpoint_path).exists():
        source_checkpoint = Path(checkpoint_path)
        checkpoint_name = 'latest_checkpoint.pth' if source_checkpoint.name == 'latest_checkpoint.pth' else source_checkpoint.name
        copied_checkpoint = checkpoint_dir / checkpoint_name
        if source_checkpoint.resolve() != copied_checkpoint.resolve():
            shutil.copy2(source_checkpoint, copied_checkpoint)

    if log_file and Path(log_file).exists():
        shutil.copy2(log_file, artifact_dir / 'test.log')

    write_json(artifact_dir / 'config.json', serialize_args(args))
    write_json(
        artifact_dir / 'commands.json',
        {
            'argv': sys.argv,
            'test_command': ' '.join(sys.argv),
        },
    )
    write_json(artifact_dir / 'metrics.json', metrics)
    write_json(
        artifact_dir / 'confusion_matrix.json',
        {
            'class_names': CLASS_NAMES[:args.num_classes],
            'matrix': confusion.tolist(),
        },
    )
    write_csv(
        artifact_dir / 'per_class_metrics.csv',
        per_class,
        [
            'class_id',
            'class_name',
            'mean_dice',
            'mean_hd95',
            'mean_jaccard',
            'accuracy',
            'accuracy_percent',
            'true_voxels',
            'predicted_voxels',
            'correct_voxels',
        ],
    )
    write_csv(
        artifact_dir / 'per_case_metrics.csv',
        per_case,
        [
            'case_name',
            'class_id',
            'class_name',
            'dice',
            'hd95',
            'jaccard',
            'accuracy',
            'accuracy_percent',
            'presence_status',
            'true_voxels',
            'predicted_voxels',
            'correct_voxels',
        ],
    )

    zip_path = None
    if args.export_artifact_zip or args.run_id:
        zip_path = artifact_dir / f'{args.run_id}__{snapshot_name}.zip'

    manifest = {
        'schema_version': 1,
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'run_id': args.run_id,
        'snapshot_name': snapshot_name,
        'artifact_dir': str(artifact_dir),
        'checkpoint_source': str(checkpoint_path) if checkpoint_path else None,
        'checkpoint_artifact': str(copied_checkpoint) if copied_checkpoint else None,
        'prediction_dir': str(artifact_dir / 'predictions'),
        'metrics_json': str(artifact_dir / 'metrics.json'),
        'per_case_metrics_csv': str(artifact_dir / 'per_case_metrics.csv'),
        'per_class_metrics_csv': str(artifact_dir / 'per_class_metrics.csv'),
        'confusion_matrix_json': str(artifact_dir / 'confusion_matrix.json'),
        'artifact_zip': str(zip_path) if zip_path else None,
        'drive_export_dir': str(args.drive_export_dir) if args.drive_export_dir else None,
    }
    write_json(artifact_dir / 'manifest.json', manifest)
    if zip_path:
        zip_directory(artifact_dir, zip_path)
    if args.drive_export_dir:
        drive_dir = Path(args.drive_export_dir) / args.run_id
        mirror_artifact_directory(artifact_dir, drive_dir)
    return manifest


def inference(args, model, test_save_path=None):
    from utils import summarize_accuracy_confusion, test_single_volume

    class_names = CLASS_NAMES[:args.num_classes]
    db_test = args.Dataset(
        base_dir=args.volume_path,
        split="test_vol",
        list_dir=args.list_dir,
    )
    testloader = DataLoader(db_test, batch_size=1, shuffle=False, num_workers=1)
    logging.info("{} test iterations per epoch".format(len(testloader)))
    model.eval()
    metric_list = np.zeros((args.num_classes - 1, 3), dtype=np.float64)
    confusion = np.zeros((args.num_classes, args.num_classes), dtype=np.int64)
    per_case = []
    for i_batch, sampled_batch in tqdm(enumerate(testloader)):
        h, w = sampled_batch["image"].size()[2:]
        image, label, case_name = sampled_batch["image"], sampled_batch["label"], sampled_batch['case_name'][0]
        metric_i, confusion_i = test_single_volume(
            image,
            label,
            model,
            classes=args.num_classes,
            patch_size=[args.img_size, args.img_size],
            test_save_path=test_save_path,
            case=case_name,
            z_spacing=args.z_spacing,
            return_confusion=True,
        )
        metric_i = np.array(metric_i, dtype=np.float64)
        metric_list += metric_i
        confusion += confusion_i
        per_case.extend(per_case_rows(case_name, metric_i, confusion_i, class_names))
        logging.info(
            'idx %d case %s mean_dice %f mean_hd95 %f mean_jaccard %f'
            % (
                i_batch,
                case_name,
                np.mean(metric_i, axis=0)[0],
                np.mean(metric_i, axis=0)[1],
                np.mean(metric_i, axis=0)[2],
            )
        )
    metric_list = metric_list / len(db_test)
    for i in range(1, args.num_classes):
        logging.info(
            'Mean class %d mean_dice %f mean_hd95 %f mean_jaccard %f'
            % (i, metric_list[i-1][0], metric_list[i-1][1], metric_list[i-1][2])
        )
    performance = np.mean(metric_list, axis=0)[0]
    mean_hd95 = np.mean(metric_list, axis=0)[1]
    mean_jaccard = np.mean(metric_list, axis=0)[2]
    logging.info(
        'Testing performance in best val model: mean_dice : %f mean_hd95 : %f mean_jaccard : %f'
        % (performance, mean_hd95, mean_jaccard)
    )
    accuracy = summarize_accuracy_confusion(confusion)
    for i in range(1, args.num_classes):
        logging.info('Accuracy class %d recall %f' % (i, accuracy["class_accuracy"][i]))
    logging.info(
        'Accuracy performance: voxel_accuracy : %f foreground_voxel_accuracy : %f '
        'mean_foreground_accuracy : %f pancreas_accuracy : %f'
        % (
            accuracy["voxel_accuracy"],
            accuracy["foreground_voxel_accuracy"],
            accuracy["mean_foreground_accuracy"],
            accuracy["pancreas_accuracy"],
        )
    )
    per_class = summarize_per_class(metric_list, confusion, class_names)
    pancreas_index = 6 - 1
    metrics = {
        'run_id': args.run_id or None,
        'dataset': args.dataset,
        'snapshot_name': getattr(args, 'snapshot_name', None),
        'case_count': len(db_test),
        'overall': {
            'mean_dice': finite_or_none(performance),
            'mean_dice_percent': finite_or_none(performance * 100),
            'mean_hd95': finite_or_none(mean_hd95),
            'mean_jaccard': finite_or_none(mean_jaccard),
            'mean_jaccard_percent': finite_or_none(mean_jaccard * 100),
        },
        'pancreas': {
            'mean_dice': finite_or_none(metric_list[pancreas_index][0]) if pancreas_index < len(metric_list) else None,
            'mean_dice_percent': finite_or_none(metric_list[pancreas_index][0] * 100) if pancreas_index < len(metric_list) else None,
            'mean_hd95': finite_or_none(metric_list[pancreas_index][1]) if pancreas_index < len(metric_list) else None,
            'mean_jaccard': finite_or_none(metric_list[pancreas_index][2]) if pancreas_index < len(metric_list) else None,
            'mean_jaccard_percent': finite_or_none(metric_list[pancreas_index][2] * 100) if pancreas_index < len(metric_list) else None,
        },
        'accuracy': {
            'voxel_accuracy': finite_or_none(accuracy["voxel_accuracy"]),
            'voxel_accuracy_percent': finite_or_none(accuracy["voxel_accuracy"] * 100),
            'foreground_voxel_accuracy': finite_or_none(accuracy["foreground_voxel_accuracy"]),
            'foreground_voxel_accuracy_percent': finite_or_none(accuracy["foreground_voxel_accuracy"] * 100),
            'mean_foreground_accuracy': finite_or_none(accuracy["mean_foreground_accuracy"]),
            'mean_foreground_accuracy_percent': finite_or_none(accuracy["mean_foreground_accuracy"] * 100),
            'pancreas_accuracy': finite_or_none(accuracy["pancreas_accuracy"]),
            'pancreas_accuracy_percent': finite_or_none(accuracy["pancreas_accuracy"] * 100),
            'class_accuracy': [finite_or_none(value) for value in accuracy["class_accuracy"]],
            'class_accuracy_percent': [finite_or_none(value * 100) for value in accuracy["class_accuracy"]],
        },
        'per_class': per_class,
    }
    return metrics, per_class, per_case, confusion


if __name__ == "__main__":
    from datasets.synapse import Synapse_dataset
    from networks.vit_seg_modeling import CONFIGS as CONFIGS_ViT_seg
    from networks.vit_seg_modeling import VisionTransformer as ViT_seg

    if not args.deterministic:
        cudnn.benchmark = True
        cudnn.deterministic = False
    else:
        cudnn.benchmark = False
        cudnn.deterministic = True
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(args.seed)

    dataset_config = {
        'Synapse': {
            'Dataset': Synapse_dataset,
            'volume_path': './data/Synapse/test_vol_h5',
            'list_dir': './splits/synapse',
            'num_classes': 9,
            'z_spacing': 1,
        },
    }
    dataset_name = args.dataset
    args.num_classes = dataset_config[dataset_name]['num_classes']
    args.volume_path = os.environ.get('TRANSUNET_TEST_DATA_DIR', args.volume_path)
    args.Dataset = dataset_config[dataset_name]['Dataset']
    args.list_dir = dataset_config[dataset_name]['list_dir']
    args.z_spacing = dataset_config[dataset_name]['z_spacing']
    args.is_pretrain = True
    args.attention_scales = parse_attention_scales(args.attention_mode, args.attention_scales)
    args.ra_scales = parse_reverse_attention_scales(args.ra_mode, args.ra_scales)
    args.skip_indices = parse_skip_indices(args.skip_indices)
    if args.attention_mode != 'none' and 'R50' not in args.vit_name:
        raise ValueError('CNN attention modes require a hybrid R50-ViT backbone.')

    # name the same snapshot defined in train script!
    args.exp = 'TU_' + dataset_name + str(args.img_size)
    snapshot_path = "./model/{}/{}".format(args.exp, 'TU')
    snapshot_path = snapshot_path + '_pretrain' if args.is_pretrain else snapshot_path
    snapshot_path += '_' + args.vit_name
    snapshot_path = snapshot_path + '_skip' + str(args.n_skip)
    snapshot_path = snapshot_path + '_vitpatch' + str(args.vit_patches_size) if args.vit_patches_size!=16 else snapshot_path
    snapshot_path = snapshot_path+'_'+str(args.max_iterations)[0:2]+'k' if args.max_iterations != 30000 else snapshot_path
    snapshot_path = snapshot_path + '_epo' + str(args.max_epochs) if args.max_epochs != 30 else snapshot_path
    snapshot_path = snapshot_path+'_bs'+str(args.batch_size)
    snapshot_path = snapshot_path + '_lr' + str(args.base_lr) if args.base_lr != 0.01 else snapshot_path
    snapshot_path = snapshot_path + '_'+str(args.img_size)
    snapshot_path = snapshot_path + '_s'+str(args.seed) if args.seed!=1234 else snapshot_path
    snapshot_path = snapshot_path + build_attention_suffix(
        args.attention_mode,
        args.attention_scales,
        args.attention_reduction,
    )

    snapshot_path = snapshot_path + build_reverse_attention_suffix(
        args.ra_mode,
        args.ra_scales,
        args.ra_reduction,
    )

    snapshot_path = snapshot_path + build_skip_indices_suffix(args.skip_indices)

    config_vit = CONFIGS_ViT_seg[args.vit_name]
    config_vit.n_classes = args.num_classes
    config_vit.n_skip = args.n_skip
    if args.skip_indices:
        config_vit.skip_indices = args.skip_indices
    config_vit.patches.size = (args.vit_patches_size, args.vit_patches_size)
    apply_attention_config(
        config_vit,
        mode=args.attention_mode,
        scales=args.attention_scales,
        reduction=args.attention_reduction,
    )
    apply_reverse_attention_config(
        config_vit,
        mode=args.ra_mode,
        scales=args.ra_scales,
        reduction=args.ra_reduction,
    )
    if args.vit_name.find('R50') !=-1:
        config_vit.patches.grid = (int(args.img_size/args.vit_patches_size), int(args.img_size/args.vit_patches_size))
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    net = ViT_seg(config_vit, img_size=args.img_size, num_classes=config_vit.n_classes).to(device)

    model_dir = os.environ.get('TRANSUNET_MODEL_DIR', None)
    checkpoint_dir = os.environ.get('TRANSUNET_CHECKPOINT_DIR', None)

    if model_dir:
        snapshot = os.path.join(model_dir, 'epoch_' + str(args.max_epochs - 1) + '.pth')
        if not os.path.exists(snapshot):
            snapshot = os.path.join(model_dir, 'best_model.pth')
    else:
        snapshot = os.path.join(snapshot_path, 'best_model.pth')
        if not os.path.exists(snapshot):
            snapshot = snapshot.replace('best_model', 'epoch_' + str(args.max_epochs - 1))

    snapshot_name = snapshot_path.split('/')[-1]
    if checkpoint_dir:
        resume_snapshot = os.path.join(checkpoint_dir, 'latest_checkpoint.pth')
    else:
        resume_snapshot = None

    checkpoint_path_used = None
    if os.path.exists(snapshot):
        state = torch.load(snapshot, map_location=device)
        net.load_state_dict(state)
        checkpoint_path_used = snapshot
    elif resume_snapshot and os.path.exists(resume_snapshot):
        state = torch.load(resume_snapshot, map_location=device)
        if isinstance(state, dict) and 'model_state' in state:
            net.load_state_dict(state['model_state'])
        else:
            net.load_state_dict(state)
        checkpoint_path_used = resume_snapshot
        logging_message = f"Using resume checkpoint from {resume_snapshot}"
        print(logging_message)
    else:
        raise FileNotFoundError(
            f"No evaluation checkpoint found. Checked {snapshot}"
            + (f" and {resume_snapshot}" if resume_snapshot else "")
        )
    args.snapshot_name = snapshot_name

    log_folder = './test_log/test_log_' + args.exp
    os.makedirs(log_folder, exist_ok=True)
    log_file = os.path.join(log_folder, snapshot_name + ".txt")
    logging.basicConfig(filename=log_file, level=logging.INFO, format='[%(asctime)s.%(msecs)03d] %(message)s', datefmt='%H:%M:%S')
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logging.info(str(args))
    logging.info(snapshot_name)

    if args.run_id:
        artifact_dir = Path(args.artifact_root) / args.run_id
        test_save_path = artifact_dir / 'predictions'
        os.makedirs(test_save_path, exist_ok=True)
        args.is_savenii = True
        args.test_save_dir = str(test_save_path)
    elif args.is_savenii:
        args.test_save_dir = './predictions'
        test_save_path = os.path.join(args.test_save_dir, args.exp, snapshot_name)
        os.makedirs(test_save_path, exist_ok=True)
    else:
        test_save_path = None
    metrics, per_class, per_case, confusion = inference(args, net, test_save_path)
    manifest = export_artifacts(
        args,
        snapshot_name=snapshot_name,
        checkpoint_path=checkpoint_path_used,
        log_file=log_file,
        metrics=metrics,
        per_class=per_class,
        per_case=per_case,
        confusion=confusion,
    )
    if manifest:
        logging.info("Artifact manifest: %s", manifest["artifact_dir"])
    print("Testing Finished!")


