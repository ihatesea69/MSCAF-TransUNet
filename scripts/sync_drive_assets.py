#!/usr/bin/env python3
"""Sync Synapse dataset, weights, checkpoints, and artifacts from Google Drive to local storage.

This script assumes the Google Drive content is already accessible from the local
machine, for example through Google Drive for desktop or an rclone mount.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


WEIGHT_ALIASES = ("R50+ViT-B_16.npz", "R50-ViT-B_16.npz")
INCLUDE_CHOICES = ("dataset", "weights", "artifacts", "checkpoints")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Copy the Synapse dataset, pretrained ViT weights, exported artifacts, "
            "and resume checkpoints from a locally available Google Drive root."
        )
    )
    parser.add_argument(
        "--drive-root",
        required=True,
        help=(
            "Local path to the Google Drive MyDrive root. Example: "
            '"G:\\My Drive" or "D:\\Google Drive\\MyDrive".'
        ),
    )
    parser.add_argument(
        "--dest-root",
        default=".",
        help=(
            "Local destination root. Defaults to the current project directory. "
            "Dataset is copied under data/, weights under model/, artifacts under "
            "artifacts/, and resume checkpoints under resume_checkpoints/."
        ),
    )
    parser.add_argument(
        "--run-ids",
        nargs="*",
        default=None,
        help=(
            "Optional run_id list. If omitted, all runs in docs/results/run_registry.json "
            "are copied."
        ),
    )
    parser.add_argument(
        "--include",
        nargs="+",
        choices=INCLUDE_CHOICES,
        default=list(INCLUDE_CHOICES),
        help="Which asset groups to copy.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing files and recopy directories instead of skipping them.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned actions without copying any files.",
    )
    return parser.parse_args()


def load_registry(registry_path: Path) -> dict[str, dict]:
    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    runs: dict[str, dict] = {}
    for record in payload.get("results", []):
        run_id = record.get("run_id")
        if run_id:
            runs[run_id] = record
    return runs


def ensure_exists(path: Path, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"{label} does not exist: {path}")


def copy_file(src: Path, dst: Path, overwrite: bool, dry_run: bool, summary: list[str]) -> None:
    if dst.exists() and not overwrite:
        summary.append(f"skip file  {dst}")
        return
    summary.append(f"copy file  {src} -> {dst}")
    if dry_run:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree(src: Path, dst: Path, overwrite: bool, dry_run: bool, summary: list[str]) -> None:
    if dst.exists():
        if not overwrite:
            summary.append(f"skip dir   {dst}")
            return
        summary.append(f"replace dir {dst}")
        if not dry_run:
            shutil.rmtree(dst)
    summary.append(f"copy dir   {src} -> {dst}")
    if dry_run:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst)


def resolve_resume_checkpoint(drive_root: Path, run_id: str, snapshot_name: str | None) -> Path | None:
    base_dir = drive_root / "transunet_colab_outputs" / "resume_checkpoints"
    candidates = [base_dir / run_id / "latest_checkpoint.pth"]
    if snapshot_name:
        candidates.append(base_dir / snapshot_name / "latest_checkpoint.pth")
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def sync_dataset(drive_root: Path, dest_root: Path, overwrite: bool, dry_run: bool, summary: list[str]) -> None:
    src = drive_root / "datasets" / "Synapse"
    ensure_exists(src, "Synapse dataset directory")
    dst = dest_root / "data" / "Synapse"
    copy_tree(src, dst, overwrite=overwrite, dry_run=dry_run, summary=summary)


def sync_weights(drive_root: Path, dest_root: Path, overwrite: bool, dry_run: bool, summary: list[str]) -> None:
    weight_dir = drive_root / "transunet"
    ensure_exists(weight_dir, "pretrained weight directory")
    dst_dir = dest_root / "model" / "vit_checkpoint" / "imagenet21k"

    available = [weight_dir / name for name in WEIGHT_ALIASES if (weight_dir / name).exists()]
    if not available:
        raise FileNotFoundError(
            f"No pretrained R50-ViT weight alias found in {weight_dir}. "
            f"Expected one of: {', '.join(WEIGHT_ALIASES)}"
        )

    source_map: dict[str, Path] = {}
    for alias in WEIGHT_ALIASES:
        candidate = weight_dir / alias
        if candidate.exists():
            source_map[alias] = candidate

    first_source = available[0]
    for alias in WEIGHT_ALIASES:
        copy_file(
            source_map.get(alias, first_source),
            dst_dir / alias,
            overwrite=overwrite,
            dry_run=dry_run,
            summary=summary,
        )


def sync_artifacts(
    drive_root: Path,
    dest_root: Path,
    run_ids: list[str],
    overwrite: bool,
    dry_run: bool,
    summary: list[str],
) -> None:
    runs_root = drive_root / "transunet_colab_outputs" / "runs"
    ensure_exists(runs_root, "artifact root")
    for run_id in run_ids:
        src = runs_root / run_id
        if not src.exists():
            summary.append(f"missing    {src}")
            continue
        dst = dest_root / "artifacts" / "runs" / run_id
        copy_tree(src, dst, overwrite=overwrite, dry_run=dry_run, summary=summary)


def sync_checkpoints(
    drive_root: Path,
    dest_root: Path,
    runs: dict[str, dict],
    run_ids: list[str],
    overwrite: bool,
    dry_run: bool,
    summary: list[str],
) -> None:
    for run_id in run_ids:
        record = runs[run_id]
        checkpoint = resolve_resume_checkpoint(drive_root, run_id, record.get("snapshot_name"))
        if checkpoint is None:
            summary.append(f"missing    resume checkpoint for {run_id}")
            continue
        dst = dest_root / "resume_checkpoints" / run_id / "latest_checkpoint.pth"
        copy_file(checkpoint, dst, overwrite=overwrite, dry_run=dry_run, summary=summary)


def write_summary(dest_root: Path, actions: list[str], dry_run: bool) -> Path | None:
    if dry_run:
        return None
    report_dir = dest_root / "artifacts" / "sync_reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / "drive_sync_summary.txt"
    report_path.write_text("\n".join(actions) + "\n", encoding="utf-8")
    return report_path


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    registry_path = repo_root / "docs" / "results" / "run_registry.json"
    runs = load_registry(registry_path)

    drive_root = Path(args.drive_root).expanduser().resolve()
    dest_root = Path(args.dest_root).expanduser().resolve()

    ensure_exists(drive_root, "drive root")

    run_ids = list(args.run_ids) if args.run_ids else list(runs.keys())
    unknown = [run_id for run_id in run_ids if run_id not in runs]
    if unknown:
        raise KeyError(
            "Unknown run_id(s): "
            + ", ".join(unknown)
            + ". Check docs/results/run_registry.json."
        )

    actions: list[str] = []
    if "dataset" in args.include:
        sync_dataset(drive_root, dest_root, args.overwrite, args.dry_run, actions)
    if "weights" in args.include:
        sync_weights(drive_root, dest_root, args.overwrite, args.dry_run, actions)
    if "artifacts" in args.include:
        sync_artifacts(drive_root, dest_root, run_ids, args.overwrite, args.dry_run, actions)
    if "checkpoints" in args.include:
        sync_checkpoints(drive_root, dest_root, runs, run_ids, args.overwrite, args.dry_run, actions)

    for action in actions:
        print(action)

    report_path = write_summary(dest_root, actions, args.dry_run)
    if report_path is not None:
        print(f"\nWrote sync summary: {report_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # Keep failures readable when run from PowerShell or Colab terminals.
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
