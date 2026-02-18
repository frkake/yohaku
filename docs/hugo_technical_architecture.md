# Hugo Technical Architecture Design

## 1. テーマ選定: Blowfish

### 選定理由

| 基準 | PaperMod | Blowfish | Congo | カスタムテーマ |
|------|----------|----------|-------|---------------|
| Tailwind CSS | x | o | o | 要構築 |
| ダークモード | o | o | o | 要実装 |
| 多言語対応 | o | o | o | 要実装 |
| カスタムセクション | 限定的 | o | o | 完全自由 |
| ドロップダウンメニュー | x | o | o | 要実装 |
| 画像ギャラリー | x | o | x | 要実装 |
| Lighthouse スコア | 高い | 高い | 100/100 | 未知 |
| 学習コスト | 低い | 中 | 中 | 高い |
| 保守コスト | 低い | 低い | 低い | 高い |

**Blowfish を推奨する理由:**

1. **Tailwind CSS 3.0 ベース** - モダンなデザインカスタマイズが容易。アプリ会社のブランディングに合わせた微調整が簡単
2. **カスタムセクションレイアウト** - `apps/` や `downloads/` など、独自コンテンツタイプのレイアウトを柔軟に作成可能
3. **ドロップダウンメニュー対応** - アプリが増えた際にメニュー構造を階層化できる（PaperModでは不可）
4. **豊富なショートコード** - ボタン、バッジ、ギャラリー、アラートなどが組み込み済み。ダウンロードページの構築に有用
5. **ダークモード** - ユーザートグル付きの自動切り替え対応。既存ブログと統一感のある体験
6. **多言語対応** - RTL含む多言語サポートが組み込み済み。日英対応がスムーズ
7. **Congo からの派生** - Congo の堅実な基盤 + 追加機能（Firebase連携、ビューカウンター等は不要だが将来的に活用可能）
8. **PaperMod からの移行** - オーナーは PaperMod に慣れているが、Blowfish は PaperMod と同様の Front Matter 構造を持ち、移行の学習コストが低い

**PaperMod を選ばない理由:**
- ドロップダウンメニュー非対応（アプリ増加時に構造が破綻する）
- カスタムセクションレイアウトの柔軟性が低い
- ブログ特化のため、プロダクトショーケースには不向き

**カスタムテーマを選ばない理由:**
- 開発・保守コストが大幅に増加
- Blowfish のカスタマイズ機能で十分に要件を満たせる

---

## 2. ディレクトリ構成

```
homepage/
├── hugo.toml                    # メイン設定ファイル
├── go.mod                       # Hugo Modules 用
├── go.sum
├── .github/
│   └── workflows/
│       └── deploy.yml           # GitHub Actions デプロイ
│
├── assets/
│   └── css/
│       └── custom.css           # Blowfish テーマのカスタム CSS
│
├── content/
│   ├── ja/                      # 日本語コンテンツ (デフォルト)
│   │   ├── _index.md            # ホームページ
│   │   ├── apps/
│   │   │   ├── _index.md        # アプリ一覧ページ
│   │   │   ├── stillmotion/
│   │   │   │   ├── index.md     # StillMotion 詳細ページ
│   │   │   │   ├── feature.jpg  # サムネイル画像
│   │   │   │   └── images/      # アプリスクリーンショット等
│   │   │   └── dayrhythm/
│   │   │       ├── index.md     # DayRhythm 詳細ページ (将来)
│   │   │       ├── feature.jpg
│   │   │       └── images/
│   │   ├── downloads/
│   │   │   ├── _index.md        # ダウンロード一覧ページ
│   │   │   └── stillmotion/
│   │   │       └── index.md     # StillMotion ダウンロードページ
│   │   ├── about/
│   │   │   └── index.md         # 会社概要
│   │   └── legal/
│   │       ├── _index.md
│   │       ├── privacy/
│   │       │   └── index.md     # プライバシーポリシー
│   │       └── terms/
│   │           └── index.md     # 利用規約
│   │
│   └── en/                      # 英語コンテンツ
│       ├── _index.md
│       ├── apps/
│       │   ├── _index.md
│       │   ├── stillmotion/
│       │   │   └── index.md
│       │   └── dayrhythm/
│       │       └── index.md
│       ├── downloads/
│       │   ├── _index.md
│       │   └── stillmotion/
│       │       └── index.md
│       ├── about/
│       │   └── index.md
│       └── legal/
│           ├── _index.md
│           ├── privacy/
│           │   └── index.md
│           └── terms/
│               └── index.md
│
├── layouts/
│   ├── apps/
│   │   ├── list.html            # アプリ一覧カスタムレイアウト
│   │   └── single.html          # アプリ詳細カスタムレイアウト
│   ├── downloads/
│   │   ├── list.html            # ダウンロード一覧
│   │   └── single.html          # ダウンロード詳細
│   ├── partials/
│   │   ├── app-card.html        # アプリカードコンポーネント
│   │   ├── download-button.html # ダウンロードボタン
│   │   ├── platform-badge.html  # プラットフォームバッジ
│   │   └── app-hero.html        # アプリヒーローセクション
│   └── shortcodes/
│       ├── app-store-badge.html # App Store バッジ
│       ├── download-table.html  # ダウンロードテーブル
│       └── platform-list.html   # 対応プラットフォーム一覧
│
├── static/
│   └── images/
│       ├── logo.svg             # 会社ロゴ
│       ├── logo-dark.svg        # ダークモード用ロゴ
│       └── og-default.png       # デフォルト OGP 画像
│
├── releases/                    # GitHub Releases 用バイナリ（.gitignore 対象）
│   └── stillmotion-server/
│       └── v1.1/
│           ├── StillMotion-Server-1.1.dmg
│           ├── stillmotion-server-darwin-arm64
│           ├── stillmotion-server-darwin-amd64
│           ├── stillmotion-server-linux-amd64
│           ├── stillmotion-server-linux-arm64
│           ├── stillmotion-server-windows-amd64.exe
│           └── stillmotion-server-windows-arm64.exe
│
├── i18n/
│   ├── ja.yaml                  # 日本語翻訳 (Blowfish デフォルト + カスタム)
│   └── en.yaml                  # 英語翻訳
│
├── data/
│   └── apps/
│       └── stillmotion.yaml     # アプリメタデータ (バージョン等)
│
└── docs/                        # プロジェクトドキュメント (Hugo 管理外)
    ├── requirements_v1.md
    └── hugo_technical_architecture.md
```

---

## 3. コンテンツタイプ設計

### 3.1 apps/ (アプリセクション)

**Front Matter 設計 (`content/ja/apps/stillmotion/index.md`):**

```yaml
---
title: "StillMotion"
description: "写真と動画を美しく管理するアプリ"
date: 2024-01-01
draft: false

# アプリ固有メタデータ
app:
  slug: "stillmotion"
  tagline: "写真と動画を美しく管理"
  icon: "images/app-icon.png"        # Page Bundle 内の相対パス
  platforms:
    - name: "iOS"
      icon: "apple"
    - name: "iPadOS"
      icon: "apple"
    - name: "macOS"
      icon: "apple"
    - name: "watchOS"
      icon: "apple"
  appStoreUrl: "https://apps.apple.com/app/stillmotion/id..."
  version: "1.0.0"
  status: "released"                 # released | coming_soon
  features:
    - title: "機能1"
      description: "説明"
      image: "images/feature1.png"
    - title: "機能2"
      description: "説明"
      image: "images/feature2.png"

# ダウンロードページへのリンク
hasDownloads: true
---
```

**一覧ページ (`content/ja/apps/_index.md`):**

```yaml
---
title: "アプリ"
description: "開発したアプリケーション一覧"
cascade:
  showDate: false
  showReadingTime: false
---
```

### 3.2 downloads/ (ダウンロードセクション)

バイナリファイルは **GitHub Releases** から配布する（`static/downloads/` には配置しない）。
ダウンロード URL は GitHub Releases のアセット URL を直接使用する。

**Front Matter 設計 (`content/ja/downloads/stillmotion/index.md`):**

```yaml
---
title: "StillMotion Server ダウンロード"
description: "StillMotion ローカルサーバーのダウンロード"
date: 2024-01-01
draft: false

# ダウンロード固有メタデータ
download:
  appSlug: "stillmotion"
  appName: "StillMotion Server"
  description: "StillMotion のローカルサーバー用ソフトウェア"
  releases:
    - version: "1.1"
      date: "2025-02-18"
      githubRelease: "stillmotion-server-v1.1"
      files:
        - platform: "macOS"
          arch: "Apple Silicon"
          filename: "StillMotion-Server-1.1.dmg"
          url: "https://github.com/{owner}/{repo}/releases/download/stillmotion-server-v1.1/StillMotion-Server-1.1.dmg"
          size: "5.9MB"
          type: "installer"
          icon: "apple"
          recommended: true
        - platform: "macOS"
          arch: "Apple Silicon"
          filename: "stillmotion-server-darwin-arm64"
          url: "https://github.com/{owner}/{repo}/releases/download/stillmotion-server-v1.1/stillmotion-server-darwin-arm64"
          size: "6.7MB"
          type: "binary"
          icon: "apple"
        - platform: "macOS"
          arch: "Intel"
          filename: "stillmotion-server-darwin-amd64"
          url: "https://github.com/{owner}/{repo}/releases/download/stillmotion-server-v1.1/stillmotion-server-darwin-amd64"
          size: "7.1MB"
          type: "binary"
          icon: "apple"
        - platform: "Linux"
          arch: "x86_64"
          filename: "stillmotion-server-linux-amd64"
          url: "https://github.com/{owner}/{repo}/releases/download/stillmotion-server-v1.1/stillmotion-server-linux-amd64"
          size: "6.9MB"
          type: "binary"
          icon: "linux"
        - platform: "Linux"
          arch: "ARM64"
          filename: "stillmotion-server-linux-arm64"
          url: "https://github.com/{owner}/{repo}/releases/download/stillmotion-server-v1.1/stillmotion-server-linux-arm64"
          size: "6.6MB"
          type: "binary"
          icon: "linux"
        - platform: "Windows"
          arch: "x86_64"
          filename: "stillmotion-server-windows-amd64.exe"
          url: "https://github.com/{owner}/{repo}/releases/download/stillmotion-server-v1.1/stillmotion-server-windows-amd64.exe"
          size: "7.1MB"
          type: "binary"
          icon: "windows"
        - platform: "Windows"
          arch: "ARM64"
          filename: "stillmotion-server-windows-arm64.exe"
          url: "https://github.com/{owner}/{repo}/releases/download/stillmotion-server-v1.1/stillmotion-server-windows-arm64.exe"
          size: "6.6MB"
          type: "binary"
          icon: "windows"
      changelog: |
        - 初回リリース
---
```

> **注**: `{owner}/{repo}` は実際の GitHub リポジトリのオーナー/リポジトリ名に置き換える。
> リモートが設定され次第、すべての URL を更新すること。

### 3.3 about/ (会社概要)

```yaml
---
title: "会社概要"
description: "私たちについて"
showDate: false
showReadingTime: false
showTableOfContents: false
---
```

### 3.4 legal/ (法的ページ)

```yaml
---
title: "プライバシーポリシー"
description: "個人情報の取り扱いについて"
showDate: true
showReadingTime: false
---
```

---

## 4. Hugo 設定 (hugo.toml)

```toml
# =============================================================================
# 基本設定
# =============================================================================
baseURL = "https://example.com/"    # GitHub Pages の URL に変更
languageCode = "ja-jp"
defaultContentLanguage = "ja"
defaultContentLanguageInSubdir = false
hasCJKLanguage = true
title = "会社名"                     # 正式な会社名に変更

# テーマ (Hugo Modules 経由)
theme = "blowfish"

enableInlineShortcodes = true
enableEmoji = false
enableRobotsTXT = true

# =============================================================================
# ビルド設定
# =============================================================================
[build]
  writeStats = true                  # Tailwind CSS の purge 用

[minify]
  disableXML = true
  minifyOutput = true

[outputs]
  home = ["HTML", "RSS", "JSON"]     # JSON は検索用

# =============================================================================
# マークアップ設定
# =============================================================================
[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = true
  [markup.highlight]
    noClasses = false

# =============================================================================
# Blowfish テーマパラメータ
# =============================================================================
[params]
  # -- 基本 --
  colorScheme = "ocean"              # Blowfish のカラースキーム (カスタマイズ可)
  defaultAppearance = "dark"         # ダークモードデフォルト
  autoSwitchAppearance = true        # システム設定に追従
  enableSearch = true
  enableCodeCopy = true

  # -- メタデータ --
  description = "アプリ開発会社のホームページ"
  keywords = ["アプリ", "StillMotion", "ソフトウェア"]

  # -- レイアウト --
  [params.homepage]
    layout = "custom"                # カスタムホームページレイアウト
    showRecent = false

  [params.article]
    showDate = true
    showDateUpdated = true
    showReadingTime = false
    showTableOfContents = true
    showBreadcrumbs = true

  [params.list]
    showBreadcrumbs = true
    showTableOfContents = false
    groupByYear = false

  # -- ヘッダー/フッター --
  [params.header]
    layout = "fixed"

  [params.footer]
    showCopyright = true
    showThemeAttribution = false

  # -- ラベル --
  [params.label]
    text = "会社名"
    icon = "/images/logo.svg"

  # -- OGP --
  [params.og]
    image = "/images/og-default.png"

# =============================================================================
# Hugo Modules
# =============================================================================
[module]
  [module.hugoVersion]
    extended = true
    min = "0.118.0"

  [[module.imports]]
    path = "github.com/nunocoracao/blowfish/v2"

# =============================================================================
# 多言語設定
# =============================================================================
[languages]
  [languages.ja]
    title = "会社名"
    weight = 1
    languageCode = "ja-jp"
    languageName = "日本語"
    contentDir = "content/ja"

    [[languages.ja.menus.main]]
      name = "アプリ"
      pageRef = "apps"
      weight = 1

    [[languages.ja.menus.main]]
      name = "ダウンロード"
      pageRef = "downloads"
      weight = 2

    [[languages.ja.menus.main]]
      name = "会社概要"
      pageRef = "about"
      weight = 3

  [languages.en]
    title = "Company Name"
    weight = 2
    languageCode = "en-us"
    languageName = "English"
    contentDir = "content/en"

    [[languages.en.menus.main]]
      name = "Apps"
      pageRef = "apps"
      weight = 1

    [[languages.en.menus.main]]
      name = "Downloads"
      pageRef = "downloads"
      weight = 2

    [[languages.en.menus.main]]
      name = "About"
      pageRef = "about"
      weight = 3

# =============================================================================
# Taxonomies (必要に応じて拡張)
# =============================================================================
[taxonomies]
  platform = "platforms"             # プラットフォーム別分類
```

**既存ブログ設定との差異:**

| 設定項目 | 個人ブログ (PaperMod) | 会社HP (Blowfish) |
|----------|----------------------|-------------------|
| テーマ | papermod | blowfish |
| defaultTheme | auto | dark (autoSwitch有効) |
| enableRobotsTXT | false | true (SEO重視) |
| 検索 | FuseOpts | Blowfish 内蔵検索 |
| メニュー | フラット | ドロップダウン対応 |
| contentDir | content/ja, content/en | 同じ (互換構造) |

---

## 5. カスタムレイアウト・ショートコード

### 5.1 カスタムレイアウト

#### `layouts/apps/list.html` - アプリ一覧
```
アプリカードをグリッド表示。各カードにはアイコン、名前、タグライン、
ステータス（リリース済み / 開発中）バッジを表示。
```

#### `layouts/apps/single.html` - アプリ詳細
```
構成:
1. ヒーローセクション (アプリアイコン + 名前 + タグライン + App Store ボタン)
2. スクリーンショットギャラリー
3. 機能紹介セクション (交互レイアウト)
4. 対応プラットフォーム一覧
5. ダウンロードリンク (Server がある場合)
6. 関連情報 (プライバシーポリシーへのリンク等)
```

#### `layouts/downloads/list.html` - ダウンロード一覧
```
アプリごとにグループ化されたダウンロードリンク一覧。
```

#### `layouts/downloads/single.html` - ダウンロード詳細
```
構成:
1. アプリ名 + バージョン情報
2. プラットフォーム別ダウンロードボタン (macOS / Linux)
3. システム要件
4. インストール手順
5. チェンジログ
```

### 5.2 パーシャル

| パーシャル | 用途 |
|-----------|------|
| `partials/app-card.html` | アプリカード (一覧ページ用) |
| `partials/download-button.html` | ダウンロードボタン (プラットフォームアイコン付き) |
| `partials/platform-badge.html` | プラットフォームバッジ (iOS, macOS等) |
| `partials/app-hero.html` | アプリ詳細ページのヒーローセクション |

### 5.3 ショートコード

#### `shortcodes/app-store-badge.html`
App Store のダウンロードバッジを表示。

```
使用例: {{</* app-store-badge url="https://apps.apple.com/..." */>}}
```

#### `shortcodes/download-table.html`
ダウンロードファイルをテーブル形式で表示。Front Matter の `download.releases` から自動生成。

```
使用例: {{</* download-table */>}}
```

#### `shortcodes/platform-list.html`
対応プラットフォームをアイコン付きで一覧表示。

```
使用例: {{</* platform-list */>}}
```

---

## 6. 多言語対応 (i18n)

### 6.1 設計方針

- **ディレクトリベースの多言語** - `content/ja/`, `content/en/` (既存ブログと同じ構造)
- **デフォルト言語** - 日本語 (`ja`)、サブディレクトリなし
- **言語切替** - Blowfish 組み込みの言語スイッチャーを使用

### 6.2 翻訳ファイル

**`i18n/ja.yaml`:**

```yaml
# カスタム翻訳キー (Blowfish デフォルトに追加)
app_released: "リリース済み"
app_coming_soon: "開発中"
download_for: "ダウンロード"
download_size: "ファイルサイズ"
download_version: "バージョン"
system_requirements: "システム要件"
install_instructions: "インストール手順"
changelog: "変更履歴"
platforms: "対応プラットフォーム"
view_on_app_store: "App Store で見る"
latest_release: "最新リリース"
```

**`i18n/en.yaml`:**

```yaml
app_released: "Released"
app_coming_soon: "Coming Soon"
download_for: "Download"
download_size: "File Size"
download_version: "Version"
system_requirements: "System Requirements"
install_instructions: "Installation Guide"
changelog: "Changelog"
platforms: "Supported Platforms"
view_on_app_store: "View on App Store"
latest_release: "Latest Release"
```

### 6.3 テンプレートでの使用

```html
{{ i18n "app_released" }}
{{ i18n "download_for" }} {{ .Params.download.appName }}
```

---

## 7. GitHub Actions CI/CD パイプライン

### 7.1 デプロイワークフロー

**`.github/workflows/deploy.yml`:**

```yaml
name: Deploy Hugo site to GitHub Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

defaults:
  run:
    shell: bash

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      HUGO_VERSION: "0.140.0"
    steps:
      - name: Install Hugo CLI
        run: |
          wget -O ${{ runner.temp }}/hugo.deb \
            https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb
          sudo dpkg -i ${{ runner.temp }}/hugo.deb

      - name: Install Dart Sass
        run: sudo snap install dart-sass

      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v5

      - name: Install Node.js dependencies
        run: "[[ -f package-lock.json || -f npm-shrinkwrap.json ]] && npm ci || true"

      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: "1.22"

      - name: Build with Hugo
        env:
          HUGO_CACHEDIR: ${{ runner.temp }}/hugo_cache
          HUGO_ENVIRONMENT: production
          TZ: Asia/Tokyo
        run: |
          hugo \
            --gc \
            --minify \
            --baseURL "${{ steps.pages.outputs.base_url }}/"

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### 7.2 パイプラインの特徴

- **Hugo Modules 対応** - Go のセットアップを含む（Blowfish を Hugo Module として管理するため）
- **Hugo Extended** - Tailwind CSS のビルドに必要
- **タイムゾーン設定** - `Asia/Tokyo` で日付表示を日本時間に統一
- **キャッシュ** - Hugo のキャッシュディレクトリを設定してビルド高速化
- **concurrency 制御** - 同時デプロイを防止

---

## 8. 画像最適化・パフォーマンス方針

### 8.1 画像最適化

- **Hugo の Image Processing** を活用し、レスポンシブ画像を自動生成
- アプリスクリーンショットは Page Bundle 内に配置し、Hugo の `resources.Get` でリサイズ
- WebP 形式への変換を Hugo のパイプラインで実施
- OGP 画像は `static/images/` に事前生成済みで配置

### 8.2 パフォーマンス

- **Blowfish のビルトイン最適化** - CSS/JS の minify、lazy loading
- **minifyOutput = true** でHTML出力を圧縮
- **writeStats = true** で Tailwind CSS の不要クラスを purge
- ダウンロードファイルは `static/downloads/` に配置（Hugo の処理対象外）

---

## 9. 実装優先順位

| 優先度 | タスク | 内容 |
|--------|--------|------|
| P0 | プロジェクト初期化 | Hugo init, Blowfish テーマ導入, hugo.toml 設定 |
| P0 | StillMotion アプリページ | apps/stillmotion のコンテンツとレイアウト |
| P0 | ダウンロードページ | downloads/stillmotion のコンテンツとレイアウト |
| P0 | GitHub Actions | デプロイパイプライン構築 |
| P1 | ホームページ | カスタムホームレイアウト |
| P1 | ダークモード調整 | カラースキームのカスタマイズ |
| P1 | 多言語対応 | 英語コンテンツの追加 |
| P2 | 会社概要ページ | about/ コンテンツ |
| P2 | 法的ページ | privacy/, terms/ コンテンツ |
| P3 | DayRhythm ページ | 開発完了後に追加 |

---

## 10. 注意事項・技術的制約

1. **Hugo バージョン**: ローカルは v0.118.0 がインストール済み。Blowfish v2 は v0.114.0 以上で動作するため互換性あり。ただし CI では最新版 (v0.140.0) を使用推奨
2. **Hugo Modules vs git submodule**: Hugo Modules（Go Modules ベース）を推奨。git submodule より管理が容易でバージョン固定が確実
3. **static/downloads/ のファイルサイズ**: GitHub Pages のリポジトリサイズ制限（推奨1GB）に注意。大きなバイナリは GitHub Releases や外部ストレージを検討
4. **個人ブログとの独立性**: 完全に別リポジトリ・別ドメインとして運用。テーマも設定も独立
