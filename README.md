# PNG Metadata Viewer

PySide6 で構築した、生成画像向けの高速メタデータビューアです。  
PNG を中心に、LoRA 管理、サムネイル一覧、全文検索、重複検出、タグ集計までを 1 つのデスクトップアプリにまとめています。

## Highlights

- `PySide6` ベースの 3 ペイン GUI
- 非同期スキャン、先読み、サムネイル生成
- PNG メタデータ解析と再保存
- LoRA / モデル情報の一覧化と検索補助
- 重複検出、評価、Favorites、タグ集計
- キャッシュを使った大規模フォルダの実用運用

## Tech Points

- `QThread` / `QRunnable` / `QThreadPool` を使い分けて UI 応答性を維持
- `QSplitter` ベースで複数レイアウトを切り替え可能
- Pillow と Qt の橋渡しを行う画像パイプライン
- ローカルキャッシュと永続設定で再起動後も状態を復元
- 単一スクリプトながら、ワーカー、ビュー、モデルが役割分離されている構成

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
  - Civitai API を使った補助検索を有効にします

例:

```powershell
$env:PNG_VIEWER_DEFAULT_FOLDER = "D:\Images"
$env:CIVITAI_API_KEY = "your_api_key"
python .\png_viewer_v203.py
```

## Project Structure

- `png_viewer_v203.py`
  - アプリ本体
- `CHANGELOG.md`
  - 開発履歴
- `app_icon.ico`
  - アプリアイコン
- `PNG_Metadata_Viewer_v203_onefile.spec`
  - PyInstaller 用設定

## Notes For GitHub Release

- ローカル依存の固定パスは環境変数ベースに変更済みです
- API キーはコードに埋め込まず、環境変数から読む方式です
- `build/`, `dist/`, `__pycache__/` はコミット対象から外す想定です

## Why This Project Matters

このアプリは、単なる画像ビューアではなく、

- 実運用を意識した GUI 設計
- 速度改善のための並列処理
- メタデータ活用
- 生成ワークフローに寄せた UX 設計

をまとめて形にしたデスクトップツールです。  
GitHub では「便利ツール」としてだけでなく、「設計と改善を積み重ねられる実装者」であることが伝わる題材として公開できます。
