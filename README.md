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

Accuracy cannot be reconstructed from Dice and HD95 alone. Use [notebooks/transunet-calculate-artifact-accuracy.ipynb](notebooks/transunet-calculate-artifact-accuracy.ipynb) to calculate voxel accuracy, foreground macro accuracy, and pancreas accuracy from the retained NIfTI predictions in Drive artifact zips.

Current completed runs:

- `mscaf_cnn_fusion_3scale`: `cnn_fusion` on `1/8,1/4,1/2`, Mean Dice `76.61%`, Mean HD95 `28.80`
- `pre_hidden_1_16_r16_run_01`: `pre_hidden` on `1/16`, Mean Dice `78.3119%`, Mean HD95 `29.879884`, Pancreas Dice `0.549484`
- `pre_hidden_1_16_r16_run_02`: `pre_hidden` on `1/16`, Mean Dice `78.0560%`, Mean HD95 `28.846281`, Pancreas Dice `0.564749`
- `reverse_attention_s0_r4_run_01`: `pre_hidden` on `1/16` with RA skip `0`, reduction `4`, Mean Dice `78.1807%`, Mean HD95 `31.889628`, Pancreas Dice `0.553947`
- `reverse_bottleneck_fusion_s0_r4_run_01`: `pre_hidden` on `1/16` with post-fusion RA block `0`, reduction `4`, Mean Dice `77.8149%`, Mean HD95 `28.049328`, Pancreas Dice `0.571350`

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

## Colab notebooks

For reproducibility on Google Colab:

- [notebooks/transunet-drive-data-setup.ipynb](notebooks/transunet-drive-data-setup.ipynb): prepare the Synapse dataset and pretrained TransUNet weight on Google Drive
- [notebooks/transunet-cnn-attention-research-colab.ipynb](notebooks/transunet-cnn-attention-research-colab.ipynb): run the primary MSCAF-TransUNet `cnn_fusion` experiment end-to-end
- [notebooks/transunet-prehidden-1-16-rerun.ipynb](notebooks/transunet-prehidden-1-16-rerun.ipynb): completed non-RA `pre_hidden` run `02`; reuse only for the remaining fresh run `03`
- [notebooks/transunet-reverse-bottleneck-fusion.ipynb](notebooks/transunet-reverse-bottleneck-fusion.ipynb): completed advisor-requested reverse attention + bottleneck fusion at the first `1/8` decoder merge
- [notebooks/transunet-mscaf-reverse-attention.ipynb](notebooks/transunet-mscaf-reverse-attention.ipynb): historical completed Reverse Attention `s0/r4` artifact with retained metrics
- [notebooks/transunet-calculate-artifact-accuracy.ipynb](notebooks/transunet-calculate-artifact-accuracy.ipynb): calculate accuracy for every retained prediction artifact without retraining; reports missing or ambiguous zips explicitly

## Artifact policy

- Commit source code, split metadata, notebooks, and lightweight result registries.
- Keep checkpoints, prediction volumes, compiled reports, generated figures, paper PDFs, and local work archives outside Git.
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
