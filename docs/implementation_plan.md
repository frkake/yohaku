# 実装計画書 - Less is More ホームページ

> 本文書は `requirements_v2.md` および6名のプロフェッショナルチームの設計成果に基づく、段階的な実装計画です。
> 実装→検証→改善のサイクルを繰り返し、100点のホームページを目指します。

---

## 現状分析

### 存在するもの

- 設計ドキュメント一式（6ファイル、合計 3,968 行）
- アプリメタデータ（`data/apps/stillmotion.yaml`, `data/apps/dayrhythm.yaml`）
- アプリアイコン画像（ライト/ダーク各2枚 × 2アプリ = 4ファイル）
- Git リポジトリ（初期コミット済み）

### 存在しないもの（すべて新規作成）

- `hugo.toml`（サイト設定）
- `go.mod` / `go.sum`（Hugo Modules）
- `content/` ディレクトリ一式（全ページのマークダウン）
- `layouts/` テンプレート一式（カスタムレイアウト）
- `assets/css/custom.css`（デザイントークン・カスタムスタイル）
- `i18n/` 翻訳ファイル
- `static/` 静的ファイル（favicon 等）
- `.github/workflows/deploy.yml`（CI/CD）
- `package.json`（PostCSS / Tailwind 依存）

---

## 実装フェーズ

全体を5つのフェーズに分割する。各フェーズは「実装 → Hugo ビルド検証 → 修正」のサイクルを含む。

---

## Phase 1: 基盤構築（P0）

Hugo プロジェクトとしてビルドが通り、ローカルでサイトが表示される状態を作る。

### 1.1 Hugo プロジェクト初期化

**ファイル**: `hugo.toml`

```toml
baseURL = "https://example.com/"
languageCode = "ja"
defaultContentLanguage = "ja"
defaultContentLanguageInSubdir = true
hasCJKLanguage = true
title = "Less is More"
enableRobotsTXT = true

[build]
  writeStats = true

[module]
  [[module.imports]]
    path = "github.com/nunocoracao/blowfish/v2"
```

主要設定項目:
- デフォルト言語: `ja`（サブディレクトリ方式 `/ja/`, `/en/`）
- テーマ: Blowfish v2（Hugo Modules 経由）
- CJK 言語サポート有効
- robots.txt 自動生成有効
- minifyOutput 有効

**ファイル**: `go.mod`
- Hugo Modules 初期化（`hugo mod init`）
- Blowfish テーマ依存追加

**ファイル**: `package.json`
- PostCSS / autoprefixer 等の Node.js 依存定義（Blowfish の Tailwind ビルドに必要）

### 1.2 Blowfish テーマ基本設定

**ファイル群**: `hugo.toml`（言語別設定セクション）

```
[languages.ja]
  title = "Less is More"
  weight = 1
  languageCode = "ja"
  [languages.ja.params]
    description = "Less, but better."

[languages.en]
  title = "Less is More"
  weight = 2
  languageCode = "en"
  [languages.en.params]
    description = "Less, but better."
```

Blowfish 固有パラメータ:
- `colorScheme`: カスタムスキーム（後述の CSS で定義）
- `defaultAppearance = "light"`
- `autoSwitchAppearance = true`（OS設定に追従）
- ヘッダーレイアウト: `basic`
- フッターレイアウト: カスタム
- メニュー設定（Apps, Contact, 言語切替）

### 1.3 カスタムカラースキーム

**ファイル**: `assets/css/schemes/lessismore.css`

Blowfish のカラースキーム仕組みに準拠して、仕様書のカラーパレットを Tailwind カラー変数に変換する。

ライトモード:
- `--color-neutral-50` 〜 `--color-neutral-900`: `#FAFAFA` 〜 `#1A1A1A` のスケール
- `--color-primary-*`: Brand `#4A9ECC` 基調のスケール
- `--color-secondary-*`: Accent `#4DD9C0` 基調のスケール

ダークモード:
- 背景: `#121212` / `#1E1E1E`
- テキスト: `#F0F0F0` / `#A0A0A0`
- Brand: `#5AAEDC`
- Accent: `#5DE9D0`

### 1.4 カスタム CSS（デザイントークン）

**ファイル**: `assets/css/custom.css`

仕様書セクション 4.6 のデザイントークンを CSS Custom Properties として定義:

- タイポグラフィ: Inter + Noto Sans JP フォントスタック、Major Third スケール
- スペーシング: 8px ベースの 10 段階システム
- レイアウト: `--content-max: 1200px`, `--content-text: 720px`
- 角丸: カード 8px、ボタン 4px、チップ 2px
- シャドウ: ライトモードのみ微細
- アニメーション: 120ms / 200ms / 350ms の 3 段階
- `prefers-reduced-motion` 対応

### 1.5 最小コンテンツ作成

Hugo ビルド確認用の最小限コンテンツ:

**ファイル**: `content/ja/_index.md` — トップページ（仮）
**ファイル**: `content/en/_index.md` — トップページ英語（仮）

### 1.6 検証

- [ ] `hugo server` でエラーなく起動する
- [ ] `http://localhost:1313/ja/` でページが表示される
- [ ] Blowfish テーマが正しく適用されている
- [ ] ライト/ダークモード切替が動作する
- [ ] カスタムカラーが反映されている

---

## Phase 2: コアページ実装（P0）

StillMotion ページ・ダウンロードページ・トップページの3つのコアページを実装する。

### 2.1 トップページ

**ファイル**: `layouts/page/home.html`（Blowfish のホームレイアウトをオーバーライド）

構成:
1. **Hero セクション**: サイト名「Less is More」+ タグライン「Less, but better.」+ 大きな余白（128px）
2. **Featured Apps セクション**: アプリカードグリッド（`data/apps/` から動的生成）
3. **フッター**: 3カラム構成（Apps / Legal / Connect）

技術的ポイント:
- Hero は全幅、テキストセンタリング、`--space-10`（128px）の余白
- アプリカードは `layouts/partials/app-card.html` として分離
- アプリカード: アイコン + 名前 + 一行説明 + プラットフォームバッジ + ステータスバッジ
- `coming_soon` ステータスの DayRhythm には「Coming Soon」バッジ表示

**コンテンツファイル**:
- `content/ja/_index.md` — ヘッドライン: 「画像も動画も、ひとつに。」
- `content/en/_index.md` — ヘッドライン: "Images and Videos, United."

### 2.2 StillMotion 詳細ページ

**ファイル**: `layouts/apps/single.html`

セクション構成（上から順に）:
1. **App Hero**: アイコン（128px）+ アプリ名 + サブタイトル + プラットフォームバッジ
2. **CTA Primary**: App Store バッジ群（iOS/iPadOS/macOS）
3. **Overview**: 概要説明（2〜3段落）
4. **Features**: 主要機能グリッド（4つ、2×2 レイアウト）
   - シームレスなスライドショー
   - タイル表示（有料）
   - デュアルエンジン動画再生
   - 7つのメディアソース
5. **料金プラン**: 無料版 vs フルバージョン 比較表
6. **Local Server**: ローカルサーバー説明 + ダウンロードリンク
7. **CTA Secondary**: App Store バッジ再掲

**コンテンツファイル**:
- `content/ja/apps/stillmotion/index.md` — Front Matter にアプリメタデータ + 本文
- `content/en/apps/stillmotion/index.md` — 英語版

**パーシャル**:
- `layouts/partials/app-hero.html` — アプリヒーローセクション
- `layouts/partials/app-store-badge.html` — App Store バッジ（Apple ガイドライン準拠）
- `layouts/partials/platform-badge.html` — プラットフォームバッジ
- `layouts/partials/feature-card.html` — 機能カード
- `layouts/partials/pricing-table.html` — 料金比較表

### 2.3 DayRhythm（Coming Soon）ページ

**ファイル**: `layouts/apps/single.html`（共通、ステータスで分岐）

セクション構成:
1. **App Hero**: アイコン + アプリ名 + 「Coming Soon」バッジ
2. **Teaser**: 簡単な紹介文 + 対応予定プラットフォーム

**コンテンツファイル**:
- `content/ja/apps/dayrhythm/index.md`
- `content/en/apps/dayrhythm/index.md`

### 2.4 アプリ一覧ページ

**ファイル**: `layouts/apps/list.html`

- アプリカードのグリッド表示（`data/apps/` のデータを使用）
- デスクトップ: 2カラム、モバイル: 1カラム

**コンテンツファイル**:
- `content/ja/apps/_index.md`
- `content/en/apps/_index.md`

### 2.5 ダウンロードページ

**ファイル**: `layouts/downloads/single.html`

セクション構成:
1. **Header**: ソフトウェア名 + バージョン
2. **概要**: 「PCのメディアを、手元のデバイスで。」
3. **System Requirements**: 対応 OS・動作要件
4. **Download Links**: macOS / Linux / Windows ダウンロードボタン（プラットフォームアイコン付き）
5. **Installation Guide**: 5 ステップの簡易セットアップ（`<details>` で折りたたみ）

**パーシャル**:
- `layouts/partials/download-button.html` — ダウンロードボタン
- `layouts/partials/download-table.html` — ダウンロードテーブル

**コンテンツファイル**:
- `content/ja/downloads/stillmotion-server/index.md`
- `content/en/downloads/stillmotion-server/index.md`

### 2.6 ナビゲーション設定

**ヘッダー**:
```
[Logo/サイト名]          [Apps]  [Contact]  [EN/JA]
```

**フッター**（3カラム）:
```
Apps            Legal            Connect
StillMotion     Privacy Policy   Contact
DayRhythm       Terms of Use
```

`hugo.toml` のメニュー設定 + カスタムフッターパーシャル（`layouts/partials/footer-custom.html`）

### 2.7 多言語対応

**ファイル**: `i18n/ja.yaml`, `i18n/en.yaml`

翻訳キー:
- `nav_apps`, `nav_contact`, `nav_download`
- `cta_appstore`, `cta_download`
- `status_released`, `status_coming_soon`
- `pricing_free`, `pricing_pro`
- `footer_apps`, `footer_legal`, `footer_connect`
- その他 UI テキスト

### 2.8 検証

- [ ] トップページ: Hero + アプリカード一覧が仕様通りに表示される
- [ ] StillMotion ページ: 全7セクションが正しい順序で表示される
- [ ] DayRhythm ページ: Coming Soon バッジ付きで表示される
- [ ] ダウンロードページ: ダウンロードテーブルとボタンが機能する
- [ ] ナビゲーション: ヘッダー・フッターが仕様通り
- [ ] レスポンシブ: モバイル(375px) / タブレット(768px) / デスクトップ(1280px) で崩れない
- [ ] ダークモード: 全ページでカラーが正しく切り替わる
- [ ] 多言語: JA/EN 切替が動作し、全ページに両言語版がある

---

## Phase 3: デザイン品質向上（P1）

ビジュアル面を仕様書レベルまで引き上げる。「デザインに超うるさい上司」を満足させるフェーズ。

### 3.1 タイポグラフィ精緻化

- Web フォント最適化: Inter + Noto Sans JP のサブセット化・preload
- Major Third スケール（1.250）の厳密適用
- フォントウェイト階層: Display/H1 = 700, H2/H3 = 600, Body = 400
- レタースペーシング: Display/H1 = -0.02em, Body = 0em, 日本語 = 0.04em
- 行間: Display = 1.1, H1 = 1.2, Body = 1.7

### 3.2 余白・スペーシング調整

- 8px ベースシステムの厳密適用
- Hero セクション: 上下 128px（`--space-10`）
- セクション間: 64px（`--space-8`）〜 96px（`--space-9`）
- カード内パディング: 24px（`--space-5`）
- コンテンツ最大幅: 1200px、本文幅: 720px

### 3.3 アニメーション実装

- スクロール時フェードイン: `fade-in-up`、12px 移動、350ms
- ホバーエフェクト: カードのシャドウ変化、120ms
- カラースキーム切替: トランジションなし（CSS 変数の即時切替）
- `prefers-reduced-motion: reduce` 時はすべてのアニメーション無効化

### 3.4 アプリ固有カラーの適用

StillMotion ページ:
- ブランドカラー `#4A9ECC` を CTA ボタン・アクセントに適用
- アクセントカラー `#4DD9C0` をハイライトに使用

DayRhythm ページ:
- ミントカラー `#78CCBE` をベースに

### 3.5 コンポーネント磨き上げ

- App Store バッジ: Apple 公式ガイドライン準拠の配置・サイズ
- プラットフォームバッジ: Lucide Icons 使用、統一サイズ
- 料金比較表: 無料版/フルバージョンの違いが一目でわかるデザイン
- ダウンロードボタン: プラットフォームアイコン付き、明確な階層
- カード: border-radius 8px、ライトモードのみ `box-shadow: 0 1px 3px rgba(0,0,0,0.06)`

### 3.6 スクリーンショット表示モード連動

アプリのスクリーンショットがサイトのダーク/ライトモードに連動する仕組み:

```html
<picture>
  <source srcset="screenshot-dark.webp" media="(prefers-color-scheme: dark)">
  <img src="screenshot-light.webp" alt="...">
</picture>
```

ショートコードまたはパーシャルとして実装し、コンテンツ作成者の負担を最小化。

### 3.7 レスポンシブ最終調整

各ブレークポイントでの表示を確認・調整:
- **375px**（iPhone SE）: 1カラム、Hero テキスト縮小、タッチターゲット 44px 以上
- **768px**（iPad）: 2カラムグリッド、サイドマージン 48px
- **1280px**（デスクトップ）: フルレイアウト、最大幅 1200px

### 3.8 検証

- [ ] フォントが Inter + Noto Sans JP で表示されている
- [ ] タイプスケールが Major Third に従っている
- [ ] 余白が 8px グリッドに整列している
- [ ] アニメーションが仕様通り（fade-in-up、12px、350ms）
- [ ] `prefers-reduced-motion` でアニメーションが無効になる
- [ ] アプリ固有カラーが正しく適用されている
- [ ] ダーク/ライトモードの全要素でコントラスト比 4.5:1 以上
- [ ] 全ブレークポイントでレイアウトが崩れない

---

## Phase 4: SEO・アクセシビリティ・法的ページ（P1-P2）

### 4.1 SEO 対応

**構造化データ（JSON-LD）**:
- `layouts/partials/schema-organization.html` — Organization スキーマ（トップページ）
- `layouts/partials/schema-software.html` — SoftwareApplication スキーマ（アプリページ）
- `layouts/partials/schema-breadcrumb.html` — BreadcrumbList（全ページ）

**メタタグ**:
- OGP (`og:title`, `og:description`, `og:image`, `og:url`, `og:type`, `og:locale`)
- Twitter Card (`twitter:card = summary_large_image`)
- canonical URL
- hreflang（`ja` / `en`）

**OGP 画像**:
- サイト共通: 1200x630px、サイト名 + タグライン
- アプリ別: アプリアイコン + アプリ名

**その他**:
- `sitemap.xml` 自動生成確認
- `robots.txt` テンプレート確認
- ページタイトル最適化（`{ページ名} | Less is More`）
- meta description 全ページ設定

### 4.2 アクセシビリティ（WCAG 2.1 AA）

- セマンティック HTML: `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>` 徹底
- 全画像に `alt` テキスト
- アイコンボタンに `aria-label`
- キーボードナビゲーション対応（`tabindex`, `:focus-visible` スタイル）
- スキップリンク（`Skip to main content`）
- `lang` 属性: `<html lang="ja">` / `<html lang="en">`
- フォントサイズ `rem` 単位（ブラウザズーム対応）

### 4.3 法的ページ

**プライバシーポリシー**:
- `content/ja/legal/privacy/index.md`
- `content/en/legal/privacy/index.md`

**利用規約**:
- `content/ja/legal/terms/index.md`
- `content/en/legal/terms/index.md`

**お問い合わせ**:
- `content/ja/contact/index.md`
- `content/en/contact/index.md`
- 注意: 仕様書の禁止事項「連絡先をかかないこと」に準拠し、問い合わせフォームサービスの利用またはシンプルなメッセージのみ

### 4.4 検証

- [ ] Lighthouse SEO スコア 100
- [ ] Lighthouse Accessibility スコア 90+
- [ ] 構造化データが Google Rich Results Test で有効
- [ ] OGP プレビューが正しく表示される
- [ ] hreflang が正しく設定されている
- [ ] キーボードのみでサイト全体をナビゲートできる
- [ ] スクリーンリーダーで論理的に読み上げられる
- [ ] 法的ページが両言語で存在する

---

## Phase 5: CI/CD・パフォーマンス最適化（P0-P2）

### 5.1 GitHub Actions デプロイパイプライン

**ファイル**: `.github/workflows/deploy.yml`

```yaml
name: Deploy Hugo Site
on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      HUGO_VERSION: "0.142.0"
    steps:
      - Hugo Extended インストール
      - チェックアウト（submodules: recursive, fetch-depth: 0）
      - GitHub Pages 設定
      - Node.js 22 セットアップ + npm キャッシュ
      - npm ci
      - Hugo モジュールキャッシュ
      - Hugo ビルド（--gc --minify, TZ=Asia/Tokyo）
      - アーティファクトアップロード

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - GitHub Pages デプロイ
```

### 5.2 画像最適化

- Hugo Pipes: WebP 自動変換 + PNG フォールバック
- レスポンシブ画像: `srcset` 生成（320/640/960/1280px）
- アプリアイコン: 64px / 96px / 128px のリサイズ
- `assets/` 配置による Hugo Pipes 処理

画像処理パーシャル:
```
layouts/partials/responsive-image.html
layouts/partials/dark-light-image.html
```

### 5.3 パフォーマンスチューニング

- HTML/CSS/JS ミニファイ（Hugo `--minify`）
- CSS: 未使用スタイル削除（Tailwind の purge）
- フォント: `font-display: swap`、サブセット化
- 画像: lazy loading（`loading="lazy"`）
- Critical CSS インライン化（ファーストビュー）

### 5.4 パフォーマンス目標

| 指標 | 目標値 |
|------|--------|
| LCP | < 1.5s |
| INP | < 100ms |
| CLS | < 0.05 |
| Lighthouse Performance | 95+ |
| Lighthouse Accessibility | 95+ |
| Lighthouse Best Practices | 95+ |
| Lighthouse SEO | 100 |

### 5.5 検証

- [ ] GitHub Actions でビルド・デプロイが成功する
- [ ] 画像が WebP で配信されている
- [ ] Lighthouse 全カテゴリ 95+ 達成
- [ ] Core Web Vitals が目標値以内
- [ ] ビルド時間が合理的（30秒以内目安）

---

## 実装ファイル一覧

作成が必要な全ファイルのチェックリスト。

### 設定ファイル

- [ ] `hugo.toml` — Hugo メイン設定
- [ ] `go.mod` — Hugo Modules
- [ ] `go.sum` — Hugo Modules ロックファイル
- [ ] `package.json` — Node.js 依存
- [ ] `package-lock.json` — Node.js ロックファイル

### スタイル

- [ ] `assets/css/schemes/lessismore.css` — Blowfish カスタムカラースキーム
- [ ] `assets/css/custom.css` — デザイントークン・カスタムスタイル

### レイアウト

- [ ] `layouts/partials/extend-head.html` — カスタム head 要素（フォント、JSON-LD）
- [ ] `layouts/page/home.html` — トップページレイアウト（Blowfish オーバーライド）
- [ ] `layouts/apps/list.html` — アプリ一覧
- [ ] `layouts/apps/single.html` — アプリ詳細
- [ ] `layouts/downloads/single.html` — ダウンロード詳細
- [ ] `layouts/partials/app-card.html` — アプリカードコンポーネント
- [ ] `layouts/partials/app-hero.html` — アプリヒーローセクション
- [ ] `layouts/partials/app-store-badge.html` — App Store バッジ
- [ ] `layouts/partials/platform-badge.html` — プラットフォームバッジ
- [ ] `layouts/partials/feature-card.html` — 機能カード
- [ ] `layouts/partials/pricing-table.html` — 料金比較表
- [ ] `layouts/partials/download-button.html` — ダウンロードボタン
- [ ] `layouts/partials/footer-custom.html` — カスタムフッター
- [ ] `layouts/partials/schema-organization.html` — Organization JSON-LD
- [ ] `layouts/partials/schema-software.html` — SoftwareApplication JSON-LD
- [ ] `layouts/partials/schema-breadcrumb.html` — BreadcrumbList JSON-LD
- [ ] `layouts/partials/responsive-image.html` — レスポンシブ画像処理
- [ ] `layouts/partials/dark-light-image.html` — ダーク/ライト画像切替

### コンテンツ（日本語）

- [ ] `content/ja/_index.md` — トップページ
- [ ] `content/ja/apps/_index.md` — アプリ一覧
- [ ] `content/ja/apps/stillmotion/index.md` — StillMotion 詳細
- [ ] `content/ja/apps/dayrhythm/index.md` — DayRhythm（Coming Soon）
- [ ] `content/ja/downloads/_index.md` — ダウンロード一覧
- [ ] `content/ja/downloads/stillmotion-server/index.md` — ローカルサーバー
- [ ] `content/ja/legal/privacy/index.md` — プライバシーポリシー
- [ ] `content/ja/legal/terms/index.md` — 利用規約
- [ ] `content/ja/contact/index.md` — お問い合わせ

### コンテンツ（英語）

- [ ] `content/en/_index.md` — トップページ
- [ ] `content/en/apps/_index.md` — アプリ一覧
- [ ] `content/en/apps/stillmotion/index.md` — StillMotion 詳細
- [ ] `content/en/apps/dayrhythm/index.md` — DayRhythm（Coming Soon）
- [ ] `content/en/downloads/_index.md` — ダウンロード一覧
- [ ] `content/en/downloads/stillmotion-server/index.md` — ローカルサーバー
- [ ] `content/en/legal/privacy/index.md` — プライバシーポリシー
- [ ] `content/en/legal/terms/index.md` — 利用規約
- [ ] `content/en/contact/index.md` — お問い合わせ

### 翻訳

- [ ] `i18n/ja.yaml` — 日本語 UI テキスト
- [ ] `i18n/en.yaml` — 英語 UI テキスト

### CI/CD

- [ ] `.github/workflows/deploy.yml` — GitHub Actions デプロイ

### 静的ファイル

- [ ] `static/CNAME` — カスタムドメイン（設定時）

---

## 作業分担（6名チーム）

### 並行作業マトリクス

```
Timeline:  Phase 1 ──→ Phase 2 ──────────→ Phase 3 ──→ Phase 4 ──→ Phase 5
           (基盤)      (コアページ)         (デザイン)   (SEO/A11y)  (CI/CD)

Hugo Developer:     Phase1全体 → layouts/templates → Blowfish カスタマイズ
Creative Director:  コピーレビュー ────→ デザインレビュー ────→ 最終チェック
UI/UX Designer:     ワイヤーフレーム確認 → レスポンシブ検証 → アクセシビリティ
Visual Designer:    カラースキーム → タイポグラフィ → アニメーション → 最終磨き
Content Strategist: コンテンツ執筆（JA/EN）──→ SEO最適化 → 法的ページ
DevOps Engineer:    CI/CD構築 ──→ 画像最適化パイプライン → パフォーマンス
```

### 依存関係

```
Phase 1.1 (Hugo init)
  → Phase 1.2 (Blowfish設定)
    → Phase 1.3 (カラースキーム) + Phase 1.4 (CSS) [並行可]
      → Phase 1.5 (最小コンテンツ)
        → Phase 2 全体

Phase 2.1 (トップ) + Phase 2.2 (StillMotion) + Phase 2.5 (DL) [並行可]
  → Phase 2.6 (ナビ) + Phase 2.7 (i18n)
    → Phase 3 全体

Phase 3 → Phase 4 [一部並行可]
Phase 5.1 (CI/CD) は Phase 2 完了後いつでも開始可
```

---

## デザイン品質基準

「デザインに超うるさい上司」を満足させるための判断基準:

### Must（必須）

1. **カラーパレット完全一致** — 仕様書のカラーコードとの差異ゼロ
2. **タイポグラフィ正確** — フォント、サイズ、ウェイト、行間が仕様通り
3. **余白 8px グリッド準拠** — すべての余白が 8 の倍数
4. **コントラスト比 4.5:1 以上** — 全テキスト/背景の組み合わせ
5. **レスポンシブ崩れなし** — 375px 〜 1280px のすべてのビューポート
6. **ダークモード完全対応** — 全要素でライト/ダーク切替が正しい
7. **Lighthouse 95+** — 全カテゴリ

### Should（推奨）

1. **アニメーションの「気づかれない」感** — 過剰でも皆無でもない微細さ
2. **余白のリズム** — セクション間の余白に一貫したリズムがある
3. **1画面完結** — トップページは 1〜2 画面で完結
4. **3秒ルール** — 各ページの目的が 3 秒以内に理解できる

### 最終チェックの問い

1. これを取り除いても伝わるか？ → 伝わるなら取り除く
2. ユーザーは 3 秒以内にこのページの目的を理解できるか？
3. PaperMod のブログを読んだ人が「同じ人が作った」と感じるか？
4. このアプリを使いたいと思えるか？

---

## 改善サイクル

各フェーズ完了後に以下のサイクルを実行:

### サイクル 1: 機能検証
- Hugo ビルドエラーチェック
- 全ページ表示確認
- リンク切れチェック
- レスポンシブ表示確認

### サイクル 2: デザイン検証
- カラーパレット一致確認
- タイポグラフィ確認
- 余白・グリッド確認
- ダークモード確認
- アニメーション確認

### サイクル 3: 品質検証
- Lighthouse スコア測定
- アクセシビリティ監査
- SEO チェック
- パフォーマンス測定

問題が発見されたら即座に修正し、再度検証する。このサイクルを各フェーズで 2〜3 回繰り返す。

---

## 注意事項・禁止事項

### 仕様書からの禁止事項
- **連絡先をかかないこと** — contact ページに具体的なメールアドレスや電話番号を掲載しない
- **誇大表現禁止** — 「革命的」「究極の」「No.1」等の表現を使わない
- **感嘆符原則不使用** — 文末に「！」を使わない
- **競合比較禁止** — 他アプリとの比較表現をしない

### 技術的注意事項
- Blowfish テーマの仕組みを理解し、オーバーライドは最小限に
- Hugo Modules でテーマ管理（git submodule ではない）
- `assets/` 配置で Hugo Pipes を活用（`static/` は最終手段）
- Tailwind のユーティリティクラスを活用しつつ、カスタム CSS は最小限に
