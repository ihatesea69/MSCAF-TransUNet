#!/usr/bin/env python3
"""Calculate segmentation accuracy metrics from exported prediction artifacts."""

from __future__ import annotations

import argparse
import json
import math
import tempfile
import zipfile
from collections import Counter
from pathlib import Path, PurePosixPath

import numpy as np


DEFAULT_CLASS_NAMES = (
    "background",
    "aorta",
    "gallbladder",
    "kidney_left",
    "kidney_right",
    "liver",
    "pancreas",
    "spleen",
    "stomach",
)
VOLUME_SUFFIXES = (".nii.gz", ".nii", ".npy")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Calculate voxel accuracy and foreground macro accuracy from "
            "prediction/ground-truth pairs stored in experiment artifact zip files."
        )
    )
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("docs/results/run_registry.json"),
        help="Tracked run registry JSON.",
    )
    parser.add_argument(
        "--artifact-dir",
        type=Path,
        required=True,
        help="Directory containing exported experiment zip files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory for accuracy_results.json and accuracy_summary.md.",
    )
    parser.add_argument(
        "--artifact-map",
        type=Path,
        help=(
            "Optional JSON object mapping run_id to an explicit artifact zip path. "
            "Use this when multiple runs share the same snapshot filename."
        ),
    )
    parser.add_argument(
        "--num-classes",
        type=int,
        default=len(DEFAULT_CLASS_NAMES),
        help="Number of segmentation classes including background.",
    )
    return parser.parse_args()


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_artifact_map(path: Path | None) -> dict[str, Path]:
    if path is None:
        return {}
    raw = load_json(path)
    if not isinstance(raw, dict):
        raise ValueError("--artifact-map must contain a JSON object.")
    return {str(run_id): Path(str(zip_path)).expanduser() for run_id, zip_path in raw.items()}


def artifact_basename(run: dict[str, object]) -> str | None:
    artifact_path = run.get("artifact_zip_colab")
    if artifact_path:
        return PurePosixPath(str(artifact_path)).name
    snapshot_name = run.get("snapshot_name")
    if snapshot_name:
        return f"{snapshot_name}.zip"
    return None


def resolve_artifact(
    run: dict[str, object],
    artifact_dir: Path,
    explicit_map: dict[str, Path],
    basename_counts: Counter[str],
) -> tuple[Path | None, str | None]:
    run_id = str(run["run_id"])
    explicit_path = explicit_map.get(run_id)
    if explicit_path is not None:
        if explicit_path.exists():
            return explicit_path, None
        return None, f"explicit artifact does not exist: {explicit_path}"

    basename = artifact_basename(run)
    if basename is None:
        return None, "registry does not provide an artifact filename; add it to --artifact-map"
    if basename_counts[basename] > 1:
        return None, (
            f"shared artifact filename is ambiguous: {basename}; "
            "add preserved per-run zip paths to --artifact-map"
        )

    artifact_path = artifact_dir / basename
    if not artifact_path.exists():
        return None, f"artifact zip not found: {artifact_path}"
    return artifact_path, None


def split_volume_suffix(filename: str) -> tuple[str, str] | None:
    for suffix in VOLUME_SUFFIXES:
        if filename.endswith(suffix):
            return filename[: -len(suffix)], suffix
    return None


def discover_prediction_pairs(zip_file: zipfile.ZipFile) -> list[tuple[str, str, str]]:
    members = set(zip_file.namelist())
    pairs: list[tuple[str, str, str]] = []
    for member in sorted(members):
        filename = PurePosixPath(member).name
        parsed = split_volume_suffix(filename)
        if parsed is None:
            continue
        stem, suffix = parsed
        if not stem.endswith("_pred"):
            continue
        case_name = stem[: -len("_pred")]
        ground_truth = str(PurePosixPath(member).with_name(f"{case_name}_gt{suffix}"))
        if ground_truth in members:
            pairs.append((case_name, member, ground_truth))
    return pairs


def read_volume_from_zip(
    zip_file: zipfile.ZipFile,
    member: str,
    temp_dir: Path,
) -> np.ndarray:
    suffix = ".nii.gz" if member.endswith(".nii.gz") else Path(member).suffix
    output_path = temp_dir / f"volume{suffix}"
    output_path.write_bytes(zip_file.read(member))
    if suffix == ".npy":
        return np.load(output_path)

    try:
        import SimpleITK as sitk
    except ImportError as error:
        raise RuntimeError(
            "SimpleITK is required for NIfTI artifacts. Install requirements.txt first."
        ) from error
    return sitk.GetArrayFromImage(sitk.ReadImage(str(output_path)))


def update_confusion_matrix(
    confusion: np.ndarray,
    prediction: np.ndarray,
    ground_truth: np.ndarray,
) -> None:
    if prediction.shape != ground_truth.shape:
        raise ValueError(
            f"prediction shape {prediction.shape} does not match ground-truth shape {ground_truth.shape}"
        )
    num_classes = confusion.shape[0]
    prediction = np.asarray(prediction, dtype=np.int64).ravel()
    ground_truth = np.asarray(ground_truth, dtype=np.int64).ravel()
    valid = (
        (ground_truth >= 0)
        & (ground_truth < num_classes)
        & (prediction >= 0)
        & (prediction < num_classes)
    )
    encoded = num_classes * ground_truth[valid] + prediction[valid]
    confusion += np.bincount(encoded, minlength=num_classes**2).reshape(num_classes, num_classes)


def safe_ratio(numerator: int | np.integer, denominator: int | np.integer) -> float | None:
    if int(denominator) == 0:
        return None
    return float(numerator) / float(denominator)


def mean_present(values: list[float | None]) -> float | None:
    present = [value for value in values if value is not None]
    if not present:
        return None
    return float(np.mean(present))


def summarize_confusion(confusion: np.ndarray, class_names: tuple[str, ...]) -> dict[str, object]:
    true_counts = confusion.sum(axis=1)
    predicted_counts = confusion.sum(axis=0)
    diagonal = np.diag(confusion)
    total = confusion.sum()

    per_class = []
    for class_id, class_name in enumerate(class_names):
        per_class.append(
            {
                "class_id": class_id,
                "class_name": class_name,
                "accuracy": safe_ratio(diagonal[class_id], true_counts[class_id]),
                "true_voxels": int(true_counts[class_id]),
                "predicted_voxels": int(predicted_counts[class_id]),
                "correct_voxels": int(diagonal[class_id]),
            }
        )

    foreground_accuracy = safe_ratio(diagonal[1:].sum(), true_counts[1:].sum())
    foreground_class_accuracies = [item["accuracy"] for item in per_class[1:]]
    pancreas = per_class[6] if len(per_class) > 6 else None
    return {
        "voxel_accuracy": safe_ratio(diagonal.sum(), total),
        "foreground_voxel_accuracy": foreground_accuracy,
        "mean_foreground_accuracy": mean_present(foreground_class_accuracies),
        "pancreas_accuracy": pancreas["accuracy"] if pancreas else None,
        "valid_voxels": int(total),
        "confusion_matrix": confusion.tolist(),
        "per_class": per_class,
    }


def calculate_artifact_metrics(
    artifact_path: Path,
    num_classes: int,
    class_names: tuple[str, ...],
) -> dict[str, object]:
    confusion = np.zeros((num_classes, num_classes), dtype=np.int64)
    with zipfile.ZipFile(artifact_path) as zip_file:
        pairs = discover_prediction_pairs(zip_file)
        if not pairs:
            raise ValueError("artifact does not contain paired *_pred and *_gt volumes")
        with tempfile.TemporaryDirectory(prefix="transunet-accuracy-") as temp_path:
            temp_dir = Path(temp_path)
            for _, prediction_member, ground_truth_member in pairs:
                prediction = read_volume_from_zip(zip_file, prediction_member, temp_dir)
                ground_truth = read_volume_from_zip(zip_file, ground_truth_member, temp_dir)
                update_confusion_matrix(confusion, prediction, ground_truth)

    metrics = summarize_confusion(confusion, class_names)
    metrics["paired_volumes"] = len(pairs)
    metrics["cases"] = [case_name for case_name, _, _ in pairs]
    return metrics


def format_percent(value: object) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "-"
    return f"{100 * float(value):.4f}%"


def write_markdown(path: Path, results: list[dict[str, object]]) -> None:
    lines = [
        "# MSCAF-TransUNet Accuracy Registry",
        "",
        "Accuracy is calculated from retained NIfTI prediction and ground-truth volumes.",
        "",
        "- `Voxel accuracy`: correctly classified voxels divided by all voxels, including background.",
        "- `Foreground voxel accuracy`: correctly classified organ voxels divided by all ground-truth organ voxels.",
        "- `Mean foreground accuracy`: macro average of per-organ recall across the 8 Synapse organs.",
        "- `Pancreas accuracy`: recall for Synapse class `6`.",
        "",
        "| Run | Status | Voxel accuracy | Foreground voxel accuracy | Mean foreground accuracy | Pancreas accuracy |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for result in results:
        metrics = result.get("accuracy", {})
        lines.append(
            "| `{run_id}` | {status} | {voxel} | {foreground} | {macro} | {pancreas} |".format(
                run_id=result["run_id"],
                status=result["status"],
                voxel=format_percent(metrics.get("voxel_accuracy")),
                foreground=format_percent(metrics.get("foreground_voxel_accuracy")),
                macro=format_percent(metrics.get("mean_foreground_accuracy")),
                pancreas=format_percent(metrics.get("pancreas_accuracy")),
            )
        )
        if result.get("reason"):
            lines.append(f"|  | `{result['reason']}` |  |  |  |  |")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    registry = load_json(args.registry)
    runs = registry["results"]
    completed_runs = [run for run in runs if run.get("status") == "completed"]
    artifact_map = load_artifact_map(args.artifact_map)
    basenames = [artifact_basename(run) for run in completed_runs]
    basename_counts = Counter(basename for basename in basenames if basename)
    class_names = DEFAULT_CLASS_NAMES
    if args.num_classes != len(class_names):
        class_names = tuple(f"class_{index}" for index in range(args.num_classes))

    results: list[dict[str, object]] = []
    for run in completed_runs:
        run_id = str(run["run_id"])
        artifact_path, reason = resolve_artifact(run, args.artifact_dir, artifact_map, basename_counts)
        if artifact_path is None:
            results.append({"run_id": run_id, "status": "missing", "reason": reason})
            continue
        try:
            accuracy = calculate_artifact_metrics(artifact_path, args.num_classes, class_names)
        except Exception as error:  # Keep the batch report useful when one artifact is incomplete.
            results.append(
                {
                    "run_id": run_id,
                    "status": "error",
                    "artifact_zip": str(artifact_path),
                    "reason": str(error),
                }
            )
            continue
        results.append(
            {
                "run_id": run_id,
                "status": "completed",
                "artifact_zip": str(artifact_path),
                "accuracy": accuracy,
            }
        )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "accuracy_results.json"
    markdown_path = args.output_dir / "accuracy_summary.md"
    json_path.write_text(json.dumps({"results": results}, indent=2), encoding="utf-8")
    write_markdown(markdown_path, results)
    print(markdown_path.read_text(encoding="utf-8"))
    print(f"\nJSON: {json_path}")
    print(f"Markdown: {markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
