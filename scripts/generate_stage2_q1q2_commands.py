#!/usr/bin/env python3
"""Generate Stage-2 Q1/Q2 experiment commands for TransUNet-CBAM.

The script is intentionally dry-run by default. It prints the controlled
experiment matrix or the train/test commands needed to produce artifacts.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


CORE_SEEDS = (1234, 2025, 3407, 42, 1337)
ABLATION_SEEDS = (1234, 2025, 3407)

PRIORITY_ORDER = {letter: index for index, letter in enumerate("ABCDEFGHIJ")}

DEFAULT_ARGS = {
    "dataset": "Synapse",
    "max_iterations": 30000,
    "max_epochs": 150,
    "batch_size": 24,
    "img_size": 224,
    "n_skip": 3,
    "skip_indices": "",
    "vit_name": "R50-ViT-B_16",
    "vit_patches_size": 16,
    "attention_mode": "none",
    "attention_scales": "",
    "attention_reduction": 16,
    "ra_mode": "none",
    "ra_scales": "0",
    "ra_reduction": 4,
    "deterministic": 1,
    "base_lr": 0.01,
    "num_workers": 8,
    "n_gpu": 1,
}

VARIANTS = {
    "baseline": {
        "label": "TransUNet baseline",
        "attention_mode": "none",
        "attention_scales": "",
        "ra_mode": "none",
        "ra_scales": "0",
    },
    "cbam_pre_patch": {
        "label": "CBAM before patch embedding",
        "attention_mode": "pre_hidden",
        "attention_scales": "1/16",
        "ra_mode": "none",
        "ra_scales": "0",
    },
    "cbam_cnn_fusion": {
        "label": "CBAM multi-scale CNN fusion",
        "attention_mode": "cnn_fusion",
        "attention_scales": "1/8,1/4,1/2",
        "ra_mode": "none",
        "ra_scales": "0",
    },
    "cbam_ra_skip": {
        "label": "CBAM pre-patch + RA on skip feature",
        "attention_mode": "pre_hidden",
        "attention_scales": "1/16",
        "ra_mode": "ra_skip",
        "ra_scales": "0",
    },
    "cbam_ra_fusion": {
        "label": "CBAM pre-patch + RA after decoder-skip concat",
        "attention_mode": "pre_hidden",
        "attention_scales": "1/16",
        "ra_mode": "ra_fusion",
        "ra_scales": "0",
    },
}

TRAIN_ARG_ORDER = (
    "dataset",
    "max_iterations",
    "max_epochs",
    "batch_size",
    "n_gpu",
    "deterministic",
    "base_lr",
    "num_workers",
    "img_size",
    "seed",
    "n_skip",
    "skip_indices",
    "vit_name",
    "vit_patches_size",
    "attention_mode",
    "attention_scales",
    "attention_reduction",
    "ra_mode",
    "ra_scales",
    "ra_reduction",
)

TEST_ARG_ORDER = (
    "dataset",
    "max_iterations",
    "max_epochs",
    "batch_size",
    "deterministic",
    "base_lr",
    "img_size",
    "seed",
    "n_skip",
    "skip_indices",
    "vit_name",
    "vit_patches_size",
    "attention_mode",
    "attention_scales",
    "attention_reduction",
    "ra_mode",
    "ra_scales",
    "ra_reduction",
)


def priority_sort(values: set[str]) -> list[str]:
    return sorted(values, key=lambda value: PRIORITY_ORDER.get(value, 999))


def ps_quote(value: object) -> str:
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    return "'" + text.replace("'", "''") + "'"


def slug(value: str) -> str:
    return (
        value.lower()
        .replace("+", "")
        .replace("-", "")
        .replace("_", "")
        .replace("/", "")
    )


def build_args(variant: str, seed: int, **overrides: object) -> dict[str, object]:
    args = dict(DEFAULT_ARGS)
    args.update({key: value for key, value in VARIANTS[variant].items() if key != "label"})
    args["seed"] = seed
    args.update(overrides)
    return args


def experiment_key(variant: str, args: dict[str, object]) -> tuple[object, ...]:
    return (
        variant,
        args["seed"],
        args["img_size"],
        args["batch_size"],
        args["n_skip"],
        args.get("skip_indices", ""),
        args["vit_name"],
        args["vit_patches_size"],
        args["attention_mode"],
        args.get("attention_scales", ""),
        args["attention_reduction"],
        args["ra_mode"],
        args.get("ra_scales", ""),
        args["ra_reduction"],
        args["max_epochs"],
        args["base_lr"],
    )


def add_row(
    rows: dict[tuple[object, ...], dict[str, object]],
    *,
    run_id: str,
    priorities: tuple[str, ...],
    groups: tuple[str, ...],
    variant: str,
    seed: int,
    status: str = "planned",
    notes: str = "",
    **overrides: object,
) -> None:
    args = build_args(variant, seed, **overrides)
    key = experiment_key(variant, args)

    if key not in rows:
        rows[key] = {
            "run_id": run_id,
            "status": status,
            "priorities": list(priorities),
            "analysis_groups": list(groups),
            "variant": variant,
            "variant_label": VARIANTS[variant]["label"],
            "seed": seed,
            "args": args,
            "notes": notes,
        }
        return

    row = rows[key]
    row["priorities"] = priority_sort(set(row["priorities"]) | set(priorities))
    row["analysis_groups"] = sorted(set(row["analysis_groups"]) | set(groups))
    if status == "completed_anchor":
        row["status"] = status
        row["run_id"] = run_id
    if notes and notes not in str(row.get("notes", "")):
        row["notes"] = (str(row.get("notes", "")) + " " + notes).strip()


def add_manual_row(
    rows: dict[tuple[object, ...], dict[str, object]],
    *,
    run_id: str,
    priorities: tuple[str, ...],
    groups: tuple[str, ...],
    variant: str,
    label: str,
    notes: str,
    status: str = "manual_required",
) -> None:
    row_args = dict(DEFAULT_ARGS)
    row_args["seed"] = ""
    rows[("manual", run_id)] = {
        "run_id": run_id,
        "status": status,
        "priorities": list(priorities),
        "analysis_groups": list(groups),
        "variant": variant,
        "variant_label": label,
        "seed": "",
        "args": row_args,
        "notes": notes,
    }


def add_existing_anchors(rows: dict[tuple[object, ...], dict[str, object]]) -> None:
    anchor_note = "Existing seed-1234 artifact; do not rerun unless a fresh replicate is intended."
    add_row(
        rows,
        run_id="baseline_reproduction",
        priorities=("A",),
        groups=("core_seed_robustness", "placement_ablation"),
        variant="baseline",
        seed=1234,
        status="completed_anchor",
        notes=anchor_note,
    )
    add_row(
        rows,
        run_id="pre_hidden_1_16_r16_run_03",
        priorities=("A",),
        groups=("core_seed_robustness", "placement_ablation"),
        variant="cbam_pre_patch",
        seed=1234,
        status="completed_anchor",
        notes=anchor_note,
    )
    add_row(
        rows,
        run_id="mscaf_cnn_fusion_3scale",
        priorities=("B",),
        groups=("placement_ablation",),
        variant="cbam_cnn_fusion",
        seed=1234,
        status="completed_anchor",
        notes=anchor_note,
    )
    add_row(
        rows,
        run_id="reverse_attention_s0_r4_run_01",
        priorities=("B",),
        groups=("placement_ablation",),
        variant="cbam_ra_skip",
        seed=1234,
        status="completed_anchor",
        notes=anchor_note,
    )
    add_row(
        rows,
        run_id="reverse_bottleneck_fusion_s0_r4_run_01",
        priorities=("B",),
        groups=("placement_ablation",),
        variant="cbam_ra_fusion",
        seed=1234,
        status="completed_anchor",
        notes=anchor_note,
    )


def build_experiment_matrix() -> list[dict[str, object]]:
    rows: dict[tuple[object, ...], dict[str, object]] = {}
    add_existing_anchors(rows)

    for seed in CORE_SEEDS:
        for variant in ("baseline", "cbam_pre_patch"):
            add_row(
                rows,
                run_id=f"stage2_{variant}_s{seed}",
                priorities=("A",),
                groups=("core_seed_robustness",),
                variant=variant,
                seed=seed,
            )

    for seed in ABLATION_SEEDS:
        for variant in (
            "baseline",
            "cbam_cnn_fusion",
            "cbam_pre_patch",
            "cbam_ra_skip",
            "cbam_ra_fusion",
        ):
            add_row(
                rows,
                run_id=f"stage2_place_{variant}_s{seed}",
                priorities=("B",),
                groups=("placement_ablation",),
                variant=variant,
                seed=seed,
            )

    for seed in ABLATION_SEEDS:
        for variant in ("baseline", "cbam_pre_patch"):
            for n_skip in (0, 1, 2, 3):
                add_row(
                    rows,
                    run_id=f"stage2_skip{n_skip}_{variant}_s{seed}",
                    priorities=("C",),
                    groups=("skip_connection_sweep",),
                    variant=variant,
                    seed=seed,
                    n_skip=n_skip,
                )

    for seed in ABLATION_SEEDS:
        for variant in ("baseline", "cbam_pre_patch"):
            for img_size, batch_size in ((224, 24), (256, 16), (384, 8)):
                add_row(
                    rows,
                    run_id=f"stage2_res{img_size}_{variant}_s{seed}",
                    priorities=("D",),
                    groups=("input_resolution_sweep",),
                    variant=variant,
                    seed=seed,
                    img_size=img_size,
                    batch_size=batch_size,
                )

    for seed in ABLATION_SEEDS:
        for variant in ("baseline", "cbam_pre_patch"):
            for patch_size in (16, 32):
                add_row(
                    rows,
                    run_id=f"stage2_patch{patch_size}_{variant}_s{seed}",
                    priorities=("E",),
                    groups=("patch_size_sweep",),
                    variant=variant,
                    seed=seed,
                    vit_patches_size=patch_size,
                    notes=(
                        "Patch-size rows test the effective hybrid token grid; "
                        "verify pretrained-position loading before using in claims."
                    )
                    if patch_size == 32
                    else "",
                )

    for seed in ABLATION_SEEDS:
        for variant in ("baseline", "cbam_pre_patch"):
            for vit_name in ("R50-ViT-B_16", "R50-ViT-L_16"):
                add_row(
                    rows,
                    run_id=f"stage2_scale_{slug(vit_name)}_{variant}_s{seed}",
                    priorities=("F",),
                    groups=("model_scale_sweep",),
                    variant=variant,
                    seed=seed,
                    vit_name=vit_name,
                    batch_size=12 if vit_name == "R50-ViT-L_16" else 24,
                    notes=(
                        "R50-ViT-L rows require matching pretrained weights and may need "
                        "lower batch size on limited GPUs."
                    )
                    if vit_name == "R50-ViT-L_16"
                    else "",
                )

    add_manual_row(
        rows,
        run_id="stage2_fair_unet_baseline",
        priorities=("G",),
        groups=("fair_baseline_comparison",),
        variant="fair_unet",
        label="U-Net fair baseline",
        notes="Requires adding or importing a U-Net implementation and evaluating with the same split and metrics.",
    )
    add_manual_row(
        rows,
        run_id="stage2_fair_attention_unet",
        priorities=("G",),
        groups=("fair_baseline_comparison",),
        variant="fair_attention_unet",
        label="Attention U-Net fair baseline",
        notes="Requires adding or importing an Attention U-Net implementation under the same evaluator.",
    )
    add_manual_row(
        rows,
        run_id="stage2_fair_nnunet",
        priorities=("G",),
        groups=("fair_baseline_comparison",),
        variant="fair_nnunet",
        label="nnU-Net fair baseline",
        notes="Run nnU-Net with the same train/test split or clearly report protocol differences.",
    )
    add_manual_row(
        rows,
        run_id="stage2_fair_transformer_baseline",
        priorities=("G",),
        groups=("fair_baseline_comparison",),
        variant="fair_transformer_baseline",
        label="UNETR/Swin-style fair baseline",
        notes="Choose one transformer baseline only if code and GPU budget allow a fair same-protocol run.",
    )
    add_manual_row(
        rows,
        run_id="stage2_generalization_external_pancreas",
        priorities=("H",),
        groups=("generalization_validation",),
        variant="external_pancreas",
        label="External pancreas or abdominal dataset",
        notes="Requires dataset selection, preprocessing alignment, and a locked evaluator before claims.",
    )
    add_manual_row(
        rows,
        run_id="stage2_generalization_cross_split",
        priorities=("H",),
        groups=("generalization_validation",),
        variant="cross_split_synapse",
        label="Cross-split Synapse robustness",
        notes="Fallback if no external dataset is available; less strong than true external validation.",
    )
    add_manual_row(
        rows,
        run_id="stage2_efficiency_profile",
        priorities=("I",),
        groups=("efficiency_profile",),
        variant="efficiency",
        label="Params, MACs/FLOPs, latency, and memory",
        notes="Use scripts/profile_stage2_model_efficiency.py on the final reported variants.",
        status="analysis_required",
    )
    add_manual_row(
        rows,
        run_id="stage2_qualitative_case_panel",
        priorities=("J",),
        groups=("qualitative_panel",),
        variant="qualitative_panel",
        label="Success, mixed, and failure case panel",
        notes="Select from saved predictions after Stage A/B metrics identify representative cases.",
        status="analysis_required",
    )

    return sorted(
        rows.values(),
        key=lambda row: (
            PRIORITY_ORDER.get(row["priorities"][0], 999),
            row["variant"],
            str(row["seed"]),
            row["args"]["img_size"],
            row["args"]["vit_patches_size"],
            row["args"]["n_skip"],
            row["args"]["vit_name"],
            row["run_id"],
        ),
    )


def selected_rows(rows: list[dict[str, object]], args: argparse.Namespace) -> list[dict[str, object]]:
    selected = rows
    if args.priority:
        wanted = set(args.priority)
        selected = [row for row in selected if wanted.intersection(row["priorities"])]
    if args.group:
        wanted = set(args.group)
        selected = [row for row in selected if wanted.intersection(row["analysis_groups"])]
    return selected


def command_for(script: str, arg_order: tuple[str, ...], row_args: dict[str, object], extra: list[str]) -> str:
    command = ["python", script]
    for key in arg_order:
        value = row_args.get(key)
        if value in ("", None):
            continue
        if key == "ra_scales" and row_args.get("ra_mode") == "none":
            continue
        command.extend((f"--{key}", ps_quote(value)))
    command.extend(extra)
    return " ".join(command)


def train_command(row: dict[str, object]) -> str:
    return command_for("train.py", TRAIN_ARG_ORDER, row["args"], [])


def test_command(row: dict[str, object], artifact_root: str) -> str:
    extra = [
        "--run_id",
        ps_quote(row["run_id"]),
        "--artifact_root",
        ps_quote(artifact_root),
        "--export_artifact_zip",
    ]
    return command_for("test.py", TEST_ARG_ORDER, row["args"], extra)


def emit_summary(rows: list[dict[str, object]]) -> None:
    by_group: dict[str, int] = {}
    by_status: dict[str, int] = {}
    for row in rows:
        by_status[row["status"]] = by_status.get(row["status"], 0) + 1
        for group in row["analysis_groups"]:
            by_group[group] = by_group.get(group, 0) + 1

    print(f"Total matrix rows: {len(rows)}")
    print("By status:")
    for status, count in sorted(by_status.items()):
        print(f"  {status}: {count}")
    print("By analysis group:")
    for group, count in sorted(by_group.items()):
        print(f"  {group}: {count}")


def public_row(row: dict[str, object]) -> dict[str, object]:
    row_args = row["args"]
    return {
        "run_id": row["run_id"],
        "status": row["status"],
        "priorities": ",".join(row["priorities"]),
        "analysis_groups": ",".join(row["analysis_groups"]),
        "variant": row["variant"],
        "seed": row["seed"],
        "img_size": row_args["img_size"],
        "batch_size": row_args["batch_size"],
        "n_skip": row_args["n_skip"],
        "vit_name": row_args["vit_name"],
        "vit_patches_size": row_args["vit_patches_size"],
        "attention_mode": row_args["attention_mode"],
        "attention_scales": row_args.get("attention_scales", ""),
        "ra_mode": row_args["ra_mode"],
        "ra_scales": row_args.get("ra_scales", ""),
        "notes": row.get("notes", ""),
    }


def emit_markdown(rows: list[dict[str, object]]) -> None:
    headers = [
        "run_id",
        "status",
        "priorities",
        "analysis_groups",
        "variant",
        "seed",
        "img_size",
        "batch_size",
        "n_skip",
        "vit_name",
        "vit_patches_size",
    ]
    print("| " + " | ".join(headers) + " |")
    print("|" + "|".join("---" for _ in headers) + "|")
    for row in rows:
        public = public_row(row)
        print("| " + " | ".join(str(public[column]) for column in headers) + " |")


def emit_csv(rows: list[dict[str, object]]) -> None:
    fieldnames = list(public_row(rows[0]).keys()) if rows else ["run_id"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow(public_row(row))


def emit_commands(rows: list[dict[str, object]], artifact_root: str, include_completed: bool) -> str:
    lines = []
    for row in rows:
        if row["status"] == "completed_anchor" and not include_completed:
            lines.append(f"# skip completed anchor: {row['run_id']}")
            continue
        if row["status"] in {"manual_required", "analysis_required"}:
            lines.append(f"# {row['status']}: {row['run_id']} - {row.get('notes', '')}")
            continue
        lines.extend(
            [
                f"Write-Host '[train] {row['run_id']}'",
                train_command(row),
                f"Write-Host '[test] {row['run_id']}'",
                test_command(row, artifact_root),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("summary", "markdown", "json", "csv", "commands"),
        default="summary",
        help="output format",
    )
    parser.add_argument("--priority", action="append", help="priority letter to include")
    parser.add_argument("--group", action="append", help="analysis group to include")
    parser.add_argument(
        "--include-completed",
        action="store_true",
        help="include completed anchors in generated commands",
    )
    parser.add_argument(
        "--artifact-root",
        default="./artifacts/runs",
        help="artifact root passed to test.py",
    )
    parser.add_argument(
        "--write-ps1",
        type=Path,
        help="write generated commands to a PowerShell script",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = selected_rows(build_experiment_matrix(), args)

    if args.write_ps1:
        commands = emit_commands(rows, args.artifact_root, args.include_completed)
        payload = "$ErrorActionPreference = 'Stop'\n" + commands
        args.write_ps1.parent.mkdir(parents=True, exist_ok=True)
        args.write_ps1.write_text(payload, encoding="utf-8")
        print(f"Wrote {args.write_ps1}")
        return 0

    if args.format == "summary":
        emit_summary(rows)
    elif args.format == "markdown":
        emit_markdown(rows)
    elif args.format == "json":
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    elif args.format == "csv":
        emit_csv(rows)
    elif args.format == "commands":
        print(emit_commands(rows, args.artifact_root, args.include_completed), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
