# Stage-2 Q1/Q2 Result Summary

Artifact root: `artifacts\runs`
Completed rows with metrics: 5
Missing rows: 64

## Completed Run Metrics

| run_id | priorities | groups | variant | seed | pancreas Dice % | pancreas HD95 | overall Dice % |
|---|---:|---|---|---:|---:|---:|---:|
| baseline_reproduction | A,B,C,D,E,F | core_seed_robustness,input_resolution_sweep,model_scale_sweep,patch_size_sweep,placement_ablation,skip_connection_sweep | baseline | 1234 | 54.37 | 15.38 | 75.78 |
| pre_hidden_1_16_r16_run_03 | A,B,C,D,E,F | core_seed_robustness,input_resolution_sweep,model_scale_sweep,patch_size_sweep,placement_ablation,skip_connection_sweep | cbam_pre_patch | 1234 | 59.23 | 12.97 | 78.15 |
| mscaf_cnn_fusion_3scale | B | placement_ablation | cbam_cnn_fusion | 1234 | 58.93 | 13.20 | 77.93 |
| reverse_bottleneck_fusion_s0_r4_run_01 | B | placement_ablation | cbam_ra_fusion | 1234 | 55.95 | 13.13 | 75.98 |
| reverse_attention_s0_r4_run_01 | B | placement_ablation | cbam_ra_skip | 1234 | 58.32 | 32.17 | 77.32 |

## Group Summaries

### core_seed_robustness

| variant | n | pancreas Dice mean +/- std | HD95 mean +/- std |
|---|---:|---:|---:|
| baseline | 1 | 54.37 +/- 0.00 | 15.38 +/- 0.00 |
| cbam_pre_patch | 1 | 59.23 +/- 0.00 | 12.97 +/- 0.00 |

### efficiency_profile

| variant | n | pancreas Dice mean +/- std | HD95 mean +/- std |
|---|---:|---:|---:|
| efficiency | 0 | NA +/- NA | NA +/- NA |

### fair_baseline_comparison

| variant | n | pancreas Dice mean +/- std | HD95 mean +/- std |
|---|---:|---:|---:|
| fair_attention_unet | 0 | NA +/- NA | NA +/- NA |
| fair_nnunet | 0 | NA +/- NA | NA +/- NA |
| fair_transformer_baseline | 0 | NA +/- NA | NA +/- NA |
| fair_unet | 0 | NA +/- NA | NA +/- NA |

### generalization_validation

| variant | n | pancreas Dice mean +/- std | HD95 mean +/- std |
|---|---:|---:|---:|
| cross_split_synapse | 0 | NA +/- NA | NA +/- NA |
| external_pancreas | 0 | NA +/- NA | NA +/- NA |

### input_resolution_sweep

| variant | n | pancreas Dice mean +/- std | HD95 mean +/- std |
|---|---:|---:|---:|
| baseline | 1 | 54.37 +/- 0.00 | 15.38 +/- 0.00 |
| cbam_pre_patch | 1 | 59.23 +/- 0.00 | 12.97 +/- 0.00 |

### model_scale_sweep

| variant | n | pancreas Dice mean +/- std | HD95 mean +/- std |
|---|---:|---:|---:|
| baseline | 1 | 54.37 +/- 0.00 | 15.38 +/- 0.00 |
| cbam_pre_patch | 1 | 59.23 +/- 0.00 | 12.97 +/- 0.00 |

### patch_size_sweep

| variant | n | pancreas Dice mean +/- std | HD95 mean +/- std |
|---|---:|---:|---:|
| baseline | 1 | 54.37 +/- 0.00 | 15.38 +/- 0.00 |
| cbam_pre_patch | 1 | 59.23 +/- 0.00 | 12.97 +/- 0.00 |

### placement_ablation

| variant | n | pancreas Dice mean +/- std | HD95 mean +/- std |
|---|---:|---:|---:|
| baseline | 1 | 54.37 +/- 0.00 | 15.38 +/- 0.00 |
| cbam_cnn_fusion | 1 | 58.93 +/- 0.00 | 13.20 +/- 0.00 |
| cbam_pre_patch | 1 | 59.23 +/- 0.00 | 12.97 +/- 0.00 |
| cbam_ra_fusion | 1 | 55.95 +/- 0.00 | 13.13 +/- 0.00 |
| cbam_ra_skip | 1 | 58.32 +/- 0.00 | 32.17 +/- 0.00 |

### qualitative_panel

| variant | n | pancreas Dice mean +/- std | HD95 mean +/- std |
|---|---:|---:|---:|
| qualitative_panel | 0 | NA +/- NA | NA +/- NA |

### skip_connection_sweep

| variant | n | pancreas Dice mean +/- std | HD95 mean +/- std |
|---|---:|---:|---:|
| baseline | 1 | 54.37 +/- 0.00 | 15.38 +/- 0.00 |
| cbam_pre_patch | 1 | 59.23 +/- 0.00 | 12.97 +/- 0.00 |

## Core Paired Deltas

| seed | delta Dice percentage points | delta HD95 mm |
|---:|---:|---:|
| 1234 | 4.86 | -2.41 |

Paired delta Dice mean +/- std: 4.86 +/- 0.00 percentage points.
Paired delta HD95 mean +/- std: -2.41 +/- 0.00 mm.
