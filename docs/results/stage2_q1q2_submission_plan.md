# Stage-2 Q1/Q2 Submission Experiment Plan

This document turns the Q1/Q2 roadmap into an executable experiment package.
It does not replace the current manuscript results. It defines the additional
evidence needed before making journal-strength claims.

## Positioning

Recommended manuscript pitch:

> A controlled study of pre-tokenization convolutional attention at the
> CNN-to-transformer interface for pancreas segmentation.

Do not frame the work as a new SOTA architecture until the Stage-2 package has
fair baseline comparisons, seed replication, and generalization evidence.

## Run Order

| Stage | Evidence block | Run first? | Purpose |
|---|---|---:|---|
| A | 5-seed baseline vs pre-patch CBAM | Yes | Establish whether the current Dice and HD95 gain is seed-stable |
| B | 3-seed placement ablation | Yes | Test whether placement, not only added capacity, explains the improvement |
| C | Skip-connection sweep | After A/B | Match the analytical-study expectation set by TransUNet-style papers |
| D | Input-resolution sweep | After A/B | Test sensitivity to 224, 256, and 384 input resolution |
| E | Patch-size sweep | After A/B | Test dependence on token grid and CNN-to-token interface |
| F | Model-scale sweep | After A/B | Test whether the effect survives a larger hybrid ViT setting |
| G | Fair baselines | Parallel project | Add U-Net, Attention U-Net, nnU-Net, and other baselines under the same evaluator |
| H | Generalization | Parallel project | Add external dataset or cross-split validation |
| I | Efficiency profile | Anytime | Report parameters, latency, peak VRAM, and MACs/FLOPs when available |
| J | Qualitative panels | After metrics | Select success, mixed, and failure cases from saved predictions |

## Commands

Generate the complete matrix:

```powershell
python scripts/generate_stage2_q1q2_commands.py --format markdown
```

Generate only the first required block:

```powershell
python scripts/generate_stage2_q1q2_commands.py --group core_seed_robustness --format commands
```

Write a runnable PowerShell batch file for the core block:

```powershell
python scripts/generate_stage2_q1q2_commands.py --group core_seed_robustness --write-ps1 tmp/stage2_core_seed_robustness.ps1
powershell -ExecutionPolicy Bypass -File tmp/stage2_core_seed_robustness.ps1
```

Summarize completed artifacts:

```powershell
python scripts/summarize_stage2_q1q2_results.py --output docs/results/stage2_q1q2_current_summary.md
```

Profile efficiency for a representative model:

```powershell
python scripts/profile_stage2_model_efficiency.py --variant baseline --variant cbam_pre_patch --device cuda
```

## Manuscript Tables After Completion

| Manuscript item | Data source | Claim boundary |
|---|---|---|
| Main Results Table | Stage A | Mean +/- std over seeds; paired deltas where seeds match |
| Placement Ablation Table | Stage B | Placement effects only within the controlled Synapse protocol |
| Analytical Study Table | Stages C-F | Sensitivity to skip connections, resolution, patch size, and model scale |
| Fair Comparison Table | Stage G | Direct comparison only for baselines run under the same split and evaluator |
| Generalization Table | Stage H | External validity or cross-split robustness |
| Efficiency Table | Stage I | Practical cost alongside accuracy |
| Qualitative Figure | Stage J | Representative success, mixed, and failure modes |

## Submission Thresholds

Q2-realistic threshold:

- Complete Stages A, B, I, and J.
- Add at least one credible fair baseline beyond TransUNet.
- If Stage H is missing, state that external validation remains future work.

Q1-ambitious threshold:

- Complete Stages A-F and I-J.
- Add Stage G with fair baselines, preferably including nnU-Net.
- Add Stage H with either external pancreas/abdominal validation or a clearly
  justified cross-split robustness design.

## Non-negotiable Wording Rules

- Use "suggests", "is consistent with", "within this protocol", and "requires
  confirmation" until replicated and external evidence is available.
- Do not call literature-only numbers a direct SOTA comparison.
- Do not count repeated same-seed reruns as independent statistical seeds.
- Keep local implementation details out of the manuscript main text.

