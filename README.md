# PNG Metadata Viewer

Stable Diffusion などの AI 生成画像を整理・閲覧するためのビューワーソフトです。

PNG を中心に、メタデータ表示、LoRA 管理、サムネイル一覧、タグ集計、重複検出、ロゴオーバーレイまでを 1 つのデスクトップアプリにまとめています。

AI 画像の制作・整理・確認と相性がよく、生成時のプロンプトや LoRA 情報を見ながら運用しやすいのが特徴です。

## Highlights

- `PySide6` ベースの 3 ペイン GUI
- 高速なスキャン、閲覧、サムネイル表示
- PNG メタデータ解析と表示
- LoRA / モデル情報の一覧管理と検索
- 重複検出、評価、Favorites、タグ集計
- キャッシュを活かした軽快なフォルダ運用

## Tech Points

- `QThread` / `QRunnable` / `QThreadPool` を使って UI を止めない設計
- `QSplitter` ベースの柔軟なレイアウト
- Pillow と Qt を組み合わせた画像処理
- ローカルキャッシュと永続化設定で再起動後も使いやすい構成
- 単体スクリプトとして配布しやすい実装

## Requirements

- Python 3.11+
- Windows 10 / 11

```bash
pip install -r requirements.txt
python png_viewer_v203.py
```

## Optional Environment Variables

- `PNG_VIEWER_DEFAULT_FOLDER`
  - 起動時に最初に開くフォルダを指定します
- `CIVITAI_API_KEY`
  - Civitai API を使った検索を有効にします

```powershell
$env:PNG_VIEWER_DEFAULT_FOLDER = "D:\Images"
$env:CIVITAI_API_KEY = "your_api_key"
python .\png_viewer_v203.py
```
