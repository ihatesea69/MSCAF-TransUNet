# MSCAF-TransUNet Result Registry

This registry keeps lightweight, source-control friendly result records. Full binary artifacts stay outside Git under `artifacts/runs/<run_id>/` and are mirrored to Google Drive as full run folders plus run-specific zip files.

## Numbered LaTeX Rows

| STT | Run | Notebook | Method | Pancreas Dice | Pancreas HD95 | Pancreas Jaccard | Pancreas Accuracy | Artifact status |
|---:|---|---|---|---:|---:|---:|---:|---|
| 01 | `baseline_reproduction` | `notebooks/01-baseline-transunet.ipynb` | TransUNet baseline, project training flow | 54.3675% | 15.3753 | 39.6635% | 44.4120% | completed and exported |
| 02 | `mscaf_cnn_fusion_3scale` | `notebooks/02-mscaf-cbam-da-ty-le.ipynb` | CBAM multi-scale CNN fusion | 58.9334% | 13.2034 | 44.2381% | 50.2227% | completed and exported |
| 03 | `pre_hidden_1_16_r16_run_03` | `notebooks/07-cbam-truoc-patch-embedding-c.ipynb` | CBAM before patch embedding | 59.2291% | 12.9671 | 43.9398% | 48.9431% | completed and exported |
| 04 | `reverse_attention_s0_r4_run_01` | `notebooks/05-cbam-reverse-attention-skip.ipynb` | CBAM + RA on skip feature | 58.3154% | 32.1677 | 42.9503% | 52.3272% | completed and exported |
| 05 | `reverse_bottleneck_fusion_s0_r4_run_01` | `notebooks/06-cbam-reverse-attention-sau-concat.ipynb` | CBAM + RA after decoder-skip concat | 55.9470% | 13.1270 | 40.9862% | 46.2828% | completed and exported |

The LaTeX paper references these five architecture rows through `docs/results/run_registry.json`. The registry is authoritative for `run_id`, notebook path, architecture arguments, snapshot name, artifact paths, and verified metrics. `Pancreas Accuracy` is stored as `accuracy.pancreas_accuracy_percent` and calculated as `TP / (TP + FN)` for Synapse pancreas class `6`.

## Mô Hình Đề Xuất Chính

Mô hình được chọn để báo cáo như cấu hình đề xuất chính là `CBAM before patch embedding`, tương ứng với `run_id = pre_hidden_1_16_r16_run_03` và notebook `notebooks/07-cbam-truoc-patch-embedding-c.ipynb`.

Lý do chọn: cấu hình này đồng thời đạt Pancreas Dice cao nhất `59.2291%` và Pancreas HD95 thấp nhất `12.9671 mm` trong năm dòng kiến trúc được báo cáo. So với TransUNet baseline thực nghiệm, Dice tăng `+4.86` điểm phần trăm và HD95 giảm `-2.41 mm`. Các dòng CBAM đa tỷ lệ và Reverse Attention được giữ trong paper như ablation để thể hiện trade-off giữa Jaccard, accuracy và chất lượng biên.

## Artifact Schema

Notebooks `01`-`07` use the same old-git Colab flow: materialize the project source snapshot, prepare Synapse data and ViT weights from Drive, run `train.py`, then run `test.py` with `--run_id` so artifacts are exported consistently. When `test.py` receives `--run_id`, it exports:

- `manifest.json`
- `config.json`
- `commands.json`
- `metrics.json`
- `per_case_metrics.csv`
- `per_class_metrics.csv`
- `confusion_matrix.json`
- `checkpoints/latest_checkpoint.pth` or the evaluated checkpoint
- `predictions/*_pred.nii.gz`, `*_gt.nii.gz`, `*_img.nii.gz`
- `<run_id>__<snapshot_name>.zip`

The run-specific zip name prevents the old ambiguity where two `pre_hidden` runs shared the same snapshot filename. Every runner keeps the local artifact folder under `artifacts/runs/<run_id>/` and mirrors the full folder plus zip to Drive under `transunet_colab_outputs/runs/<run_id>/`.

## Accuracy Backfill

Accuracy cannot be derived from Dice and HD95 alone. Use `notebooks/transunet-calculate-artifact-accuracy.ipynb` when retained NIfTI predictions still exist. For checkpoint-only recovery, open the matching numbered notebook and set `RUN_TRAIN = False`, `RUN_TEST = True` so inference is rerun and full artifacts are regenerated.

Reported accuracy fields:

- `voxel_accuracy`: all correctly classified voxels divided by all voxels, including background
- `foreground_voxel_accuracy`: correctly classified organ voxels divided by all ground-truth organ voxels
- `mean_foreground_accuracy`: macro average of per-organ recall across the 8 Synapse organs
- `pancreas_accuracy`: recall for Synapse class `6`
- `per_class_metrics.csv/accuracy`: per-organ recall over the full test set
- `per_case_metrics.csv/accuracy`: per-case, per-organ recall when that organ is present in ground truth

Reported Jaccard/IoU fields:

- `overall.mean_jaccard`: macro average of per-organ Jaccard emitted by `test.py`
- `overall.mean_jaccard_percent`: same value as a percentage
- `pancreas.mean_jaccard`: Jaccard/IoU for Synapse class `6` emitted by `test.py`
- `pancreas.mean_jaccard_percent`: same pancreas value as a percentage
- `mean_foreground_jaccard`: macro average rebuilt from saved prediction/ground-truth artifacts by `scripts/calculate_accuracy_from_artifacts.py`
- `pancreas_jaccard`: pancreas Jaccard rebuilt from saved prediction/ground-truth artifacts

Dice handling is explicit: if a class is absent from ground truth but predicted by the model, that false positive receives Dice `0`, not Dice `1`. Empty true-negative cases are recorded separately in `per_case_metrics.csv`.

## Artifact Policy

- Commit source code, split metadata, notebooks, and lightweight result registries.
- Keep checkpoints, prediction volumes, compiled reports, paper PDFs, and generated images outside Git.
- Mirror the full `artifacts/runs/<run_id>/` folder and zip snapshot to Google Drive, GitHub Releases, or another artifact store for binary outputs that need long-term retention.
