from __future__ import annotations

import argparse
import json
from pathlib import Path

from .pipeline import run_pipeline
from .presets import ANIMATION_PRESETS


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a 4x4 combat sprite sheet, 16 PNG frames, and an animated GIF from one character image."
    )
    parser.add_argument("--input", required=True, help="Input character image path")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    parser.add_argument("--animation", default="slash", choices=sorted(ANIMATION_PRESETS.keys()))
    parser.add_argument("--two-step", action="store_true", help="Pixelize the input character before animation")
    parser.add_argument("--size", type=int, default=128, help="Output GIF/frame size in pixels")
    parser.add_argument("--duration", type=int, default=140, help="Frame duration in milliseconds")
    parser.add_argument("--resolution", default="2K", choices=["1K", "2K"])
    parser.add_argument("--api-key", default=None, help="Gemini API key; otherwise environment variable is used")
    parser.add_argument("--no-keep-sheet", action="store_true", help="Delete the generated sprite sheet after GIF creation")
    parser.add_argument("--no-keep-frames", action="store_true", help="Do not save individual PNG frames")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = run_pipeline(
        input_image_path=Path(args.input),
        output_dir=Path(args.output_dir),
        animation=args.animation,
        two_step=args.two_step,
        size=args.size,
        duration=args.duration,
        resolution=args.resolution,
        api_key=args.api_key,
        keep_sheet=not args.no_keep_sheet,
        keep_frames=not args.no_keep_frames,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
