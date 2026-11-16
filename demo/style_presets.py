"""Stable V0 style presets shared by poster and Vlog generation."""

from __future__ import annotations

from typing import Any


STYLE_PRESETS: dict[str, dict[str, Any]] = {
    "oil_painting": {
        "display_name": "油画风",
        "version": "2026-06-v1",
        "palette": ["#F3E6CF", "#2B2118", "#B87433", "#2F6F68"],
        "font_title": "SourceHanSans-Bold",
        "font_body": "SourceHanSans-Regular",
        "poster_templates": ["poster_single_oil_v1", "grid_9_oil_v1"],
        "vlog_template": "vlog_oil_v1",
        "prompt_positive": (
            "oil painting pet portrait, visible brush strokes, warm canvas texture, "
            "rich impasto but readable details, keep the original pet identity and markings"
        ),
        "seedance_video_style": (
            "LOCKED OIL PAINTING VIDEO STYLE: every frame must be a moving oil painting, "
            "with visible impasto brush strokes, warm canvas texture, painterly lighting, "
            "and preserved original pet markings. It must be a flat 2D painterly video, not a 3D model render. "
            "This must not look like raw phone footage."
        ),
        "prompt_negative": (
            "extra limbs, distorted face, changed breed, plastic 3d render, unreadable text, "
            "humanized body, scary, aggressive, raw phone video, unstyled original clip, "
            "simple cutdown, photorealistic live-action footage, 3D asset render, clay render, CGI turntable"
        ),
        "caption_tone": "像宠物肖像画标题，温暖、有收藏感",
    },
    "crayon": {
        "display_name": "蜡笔风",
        "version": "2026-06-v1",
        "palette": ["#FFF6D7", "#40342C", "#E98B56", "#67B7D1"],
        "font_title": "SourceHanSans-Bold",
        "font_body": "SourceHanSans-Regular",
        "poster_templates": ["poster_single_crayon_v1", "grid_9_crayon_v1"],
        "vlog_template": "vlog_crayon_v1",
        "prompt_positive": (
            "wax crayon pet illustration, visible crayon grain, warm paper texture, "
            "childlike but polished, keep the original pet identity and markings"
        ),
        "seedance_video_style": (
            "LOCKED CRAYON VIDEO STYLE: every frame must look like an animated wax crayon "
            "illustration on warm paper, with visible crayon grain, soft handmade color blocks, "
            "slightly uneven wax edges, childlike hand-drawn texture, and preserved original pet markings. "
            "It must be a flat 2D crayon animation, not a 3D model render. This must not look like raw phone footage."
        ),
        "prompt_negative": (
            "extra limbs, distorted face, changed breed, oil paint, watercolor wash, "
            "unreadable text, scary, messy scribbles, raw phone video, unstyled original clip, "
            "simple cutdown, photorealistic live-action footage, 3D asset render, clay render, CGI turntable, "
            "polished anime, realistic fur render, generic cartoon without crayon grain"
        ),
        "caption_tone": "童趣、柔软、像手作小卡片",
    },
    "doodle": {
        "display_name": "涂鸦 Doodle 风",
        "version": "2026-06-v1",
        "palette": ["#FFFDF5", "#171717", "#FF6B6B", "#3CA7FF"],
        "font_title": "SourceHanSans-Bold",
        "font_body": "SourceHanSans-Regular",
        "poster_templates": ["grid_9_doodle_v1", "poster_single_doodle_v1"],
        "vlog_template": "vlog_doodle_v1",
        "prompt_positive": (
            "playful doodle pet illustration, bold black marker outlines, flat color fills, "
            "clean sketchbook background, sticker-like accents, preserve pet markings"
        ),
        "seedance_video_style": (
            "LOCKED DOODLE VIDEO STYLE: every frame must be a playful doodle animation, "
            "with bold black marker outlines, flat cheerful color fills, sketchbook texture, "
            "sticker-like accents, and preserved original pet markings. It must be a flat 2D doodle video, "
            "not a 3D model render. This must not look like raw phone footage."
        ),
        "prompt_negative": (
            "extra limbs, distorted face, changed breed, dense graffiti wall, unreadable text, "
            "humanized body, scary, dirty background, raw phone video, unstyled original clip, "
            "simple cutdown, photorealistic live-action footage, 3D asset render, clay render, CGI turntable"
        ),
        "caption_tone": "活泼、短句、像手绘贴纸说明",
    },
}

STYLE_ALIASES: dict[str, str] = {
    "gentle_diary": "crayon",
    "film_moment": "oil_painting",
    "film_memory": "oil_painting",
    "comic_pet": "doodle",
}


def resolve_style_id(style_id: str) -> str:
    return STYLE_ALIASES.get(style_id, style_id)


def get_style_preset(style_id: str) -> dict[str, Any]:
    style_id = resolve_style_id(style_id)
    try:
        return STYLE_PRESETS[style_id]
    except KeyError as exc:
        allowed = ", ".join(sorted([*STYLE_PRESETS, *STYLE_ALIASES]))
        raise ValueError(f"unknown style_id '{style_id}', expected one of: {allowed}") from exc
