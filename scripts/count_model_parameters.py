"""Count trainable parameters for the project's TransUNet variants."""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import torch.nn as nn

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from networks.vit_seg_modeling import (
    BottleNeckBlock,
    CONFIGS,
    CNNFeatureFusion,
    FeatureFusionBridge,
    ResidualAttention2d,
    ReverseAttentionModule,
    VisionTransformer,
)


VARIANTS = {
    "A_baseline": ("none", (), "none", ()),
    "B_pre_hidden": ("pre_hidden", ("1/16",), "none", ()),
    "C_cnn_fusion": ("cnn_fusion", ("1/8", "1/4", "1/2"), "none", ()),
    "D_ra_skip": ("pre_hidden", ("1/16",), "ra_skip", (0,)),
    "E_ra_fusion": ("pre_hidden", ("1/16",), "ra_fusion", (0,)),
}


def build_model(variant_name: str) -> VisionTransformer:
    attention_mode, attention_scales, ra_mode, ra_scales = VARIANTS[variant_name]
    config = copy.deepcopy(CONFIGS["R50-ViT-B_16"])
    config.n_classes = 9
    config.n_skip = 3
    config.skip_indices = ()
    config.patches.grid = (14, 14)
    config.attention_mode = attention_mode
    config.attention_scales = attention_scales
    config.attention_reduction = 16
    config.reverse_attention_mode = ra_mode
    config.reverse_attention_scales = ra_scales
    config.reverse_attention_reduction = 4
    return VisionTransformer(config, img_size=224, num_classes=9)


def count_trainable_parameters(module: nn.Module) -> int:
    return sum(parameter.numel() for parameter in module.parameters() if parameter.requires_grad)


def count_all_parameters(module: nn.Module) -> int:
    return sum(parameter.numel() for parameter in module.parameters())


def find_single_module(model: nn.Module, module_type: type[nn.Module]) -> nn.Module:
    modules = [module for module in model.modules() if isinstance(module, module_type)]
    if len(modules) != 1:
        raise RuntimeError(f"Expected one {module_type.__name__}, found {len(modules)}")
    return modules[0]


def format_int(value: int) -> str:
    return f"{value:,}"


def main() -> None:
    rows = []
    baseline_total = None

    for variant_name in VARIANTS:
        model = build_model(variant_name)
        total = count_all_parameters(model)
        trainable = count_trainable_parameters(model)
        fusion = find_single_module(model, CNNFeatureFusion)
        fusion_total = count_trainable_parameters(fusion)
        ra_modules = [module for module in model.modules() if isinstance(module, ReverseAttentionModule)]
        ra_total = sum(count_trainable_parameters(module) for module in ra_modules)

        if baseline_total is None:
            baseline_total = total
        delta = total - baseline_total
        if delta != fusion_total + ra_total:
            raise RuntimeError(
                f"Parameter reconciliation failed for {variant_name}: "
                f"delta={delta}, fusion+RA={fusion_total + ra_total}"
            )

        rows.append((variant_name, total, trainable, delta, fusion_total, ra_total))

    headers = ("Variant", "Total params", "Trainable", "Delta vs A", "CNN attention/fusion", "Reverse attention")
    display_rows = [
        (name, format_int(total), format_int(trainable), format_int(delta), format_int(fusion), format_int(ra))
        for name, total, trainable, delta, fusion, ra in rows
    ]
    widths = [
        max(len(headers[index]), *(len(row[index]) for row in display_rows))
        for index in range(len(headers))
    ]
    print("  ".join(value.ljust(widths[index]) for index, value in enumerate(headers)))
    print("  ".join("-" * width for width in widths))
    for row in display_rows:
        print("  ".join(value.ljust(widths[index]) for index, value in enumerate(row)))

    print("\nDetailed added modules")
    for variant_name in VARIANTS:
        model = build_model(variant_name)
        fusion = find_single_module(model, CNNFeatureFusion)
        details = []
        for scale, block in fusion.attention_blocks.items():
            details.append((f"CBAM residual [{scale}]", count_trainable_parameters(block)))
        for scale, bridge in fusion.hidden_bridges.items():
            details.append((f"Projection [{scale}]", count_trainable_parameters(bridge)))
        if fusion.fusion_weights:
            details.append(("Learnable fusion scalars", sum(p.numel() for p in fusion.fusion_weights.values())))
        for name, module in model.named_modules():
            if isinstance(module, ReverseAttentionModule):
                details.append((f"RA total [{name}]", count_trainable_parameters(module)))
                details.append((f"  Bottleneck subset [{name}]", count_trainable_parameters(module.bottleneck)))

        cbam_total = sum(
            count_trainable_parameters(module)
            for module in model.modules()
            if isinstance(module, ResidualAttention2d)
        )
        projection_total = sum(
            count_trainable_parameters(module)
            for module in model.modules()
            if isinstance(module, FeatureFusionBridge)
        )
        bottleneck_total = sum(
            count_trainable_parameters(module)
            for module in model.modules()
            if isinstance(module, BottleNeckBlock)
        )
        if details:
            details.extend(
                [
                    ("-- CBAM subtotal", cbam_total),
                    ("-- Projection subtotal", projection_total),
                    ("-- Fusion parent total (includes CBAM/projection/alpha)", count_trainable_parameters(fusion)),
                    ("-- Bottleneck subtotal (already inside RA total)", bottleneck_total),
                ]
            )

        print(f"\n{variant_name}")
        if not details:
            print("  no added attention parameters")
        for label, value in details:
            print(f"  {label:<55} {format_int(value):>12}")

    print("\nAll counts are trainable parameters; reconciliation against baseline: PASS")


if __name__ == "__main__":
    main()
