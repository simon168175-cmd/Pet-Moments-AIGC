"""Pillow local-template poster renderer for 05 AIGC outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps


STYLE_CONFIG = {
    "oil_painting": {
        "bg": (243, 230, 207),
        "ink": (43, 33, 24),
        "accent": (184, 116, 51),
        "caption": "油画高光",
    },
    "crayon": {
        "bg": (255, 246, 215),
        "ink": (64, 52, 44),
        "accent": (233, 139, 86),
        "caption": "蜡笔小日记",
    },
    "doodle": {
        "bg": (255, 253, 245),
        "ink": (23, 23, 23),
        "accent": (255, 107, 107),
        "caption": "DOODLE MOMENTS",
    },
}

STYLE_ALIASES = {
    "gentle_diary": "crayon",
    "film_moment": "oil_painting",
    "film_memory": "oil_painting",
    "comic_pet": "doodle",
}


def render_local_template_poster(
    frame_paths: list[Path],
    output_path: Path,
    style: dict[str, Any] | None = None,
    title: str = "PawRig 精彩瞬间",
) -> bool:
    existing = [path for path in frame_paths if path.exists()][:9]
    if not existing:
        return False

    style_id = STYLE_ALIASES.get(str((style or {}).get("id") or "oil_painting"), str((style or {}).get("id") or "oil_painting"))
    config = STYLE_CONFIG.get(style_id, STYLE_CONFIG["oil_painting"])
    canvas_size = 1080
    margin = 54
    header_h = 150
    gap = 16
    cell = (canvas_size - margin * 2 - gap * 2) // 3
    image_top = header_h + margin

    canvas = Image.new("RGB", (canvas_size, canvas_size), config["bg"])
    draw = ImageDraw.Draw(canvas)
    draw.text((margin, 44), title, fill=config["ink"])
    draw.text((margin, 88), config["caption"], fill=config["accent"])
    draw.line((margin, 128, canvas_size - margin, 128), fill=config["accent"], width=4)

    for index, path in enumerate(existing):
        row, col = divmod(index, 3)
        x = margin + col * (cell + gap)
        y = image_top + row * (cell + gap)
        thumb = ImageOps.fit(Image.open(path).convert("RGB"), (cell, cell), method=Image.Resampling.LANCZOS)
        thumb = _apply_style(thumb, style_id)
        if style_id == "doodle":
            border = 8
            draw.rectangle((x - border, y - border, x + cell + border, y + cell + border), fill=config["ink"])
        elif style_id == "oil_painting":
            draw.rectangle((x - 5, y - 5, x + cell + 5, y + cell + 5), outline=config["ink"], width=5)
        canvas.paste(thumb, (x, y))

    footer = "AI-selected local template"
    draw.text((margin, canvas_size - 44), footer, fill=config["ink"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path, quality=94)
    return True


def _apply_style(image: Image.Image, style_id: str) -> Image.Image:
    style_id = STYLE_ALIASES.get(style_id, style_id)
    if style_id == "oil_painting":
        image = ImageEnhance.Contrast(image).enhance(1.16)
        image = ImageEnhance.Color(image).enhance(0.95)
        image = image.filter(ImageFilter.ModeFilter(size=3))
        overlay = Image.new("RGB", image.size, (255, 210, 150))
        return Image.blend(image, overlay, 0.07)
    if style_id == "crayon":
        image = ImageEnhance.Color(image).enhance(1.08)
        paper = Image.effect_noise(image.size, 18).convert("L")
        paper = ImageOps.colorize(paper, black="#efe2bf", white="#ffffff")
        return Image.blend(image, paper, 0.16)
    if style_id == "doodle":
        edges = image.filter(ImageFilter.FIND_EDGES).convert("L")
        edges = ImageOps.autocontrast(edges)
        color = ImageEnhance.Color(image).enhance(1.35)
        return Image.blend(color, ImageOps.invert(edges).convert("RGB"), 0.20)
    return image
