#!/usr/bin/env python3
"""Profile Stage-2 TransUNet-CBAM model size and inference cost."""

from __future__ import annotations

import argparse
import copy
import json
import sys
import time
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from experiment_utils import apply_attention_config, apply_reverse_attention_config
from generate_stage2_q1q2_commands import VARIANTS
from networks.vit_seg_modeling import CONFIGS, VisionTransformer


def count_parameters(model: torch.nn.Module) -> tuple[int, int]:
    total = sum(parameter.numel() for parameter in model.parameters())
    trainable = sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)
    return total, trainable


def build_model(args: argparse.Namespace, variant: str) -> VisionTransformer:
    variant_args = VARIANTS[variant]
    config = copy.deepcopy(CONFIGS[args.vit_name])
    config.n_classes = args.num_classes
    config.n_skip = args.n_skip
    config.skip_indices = tuple()
    config.patches.size = (args.vit_patches_size, args.vit_patches_size)
    if "R50" in args.vit_name:
        config.patches.grid = (int(args.img_size / args.vit_patches_size), int(args.img_size / args.vit_patches_size))
    attention_scales = tuple(item for item in str(variant_args["attention_scales"]).split(",") if item)
    ra_scales = tuple(int(item) for item in str(variant_args["ra_scales"]).split(",") if item)
    apply_attention_config(
        config,
        mode=variant_args["attention_mode"],
        scales=attention_scales,
        reduction=args.attention_reduction,
    )
    apply_reverse_attention_config(
        config,
        mode=variant_args["ra_mode"],
        scales=ra_scales,
        reduction=args.ra_reduction,
    )
    return VisionTransformer(config, img_size=args.img_size, num_classes=args.num_classes)


def try_profile_macs(model: torch.nn.Module, inputs: torch.Tensor) -> float | None:
    try:
        from thop import profile
    except Exception:
        return None
    try:
        macs, _ = profile(model, inputs=(inputs,), verbose=False)
    except Exception:
        return None
    return float(macs)


def benchmark(model: torch.nn.Module, inputs: torch.Tensor, warmup: int, iters: int) -> tuple[float, int | None]:
    device = inputs.device
    model.eval()
    with torch.no_grad():
        for _ in range(warmup):
            _ = model(inputs)
        if device.type == "cuda":
            torch.cuda.synchronize(device)
            torch.cuda.reset_peak_memory_stats(device)
        start = time.perf_counter()
        for _ in range(iters):
            _ = model(inputs)
        if device.type == "cuda":
            torch.cuda.synchronize(device)
        elapsed = time.perf_counter() - start
    peak_memory = torch.cuda.max_memory_allocated(device) if device.type == "cuda" else None
    return elapsed / max(iters, 1), peak_memory


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", action="append", choices=sorted(VARIANTS), default=None)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--img-size", type=int, default=224)
    parser.add_argument("--vit-name", default="R50-ViT-B_16", choices=sorted(CONFIGS))
    parser.add_argument("--vit-patches-size", type=int, default=16)
    parser.add_argument("--n-skip", type=int, default=3)
    parser.add_argument("--num-classes", type=int, default=9)
    parser.add_argument("--attention-reduction", type=int, default=16)
    parser.add_argument("--ra-reduction", type=int, default=4)
    parser.add_argument("--warmup", type=int, default=5)
    parser.add_argument("--iters", type=int, default=30)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    device = torch.device(args.device)
    variants = args.variant or ["baseline", "cbam_pre_patch"]
    rows = []

    for variant in variants:
        model = build_model(args, variant).to(device)
        inputs = torch.randn(args.batch_size, 3, args.img_size, args.img_size, device=device)
        total, trainable = count_parameters(model)
        macs = try_profile_macs(model, inputs)
        latency, peak_memory = benchmark(model, inputs, args.warmup, args.iters)
        rows.append(
            {
                "variant": variant,
                "device": str(device),
                "batch_size": args.batch_size,
                "img_size": args.img_size,
                "vit_name": args.vit_name,
                "vit_patches_size": args.vit_patches_size,
                "n_skip": args.n_skip,
                "parameters_total": total,
                "parameters_trainable": trainable,
                "macs": macs,
                "latency_ms_per_batch": latency * 1000,
                "peak_memory_mb": (peak_memory / (1024**2)) if peak_memory is not None else None,
            }
        )

    if args.format == "json":
        print(json.dumps(rows, indent=2))
        return 0

    print("| variant | params M | trainable M | MACs G | latency ms/batch | peak memory MB |")
    print("|---|---:|---:|---:|---:|---:|")
    for row in rows:
        macs_g = "NA" if row["macs"] is None else f"{row['macs'] / 1e9:.2f}"
        memory = "NA" if row["peak_memory_mb"] is None else f"{row['peak_memory_mb']:.1f}"
        print(
            f"| {row['variant']} | {row['parameters_total'] / 1e6:.2f} | "
            f"{row['parameters_trainable'] / 1e6:.2f} | {macs_g} | "
            f"{row['latency_ms_per_batch']:.2f} | {memory} |"
        )
    if all(row["macs"] is None for row in rows):
        print("\nMACs require optional package `thop`; latency and memory were still measured.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

