#!/usr/bin/env python3
"""Validate that registered experiment rows match the numbered notebooks."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


EXPECTED_ROWS = [
    (1, "baseline_reproduction", "notebooks/01-baseline-transunet.ipynb"),
    (2, "mscaf_cnn_fusion_3scale", "notebooks/02-mscaf-cbam-da-ty-le.ipynb"),
    (3, "pre_hidden_1_16_r16_run_03", "notebooks/07-cbam-truoc-patch-embedding-c.ipynb"),
    (4, "reverse_attention_s0_r4_run_01", "notebooks/05-cbam-reverse-attention-skip.ipynb"),
    (5, "reverse_bottleneck_fusion_s0_r4_run_01", "notebooks/06-cbam-reverse-attention-sau-concat.ipynb"),
]

EXPECTED_EXTRA_NOTEBOOKS = [
    (
        3,
        "pre_hidden_1_16_r16_run_01",
        "notebooks/03-cbam-truoc-patch-embedding-a.ipynb",
    ),
    (
        4,
        "pre_hidden_1_16_r16_run_02",
        "notebooks/04-cbam-truoc-patch-embedding-b.ipynb",
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("docs/results/run_registry.json"),
        help="experiment registry JSON",
    )
    parser.add_argument(
        "--tex",
        type=Path,
        default=Path("output/latex/mscaf_transunet_paper/main.tex"),
        help="LaTeX paper path",
    )
    return parser.parse_args()


def load_registry(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main() -> int:
    args = parse_args()
    registry = load_registry(args.registry)
    runs = {run["run_id"]: run for run in registry.get("results", [])}
    tex_text = args.tex.read_text(encoding="utf-8")
    errors = []

    for tex_order, run_id, notebook in EXPECTED_ROWS:
        run = runs.get(run_id)
        if run is None:
            errors.append(f"missing registry run: {run_id}")
            continue
        if run.get("tex_order") != tex_order:
            errors.append(f"{run_id}: tex_order should be {tex_order}, got {run.get('tex_order')}")
        if run.get("notebook") != notebook:
            errors.append(f"{run_id}: notebook should be {notebook}, got {run.get('notebook')}")
        if not Path(notebook).exists():
            errors.append(f"{run_id}: notebook file does not exist: {notebook}")
        escaped_run_id = run_id.replace("_", "\\_")
        if run_id not in tex_text and escaped_run_id not in tex_text:
            errors.append(f"{run_id}: run_id is not referenced in {args.tex}")

    for notebook_order, run_id, notebook in EXPECTED_EXTRA_NOTEBOOKS:
        run = runs.get(run_id)
        if run is None:
            errors.append(f"missing extra notebook run: {run_id}")
            continue
        if run.get("tex_order") is not None:
            errors.append(f"{run_id}: extra notebook should not have tex_order unless added to the paper")
        if run.get("notebook_order") != notebook_order:
            errors.append(
                f"{run_id}: notebook_order should be {notebook_order}, got {run.get('notebook_order')}"
            )
        if run.get("notebook") != notebook:
            errors.append(f"{run_id}: notebook should be {notebook}, got {run.get('notebook')}")
        if not Path(notebook).exists():
            errors.append(f"{run_id}: notebook file does not exist: {notebook}")

    registered_orders = [
        run.get("tex_order")
        for run in registry.get("results", [])
        if isinstance(run.get("tex_order"), int)
    ]
    if sorted(registered_orders) != list(range(1, len(registered_orders) + 1)):
        errors.append(f"tex_order values are not contiguous: {registered_orders}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Experiment registry validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
