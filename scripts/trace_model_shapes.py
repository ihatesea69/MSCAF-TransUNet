"""Trace tensor shapes through the project's TransUNet variants.

This script uses forward hooks on the real modules. It does not load a checkpoint,
so it verifies architecture wiring and tensor compatibility, not model quality.
"""

from __future__ import annotations

import argparse
import copy
import gc
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from networks.vit_seg_modeling import CONFIGS, VisionTransformer


VARIANTS = {
    "A_baseline": {
        "attention_mode": "none",
        "attention_scales": (),
        "reverse_attention_mode": "none",
        "reverse_attention_scales": (),
    },
    "B_pre_hidden": {
        "attention_mode": "pre_hidden",
        "attention_scales": ("1/16",),
        "reverse_attention_mode": "none",
        "reverse_attention_scales": (),
    },
    "C_cnn_fusion": {
        "attention_mode": "cnn_fusion",
        "attention_scales": ("1/8", "1/4", "1/2"),
        "reverse_attention_mode": "none",
        "reverse_attention_scales": (),
    },
    "D_ra_skip": {
        "attention_mode": "pre_hidden",
        "attention_scales": ("1/16",),
        "reverse_attention_mode": "ra_skip",
        "reverse_attention_scales": (0,),
    },
    "E_ra_fusion": {
        "attention_mode": "pre_hidden",
        "attention_scales": ("1/16",),
        "reverse_attention_mode": "ra_fusion",
        "reverse_attention_scales": (0,),
    },
}


def build_model(variant_name: str, image_size: int, num_classes: int) -> VisionTransformer:
    variant = VARIANTS[variant_name]
    config = copy.deepcopy(CONFIGS["R50-ViT-B_16"])
    config.n_classes = num_classes
    config.n_skip = 3
    config.skip_indices = ()
    config.patches.grid = (image_size // 16, image_size // 16)
    config.attention_mode = variant["attention_mode"]
    config.attention_scales = variant["attention_scales"]
    config.attention_reduction = 16
    config.reverse_attention_mode = variant["reverse_attention_mode"]
    config.reverse_attention_scales = variant["reverse_attention_scales"]
    config.reverse_attention_reduction = 4
    return VisionTransformer(config, img_size=image_size, num_classes=num_classes)


def shape_tree(value) -> str:
    if isinstance(value, torch.Tensor):
        return str(list(value.shape))
    if isinstance(value, Mapping):
        parts = ", ".join(f"{key}: {shape_tree(item)}" for key, item in value.items())
        return "{" + parts + "}"
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return "(" + ", ".join(shape_tree(item) for item in value) + ")"
    if value is None:
        return "None"
    return type(value).__name__


def selected_modules(model: VisionTransformer):
    embeddings = model.transformer.embeddings
    yield "01.resnet.root", embeddings.hybrid_model.root
    for index, block in enumerate(embeddings.hybrid_model.body.children(), start=1):
        yield f"02.resnet.block{index}", block
    yield "03.cnn_feature_fusion", embeddings.cnn_feature_fusion
    for scale, block in embeddings.cnn_feature_fusion.attention_blocks.items():
        yield f"03a.attention[{scale}]", block
    for scale, bridge in embeddings.cnn_feature_fusion.hidden_bridges.items():
        yield f"03b.projection[{scale}]", bridge
    yield "04.patch_embeddings", embeddings.patch_embeddings
    for index, block in enumerate(model.transformer.encoder.layer):
        yield f"05.transformer.block{index:02d}", block
    yield "06.encoder.norm", model.transformer.encoder.encoder_norm
    yield "07.decoder.conv_more", model.decoder.conv_more
    if model.decoder.ra_bridge is not None:
        yield "08.decoder.ra_bridge", model.decoder.ra_bridge
    if model.decoder.ra_modules is not None:
        for index, block in model.decoder.ra_modules.items():
            yield f"08.decoder.ra_skip[{index}]", block
    for index, block in enumerate(model.decoder.blocks):
        if block.fusion_attention is not None:
            yield f"09.decoder.ra_fusion[{index}]", block.fusion_attention
        yield f"10.decoder.block{index}", block
    yield "11.segmentation_head", model.segmentation_head


def trace_variant(
    variant_name: str,
    image_size: int,
    num_classes: int,
    batch_size: int,
    device: torch.device,
) -> None:
    model = build_model(variant_name, image_size, num_classes).to(device).eval()
    handles = []

    def make_hook(label: str):
        def hook(_module, inputs, kwargs, output):
            input_description = shape_tree(inputs)
            if kwargs:
                input_description += f"; kwargs={shape_tree(kwargs)}"
            print(f"{label:<31} {input_description:<48} -> {shape_tree(output)}")

        return hook

    for label, module in selected_modules(model):
        handles.append(module.register_forward_hook(make_hook(label), with_kwargs=True))

    x = torch.randn(batch_size, 1, image_size, image_size, device=device)
    print(f"\n=== {variant_name} ===")
    print(f"input                           {shape_tree(x)}; channel 1 is repeated to channel 3")
    with torch.no_grad():
        logits = model(x)

    expected = (batch_size, num_classes, image_size, image_size)
    if tuple(logits.shape) != expected:
        raise RuntimeError(f"Unexpected output for {variant_name}: {tuple(logits.shape)} != {expected}")
    print(f"verified output                 {shape_tree(logits)}")

    for handle in handles:
        handle.remove()
    del logits, x, model
    gc.collect()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", choices=["all", *VARIANTS], default="B_pre_hidden")
    parser.add_argument("--image-size", type=int, default=224)
    parser.add_argument("--num-classes", type=int, default=9)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--device", choices=("auto", "cpu", "cuda"), default="auto")
    parser.add_argument("--threads", type=int, default=4)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    torch.set_num_threads(args.threads)
    torch.manual_seed(1234)
    if args.device == "auto":
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device(args.device)
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is not available.")

    variants = VARIANTS if args.variant == "all" else (args.variant,)
    print(f"device={device}; random_init=True; variants={list(variants)}")
    for variant_name in variants:
        trace_variant(variant_name, args.image_size, args.num_classes, args.batch_size, device)


if __name__ == "__main__":
    main()
