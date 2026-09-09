# Combat Sprite Generator

1枚のキャラ画像から、**4×4・16コマのピクセルアート戦闘スプライトシート**を生成し、16枚のPNGフレームとアニメGIFを書き出すツールです。

## 主な機能

- キャラ画像1枚を入力
- 写真や通常イラストを先にピクセルキャラ化する2段階モード
- 4×4・16コマのスプライトシート生成
- 16フレームPNGの自動切り出し
- GIFアニメーション生成
- StreamlitのブラウザUI
- 生成物ZIPダウンロード
- GitHub Actionsによる自動テスト

## モーション

現在は5種類あります。

- `slash` — 剣の斬撃
- `punch` — パンチコンボ
- `spell` — 魔法詠唱・発射
- `jump_attack` — ジャンプ攻撃
- `idle` — 待機モーション

モーションは `combat_sprite_generator/presets.py` に追加できます。

## 必要なもの

- Python 3.10+
- Gemini APIキー

Gemini APIキーは `GEMINI_API_KEY` または `GOOGLE_API_KEY` として設定できます。

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

## セットアップ

```bash
git clone https://github.com/yutateru6-collab/gif.git
cd gif
python -m venv .venv
```

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

インストール:

```bash
pip install -e .
```

## ブラウザUIで使う

```bash
streamlit run app_streamlit.py
```

ブラウザが開いたら、

1. キャラ画像をアップロード
2. モーションを選ぶ
3. 写真なら「先にピクセルキャラ化」をON
4. `生成する` を押す
5. スプライトシート、GIF、16フレームを確認
6. ZIPでまとめてダウンロード

という流れです。

## CLIで使う

写真から剣攻撃を作る例:

```bash
combat-sprite-generator \
  --input ./character.png \
  --output-dir ./out \
  --animation slash \
  --two-step \
  --size 256 \
  --duration 140 \
  --resolution 2K
```

既にピクセルアート化した画像を使う場合:

```bash
combat-sprite-generator \
  --input ./pixel_character.png \
  --output-dir ./out \
  --animation spell \
  --size 256 \
  --resolution 2K
```

## 出力

標準では次のファイルが作られます。

```text
out/
├── base_pixelart.png     # --two-step の場合
├── template.png
├── sprite_sheet.png
├── animation.gif
└── frames/
    ├── frame_01.png
    ├── frame_02.png
    ├── ...
    └── frame_16.png
```

## 2段階方式を推奨する理由

人物写真や特定キャラでは、

1. 元画像からベースのピクセルキャラを作る
2. その確定した見た目を参照して16コマを作る

という2段階の方が、1回で「デザイン変更＋アニメーション生成」を同時に行わせるより、キャラの見た目を揃えやすくなります。

## キャラ一貫性のためにプロンプトで固定しているもの

- 髪型
- 服装
- 配色
- 体格・シルエット
- 武器・アクセサリー
- キャラの大きさ
- フレーム内での位置
- 4×4のセル境界

## テスト

```bash
pip install pytest
pytest -q
```

現在のローカルテストでは、

- 4×4テンプレートが16フレームに正しく分割されること
- 16枚のPNGを書き出せること
- GIFを生成できること

を検証しています。

GitHub Actionsでも `main` へのpushごとに同じテストを実行します。

## 注意点

Geminiによる画像生成部分は外部APIを使用します。APIキー、利用可能モデル、料金、レート制限などはGoogle側の設定に依存します。

AI画像生成なので、16コマすべてのキャラ一致やセル境界が毎回100%保証されるわけではありません。特に実在人物や細かい装飾のあるキャラでは、ベース画像を先に確定する2段階方式を推奨します。

## 構成

```text
combat_sprite_generator/
├── cli.py        # CLI
├── pipeline.py   # Gemini呼び出し、フレーム分割、GIF化
├── presets.py    # 戦闘モーション定義
└── template.py   # 4×4テンプレート生成・切り出し

app_streamlit.py  # Web UI
tests/            # ローカルテスト
.github/workflows/ci.yml
```
