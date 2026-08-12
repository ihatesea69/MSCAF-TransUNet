#!/usr/bin/env python3
"""Summarize completed Stage-2 Q1/Q2 artifacts."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from generate_stage2_q1q2_commands import build_experiment_matrix


def load_metrics(artifact_root: Path, run_id: str) -> dict[str, object] | None:
    path = artifact_root / run_id / "metrics.json"
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def nested(payload: dict[str, object] | None, path: str) -> float | None:
    if payload is None:
        return None
    value: object = payload
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    if value is None:
        return None
    return float(value)


def mean_std(values: list[float]) -> tuple[float | None, float | None]:
    if not values:
        return None, None
    if len(values) == 1:
        return values[0], 0.0
    return statistics.mean(values), statistics.stdev(values)


def fmt(value: float | None, digits: int = 2) -> str:
    if value is None:
        return "NA"
    return f"{value:.{digits}f}"


def build_report(artifact_root: Path) -> str:
    rows = build_experiment_matrix()
    completed = []
    missing = []
    for row in rows:
        metrics = load_metrics(artifact_root, row["run_id"])
        if metrics is None:
            missing.append(row)
            continue
        completed.append((row, metrics))

    lines = [
        "# Stage-2 Q1/Q2 Result Summary",
        "",
        f"Artifact root: `{artifact_root}`",
        f"Completed rows with metrics: {len(completed)}",
        f"Missing rows: {len(missing)}",
        "",
        "## Completed Run Metrics",
        "",
        "| run_id | priorities | groups | variant | seed | pancreas Dice % | pancreas HD95 | overall Dice % |",
        "|---|---:|---|---|---:|---:|---:|---:|",
    ]

    for row, metrics in completed:
        lines.append(
            "| {run_id} | {priorities} | {groups} | {variant} | {seed} | {pdice} | {phd95} | {odice} |".format(
                run_id=row["run_id"],
                priorities=",".join(row["priorities"]),
                groups=",".join(row["analysis_groups"]),
                variant=row["variant"],
                seed=row["seed"],
                pdice=fmt(nested(metrics, "pancreas.mean_dice_percent"), 2),
                phd95=fmt(nested(metrics, "pancreas.mean_hd95"), 2),
                odice=fmt(nested(metrics, "overall.mean_dice_percent"), 2),
            )
        )

    lines.extend(["", "## Group Summaries", ""])
    groups = sorted({group for row in rows for group in row["analysis_groups"]})
    for group in groups:
        lines.append(f"### {group}")
        lines.append("")
        lines.append("| variant | n | pancreas Dice mean +/- std | HD95 mean +/- std |")
        lines.append("|---|---:|---:|---:|")
        variants = sorted({row["variant"] for row in rows if group in row["analysis_groups"]})
        for variant in variants:
            values_dice = []
            values_hd95 = []
            for row, metrics in completed:
                if group not in row["analysis_groups"] or row["variant"] != variant:
                    continue
                dice = nested(metrics, "pancreas.mean_dice_percent")
                hd95 = nested(metrics, "pancreas.mean_hd95")
                if dice is not None:
                    values_dice.append(dice)
                if hd95 is not None:
                    values_hd95.append(hd95)
            dice_mean, dice_std = mean_std(values_dice)
            hd95_mean, hd95_std = mean_std(values_hd95)
            lines.append(
                f"| {variant} | {len(values_dice)} | {fmt(dice_mean)} +/- {fmt(dice_std)} | "
                f"{fmt(hd95_mean)} +/- {fmt(hd95_std)} |"
            )
        lines.append("")

    lines.extend(["## Core Paired Deltas", ""])
    by_seed: dict[int, dict[str, dict[str, object]]] = {}
    for row, metrics in completed:
        if "core_seed_robustness" not in row["analysis_groups"]:
            continue
        by_seed.setdefault(int(row["seed"]), {})[str(row["variant"])] = metrics

    lines.append("| seed | delta Dice percentage points | delta HD95 mm |")
    lines.append("|---:|---:|---:|")
    deltas_dice = []
    deltas_hd95 = []
    for seed in sorted(by_seed):
        pair = by_seed[seed]
        if "baseline" not in pair or "cbam_pre_patch" not in pair:
            continue
        baseline = pair["baseline"]
        proposed = pair["cbam_pre_patch"]
        delta_dice = nested(proposed, "pancreas.mean_dice_percent") - nested(baseline, "pancreas.mean_dice_percent")
        delta_hd95 = nested(proposed, "pancreas.mean_hd95") - nested(baseline, "pancreas.mean_hd95")
        deltas_dice.append(delta_dice)
        deltas_hd95.append(delta_hd95)
        lines.append(f"| {seed} | {fmt(delta_dice)} | {fmt(delta_hd95)} |")
    dice_mean, dice_std = mean_std(deltas_dice)
    hd95_mean, hd95_std = mean_std(deltas_hd95)
    lines.append("")
    lines.append(f"Paired delta Dice mean +/- std: {fmt(dice_mean)} +/- {fmt(dice_std)} percentage points.")
    lines.append(f"Paired delta HD95 mean +/- std: {fmt(hd95_mean)} +/- {fmt(hd95_std)} mm.")
    lines.append("")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-root", type=Path, default=Path("./artifacts/runs"))
    parser.add_argument("--output", type=Path, help="optional Markdown output path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report(args.artifact_root)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

