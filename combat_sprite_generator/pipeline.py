from __future__ import annotations

import base64
import io
import os
from pathlib import Path
from typing import Sequence

from PIL import Image

from .presets import build_two_step_prompt, get_preset
from .template import create_template, extract_frames

SUPPORTED_IMAGE_MIME = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}


def get_api_key(explicit_api_key: str | None = None) -> str:
    api_key = explicit_api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY か GOOGLE_API_KEY を設定してください。")
    return api_key


def _get_client(api_key: str):
    from google import genai

    return genai.Client(api_key=api_key)


def _mime_from_path(path: Path) -> str:
    mime = SUPPORTED_IMAGE_MIME.get(path.suffix.lower())
    if not mime:
        raise ValueError(f"Unsupported image type: {path.suffix}")
    return mime


def _image_input_dict(path: Path) -> dict:
    image_bytes = path.read_bytes()
    return {
        "type": "image",
        "data": base64.b64encode(image_bytes).decode("utf-8"),
        "mime_type": _mime_from_path(path),
    }


def _save_output_image(interaction, output_path: Path) -> Image.Image:
    if not getattr(interaction, "output_image", None):
        raise RuntimeError("Gemini response did not include output_image")
    output_bytes = base64.b64decode(interaction.output_image.data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(output_bytes)
    return Image.open(io.BytesIO(output_bytes)).convert("RGBA")


def create_base_pixelart(
    input_image_path: Path,
    output_path: Path,
    resolution: str = "1K",
    api_key: str | None = None,
    model: str = "gemini-3.1-flash-image",
) -> Path:
    api_key = get_api_key(api_key)
    client = _get_client(api_key)
    interaction = client.interactions.create(
        model=model,
        input=[
            {"type": "text", "text": build_two_step_prompt()},
            _image_input_dict(input_image_path),
        ],
        response_format={
            "type": "image",
            "image_size": resolution,
        },
    )
    _save_output_image(interaction, output_path)
    return output_path


def generate_sprite_sheet(
    source_image_path: Path,
    template_path: Path,
    output_sheet_path: Path,
    animation: str,
    resolution: str = "2K",
    api_key: str | None = None,
    model: str = "gemini-3.1-flash-image",
) -> Path:
    api_key = get_api_key(api_key)
    client = _get_client(api_key)
    preset = get_preset(animation)

    prompt = (
        "Use Image A as the character identity reference and Image B as the 4x4 sprite sheet layout template. "
        f"Generate exactly one 4x4 sprite sheet image. {preset['prompt']} "
        "The final image must be one complete sprite sheet, not separate images. "
        "Keep every pose inside its own cell and do not add titles, captions, UI, borders, or extra characters."
    )

    interaction = client.interactions.create(
        model=model,
        input=[
            {"type": "text", "text": prompt},
            _image_input_dict(source_image_path),
            _image_input_dict(template_path),
        ],
        response_format={
            "type": "image",
            "image_size": resolution,
            "aspect_ratio": "1:1",
        },
    )
    _save_output_image(interaction, output_sheet_path)
    return output_sheet_path


def frames_to_gif(
    frames: Sequence[Image.Image],
    output_path: Path,
    frame_duration: int = 140,
    size: int = 128,
) -> Path:
    if not frames:
        raise ValueError("frames must not be empty")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    resized = [frame.convert("RGBA").resize((size, size), Image.Resampling.NEAREST) for frame in frames]
    first, *rest = resized
    first.save(
        output_path,
        save_all=True,
        append_images=rest,
        duration=frame_duration,
        loop=0,
        disposal=2,
        optimize=False,
    )
    return output_path


def save_frames(
    frames: Sequence[Image.Image],
    output_dir: Path,
    size: int | None = None,
) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []
    for idx, frame in enumerate(frames, start=1):
        img = frame.convert("RGBA")
        if size is not None:
            img = img.resize((size, size), Image.Resampling.NEAREST)
        path = output_dir / f"frame_{idx:02d}.png"
        img.save(path)
        saved.append(path)
    return saved


def run_pipeline(
    input_image_path: Path,
    output_dir: Path,
    animation: str = "slash",
    two_step: bool = False,
    size: int = 128,
    duration: int = 140,
    resolution: str = "2K",
    api_key: str | None = None,
    keep_sheet: bool = True,
    keep_frames: bool = True,
) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    working_source = input_image_path
    base_pixelart_path = output_dir / "base_pixelart.png"

    if two_step:
        create_base_pixelart(
            input_image_path=input_image_path,
            output_path=base_pixelart_path,
            resolution="1K",
            api_key=api_key,
        )
        working_source = base_pixelart_path

    preset = get_preset(animation)
    template_path = output_dir / "template.png"
    create_template(labels=preset["labels"], out_path=template_path)

    sheet_path = output_dir / "sprite_sheet.png"
    generate_sprite_sheet(
        source_image_path=working_source,
        template_path=template_path,
        output_sheet_path=sheet_path,
        animation=animation,
        resolution=resolution,
        api_key=api_key,
    )

    sheet_img = Image.open(sheet_path).convert("RGBA")
    frames = extract_frames(sheet_img, cols=4, rows=4)

    frame_paths: list[Path] = []
    if keep_frames:
        frame_paths = save_frames(frames, output_dir / "frames", size=size)

    gif_path = frames_to_gif(
        frames,
        output_dir / "animation.gif",
        frame_duration=duration,
        size=size,
    )

    if not keep_sheet and sheet_path.exists():
        sheet_path.unlink()

    return {
        "input": str(input_image_path),
        "source_used": str(working_source),
        "base_pixelart": str(base_pixelart_path) if two_step else None,
        "template": str(template_path),
        "sheet": str(sheet_path) if keep_sheet else None,
        "frames": [str(path) for path in frame_paths],
        "gif": str(gif_path),
        "animation": animation,
    }
