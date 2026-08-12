import numpy as np
import torch
from medpy import metric
from scipy.ndimage import zoom
import torch.nn as nn
import SimpleITK as sitk
from pathlib import Path


class DiceLoss(nn.Module):
    def __init__(self, n_classes):
        super(DiceLoss, self).__init__()
        self.n_classes = n_classes

    def _one_hot_encoder(self, input_tensor):
        tensor_list = []
        for i in range(self.n_classes):
            temp_prob = input_tensor == i  # * torch.ones_like(input_tensor)
            tensor_list.append(temp_prob.unsqueeze(1))
        output_tensor = torch.cat(tensor_list, dim=1)
        return output_tensor.float()

    def _dice_loss(self, score, target):
        target = target.float()
        smooth = 1e-5
        intersect = torch.sum(score * target)
        y_sum = torch.sum(target * target)
        z_sum = torch.sum(score * score)
        loss = (2 * intersect + smooth) / (z_sum + y_sum + smooth)
        loss = 1 - loss
        return loss

    def forward(self, inputs, target, weight=None, softmax=False):
        if softmax:
            inputs = torch.softmax(inputs, dim=1)
        target = self._one_hot_encoder(target)
        if weight is None:
            weight = [1] * self.n_classes
        assert inputs.size() == target.size(), 'predict {} & target {} shape do not match'.format(inputs.size(), target.size())
        class_wise_dice = []
        loss = 0.0
        for i in range(0, self.n_classes):
            dice = self._dice_loss(inputs[:, i], target[:, i])
            class_wise_dice.append(1.0 - dice.item())
            loss += dice * weight[i]
        return loss / self.n_classes


def calculate_metric_percase(pred, gt):
    pred[pred > 0] = 1
    gt[gt > 0] = 1
    if pred.sum() > 0 and gt.sum()>0:
        dice = metric.binary.dc(pred, gt)
        hd95 = metric.binary.hd95(pred, gt)
        jaccard = metric.binary.jc(pred, gt)
        return dice, hd95, jaccard
    # Do not score false positives as perfect Dice when the ground truth is empty.
    # Empty true-negative cases are tracked separately in per-case artifacts.
    return 0, 0, 0


def calculate_confusion_matrix(prediction, label, classes):
    prediction = np.asarray(prediction, dtype=np.int64).ravel()
    label = np.asarray(label, dtype=np.int64).ravel()
    valid = (
        (label >= 0)
        & (label < classes)
        & (prediction >= 0)
        & (prediction < classes)
    )
    encoded = classes * label[valid] + prediction[valid]
    return np.bincount(encoded, minlength=classes ** 2).reshape(classes, classes)


def summarize_accuracy_confusion(confusion, pancreas_class=6):
    confusion = np.asarray(confusion, dtype=np.int64)
    true_counts = confusion.sum(axis=1)
    diagonal = np.diag(confusion)
    total = confusion.sum()

    class_accuracy = np.divide(
        diagonal,
        true_counts,
        out=np.full(diagonal.shape, np.nan, dtype=np.float64),
        where=true_counts != 0,
    )
    foreground_accuracy = (
        float(diagonal[1:].sum() / true_counts[1:].sum())
        if true_counts[1:].sum()
        else float("nan")
    )
    return {
        "voxel_accuracy": float(diagonal.sum() / total) if total else float("nan"),
        "foreground_voxel_accuracy": foreground_accuracy,
        "mean_foreground_accuracy": float(np.nanmean(class_accuracy[1:])),
        "pancreas_accuracy": (
            float(class_accuracy[pancreas_class])
            if pancreas_class < len(class_accuracy)
            else float("nan")
        ),
        "class_accuracy": class_accuracy,
    }


def test_single_volume(image, label, net, classes, patch_size=[256, 256], test_save_path=None, case=None, z_spacing=1,
                       return_confusion=False):
    device = next(net.parameters()).device
    image, label = image.squeeze(0).cpu().detach().numpy(), label.squeeze(0).cpu().detach().numpy()
    if len(image.shape) == 3:
        prediction = np.zeros_like(label)
        for ind in range(image.shape[0]):
            slice = image[ind, :, :]
            x, y = slice.shape[0], slice.shape[1]
            if x != patch_size[0] or y != patch_size[1]:
                slice = zoom(slice, (patch_size[0] / x, patch_size[1] / y), order=3)  # previous using 0
            input = torch.from_numpy(slice).unsqueeze(0).unsqueeze(0).float().to(device)
            net.eval()
            with torch.no_grad():
                outputs = net(input)
                out = torch.argmax(torch.softmax(outputs, dim=1), dim=1).squeeze(0)
                out = out.cpu().detach().numpy()
                if x != patch_size[0] or y != patch_size[1]:
                    pred = zoom(out, (x / patch_size[0], y / patch_size[1]), order=0)
                else:
                    pred = out
                prediction[ind] = pred
    else:
        input = torch.from_numpy(image).unsqueeze(
            0).unsqueeze(0).float().to(device)
        net.eval()
        with torch.no_grad():
            out = torch.argmax(torch.softmax(net(input), dim=1), dim=1).squeeze(0)
            prediction = out.cpu().detach().numpy()
    metric_list = []
    for i in range(1, classes):
        metric_list.append(calculate_metric_percase(prediction == i, label == i))

    if test_save_path is not None:
        test_save_path = Path(test_save_path)
        test_save_path.mkdir(parents=True, exist_ok=True)
        img_itk = sitk.GetImageFromArray(image.astype(np.float32))
        prd_itk = sitk.GetImageFromArray(prediction.astype(np.float32))
        lab_itk = sitk.GetImageFromArray(label.astype(np.float32))
        img_itk.SetSpacing((1, 1, z_spacing))
        prd_itk.SetSpacing((1, 1, z_spacing))
        lab_itk.SetSpacing((1, 1, z_spacing))
        sitk.WriteImage(prd_itk, str(test_save_path / f"{case}_pred.nii.gz"))
        sitk.WriteImage(img_itk, str(test_save_path / f"{case}_img.nii.gz"))
        sitk.WriteImage(lab_itk, str(test_save_path / f"{case}_gt.nii.gz"))
    if return_confusion:
        return metric_list, calculate_confusion_matrix(prediction, label, classes)
    return metric_list
