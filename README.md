# MSCAF-TransUNet for Synapse Segmentation

PyTorch research repo for extending TransUNet on the Synapse multi-organ segmentation benchmark, with the current focus on **MSCAF-TransUNet**: Multi-Scale CNN Attention Fusion inside the hybrid R50-ViT encoder.

This cleaned version keeps only the research codepath, lightweight utilities, and reproducibility notebooks. AWS/SageMaker and CloudFormation deployment assets were intentionally removed so the repository is easier to read, reproduce, and push to GitHub.

## Research focus

This repo currently centers on **MSCAF-TransUNet** and its related ablations on top of the hybrid ResNet-50 + ViT-B/16 encoder:

- `pre_hidden`: refine selected CNN scales and fuse them into the hidden feature before patch projection
- `cnn_fusion`: refine selected CNN skip features and fuse multiple CNN scales back into the hidden feature
- `ra_fusion`: apply reverse attention plus bottleneck immediately after the first decoder fusion at `1/8`
- Historical ablation: `ra_skip` applies Reverse Attention to selected decoder skip connections

## Result snapshot

Tracked result records live in [docs/results/results_summary.md](docs/results/results_summary.md) and [docs/results/run_registry.json](docs/results/run_registry.json). Large binary outputs are kept outside Git.

Accuracy cannot be reconstructed from Dice and HD95 alone. Numbered notebooks `01`-`06` map to one LaTeX result row and one `run_id` in [docs/results/run_registry.json](docs/results/run_registry.json). Notebook `07` is an optional Synapse repeat on the same project training flow. Use [notebooks/transunet-calculate-artifact-accuracy.ipynb](notebooks/transunet-calculate-artifact-accuracy.ipynb) when retained NIfTI predictions still exist. If old artifacts were deleted but the latest checkpoints remain on Drive, rerun the matching numbered notebook with `RUN_TRAIN = False` and `RUN_TEST = True`.

Current report rows with pancreas metrics:

| Run | Method | Pancreas Dice | Pancreas HD95 | Pancreas Jaccard | Pancreas Accuracy |
|---|---|---:|---:|---:|---:|
| `baseline_reproduction` | TransUNet baseline | `54.3675%` | `15.3753` | `39.6635%` | `44.4120%` |
| `mscaf_cnn_fusion_3scale` | CBAM multi-scale CNN fusion | `58.9334%` | `13.2034` | `44.2381%` | `50.2227%` |
| `pre_hidden_1_16_r16_run_03` | CBAM before patch embedding | `59.2291%` | `12.9671` | `43.9398%` | `48.9431%` |
| `reverse_attention_s0_r4_run_01` | CBAM + RA on skip feature | `58.3154%` | `32.1677` | `42.9503%` | `52.3272%` |
| `reverse_bottleneck_fusion_s0_r4_run_01` | CBAM + RA after decoder-skip concat | `55.9470%` | `13.1270` | `40.9862%` | `46.2828%` |

`Pancreas Accuracy` is read from `accuracy.pancreas_accuracy_percent` in `docs/results/run_registry.json` and is calculated as `TP / (TP + FN)` for Synapse pancreas class `6`.

Reference baseline from the earlier cleaned reproduction:

- Mean Dice: `77.29%`
- Mean HD95: `30.71`

### Comparison with the original TransUNet paper

| Framework | Encoder | Decoder | Average DSC ↑ | HD ↓ | Pancreas | Liver | Spleen | Stomach | Aorta | Gallbladder | Kidney (L) | Kidney (R) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **MSCAF-TransUNet (Ours)** | R50-ViT | CUP | 76.61 | **28.80** | **57.36** | **94.40** | **86.54** | **76.20** | 86.72 | 57.15 | 79.33 | 75.14 |
| TransUNet (paper) | R50-ViT | CUP | **77.48** | 31.69 | 55.86 | 94.08 | 85.08 | 75.62 | **87.23** | **63.13** | **81.87** | **77.02** |

Bold values indicate the better score between **MSCAF-TransUNet** and the original paper row. The current method first stands out on the metrics it improves: `HD95` is lower (`28.80` vs `31.69`), and organ-wise Dice is higher on `Pancreas` (`57.36` vs `55.86`), `Liver` (`94.40` vs `94.08`), `Spleen` (`86.54` vs `85.08`), and `Stomach` (`76.20` vs `75.62`). It still trails the original paper on mean Dice and several other organs.

Relevant implementation files:

- [networks/vit_seg_modeling.py](networks/vit_seg_modeling.py)
- [networks/vit_seg_modeling_resnet_skip.py](networks/vit_seg_modeling_resnet_skip.py)
- [experiment_utils.py](experiment_utils.py)
- [train.py](train.py)
- [test.py](test.py)

## Repository layout

```text
datasets/          dataset package and Synapse loader
splits/            explicit train/test split metadata
networks/          TransUNet model + hybrid encoder attention modules
notebooks/         Colab notebooks for Drive bootstrap and end-to-end experiments
docs/results/      lightweight result registry and artifact manifest
train.py           training entrypoint
test.py            evaluation entrypoint
trainer.py         training loop with epoch-level resume checkpointing
```

## Environment

Recommended:

- Python 3.10 to 3.12
- CUDA-enabled PyTorch
- `pip install -r requirements.txt`

Main Python dependencies are tracked in [requirements.txt](requirements.txt). PyTorch and torchvision should match your CUDA runtime.

## Data

The repo expects preprocessed Synapse data in:

```text
data/
  Synapse/
    train_npz/
    test_vol_h5/
```

Recommended workflow:

- use [notebooks/transunet-drive-data-setup.ipynb](notebooks/transunet-drive-data-setup.ipynb) to cache the dataset to Google Drive for Colab
- or prepare the Synapse layout manually under `data/Synapse`

## Pretrained weights

The hybrid encoder expects the R50-ViT-B/16 ImageNet-21k checkpoint under:

```text
model/vit_checkpoint/imagenet21k/
  R50+ViT-B_16.npz
  R50-ViT-B_16.npz
```

Recommended workflow:

- use [notebooks/transunet-drive-data-setup.ipynb](notebooks/transunet-drive-data-setup.ipynb) to cache the pretrained weight to Google Drive for Colab
- or place the checkpoint manually under `model/vit_checkpoint/imagenet21k/`

Both filename aliases are supported because different codepaths and notebooks reference both forms.

## Training

Example: run **MSCAF-TransUNet** (`cnn_fusion` on `1/8,1/4,1/2`)

```bash
python train.py ^
  --dataset Synapse ^
  --vit_name R50-ViT-B_16 ^
  --attention_mode cnn_fusion ^
  --attention_scales 1/8,1/4,1/2
```

Alternative attention experiment:

```bash
python train.py ^
  --dataset Synapse ^
  --vit_name R50-ViT-B_16 ^
  --attention_mode pre_hidden ^
  --attention_scales 1/16
```

Advisor-requested reverse bottleneck fusion experiment:

```bash
python train.py ^
  --dataset Synapse ^
  --vit_name R50-ViT-B_16 ^
  --attention_mode pre_hidden ^
  --attention_scales 1/16 ^
  --ra_mode ra_fusion ^
  --ra_scales 0 ^
  --ra_reduction 4
```

Baseline ablation:

```bash
python train.py --dataset Synapse --vit_name R50-ViT-B_16 --attention_mode none
```

## Evaluation

```bash
python test.py ^
  --dataset Synapse ^
  --vit_name R50-ViT-B_16 ^
  --attention_mode cnn_fusion ^
  --attention_scales 1/8,1/4,1/2
```

Save NIfTI predictions:

```bash
python test.py --dataset Synapse --vit_name R50-ViT-B_16 --is_savenii
```

Full artifact export:

```bash
python test.py ^
  --dataset Synapse ^
  --vit_name R50-ViT-B_16 ^
  --is_savenii ^
  --run_id mscaf_cnn_fusion_3scale ^
  --artifact_root artifacts/runs ^
  --export_artifact_zip
```

Evaluation artifacts include `metrics.json`, `per_case_metrics.csv`, `per_class_metrics.csv`, `confusion_matrix.json`, NIfTI predictions/ground truth/images, and an artifact zip. Logs include `voxel_accuracy`, `foreground_voxel_accuracy`, `mean_foreground_accuracy`, `pancreas_accuracy`, and Jaccard/IoU fields (`mean_jaccard`, `pancreas.mean_jaccard`). The CSV exports include per-class and per-case `accuracy` plus `jaccard`. Use the foreground metrics for research comparisons because whole-volume voxel accuracy can be dominated by background.

## Colab notebooks

For reproducibility on Google Colab:

- [notebooks/transunet-drive-data-setup.ipynb](notebooks/transunet-drive-data-setup.ipynb): prepare the Synapse dataset and pretrained TransUNet weight on Google Drive
- [notebooks/01-baseline-transunet.ipynb](notebooks/01-baseline-transunet.ipynb): TransUNet baseline using the same old-git Colab training flow as the other notebooks
- [notebooks/02-mscaf-cbam-da-ty-le.ipynb](notebooks/02-mscaf-cbam-da-ty-le.ipynb): MSCAF CBAM multi-scale fusion
- [notebooks/03-cbam-truoc-patch-embedding-a.ipynb](notebooks/03-cbam-truoc-patch-embedding-a.ipynb): CBAM before patch embedding run A
- [notebooks/04-cbam-truoc-patch-embedding-b.ipynb](notebooks/04-cbam-truoc-patch-embedding-b.ipynb): CBAM before patch embedding run B
- [notebooks/05-cbam-reverse-attention-skip.ipynb](notebooks/05-cbam-reverse-attention-skip.ipynb): CBAM + Reverse Attention on the `1/8` skip feature
- [notebooks/06-cbam-reverse-attention-sau-concat.ipynb](notebooks/06-cbam-reverse-attention-sau-concat.ipynb): CBAM + Reverse Attention after the first decoder-skip concat
- [notebooks/07-cbam-truoc-patch-embedding-c.ipynb](notebooks/07-cbam-truoc-patch-embedding-c.ipynb): optional Synapse repeat for CBAM before patch embedding
- [notebooks/transunet-calculate-artifact-accuracy.ipynb](notebooks/transunet-calculate-artifact-accuracy.ipynb): calculate accuracy for every retained prediction artifact without retraining; reports missing or ambiguous zips explicitly
- [notebooks/transunet-evaluate-latest-checkpoint-accuracy.ipynb](notebooks/transunet-evaluate-latest-checkpoint-accuracy.ipynb): rerun inference for the two latest retained checkpoints and export measured accuracy when prediction artifacts have already been deleted

## Artifact policy

- Commit source code, split metadata, notebooks, and lightweight result registries.
- Keep full binary artifacts outside Git under `artifacts/runs/<run_id>/` and mirror the full run folder plus zip to Drive: checkpoints, prediction volumes or masks, ground truth volumes or masks, image volumes or images, logs, metrics, and manifests.
- Reference retained binary outputs from README or `docs/results/` using Drive, Colab, or GitHub Release paths.

## Notes

- `trainer.py` saves `latest_checkpoint.pth` every epoch and can resume automatically.
- Package markers were added to `datasets/` and `networks/` so Colab does not confuse them with third-party packages.
- The repo intentionally no longer contains AWS deployment code, CloudFormation templates, SageMaker helpers, local archives, or generated binary reports.

## Citation

If you use this repo, cite the original TransUNet work and document the attention extension separately in your report or paper.

```bibtex
@article{chen2024transunet,
  title={TransUNet: Rethinking the U-Net architecture design for medical image segmentation through the lens of transformers},
  author={Chen, Jieneng and Mei, Jieru and Li, Xianhang and Lu, Yongyi and Yu, Qihang and Wei, Qingyue and Luo, Xiangde and Xie, Yutong and Adeli, Ehsan and Wang, Yan and others},
  journal={Medical Image Analysis},
  pages={103280},
  year={2024}
}
```

## License

Apache License 2.0. See [LICENSE](LICENSE).
