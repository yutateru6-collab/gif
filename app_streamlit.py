from __future__ import annotations

import io
import os
import tempfile
import zipfile
from pathlib import Path

import streamlit as st

from combat_sprite_generator.pipeline import run_pipeline
from combat_sprite_generator.presets import ANIMATION_PRESETS

st.set_page_config(page_title="Combat Sprite Generator", page_icon="🎮", layout="wide")
st.title("🎮 Combat Sprite Generator")
st.caption("1枚のキャラ画像 → 4×4・16コマの戦闘スプライト → GIF")

uploaded = st.file_uploader("キャラ画像", type=["png", "jpg", "jpeg", "webp"])

left, right = st.columns(2)
with left:
    animation = st.selectbox(
        "モーション",
        list(ANIMATION_PRESETS.keys()),
        format_func=lambda key: f"{key} — {ANIMATION_PRESETS[key]['title']}",
    )
    two_step = st.checkbox("先にピクセルキャラ化する（写真・イラスト向け）", value=True)
    resolution = st.selectbox("生成解像度", ["1K", "2K"], index=1)
with right:
    size = st.slider("GIFの1フレームサイズ", 64, 512, 256, 32)
    duration = st.slider("1フレームの表示時間（ms）", 60, 300, 140, 10)
    api_key_input = st.text_input(
        "Gemini APIキー（未入力なら環境変数を使用）",
        type="password",
        help="GEMINI_API_KEY / GOOGLE_API_KEY が設定済みなら空欄でOKです。",
    )

st.info("写真の場合は2段階方式を推奨。まず見た目をピクセル化し、その画像を参照して16コマを生成します。")

if uploaded is not None:
    st.image(uploaded, caption="入力画像", width=260)

if uploaded is not None and st.button("生成する", type="primary", use_container_width=True):
    api_key = api_key_input.strip() or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("Gemini APIキーが必要です。画面で入力するか、GEMINI_API_KEY を設定してください。")
        st.stop()

    with st.spinner("16コマを生成しています…"):
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            suffix = Path(uploaded.name).suffix.lower() or ".png"
            input_path = td_path / f"input{suffix}"
            input_path.write_bytes(uploaded.getvalue())
            out_dir = td_path / "output"

            try:
                result = run_pipeline(
                    input_image_path=input_path,
                    output_dir=out_dir,
                    animation=animation,
                    two_step=two_step,
                    size=size,
                    duration=duration,
                    resolution=resolution,
                    api_key=api_key,
                    keep_sheet=True,
                    keep_frames=True,
                )
            except Exception as exc:
                st.exception(exc)
                st.stop()

            st.success("生成完了")

            if result.get("base_pixelart"):
                st.subheader("1. ベースのピクセルキャラ")
                st.image(result["base_pixelart"], width=320)

            st.subheader("2. 4×4 スプライトシート")
            st.image(result["sheet"])

            st.subheader("3. GIF")
            st.image(result["gif"], width=320)

            st.subheader("4. 16フレーム")
            cols = st.columns(4)
            for index, frame in enumerate(result["frames"]):
                cols[index % 4].image(frame, caption=Path(frame).name)

            bundle = io.BytesIO()
            with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as zf:
                for path in out_dir.rglob("*"):
                    if path.is_file():
                        zf.write(path, arcname=path.relative_to(out_dir))
            bundle.seek(0)

            st.download_button(
                "生成物をZIPでダウンロード",
                data=bundle.getvalue(),
                file_name=f"combat_sprite_{animation}.zip",
                mime="application/zip",
                use_container_width=True,
            )
