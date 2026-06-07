# CHANGELOG

PNG/画像メタデータビューア (PySide6版) — 更新履歴

---

## [v2.03] 2026-04-07 (Claude Sonnet 4.6)

### 新機能
- **タイトルロゴ オーバーレイ機能**を実装 (`OverlayManager` クラスを新設)。設定は `overlay_settings.json` に永続化。
  - グリッド右クリックメニュー「🎨 ロゴオーバーレイ」サブメニューを追加:
    - 「ロゴを設定...」: PNG を選択して1件または複数件に一括適用
    - 「位置・サイズ調整...」: X/Y位置(0.0〜1.0)・スケールをスピンボックスで調整
    - 「ロゴを削除」: 選択件数分のオーバーレイ設定を削除
    - 「合成画像を出力...」: 元ファイルを変更せず、合成済みPNGを別途保存
  - ツールメニュー「🎨 ロゴ/タグ連動設定」を追加（タグ→ロゴの紐付けテーブル管理）
  - `_compose_overlay()` メソッド: QPixmap をオフスクリーンで合成し全プレビュー表示に反映
  - `_sel_image()` でタグ連動 auto_apply を実行

---

## [v2.02] 2026-04-07 (Claude Sonnet 4.6)

### 新機能
- **メタキャッシュの永続化**: `MetaCache` に `save_to_disk` / `load_from_disk` メソッドを追加。pickle形式で `%LOCALAPPDATA%/png_viewer/meta_cache.pkl` に保存。起動時に自動ロード、closeEvent で自動保存。`META.get()` に mtime チェックを追加し外部更新ファイルのキャッシュを自動無効化。ツールメニューに「🗑 メタキャッシュを初期化」を追加。
- **全サムネ事前生成**: `_prebuild_all_thumbs` メソッドを追加。ツールメニュー「🖼 全サムネイルを一括生成」から実行可能。キャッシュ済みをスキップしてディスクキャッシュがないものだけ ThumbLoader に一括投入。

### 高速化
- **PreloadWorker のキャッシュ済みスキップ最適化**: ScanWorker が収集した mtime と MetaCache の mtime を照合し、一致するファイルはメタ解析をスキップ。2回目以降のフォルダスキャンで未変更ファイルが即完了するようになる。

---

## [v2.01] 2026-04-07 (Claude Sonnet 4.6)

### UI修正
- **LoRA分析ウィンドウの検索欄の幅を倍に拡大**: `setFixedWidth(240)` → `setFixedWidth(480)` に変更。より長いLoRA名でも切れずに表示・入力できるようになった。

---

## [v2.00] 2026-04-07 (Claude Sonnet 4.6)

### 重大バグ修正
- **サブフォルダ読み込み時にファイル数が多いと絞り込みが機能しない問題**を修正:
  - 根本原因①: `MetaCache._MAX_META_ENTRIES = 5000` が小さすぎた → `50000` に拡大
  - 根本原因②: `FilterWorker` / `TagCountWorker` が未キャッシュファイルを同期パースしていた → 同期パース廃止、未キャッシュはスキップ
  - 根本原因③: `_apply_filter()` が PreloadWorker 完了前に走るタイミング問題 → `_on_preload_progress()` に500件ごとのフィルター再適用ロジックを追加
  - `_on_preload_done()` でもフィルター条件が設定されていれば再適用（全件確定後の最終反映）

---

## [v1.99] 2026-04-07 (Claude Sonnet 4.6)

### 新機能
- **モデル名クリックでツールバーのモデル検索コンボに反映**: 右パネルの「モデル:」欄をクリックすると `model_cb` にセットされ即座にフィルター適用。`MetaPanel` に `model_search_requested` シグナルを新設。フェードトースト「🔍 モデルで絞り込み: <名前>」を表示。

---

## [v1.98] 2026-04-07 (Claude Sonnet 4.6)

### 新機能
- **Positive/Negativeヘッダーに重複タグ数バッジと2種コピーボタンを追加**:
  - 重複タグが1件以上ある場合、ヘッダー右端に「重複N」バッジ（黄色）を表示
  - 📋✨ (dedup): 重複除去済みテキストをコピー / 📋 (plain): 元テキストをそのままコピー

### UI修正
- **並び替えコンボボックス（QComboBox）の高さ**をボタンに揃える: `setFixedHeight(26)` を追加。

---

## [v1.97] 2026-04-06 (Claude Sonnet 4.6)

### バグ修正
- **EXE関連付けで画像をクリックしてもビュアーが画像を開いた状態にならない問題**を修正: `_pending_open` フラグを新設。`_on_scan_done` 内の `_do_select()` 完了後100ms待ってから `_open_full()` を呼ぶ。

---

## [v1.94] 2026-04-06 (Claude Sonnet 4.6)

### 新機能
- **アプリアイコンをBase64埋め込みで設定**: `PNGViewer.ico` (16/32/48/64/128/256px) をソース内にBase64で埋め込み。外部icoファイル不要。exe化後もアイコンが正しく表示される。

---

## [v1.93] 2026-04-06 (Claude Sonnet 4.6)

### UI整理
- **ツールバーとコントロールバーを1本に統合**: 「📂ファイル▼」「🔧ツール▼」「⚙設定▼」「📊LoRA分析」の4つのドロップダウン/ボタンを削除。コントロールバー行を廃止し画面の行数が1行減少。

### 新機能
- **パス表示ラベルを編集可能なアドレスバー（QLineEdit）に変更**: フォルダパスを直接入力してEnterで移動できる。存在しないパスを入力すると赤くハイライトしてエラーをステータスバーに表示。

---

## [v1.92] 2026-04-06 (Claude Sonnet 4.6)

### バグ修正
- **レイアウトボタンを2回クリックするとハイライトが消える問題**を修正: `setCheckable(False)` に変更しQtの自動トグルを排除。ハイライトは `setProperty("active","true/false")` + QSS で管理。

### 改善
- レイアウトボタンのクリック反応を高速化: `clicked` → `pressed` シグナルに変更。

---

## [v1.91] 2026-04-06 (Claude Sonnet 4.6)

### 設計改善・再発防止
- **レイアウトボタンのハイライトが毎回元に戻る根本原因**を構造レベルで修正: `_switch_layout()` を2つに分離（`_switch_layout()`: ユーザー操作用、`_apply_layout_by_id()`: 処理実行用）。

### バグ修正
- `setChecked` 後にQSSの `:checked` 擬似クラスが反映されない問題を修正。
- コントロールバーの「🔍タグ:」ラベルの絵文字がWindowsで豆腐（□）になる問題を修正: `QLabel("タグ:")` に変更。

---

## [v1.90] 2026-04-06 (Claude Sonnet 4.6)

### 改善
- **コピー通知トーストの表示位置**をウィンドウのど真ん中（縦横中央）に変更。

---

## [v1.89] 2026-04-06 (Claude Sonnet 4.6)

### 改善
- コピー通知トーストの表示位置をステータスバーからウィンドウ上部中央に変更。スタイルも強調（border-radius:6px, font-size:10pt, accent カラーボーダー）。

---

## [v1.88] 2026-04-06 (Claude Sonnet 4.6)

### バグ修正
- **フェードアニメーションが依然動作しない問題**を根本修正: `self._anim_in` / `self._anim_out` を一度だけ生成し、`.start()` / `.stop()` のみ呼ぶ設計に変更（毎回newするとGCに破棄されていた）。

---

## [v1.87] 2026-04-06 (Claude Sonnet 4.6)

### バグ修正
- **フェードイン・フェードアウトが動作しない問題**を修正: `_init_fade_message()` を新設しQLabel/QGraphicsOpacityEffect/QTimerを初回のみ生成して使い回す設計に変更。

---

## [v1.86] 2026-04-06 (Claude Sonnet 4.6)

### 重大バグ修正
- **サムネイルが壊れてノイズ画像になる問題**を修正: RAWXキャッシュのヘッダーに `bytesPerLine` (2バイト, uint16 LE) を追加し、stride不一致によるピクセルずれを解消。

### 自動修復
- 起動時に旧フォーマットのキャッシュを自動削除: `_CACHE_FORMAT_VERSION=2` を追加し、バージョン変更時に `thumbs/*.raw` を全削除してクリーンビルドを強制。

---

## [v1.85] 2026-04-06 (Claude Sonnet 4.6)

### 新機能
- **コピー後のステータスメッセージをフェードイン・フェードアウト表示に変更**: フェードイン300ms → 2秒表示 → フェードアウト500ms。`QGraphicsOpacityEffect` + `QPropertyAnimation` を使用。

---

## [v1.84] 2026-04-06 (Claude Sonnet 4.6)

### 根本修正
- **クリックしてもメタデータが表示されない問題**を修正: バックグラウンドスレッドからの `QTimer.singleShot` が動作しない問題を解消するため、`_meta_loaded = Signal(str, dict)` を追加しシグナル経由でメインスレッドに通知。

---

## [v1.83] 2026-04-06 (Claude Sonnet 4.6)

### バグ修正
- **シングルクリックでメタデータが表示されない問題**を修正 (v1.82の修正が逆効果だったため): `mousePressEvent` で直接 `clicked` を emit する元の動作に戻す。

---

## [v1.82] 2026-04-06 (Claude Sonnet 4.6)

### バグ修正
- **画像を2回クリックしないとメタデータが表示されない問題**を修正: `clicked` の emit を `mousePressEvent` → `mouseReleaseEvent` に移動。`mouseDoubleClickEvent` では `_drag_start_pos` を無効値に設定して直前の emit を抑制。

---

## [v1.81] 2026-04-06 (Claude Sonnet 4.6)

### 根本修正・高速化
- **クリック後にメタデータが切り替わらない・5秒以上かかる問題**を修正:
  - `_read_png_text_chunks()` を新設し、PNGファイルを直接バイナリ読み取りして高速化（Pillowを不使用）
  - 画像サイズ取得を `QImageReader.size()` に変更（ヘッダーのみ読む）
  - PNG は完全にPillow不使用、JPG/WebP のみPillowフォールバック
- キャッシュミス時に `MetaPanel.show_loading()` でファイル名を即表示するよう改善

---

## [v1.80] 2026-04-05 (Claude Sonnet 4.6)

### 根本修正・高速化
- **クリック・画像切り替え時のUIフリーズを完全排除**: `PreviewLoader` (QRunnable) を新設し非同期プレビューロードを実装。
- `load_preview_pixmap` を PillowからQImageReaderベースに刷新。`setScaledSize()` でデコード段階で縮小。
- リサイズ時のディスクI/Oを完全排除: メモリキャッシュ(`_mem`)のみ参照して `scaled()` するよう変更。
- `dedup_tags` の正規表現を廃止し純粋な文字列操作に置換。

---

## [v1.79] 2026-04-05 (Claude Sonnet 4.6)

### バグ修正
- **コピー操作でステータスバーにメッセージが表示されない問題**を修正: `MetaPanel` に `status_message = Signal(str)` を追加し `_set_status` に接続。

---

## [v1.78] 2026-04-05 (Claude Sonnet 4.6)

### 根本修正
- **メタデータ表示が5秒遅い問題**を修正: `_init_meta_rows()` で固定行ウィジェットを初回のみ生成してキャッシュし、`_update_meta_rows()` で値ラベルの `setText()` だけを更新する方式に変更。

### バグ修正
- Positive/Negativeヘッダーのコピーボタン(📋)が機能しない問題を修正。
- メタ情報のSeed行クリック時にマウスカーソルが指に変わらない問題を修正。

---

## [v1.77] 2026-04-05 (Claude Sonnet 4.6)

### 高速化
- `ScanWorker` で拡張子判定を `endswith` に変更 + `stat` を同時取得。`ScanWorker.finished` シグナルを `Signal(list, dict)` に変更。
- `FilterWorker` のソートで `os.stat()` 呼び出しをゼロに: ScanWorker が取得済みの stat 辞書を参照するだけで即時ソート完了。
- `imgsize` ソートの `Image.open()` フォールバックを廃止。

### 最適化
- `PreloadWorker` のスレッド数を最大16→最大4に制限。
- `VirtualGrid` の `_live_loaders` を `list` → `dict` (path→loader) に変更し、スクロールアウト時に即 `cancel()` 可能に。

---

## [v1.76] 2026-04-05 (Claude Sonnet 4.6)

### バグ修正
- `_live_loaders` リストの肥大化によるサムネイル表示遅延を修正: ロード完了時に自動削除するよう変更。
- `_pixmap_cache`（VirtualGrid ローカル）の無制限肥大化を修正: 800件超で古い200件を削除する上限チェックを追加。

---

## [v1.75] 2026-04-05 (Claude Sonnet 4.6)

### 新機能
- **画像の「既定のプログラム」として起動対応**: コマンドライン引数にファイルパス/フォルダパスを渡すとそのフォルダを開き、ファイルの場合は選択・プレビュー状態で起動。

---

## [v1.74] 2026-04-04 (Claude Sonnet 4.6)

### 根本修正
- **「エクスプローラーで選択」でファイルが選択されない問題**を修正: `Popen(f'explorer /select,"{norm}"', shell=False)` に変更。

### 新機能
- 複数選択時に全ファイルを選択状態でエクスプローラーを開く: `SHOpenFolderAndSelectItems` を ctypes 経由で呼び出し。

---

## [v1.73] 2026-04-04 (Claude Sonnet 4.6)

### 高速化
- `ScanWorker` を `os.scandir` に全面置き換え。
- `PreloadWorker` をスレッドプール並列化 (`concurrent.futures`): max_workers = min(16, cpu_count * 2)。
- `load_thumb` を `QImageReader` ネイティブ縮小に刷新。Pillow非対応形式は自動フォールバック。サムネ正方形パディング廃止。

---

## [v1.72] 2026-04-04 (Claude Sonnet 4.6)

### 根本修正
- **Ctrl+Left / Ctrl+Right によるフォルダ移動が効かない問題**を修正: `_build_menubar` と `_setup_shortcuts` での同一キー二重登録（Ambiguous Shortcut）を解消。

---

## [v1.71] 2026-04-04 (Claude Sonnet 4.6)

### バグ修正
- `_mem` キャッシュのスレッド競合を解消: `_mem_lock` (threading.Lock) を新設。
- `MetaCache` LRUキャッシュ上限を追加: `_MAX_META_ENTRIES = 5000` で無制限肥大化を防止。

### 改善
- `tag_list` 早期リターンで正規表現エンジンの無駄呼び出しを削減。
- `_normalize_path` のUNCパス処理を強化。
- JPEG/WebP サムネイル生成を `Image.draft()` で高速化。

---

## [v1.70] 2026-04-04 (Claude Sonnet 4.6)

### 改善
- 画像読み込み速度向上: ThumbLoader 並列スレッド数 4→8、`_SCROLL_DEBOUNCE` 60→40ms、`_ROW_BUFFER` 2→3行、`_mem` キャッシュ上限 600→1200エントリ。

### 新機能
- LoRA分析ダイアログに最大化ボタン追加。
- コピーボタン付きエラーダイアログ (`_ErrorDialog`) を追加。
- **アクティビティログパネル (`_ConsolePanel`)**: ツールバー「📋 ログ」ボタンでトグル表示。タイムスタンプ + レベル(INFO/OK/WARN/ERR) + 処理時間(ms) を記録。

---

## [v1.69] 2026-04-04 (Claude Sonnet 4.6)

### バグ修正
- **LoRA分析が全く動かなくなっていた問題**を修正: `META._lock` 保持中に `parse_meta` (ファイルI/O) を呼ぶデッドロックを解消。`META` にスレッドセーフな `snapshot()` メソッドを追加。
- Ctrl+Left/Right でフォルダ移動できない問題を修正。

### 新機能
- プロパティダイアログ / ショートカットダイアログに「📋 コピー」ボタンを追加。

### 改善
- `_render_visible` の `to_remove` 判定を `O(n)` → `O(1)` の set 判定に変更。
- `_sel_image` でキャッシュミス時に非同期でメタを取得しUIをブロックしない方式に変更。

---

## [v1.68] 2026-04-04 (Claude Sonnet 4.6)

### バグ修正
- サムネイル二重表示: `DecorationRole` を廃止し `UserRole+1` でピクスマップを渡す方式に変更。

### 新機能
- LoRA使用率分析に「作成日」列 (COL_CDATE=5) を追加。
- 最大化ボタンを追加。
- 列ヘッダークリックでソート: 使用枚数/使用率/作成日/最終使用日の4列をクリックで昇順↔降順切り替え。

---

## [v1.67] 2026-04-03 (Claude Sonnet 4.6)

### 根本修正
- **LoRA使用率分析のサムネイルが表示されない問題**を完全修正: `QTimer.singleShot()` をバックグラウンドスレッドから呼び出していた（スレッドにQtイベントループがなく発火しない）問題を解消。`_thumb_loaded = Signal(str, object)` を追加しシグナル経由でUIスレッドにサムネを渡す。

---

## [v1.65] 2026-04-03 (Claude Sonnet 4.6)

### バグ修正
- サムネイル列が幅ゼロで表示されない問題を修正: `_build_ui` 末尾に `QTimer.singleShot(0, _fix_columns)` を追加。バックグラウンドスレッドでのQPixmap生成（Qt規約違反）を修正。

---

## [v1.64] 2026-04-03 (Claude Sonnet 4.6)

### 改善
- LoRA使用率分析のサムネイル表示を大きく改善: 行の高さを 56px → 120px に拡大。

---

## [v1.63] 2026-04-03 (Claude Sonnet 4.6)

### 新機能
- **LoRA使用率分析に削除機能を追加**: 右クリックメニュー「🗑 削除」と、チェックボックス一括削除機能を追加。
- **LoRA使用率分析にサムネイル列を追加**: 同stem の `.preview.jpeg` 等を非同期ロードして表示。

---

## [v1.62] 2026-04-03 (Claude Sonnet 4.6)

### バグ修正
- 「エクスプローラーで開く」でファイルが選択されない問題を修正: `subprocess.Popen(['explorer', '/select,', ファイルパス])` に変更。

---

## [v1.61] 2026-04-03 (Claude Sonnet 4.6)

### バグ修正
- **メタ情報のLoRAをクリックするとタグ一覧タブが開いてしまう問題**を修正: `_set_tag_search` に `switch_tab: bool = False` 引数を追加。

---

## [v1.60] 2026-04-03 (Claude Sonnet 4.6)

### 改善
- MetaPanel のスプリッターを縮めてもヘッダー行が消えないよう変更: `_HDR_H = 24px` を定義し `setMinimumHeight(_HDR_H)` を設定。

---

## [v1.59] 2026-04-03 (Claude Sonnet 4.6)

### 新機能
- **MetaPanel のセクションヘッダーをダブルクリックで「全コンテンツ表示」高さに瞬時展開**: 既に展開済みの場合は均等分割に戻すトグル動作。

---

## [v1.58] 2026-04-03 (Claude Sonnet 4.6)

### 改善
- 右パネルのタブ廃止: MetaPanel の「ファイル情報・メタ」ペインに 📋 メタ情報 / 🏷 タグ一覧 タブを内包。右パネルの `QTabWidget` を削除。
- お気に入り追加ボタンを "+" → "➕" 絵文字に変更 + フォント指定。
- サブフォルダ QCheckBox にチェックマーク表示を追加。

---

## [v1.57] 2026-04-03 (Claude Sonnet 4.6)

### バグ修正
- 左ペインお気に入りヘッダーの⭐アイコンが表示されない問題を修正: QLabel 個別にスタイルを設定（Segoe UI Emoji を明示指定）。

---

## [v1.56] 2026-04-03 (Claude Sonnet 4.6)

### バグ修正
- 絵文字アイコンが表示されない問題を修正: グローバルQSSの `font-family` に `"Segoe UI Emoji"` を先頭に追加。

---

## [v1.55] 2026-04-03 (Claude Sonnet 4.6)

### 改善
- Positive/Negativeのコピーボタンをヘッダー右端に移動: `_section_header` に `copy_fn` 引数を追加。

---

## [v1.54] 2026-04-03 (Claude Sonnet 4.6)

### 改善
- 右ペイン内の折りたたみ機能を廃止（バグの温床のため）。ツールバーの「メタ ▶」ボタンによる右パネル全体の折りたたみは引き続き動作。

---

## [v1.53] 2026-04-02 (Claude Sonnet 4.6)

### バグ修正
- レイアウトボタン再クリック時のサムネ点滅・スプリッターリセットを修正。

### 改善
- レイアウトA・C・Dのインラインプレビュースプリッター位置を永続化。
- 右パネル内を QSplitter(Vertical) で「プレビュー」と「メタ情報/タブ」に分割。MetaPanel 内部も QSplitter(Vertical) で3セクションに分割。

---

## [v1.52] 2026-04-02 (Claude Sonnet 4.6)

### 改善
- レイアウトBのみメタデータプレビュー（`_preview_label`）を表示。A/C/D/E レイアウト時は非表示。

### 新機能
- レイアウトA・Cで同じレイアウトボタンを再クリックするとサムネイルとプレビューの位置を逆転できるフリップ機能。

---

## [v1.50] 2026-04-02 (Claude Sonnet 4.6)

### 根本修正
- **同じレイアウトボタンを2回クリックするとサムネイルが消える問題**を根本修正: `_grid._resize_timer.stop()` + `_grid._render_timer.stop()` でタイマーを停止してから操作し、完了後に `_grid._full_rebuild()` を即時呼び出し。

---

## [v1.49] 2026-04-01 (Claude Sonnet 4.6)

### 改善
- LoRAフォルダ未設定→設定→保存後に自動でLoRA分析を再実行。

---

## [v1.46] 2026-04-01 (Claude Sonnet 4.6)

### 改善
- LoRAフォルダ未設定時のダイアログを改善: キーボード操作対応ダイアログに変更。設定画面を開きLoRAタブを直接フォーカスして表示。

---

## [v1.45] 2026-04-01 (Claude Sonnet 4.6)

### 改善
- **削除確認ダイアログにキーボード操作**を追加: ← / → / Tab でフォーカス移動、Enterで決定。

### 新機能
- **ファイルのドラッグ＆ドロップ送り出し対応**: サムネイルセルからブラウザ・エクスプローラー等へファイルをドラッグしてコピー/移動できる。

---

## [v1.44] 2026-04-01 (Claude Sonnet 4.6)

### 改善
- 削除確認ダイアログをキーボード操作に最適化: `QMessageBox` を廃止し `_DeleteConfirmDialog`（カスタムQDialog）を新設。Y/N/Enter/Esc を直接処理。`_delete_path` / `_delete_multi` / `_delete_current`（FullViewer）の3箇所すべてに適用。

---

## [v1.43] 2026-04-01 (Claude Sonnet 4.6)

### 設計変更
- レイアウトC/EでフォルダツリーはそのまW維持、右パネル（メタ）のみ非表示にするよう設計変更。

---

## [v1.42] 2026-04-01 (Claude Sonnet 4.6)

### バグ修正
- 起動時にレイアウトC/Eを復元するとフォルダツリーが消える問題を修正: レイアウト復元タイマーを `_build_ui()` 内から `__init__` 末尾に移動。

---

## [v1.41] 2026-04-01 (Claude Sonnet 4.6)

### 根本修正
- **レイアウト切り替え時にユーザーが閉じたパネルが勝手に復元される問題**を完全修正: `_user_collapsed_right` フラグを新設し左パネルと完全対称化。

---

## [v1.40] 2026-04-01 (Claude Sonnet 4.6)

### バグ修正
- FullViewer: ズーム中の矢印キーがナビゲーションとスクロールのどちらに働くか不明瞭だった問題を修正。ズーム時はパン、通常時は前後ナビゲーションに分岐。
- MainWindow: OSリサイズ/最大化解除でパネル幅が誤った値で上書き保存される問題を修正: `changeEvent` で300ms デバウンス後に更新。
- `splitterMoved` デバウンス保存を実装。

---

## [v1.39] 2026-04-01 (Claude Sonnet 4.6)

### 改善
- `parse_meta` のメタデータ解析強化: JPG/WebP/HEICのEXIF UserComment・XMP・IFD0からSD生成パラメータを抽出するよう拡張。

### 新機能
- **FullViewer非同期デコード導入** (`_PixmapLoader` / `_load_pixmap_async`): 巨大画像でのGUIフリーズを防止。
- 削除ダイアログの誤操作防止: デフォルトボタンをNoに変更。
- MetaCache スレッドセーフ化: `threading.Lock` を追加。
- `_normalize_path` 堅牢化: Windows MAX_PATH対応、UNCパス正規化改善。

---

## [v1.34] 2026-04-01 (Claude Sonnet 4.6)

### バグ修正
- 全ペインのフォルダツリー表示/非表示の挙動を統一: 全ペイン（C・E含む）で `_left_panel_widget.hide()/show()` に統一。

---

## [v1.33] 2026-04-01 (Claude Sonnet 4.6)

### 根本修正
- レイアウト「全(E)」から他レイアウトへの切り替え時にフォルダツリーが表示されない問題を根本修正: `_user_collapsed_left` フラグを新設。

---

## [v1.32] 2026-04-01 (Claude Sonnet 4.6)

### バグ修正
- フォルダツリーの幅がペイン操作で変わってしまう問題を修正: `splitter.splitterMoved` シグナルで随時更新。
- パネル非表示時に他パネルの幅計算がズレる問題を修正。
- レイアウト「全(E)」から他レイアウトに戻るとフォルダツリーが消える問題を修正。

---

## [v1.31] 2026-04-01 (Claude Sonnet 4.6)

### バグ修正
- レイアウトE（全）: ≡ボタンを押すとフォルダツリーエリアが残る問題を修正: `_left_panel_widget.hide()` で左パネルwidgetごと非表示に変更。
- レイアウトE: メタ情報オーバーレイを完全削除（右パネルに同等機能があるため）。レイアウトEの定義を「グリッド全画面」に変更（オーバーレイなし）。

---

## [v1.30] 2026-04-01 (Claude Sonnet 4.6)

### バグ修正
- FullViewer: fitボタンを押すと勝手に最大化する問題を修正。
- FullViewer: `_apply_view` をウィンドウ状態から完全に切り離し。
- FullViewer: ボタンラベルを「⊞ fit」「⊟ 原寸」に統一。

---

## [v1.29] 2026-04-01 (Claude Sonnet 4.6)

### バグ修正
- FullViewer: 小ウィンドウで開いた時に画像が原寸大にならない問題を修正。
- FullViewer: 最大化→通常ウィンドウに戻すと画像が縮小される問題を修正。

---

## [v1.28] 2026-04-01 (Claude Sonnet 4.6)

### 新機能
- FullViewer: ウィンドウの最大化状態を記憶して次回に引き継ぐ機能を追加。

---

## [v1.27] 2026-03-31 (Claude Sonnet 4.6)

### バグ修正
- 起動時CMDウィンドウが残る問題を修正: `pythonw.exe` へ DETACHED_PROCESS で再起動するよう変更。
- FullViewer: SpaceでSSボタンが反応する問題を修正。
- FullViewer: 全画面→最大化→全画面で元の大きさに戻らない問題を修正。
- FullViewer: ウィンドウモード時のサイズが毎回バラバラな問題を修正: `_init_window()` を新設し画像サイズに合わせたウィンドウサイズを計算。

---

## [v1.26] 2026-03-31 (Claude Sonnet 4.6)

### バグ修正
- FullViewer: 画像画質が悪い問題を修正: `SmoothTransformation` を追加。
- FullViewer: キー入力が効かない問題を修正: ツールバーボタンに `setFocusPolicy(NoFocus)` を設定。

---

## [v2.0f-Qt] 2026-03-31 (Claude Sonnet 4.6)

### バグ修正
- FullViewer: ウィンドウが開いても画像が表示されない問題を修正: `QTimer.singleShot(50ms)` で `_show_image` を遅延呼び出し。
- 起動時のCMDコンソールウィンドウを非表示に。
- 左パネル開閉の ≡ ボタンを拡大（18×48px → 22×80px）。

---

## [v2.0e-Qt] 2026-03-31 (Claude Sonnet 4.6)

### バグ修正
- FullViewer: ダブルクリックで開いた画像の画質が悪い問題を修正: `_load_pixmap` を新設し `QPixmap(path)` でQtネイティブデコード。
- FullViewer: キー入力が効かない問題を修正: `QGraphicsView` に `setFocusPolicy(NoFocus)` / `setInteractive(False)` を設定。
- FullViewer: 全画面化してもツールバーが見える問題を修正: `showFullScreen()` / `showMaximized()` を `_toggle_immersive` で切り替え。

---

## [v2.0d-Qt] 2026-03-31 (Claude Sonnet 4.6)

### バグ修正
- レイアウトC/E → A/B/D に切り替えたとき左パネル（ツリー）が復元されない問題を修正。

---

## [v2.0c-Qt] 2026-03-31 (Claude Sonnet 4.6)

### バグ修正
- ≡縦バーボタンを押すとボタンごと消える問題を修正: `_left_panel_widget.hide()` → `_left_main_content.hide()` に変更。

---

## [v2.0b-Qt] 2026-03-31 (Claude Sonnet 4.6)

### バグ修正
- 左ペイン縦バー「≡」ボタンがツールバー「◀ フォルダ」と異なる挙動をする問題を修正: 縦バーボタンの `clicked` → `_toggle_left_panel` を直接呼ぶよう変更。

---

## [v2.0-Qt] 2026-03-31 (Claude Sonnet 4.6)

### 新機能
- **左ペインをWindowsエクスプローラー風に全面刷新**: QFileSystemModel のルートをPC全体に変更。ツリーをスプリッターで「⭐ お気に入り」と「📁 フォルダ」に分割。ツリー右クリックメニューに「⭐ お気に入りに追加」を実装。
- 左ペイン表示/非表示ボタンを左端縦バーとして配置。

---

## [v1.9b-Qt] 2026-03-31 (Claude Sonnet 4.6)

### バグ修正
- `monkey-patch(mousePressEvent代入)` はPySide6では動作しないため `installEventFilter` + `eventFilter` で正しく viewport イベントを捕捉する方式に全面置き換え。
- Ctrl+A が動かない問題を修正: `VirtualGrid.keyPressEvent` 冒頭で明示的に処理。

---

## [v1.9-Qt] 2026-03-31 (Claude Sonnet 4.6)

### 新機能
- 前回開いていたフォルダを起動時に自動復元。
- Ctrl+B でブックマーク（お気に入り）ダイアログを表示: `_show_bookmark_dialog` を新設。
- **マウスドラッグによる範囲選択（ラバーバンド選択）**: ドラッグ矩形と交差するセルを複数選択。`QRubberBand` で描画。
- 右パネルのプレビューと右パネル全体をドラッグでリサイズ可能: `_right_vsplitter` を新設。

---

## [v1.8-Qt] 2026-03-31 (Claude Sonnet 4.6)

### バグ修正
- 複数選択の一括削除バグ修正: `get_selection()` で複数取得し `_delete_multi()` で一括処理。

### 新機能
- PageUp/PageDown でページ送り。
- Windowsエクスプローラー相当のキーボード操作を実装: F2 / Shift+Delete / Ctrl+C / Ctrl+X / Ctrl+V / Ctrl+Shift+N / Ctrl+D / Alt+矢印 / Alt+Enter / Shift+矢印 / Escape。
- 右クリックメニューをエクスプローラー相当に拡張。

---

## [v1.7-Qt] 2026-03-31 (Claude Sonnet 4.6)

### バグ修正
- **複数選択バグ修正**: クリック①→Ctrl+クリック②でクリック①の選択が消える問題を修正。通常クリック時も `_multi_sel.add(path)` を追加するなど3点の原因を修正。

---

## [v1.6-Qt] 2026-03-31 (Claude Sonnet 4.6)

### 改善
- サムネサイズ変更をCtrl+ホイールに一本化: ツールバーのプリセットボタンを廃止。

---

## [v1.5-Qt] 2026-03-31 (Claude Sonnet 4.6)

### バグ修正
- プレビュースケール修正: `load_preview_pixmap` を新設（アスペクト比保持、パディングなし）。

### 新機能
- 右パネルのプレビューを復活: レイアウトBでのみ表示。

---

## [v1.4-Qt] 2026-03-31 (Claude Sonnet 4.6)

### バグ修正
- プレビューサイズ修正: ラベルの実サイズを使いパネルにフィットするよう修正。resizeEvent フックを追加。

### 改善
- サイズスライダー → タブボタン化: 「小(80px)」「中(160px)」「大(260px)」のプリセットタブボタンに置換。
- レイアウトボタンを文字表記に変更（「上下」「右」「左右」「帯」「全」）。

---

## [v1.3-Qt] 2026-03-31 (Claude Sonnet 4.6)

### バグ修正
- ◀フォルダ / メタ▶ ボタンが機能しない・完全に隠れない問題を修正: `setChildrenCollapsible(True)` に変更し `hide()/show()` を組み合わせて確実に完全非表示。`toggled` → `clicked` シグナルに変更（再帰呼び出し防止）。

---

## [v1.2-Qt] 2026-03-31 (Claude Sonnet 4.6)

### 改善
- レイアウトボタンA〜Eを絵文字アイコンに変更（🔼📋↔🎞👁）。
- ◀フォルダ / メタ▶ ボタンをpane_barからツールバーに移動。
- ボタンON/OFFの表示を背景塗りつぶしから下線スタイルに変更。
- バージョン情報・AI向けアーキテクチャ説明をファイル冒頭に追加。

---

## [v1.1-Qt] 2026-03-31 (Claude Sonnet 4.6)

### 新機能
- レイアウト A〜E を全実装: A(上部プレビュー) / B(右パネル) / C(左右分割) / D(フィルムストリップ) / E(オーバーレイ)。
- メタ情報/タグ一覧ボタンをセンターpane_barから右パネルヘッダーバーに移動。
- ボタンスタイル管理を `setObjectName` + QSSに統一。

### バグ修正
- `_switch_layout` の `_bg/_fg` 未定義 NameError を修正。
- f-string内クォート競合 SyntaxError を修正（Python 3.11以下対応）。

---

## [v1.0-Qt] 2026-03-31 (Claude Sonnet 4.6)

### 初版
- tkinter版 v11 を PySide6 で完全書き直し。
- 仮想スクロールグリッド / メタデータ解析 / LoRA分析 / FullViewer 等を移植。

---

## [v2.03a] 2026-04-08 (Codex)

### UI更新
- サムネイル一覧の更新を差分反映寄りにして、削除後にサムネイルが一瞬消えにくいよう調整。
- `VirtualGrid` のスクロール処理でデバウンス待ちの前に描画を走らせ、スクロールバーをドラッグ中の空白を減らすよう修正。
- Ctrl+ホイールでサムネイルサイズ変更時に先頭へ飛んでしまう不具合を修正。スクロール位置を比率で維持するよう調整。
- 削除確認ダイアログを先に描画してから待機に入るようにし、白いまま遅れて表示される体感を改善。
- サムネイルのクリック確定をマウスリリース時へ変更し、ドラッグ開始時に追尾画像の表示や選択ハイライトが遅れやすい問題を軽減。
