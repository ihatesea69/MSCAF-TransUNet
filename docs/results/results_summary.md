# MSCAF-TransUNet Result Registry

This registry keeps lightweight, source-control friendly result records. Large binary artifacts stay outside Git and are referenced by their Colab or Drive paths.

## Completed Runs

| Run | Method | Mean Dice (%) | Mean HD95 | Pancreas Dice | Pancreas HD95 | Artifact |
|---|---|---:|---:|---:|---:|---|
| `baseline_reproduction` | TransUNet reproduction | 77.29 | 30.71 | - | - | External baseline record |
| `mscaf_cnn_fusion_3scale` | MSCAF-TransUNet `cnn_fusion` on `1/8,1/4,1/2` | 76.61 | 28.80 | 57.36% | - | External report artifact |
| `pre_hidden_1_16_r16_run_01` | MSCAF-TransUNet `pre_hidden` on `1/16` | 78.3119 | 29.879884 | 0.549484 | 13.912953 | `/content/drive/MyDrive/transunet_colab_outputs` |
| `pre_hidden_1_16_r16_run_02` | MSCAF-TransUNet `pre_hidden` on `1/16` | 78.0560 | 28.846281 | 0.564749 | 13.652530 | `/content/drive/MyDrive/transunet_colab_outputs` |
| `reverse_attention_s0_r4_run_01` | MSCAF-TransUNet + RA skip `0`, reduction `4` | 78.1807 | 31.889628 | 0.553947 | 19.290868 | `/content/drive/MyDrive/transunet_colab_outputs` |
| `reverse_bottleneck_fusion_s0_r4_run_01` | MSCAF-TransUNet + post-fusion RA block `0`, reduction `4` | 77.8149 | 28.049328 | 0.571350 | 14.538932 | `/content/drive/MyDrive/transunet_colab_outputs` |

The two latest notebook completions resumed existing Drive checkpoints: `pre_hidden_1_16_r16_run_02` from epoch `145` and `reverse_bottleneck_fusion_s0_r4_run_01` from epoch `148`.

## Accuracy Backfill

Accuracy cannot be derived from the retained Dice and HD95 values. Run `notebooks/transunet-calculate-artifact-accuracy.ipynb` to calculate it from the NIfTI predictions stored inside Drive artifact zips.

The post-processing notebook exports:

- `voxel_accuracy`: all correctly classified voxels divided by all voxels, including background
- `foreground_voxel_accuracy`: correctly classified organ voxels divided by all ground-truth organ voxels
- `mean_foreground_accuracy`: macro average of per-organ recall across the 8 Synapse organs
- `pancreas_accuracy`: recall for Synapse class `6`

Use `mean_foreground_accuracy` and `pancreas_accuracy` in research comparisons. `voxel_accuracy` is retained for completeness but can be dominated by background voxels.

The two `pre_hidden` runs share one snapshot zip filename. If Drive no longer contains a separately preserved run `01` zip, leave that row as missing rather than assigning the run `02` accuracy to both rows.

## Pending Or Planned Runs

| Run | Status | Notebook | Target snapshot suffix |
|---|---|---|---|
| `pre_hidden_1_16_r16_run_03` | pending | `notebooks/transunet-prehidden-1-16-rerun.ipynb` | `_attn-pre_hidden-1_16-r16` |

## Artifact Policy

- Commit text result registries, notebook definitions, and source code.
- Keep model checkpoints, prediction volumes, compiled reports, paper PDFs, and generated images outside Git.
- Use Google Drive, GitHub Releases, or another artifact store for binary outputs that need long-term retention.
