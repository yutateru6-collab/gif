from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from PIL import Image, ImageDraw, ImageFont


def _safe_font(size: int = 14):
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except Exception:
        return ImageFont.load_default()


def create_template(
    cols: int = 4,
    rows: int = 4,
    cell_size: int = 256,
    labels: Iterable[str] | None = None,
    out_path: Path | None = None,
) -> Image.Image:
    width = cols * cell_size
    height = rows * cell_size
    img = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = _safe_font(max(12, cell_size // 18))

    labels = list(labels or [f"frame-{i+1}" for i in range(cols * rows)])
    if len(labels) != cols * rows:
        raise ValueError("labels length must equal cols * rows")

    for y in range(rows):
        for x in range(cols):
            left = x * cell_size
            top = y * cell_size
            right = left + cell_size
            bottom = top + cell_size
            draw.rectangle([left, top, right, bottom], outline=(0, 0, 0, 255), width=2)
            idx = y * cols + x
            label = f"{idx+1:02d} {labels[idx]}"
            text_width = draw.textlength(label, font=font)
            draw.rectangle(
                [left + 8, top + 8, left + 16 + text_width, top + 32],
                fill=(255, 255, 255, 220),
            )
            draw.text((left + 12, top + 10), label, fill=(0, 0, 0, 255), font=font)

    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(out_path)
    return img


def extract_frames(sheet: Image.Image, cols: int = 4, rows: int = 4) -> List[Image.Image]:
    frame_w = sheet.width // cols
    frame_h = sheet.height // rows
    frames = []
    for y in range(rows):
        for x in range(cols):
            left = x * frame_w
            top = y * frame_h
            frames.append(sheet.crop((left, top, left + frame_w, top + frame_h)))
    return frames
