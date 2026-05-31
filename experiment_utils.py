VALID_ATTENTION_MODES = ("none", "pre_hidden", "cnn_fusion")
VALID_ATTENTION_SCALES = ("1/2", "1/4", "1/8", "1/16")
VALID_REVERSE_ATTENTION_MODES = ("none", "ra_skip", "ra_bridge", "ra_fusion")


def parse_attention_scales(mode, scales_arg):
    if mode not in VALID_ATTENTION_MODES:
        raise ValueError(f"Unsupported attention mode: {mode}")

    if mode == "none":
        return tuple()

    if scales_arg:
        raw_scales = [item.strip() for item in scales_arg.split(",") if item.strip()]
    elif mode == "pre_hidden":
        raw_scales = ["1/16"]
    else:
        raw_scales = ["1/8", "1/4", "1/2"]

    seen = set()
    normalized = []
    for scale in raw_scales:
        if scale not in VALID_ATTENTION_SCALES:
            valid = ", ".join(VALID_ATTENTION_SCALES)
            raise ValueError(f"Unsupported attention scale '{scale}'. Valid values: {valid}")
        if scale not in seen:
            normalized.append(scale)
            seen.add(scale)

    if not normalized:
        raise ValueError("At least one attention scale is required when attention is enabled.")

    return tuple(normalized)


def apply_attention_config(config, mode, scales, reduction):
    config.attention_mode = mode
    config.attention_scales = tuple(scales)
    config.attention_reduction = reduction
    return config


def build_attention_suffix(mode, scales, reduction=None):
    if mode == "none":
        return ""
    scale_tag = "-".join(scale.replace("/", "_") for scale in scales)
    suffix = f"_attn-{mode}-{scale_tag}"
    if reduction is not None:
        suffix += f"-r{reduction}"
    return suffix


def parse_reverse_attention_scales(mode, scales_arg):
    if mode not in VALID_REVERSE_ATTENTION_MODES:
        valid = ", ".join(VALID_REVERSE_ATTENTION_MODES)
        raise ValueError(f"Unsupported reverse attention mode '{mode}'. Valid values: {valid}")

    if mode == "none":
        return tuple()

    if mode == "ra_bridge":
        return tuple()

    raw_scales = [item.strip() for item in str(scales_arg).split(",") if item.strip()]
    if not raw_scales:
        raw_scales = ["0"]

    seen = set()
    normalized = []
    for raw_scale in raw_scales:
        try:
            scale = int(raw_scale)
        except ValueError as exc:
            raise ValueError(f"Reverse attention scale must be an integer, got '{raw_scale}'.") from exc
        if scale < 0:
            raise ValueError(f"Reverse attention scale must be non-negative, got {scale}.")
        if scale not in seen:
            normalized.append(scale)
            seen.add(scale)

    return tuple(normalized)


def apply_reverse_attention_config(config, mode, scales, reduction):
    config.reverse_attention_mode = mode
    config.reverse_attention_scales = tuple(scales)
    config.reverse_attention_reduction = reduction
    return config


def build_reverse_attention_suffix(mode, scales, reduction=None):
    if mode == "none":
        return ""

    if mode == "ra_bridge":
        suffix = f"_ra-{mode}"
        if reduction is not None:
            suffix += f"-r{int(reduction)}"
        return suffix

    parsed_scales = parse_reverse_attention_scales(mode, scales) if isinstance(scales, str) else tuple(scales)
    scale_tag = "".join(str(scale) for scale in parsed_scales)
    suffix = f"_ra-{mode}-s{scale_tag}"
    if reduction is not None:
        suffix += f"-r{int(reduction)}"
    return suffix


def parse_skip_indices(indices_arg):
    raw_indices = [item.strip() for item in str(indices_arg).split(",") if item.strip()]
    if not raw_indices:
        return tuple()

    seen = set()
    normalized = []
    for raw_index in raw_indices:
        try:
            index = int(raw_index)
        except ValueError as exc:
            raise ValueError(f"Skip index must be an integer, got '{raw_index}'.") from exc
        if index < 0:
            raise ValueError(f"Skip index must be non-negative, got {index}.")
        if index not in seen:
            normalized.append(index)
            seen.add(index)
    return tuple(normalized)


def build_skip_indices_suffix(skip_indices):
    if not skip_indices:
        return ""
    tag = "".join(str(index) for index in skip_indices)
    return f"_skipidx{tag}"
