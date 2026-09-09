from pathlib import Path

from PIL import Image, ImageDraw

from combat_sprite_generator.pipeline import frames_to_gif, save_frames
from combat_sprite_generator.template import create_template, extract_frames


def test_template_has_16_frames(tmp_path: Path):
    template_path = tmp_path / "template.png"
    template = create_template(cell_size=64, out_path=template_path)
    frames = extract_frames(template)
    assert template_path.exists()
    assert len(frames) == 16
    assert all(frame.size == (64, 64) for frame in frames)


def test_extract_and_gif(tmp_path: Path):
    sheet = Image.new("RGBA", (256, 256), (255, 255, 255, 0))
    draw = ImageDraw.Draw(sheet)
    for i in range(16):
        x = (i % 4) * 64
        y = (i // 4) * 64
        draw.rectangle(
            [x + 8, y + 8, x + 56, y + 56],
            fill=((17 * i) % 255, (41 * i) % 255, (73 * i) % 255, 255),
        )

    frames = extract_frames(sheet)
    frame_paths = save_frames(frames, tmp_path / "frames", size=64)
    gif_path = frames_to_gif(frames, tmp_path / "animation.gif", frame_duration=120, size=64)

    assert len(frame_paths) == 16
    assert all(path.exists() for path in frame_paths)
    assert gif_path.exists()
    assert gif_path.stat().st_size > 0
