# DevOps・パフォーマンス・SEO 設計書

## 1. GitHub Actions ワークフロー設計

### 1.1 ブランチ戦略

```
main (開発・コンテンツ編集)
  └── GitHub Actions → ビルド → GitHub Pages (gh-pages ブランチ or Actions artifact)
```

- **main**: 全てのコンテンツ・コード変更はここにマージ
- **デプロイ**: GitHub Actions が main への push をトリガーにビルド・デプロイを自動実行
- PR ベースのワークフローにより、デプロイ前にプレビュー確認が可能

### 1.2 ワークフロー定義

```yaml
# .github/workflows/deploy.yml
name: Deploy Hugo Site to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:  # 手動トリガー対応

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
      HUGO_VERSION: "0.142.0"  # 使用時点の最新安定版に更新すること
    steps:
      - name: Install Hugo CLI
        run: |
          wget -O ${{ runner.temp }}/hugo.deb \
            https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb
          sudo dpkg -i ${{ runner.temp }}/hugo.deb

      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0  # Git情報（更新日時等）を取得

      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v5

      - name: Setup Node.js (PostCSS等で必要な場合)
        uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: "npm"

      - name: Install Node dependencies
        run: npm ci

      - name: Cache Hugo modules
        uses: actions/cache@v4
        with:
          path: /tmp/hugo_cache
          key: ${{ runner.os }}-hugo-${{ hashFiles('**/go.sum') }}
          restore-keys: |
            ${{ runner.os }}-hugo-

      - name: Build with Hugo
        env:
          HUGO_CACHEDIR: /tmp/hugo_cache
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

### 1.3 キャッシュ戦略

| 対象 | キャッシュキー | 効果 |
|------|--------------|------|
| Hugo モジュール | `go.sum` のハッシュ | モジュール再ダウンロード回避 |
| npm パッケージ | `package-lock.json` のハッシュ | Node依存の再インストール回避 |
| Hugo ビルドキャッシュ | `/tmp/hugo_cache` | 画像処理結果等のキャッシュ |

### 1.4 PR プレビュー（オプション）

将来的に PR ごとのプレビュー環境が必要な場合は、Cloudflare Pages や Netlify をプレビュー専用で利用可能。初期段階では不要。

---

## 2. ドメイン設計

### 2.1 ドメイン構成案

| 構成 | URL | 備考 |
|------|-----|------|
| **案A: カスタムドメイン** | `https://example.com` | 独自ドメインを取得して利用 |
| **案B: GitHub Pages デフォルト** | `https://<org>.github.io/<repo>` | ドメイン費用不要 |
| **推奨** | 案A（カスタムドメイン） | 会社のブランディングに必須 |

### 2.2 カスタムドメイン設定手順

1. ドメインレジストラで独自ドメインを取得
2. DNS に以下のレコードを設定:

```
# A レコード（apex ドメイン用）
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153

# CNAME レコード（www サブドメイン用）
www  CNAME  <username>.github.io
```

3. リポジトリの Settings > Pages でカスタムドメインを入力
4. 「Enforce HTTPS」を有効化
5. Hugo の `config.toml` / `hugo.toml` で `baseURL` をカスタムドメインに設定

### 2.3 CNAME ファイル

Hugo の `static/` ディレクトリに `CNAME` ファイルを配置:

```
# static/CNAME
example.com
```

### 2.4 個人ブログとの共存

- 個人ブログ: `frkake.com` (既存)
- 会社ホームページ: 別ドメインを取得（例: `company-name.com`）
- GitHub 組織アカウントを作成してリポジトリを管理するのが望ましい

---

## 3. 画像最適化

### 3.1 Hugo Pipes による画像処理

アプリアイコン（最大1024px）やスクリーンショットを最適化する。

```html
{{/* layouts/partials/image.html */}}

{{ $src := resources.Get .src }}
{{ if $src }}
  {{/* WebP 変換 */}}
  {{ $webp := $src.Resize (printf "%dx webp q85" .width) }}

  {{/* フォールバック用の元形式 */}}
  {{ $fallback := $src.Resize (printf "%dx q85" .width) }}

  <picture>
    <source srcset="{{ $webp.RelPermalink }}" type="image/webp">
    <img
      src="{{ $fallback.RelPermalink }}"
      alt="{{ .alt }}"
      width="{{ $fallback.Width }}"
      height="{{ $fallback.Height }}"
      loading="{{ default "lazy" .loading }}"
      decoding="async"
    >
  </picture>
{{ end }}
```

### 3.2 レスポンシブ画像

```html
{{/* layouts/partials/responsive-image.html */}}

{{ $src := resources.Get .src }}
{{ if $src }}
  {{ $sizes := slice 320 640 960 1280 }}
  {{ $srcset := slice }}

  {{ range $sizes }}
    {{ if le . $src.Width }}
      {{ $resized := $src.Resize (printf "%dx webp q85" .) }}
      {{ $srcset = $srcset | append (printf "%s %dw" $resized.RelPermalink .) }}
    {{ end }}
  {{ end }}

  {{ $default := $src.Resize "640x webp q85" }}

  <picture>
    <source
      srcset="{{ delimit $srcset ", " }}"
      sizes="{{ default "(max-width: 640px) 100vw, 640px" .sizes }}"
      type="image/webp"
    >
    <img
      src="{{ $default.RelPermalink }}"
      alt="{{ .alt }}"
      width="{{ $default.Width }}"
      height="{{ $default.Height }}"
      loading="{{ default "lazy" .loading }}"
      decoding="async"
    >
  </picture>
{{ end }}
```

### 3.3 アプリアイコン最適化ガイドライン

| 用途 | サイズ | フォーマット | 品質 |
|------|--------|-------------|------|
| ヒーローセクション | 512px | WebP + PNG fallback | q85 |
| カード・サムネイル | 256px | WebP + PNG fallback | q85 |
| OGP 画像 | 1200x630 | PNG（SNS互換性のため） | q90 |
| favicon | 32px, 180px | ICO, PNG | ロスレス |

### 3.4 画像配置

```
assets/
├── images/
│   ├── apps/
│   │   ├── stillmotion/
│   │   │   ├── icon.png          # 元画像 (1024px)
│   │   │   ├── screenshot-1.png
│   │   │   └── screenshot-2.png
│   │   └── dayrhythm/
│   │       └── icon.png
│   └── common/
│       ├── og-default.png        # デフォルトOGP画像
│       └── logo.png
static/
├── favicon.ico
├── apple-touch-icon.png          # 180x180
└── CNAME
```

`assets/` に配置することで Hugo Pipes による動的な画像処理が可能になる。`static/` は処理不要なファイル用。

---

## 4. パフォーマンス目標

### 4.1 Core Web Vitals 目標

| 指標 | 目標値 | 説明 |
|------|--------|------|
| **LCP** (Largest Contentful Paint) | < 1.5s | メインコンテンツの表示速度 |
| **INP** (Interaction to Next Paint) | < 100ms | インタラクション応答性 |
| **CLS** (Cumulative Layout Shift) | < 0.05 | レイアウトの安定性 |

### 4.2 Lighthouse スコア目標

| カテゴリ | 目標 |
|----------|------|
| Performance | 95+ |
| Accessibility | 95+ |
| Best Practices | 95+ |
| SEO | 100 |

### 4.3 パフォーマンス施策

#### ビルド時最適化（Hugo）

- `--minify` フラグで HTML/CSS/JS/XML を圧縮
- `--gc` で未使用キャッシュファイルのクリーンアップ
- Hugo Pipes による CSS/JS のバンドル・最小化

```toml
# hugo.toml
[minify]
  disableCSS = false
  disableHTML = false
  disableJS = false
  disableJSON = false
  disableSVG = false
  disableXML = false
  minifyOutput = true

[minify.tdewolff.html]
  keepWhitespace = false
```

#### CSS 最適化

```html
{{/* CSS をインライン化（クリティカルCSS） */}}
{{ $styles := resources.Get "css/main.css" | minify | fingerprint }}
<link rel="stylesheet" href="{{ $styles.RelPermalink }}" integrity="{{ $styles.Data.Integrity }}">

{{/* Above-the-fold CSS のインライン化 */}}
{{ $critical := resources.Get "css/critical.css" | minify }}
<style>{{ $critical.Content | safeCSS }}</style>
```

#### フォント最適化

```html
{{/* システムフォントスタック推奨 */}}
<style>
  :root {
    --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                 "Helvetica Neue", Arial, "Noto Sans JP", sans-serif;
    --font-mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, monospace;
  }
</style>

{{/* Web フォントを使う場合は preload */}}
<link rel="preload" href="/fonts/subset.woff2" as="font" type="font/woff2" crossorigin>
```

#### 静的アセットの最適化

- Hugo の `fingerprint` パイプでキャッシュバスティング
- GitHub Pages はデフォルトで CDN (Fastly) 経由配信
- `Cache-Control` は GitHub Pages が自動設定（カスタマイズ不可）

---

## 5. SEO 技術要件

### 5.1 sitemap.xml

Hugo はデフォルトで `sitemap.xml` を自動生成する。

```toml
# hugo.toml
[sitemap]
  changefreq = "weekly"
  filename = "sitemap.xml"
  priority = 0.5
```

### 5.2 robots.txt

Hugo テンプレートで生成:

```toml
# hugo.toml
enableRobotsTXT = true
```

```html
{{/* layouts/robots.txt */}}
User-agent: *
Allow: /

Sitemap: {{ .Site.BaseURL }}sitemap.xml
```

### 5.3 OGP (Open Graph Protocol) メタタグ

```html
{{/* layouts/partials/head/ogp.html */}}

{{/* 基本OGPタグ */}}
<meta property="og:title" content="{{ .Title }}">
<meta property="og:description" content="{{ with .Description }}{{ . }}{{ else }}{{ .Site.Params.description }}{{ end }}">
<meta property="og:type" content="{{ if .IsHome }}website{{ else }}article{{ end }}">
<meta property="og:url" content="{{ .Permalink }}">
<meta property="og:site_name" content="{{ .Site.Title }}">
<meta property="og:locale" content="ja_JP">

{{/* OGP画像 */}}
{{ with .Params.ogImage }}
  {{ $ogImg := resources.Get . }}
  {{ if $ogImg }}
    {{ $ogImg = $ogImg.Resize "1200x630 png q90" }}
    <meta property="og:image" content="{{ $ogImg.Permalink }}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
  {{ end }}
{{ else }}
  {{ $defaultOg := resources.Get "images/common/og-default.png" }}
  {{ if $defaultOg }}
    <meta property="og:image" content="{{ $defaultOg.Permalink }}">
  {{ end }}
{{ end }}

{{/* Twitter Card */}}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{ .Title }}">
<meta name="twitter:description" content="{{ with .Description }}{{ . }}{{ else }}{{ .Site.Params.description }}{{ end }}">
```

### 5.4 構造化データ (JSON-LD)

```html
{{/* layouts/partials/head/jsonld.html */}}

{{/* 組織情報 */}}
{{ if .IsHome }}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{{ .Site.Title }}",
  "url": "{{ .Site.BaseURL }}",
  "logo": "{{ (.Site.BaseURL) }}images/logo.png",
  "description": "{{ .Site.Params.description }}"
}
</script>
{{ end }}

{{/* アプリケーション（SoftwareApplication）*/}}
{{ if eq .Type "apps" }}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "{{ .Title }}",
  "description": "{{ .Description }}",
  "applicationCategory": "{{ .Params.appCategory }}",
  "operatingSystem": "{{ delimit .Params.platforms ", " }}",
  "offers": {
    "@type": "Offer",
    "price": "{{ .Params.price | default "0" }}",
    "priceCurrency": "JPY"
  },
  {{ with .Params.appStoreUrl }}
  "installUrl": "{{ . }}",
  {{ end }}
  "image": "{{ with .Params.icon }}{{ . }}{{ end }}"
}
</script>
{{ end }}

{{/* パンくずリスト */}}
{{ if not .IsHome }}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "{{ .Site.BaseURL }}"
    }
    {{ if .Parent }}
    ,{
      "@type": "ListItem",
      "position": 2,
      "name": "{{ .Parent.Title }}",
      "item": "{{ .Parent.Permalink }}"
    }
    {{ end }}
    ,{
      "@type": "ListItem",
      "position": {{ if .Parent }}3{{ else }}2{{ end }},
      "name": "{{ .Title }}",
      "item": "{{ .Permalink }}"
    }
  ]
}
</script>
{{ end }}
```

### 5.5 canonical URL

```html
{{/* layouts/partials/head/canonical.html */}}
<link rel="canonical" href="{{ .Permalink }}">
```

### 5.6 その他 SEO メタタグ

```html
{{/* layouts/partials/head/meta.html */}}
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{{ with .Description }}{{ . }}{{ else }}{{ .Site.Params.description }}{{ end }}">
{{ with .Params.keywords }}<meta name="keywords" content="{{ delimit . ", " }}">{{ end }}
<meta name="author" content="{{ .Site.Params.author }}">

{{/* 多言語対応（将来対応用） */}}
{{ if .IsTranslated }}
  {{ range .Translations }}
    <link rel="alternate" hreflang="{{ .Lang }}" href="{{ .Permalink }}">
  {{ end }}
  <link rel="alternate" hreflang="{{ .Lang }}" href="{{ .Permalink }}">
{{ end }}

{{/* RSS */}}
{{ range .AlternativeOutputFormats }}
  {{ printf `<link rel="%s" type="%s" href="%s" title="%s">` .Rel .MediaType.Type .Permalink (printf "%s - %s" $.Site.Title .Name) | safeHTML }}
{{ end }}
```

---

## 6. セキュリティ

### 6.1 HTTPS

- GitHub Pages はカスタムドメインでも **自動HTTPS** (Let's Encrypt) を提供
- リポジトリ設定で「Enforce HTTPS」を有効化
- Hugo 設定で `baseURL` は `https://` で指定

### 6.2 セキュリティヘッダー

GitHub Pages では HTTP ヘッダーのカスタマイズが不可のため、`<meta>` タグで対応可能な範囲を設定:

```html
{{/* layouts/partials/head/security.html */}}

{{/* CSP (Content Security Policy) - meta タグ版 */}}
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self';
  script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com;
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https://www.google-analytics.com;
  font-src 'self';
  connect-src 'self' https://www.google-analytics.com https://analytics.google.com;
  frame-src 'none';
  object-src 'none';
  base-uri 'self';
">

{{/* その他のセキュリティ meta タグ */}}
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta name="referrer" content="strict-origin-when-cross-origin">
```

### 6.3 注意事項

- GitHub Pages では `X-Frame-Options`, `Strict-Transport-Security` 等のヘッダーはプラットフォーム側が設定
- より高度なセキュリティヘッダーが必要な場合は Cloudflare (無料プラン) をプロキシとして利用を検討
- 外部スクリプトは最小限に抑え、SRI (Subresource Integrity) を活用

---

## 7. 分析ツール

### 7.1 推奨構成

| ツール | 用途 | 理由 |
|--------|------|------|
| **Google Analytics 4 (GA4)** | アクセス解析 | 無料、App Store連携データと統合可能 |
| **Google Search Console** | 検索パフォーマンス | インデックス管理、検索クエリ分析 |

### 7.2 GA4 実装

```html
{{/* layouts/partials/head/analytics.html */}}

{{ if eq hugo.Environment "production" }}
{{ with .Site.Params.googleAnalyticsID }}
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={{ . }}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', '{{ . }}');
</script>
{{ end }}
{{ end }}
```

```toml
# hugo.toml
[params]
  googleAnalyticsID = "G-XXXXXXXXXX"  # 実際のIDに置換
```

### 7.3 プライバシー配慮

GA4 を使用する場合、日本の個人情報保護法に準拠するため:

- プライバシーポリシーページを作成
- Cookie利用の告知（簡易バナーで可）
- GA4 の IP 匿名化はデフォルトで有効

### 7.4 代替ツール（プライバシー重視の場合）

Cookie不要・軽量な代替として以下も検討可:

| ツール | 特徴 |
|--------|------|
| **Plausible Analytics** | Cookie不使用、軽量(< 1KB)、有料($9/月) |
| **Umami** | オープンソース、セルフホスト可能、Cookie不使用 |
| **Cloudflare Web Analytics** | 無料、Cookie不使用、JSスニペットのみ |

初期段階では **GA4** を推奨。App Store のマーケティング分析と統合しやすく、無料で利用可能。

---

## 8. Hugo 設定ファイル（まとめ）

上記の設計を統合した Hugo 設定の概要:

```toml
# hugo.toml

baseURL = "https://example.com/"  # カスタムドメインまたは GitHub Pages URL
languageCode = "ja"
defaultContentLanguage = "ja"
title = "会社名"
enableRobotsTXT = true
enableGitInfo = true  # Git の最終更新日時を利用

[sitemap]
  changefreq = "weekly"
  filename = "sitemap.xml"
  priority = 0.5

[params]
  description = "サイトの説明文"
  author = "作者名"
  googleAnalyticsID = "G-XXXXXXXXXX"

[minify]
  disableCSS = false
  disableHTML = false
  disableJS = false
  disableJSON = false
  disableSVG = false
  disableXML = false
  minifyOutput = true

[outputs]
  home = ["HTML", "RSS", "JSON"]  # JSON は検索機能用（将来対応）

[markup.goldmark.renderer]
  unsafe = false  # セキュリティのため
```

---

## 9. ディレクトリ構成（DevOps 関連）

```
homepage/
├── .github/
│   └── workflows/
│       └── deploy.yml          # デプロイワークフロー
├── assets/
│   ├── css/
│   │   ├── critical.css        # Above-the-fold CSS
│   │   └── main.css            # メインCSS
│   └── images/                 # Hugo Pipes 処理対象画像
├── layouts/
│   └── partials/
│       └── head/
│           ├── meta.html       # 基本メタタグ
│           ├── ogp.html        # OGP タグ
│           ├── jsonld.html     # 構造化データ
│           ├── canonical.html  # canonical URL
│           ├── security.html   # セキュリティ meta
│           └── analytics.html  # GA4
├── static/
│   ├── CNAME                   # カスタムドメイン
│   ├── favicon.ico
│   └── apple-touch-icon.png
├── hugo.toml                   # Hugo 設定
├── package.json                # Node 依存（PostCSS 等）
└── package-lock.json
```

---

## 10. デザイン品質検証

実装がデザイン仕様に忠実であること、ビジュアルとして完璧であることを自動的に検証する。
構文の正しさではなく、**見た目の正しさ**が検証の中心。

### 10.1 テスト構成

```
tests/
├── design/
│   ├── design-tokens.spec.ts     # デザイントークン検証
│   ├── layout.spec.ts            # レイアウト構造検証
│   ├── visual-regression.spec.ts # ビジュアルリグレッション
│   ├── design-tokens.ts          # 仕様値の定義
│   └── baseline/                 # ベースラインスクリーンショット（Git 管理）
├── playwright.config.ts
└── package.json
```

### 10.2 デザイントークン検証

CSS の算出値を取得し、デザイン仕様（visual-identity.md セクション 4）で定義した値と一致するかを検証する。

```typescript
// tests/design/design-tokens.ts
// デザイン仕様から抽出したトークン定義

export const tokens = {
  light: {
    bgPrimary: "rgb(250, 250, 250)",       // #FAFAFA
    bgSecondary: "rgb(255, 255, 255)",      // #FFFFFF
    textPrimary: "rgb(26, 26, 26)",         // #1A1A1A
    textSecondary: "rgb(107, 107, 107)",    // #6B6B6B
    border: "rgb(229, 229, 229)",           // #E5E5E5
    brand: "rgb(74, 158, 204)",             // #4A9ECC
    accent: "rgb(77, 217, 192)",            // #4DD9C0
  },
  dark: {
    bgPrimary: "rgb(18, 18, 18)",           // #121212
    bgSecondary: "rgb(30, 30, 30)",         // #1E1E1E
    textPrimary: "rgb(240, 240, 240)",      // #F0F0F0
    textSecondary: "rgb(160, 160, 160)",    // #A0A0A0
    border: "rgb(51, 51, 51)",              // #333333
    brand: "rgb(90, 174, 220)",             // #5AAEDC
    accent: "rgb(93, 233, 208)",            // #5DE9D0
  },
  typography: {
    fontFamily: /Inter|Noto Sans JP|-apple-system|sans-serif/,
    monoFamily: /JetBrains Mono|SF Mono|monospace/,
    display: { size: "48.83px", weight: "700" },   // 3.052rem
    h1: { size: "39.06px", weight: "700" },         // 2.441rem
    h2: { size: "31.25px", weight: "600" },         // 1.953rem
    h3: { size: "25.00px", weight: "600" },         // 1.563rem (25.008 ≈ 25px)
    body: { size: "16px", weight: "400" },           // 1.0rem
  },
  spacing: {
    base: 8,  // px
    contentMax: 1200,
    contentText: 720,
  },
  borderRadius: {
    card: "8px",
    button: "4px",
    chip: "2px",
  },
};
```

```typescript
// tests/design/design-tokens.spec.ts
import { test, expect } from "@playwright/test";
import { tokens } from "./design-tokens";

const pages = [
  { name: "home", path: "/" },
  { name: "stillmotion", path: "/apps/stillmotion/" },
  { name: "dayrhythm", path: "/apps/dayrhythm/" },
];

for (const page of pages) {
  test.describe(`${page.name} - デザイントークン`, () => {

    // ----- カラーパレット: ライトモード -----
    test("ライトモード: カラーパレットが仕様通り", async ({ browser }) => {
      const context = await browser.newContext({ colorScheme: "light" });
      const p = await context.newPage();
      await p.goto(page.path);
      await p.waitForLoadState("networkidle");

      const bgColor = await p.evaluate(() =>
        getComputedStyle(document.body).backgroundColor
      );
      // テーマのCSS変数経由で適用されるため、最終的なRGB値で比較
      expect(bgColor).toBe(tokens.light.bgPrimary);

      await context.close();
    });

    // ----- カラーパレット: ダークモード -----
    test("ダークモード: カラーパレットが仕様通り", async ({ browser }) => {
      const context = await browser.newContext({ colorScheme: "dark" });
      const p = await context.newPage();
      await p.goto(page.path);
      await p.waitForLoadState("networkidle");

      const bgColor = await p.evaluate(() =>
        getComputedStyle(document.body).backgroundColor
      );
      expect(bgColor).toBe(tokens.dark.bgPrimary);

      await context.close();
    });

    // ----- タイポグラフィ -----
    test("タイポグラフィ: フォントファミリーとサイズが仕様通り", async ({ page: p }) => {
      await p.goto(page.path);
      await p.waitForLoadState("networkidle");

      const bodyFont = await p.evaluate(() =>
        getComputedStyle(document.body).fontFamily
      );
      expect(bodyFont).toMatch(tokens.typography.fontFamily);

      const bodySize = await p.evaluate(() =>
        getComputedStyle(document.body).fontSize
      );
      expect(bodySize).toBe(tokens.typography.body.size);
    });

    // ----- コントラスト比 -----
    test("コントラスト比: WCAG AA (4.5:1) を満たす", async ({ browser }) => {
      for (const scheme of ["light", "dark"] as const) {
        const context = await browser.newContext({ colorScheme: scheme });
        const p = await context.newPage();
        await p.goto(page.path);
        await p.waitForLoadState("networkidle");

        const ratio = await p.evaluate(() => {
          const body = document.body;
          const style = getComputedStyle(body);
          const bg = style.backgroundColor;
          const fg = style.color;

          function parseRgb(color: string) {
            const m = color.match(/\d+/g)!.map(Number);
            return m.map((c) => {
              const s = c / 255;
              return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
            });
          }

          function luminance(rgb: number[]) {
            return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2];
          }

          const bgL = luminance(parseRgb(bg));
          const fgL = luminance(parseRgb(fg));
          const lighter = Math.max(bgL, fgL);
          const darker = Math.min(bgL, fgL);
          return (lighter + 0.05) / (darker + 0.05);
        });

        expect(ratio).toBeGreaterThanOrEqual(4.5);
        await context.close();
      }
    });
  });
}
```

### 10.3 レイアウト構造検証

要素の配置・サイズ・間隔がデザイン仕様に一致するかを数値で検証する。

```typescript
// tests/design/layout.spec.ts
import { test, expect } from "@playwright/test";
import { tokens } from "./design-tokens";

test.describe("レイアウト構造", () => {

  // ----- コンテンツ幅 -----
  test("コンテンツ最大幅が 1200px を超えない", async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto("/");
    await page.waitForLoadState("networkidle");

    const mainWidth = await page.evaluate(() => {
      const main = document.querySelector("main");
      return main ? main.getBoundingClientRect().width : 0;
    });
    expect(mainWidth).toBeLessThanOrEqual(tokens.spacing.contentMax);
  });

  // ----- レスポンシブ: レイアウト崩れ検出 -----
  const viewports = [
    { name: "mobile", width: 375, height: 812 },
    { name: "tablet", width: 768, height: 1024 },
    { name: "desktop", width: 1280, height: 800 },
  ];

  for (const vp of viewports) {
    test(`${vp.name} (${vp.width}px): 水平スクロールが発生しない`, async ({ page }) => {
      await page.setViewportSize({ width: vp.width, height: vp.height });
      await page.goto("/");
      await page.waitForLoadState("networkidle");

      const hasOverflow = await page.evaluate(() => {
        return document.documentElement.scrollWidth > document.documentElement.clientWidth;
      });
      expect(hasOverflow).toBe(false);
    });

    test(`${vp.name} (${vp.width}px): 要素同士がオーバーラップしない`, async ({ page }) => {
      await page.setViewportSize({ width: vp.width, height: vp.height });
      await page.goto("/");
      await page.waitForLoadState("networkidle");

      const overlaps = await page.evaluate(() => {
        const elements = Array.from(
          document.querySelectorAll("header, main, footer, section, nav")
        );
        const rects = elements.map((el) => el.getBoundingClientRect());
        const found: string[] = [];

        for (let i = 0; i < rects.length; i++) {
          for (let j = i + 1; j < rects.length; j++) {
            const a = rects[i], b = rects[j];
            // 親子関係でない同階層要素が重なっていないか
            if (
              !elements[i].contains(elements[j]) &&
              !elements[j].contains(elements[i]) &&
              a.right > b.left && a.left < b.right &&
              a.bottom > b.top && a.top < b.bottom
            ) {
              found.push(
                `${elements[i].tagName} と ${elements[j].tagName} が重なっている`
              );
            }
          }
        }
        return found;
      });
      expect(overlaps).toEqual([]);
    });
  }

  // ----- ナビゲーション構造 -----
  test("ヘッダー: 仕様通りの項目数", async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto("/");
    await page.waitForLoadState("networkidle");

    const navItems = await page.locator("header nav a, header nav button").count();
    // Apps, Contact, 言語切替 = 最低3つ
    expect(navItems).toBeGreaterThanOrEqual(3);
  });

  // ----- 角丸の統一性 -----
  test("カード要素の border-radius が 8px", async ({ page }) => {
    await page.goto("/");
    await page.waitForLoadState("networkidle");

    const cards = page.locator("[class*='card'], [class*='Card']");
    const count = await cards.count();
    for (let i = 0; i < count; i++) {
      const radius = await cards.nth(i).evaluate((el) =>
        getComputedStyle(el).borderRadius
      );
      expect(radius).toBe(tokens.borderRadius.card);
    }
  });
});
```

### 10.4 ビジュアルリグレッションテスト

ベースライン画像との差分で、意図しないデザイン変更を検出する。

```typescript
// tests/design/visual-regression.spec.ts
import { test, expect } from "@playwright/test";

const pages = [
  { name: "home", path: "/" },
  { name: "stillmotion", path: "/apps/stillmotion/" },
  { name: "dayrhythm", path: "/apps/dayrhythm/" },
  { name: "download", path: "/downloads/stillmotion/" },
  { name: "privacy", path: "/legal/privacy/" },
  { name: "contact", path: "/contact/" },
];

const viewports = [
  { name: "mobile", width: 375, height: 812 },
  { name: "tablet", width: 768, height: 1024 },
  { name: "desktop", width: 1280, height: 800 },
];

const colorSchemes = ["light", "dark"] as const;

for (const page of pages) {
  for (const vp of viewports) {
    for (const scheme of colorSchemes) {
      test(`${page.name} - ${vp.name} - ${scheme}`, async ({ browser }) => {
        const context = await browser.newContext({
          viewport: { width: vp.width, height: vp.height },
          colorScheme: scheme,
        });
        const p = await context.newPage();
        await p.goto(page.path);
        await p.waitForLoadState("networkidle");

        await expect(p).toHaveScreenshot(
          `${page.name}-${vp.name}-${scheme}.png`,
          { maxDiffPixelRatio: 0.001, fullPage: true }
        );
        await context.close();
      });
    }
  }
}
```

### 10.5 CI ワークフロー

```yaml
# .github/workflows/design-quality.yml
name: Design Quality

on:
  pull_request:
    branches: [main]

jobs:
  design-test:
    runs-on: ubuntu-latest
    env:
      HUGO_VERSION: "0.142.0"
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Install Hugo CLI
        run: |
          wget -O ${{ runner.temp }}/hugo.deb \
            https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb
          sudo dpkg -i ${{ runner.temp }}/hugo.deb

      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium

      - name: Build Hugo
        env:
          HUGO_ENVIRONMENT: production
          TZ: Asia/Tokyo
        run: hugo --gc --minify

      - name: Start local server
        run: npx serve public -l 8080 &

      - name: Wait for server
        run: npx wait-on http://localhost:8080

      - name: Run design token tests
        run: npx playwright test tests/design/design-tokens.spec.ts
        env:
          BASE_URL: "http://localhost:8080"

      - name: Run layout tests
        run: npx playwright test tests/design/layout.spec.ts
        env:
          BASE_URL: "http://localhost:8080"

      - name: Run visual regression tests
        run: npx playwright test tests/design/visual-regression.spec.ts
        env:
          BASE_URL: "http://localhost:8080"

      - name: Upload screenshots & diffs
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: design-screenshots
          path: |
            test-results/
            tests/design/baseline/
          retention-days: 14

  lighthouse:
    runs-on: ubuntu-latest
    env:
      HUGO_VERSION: "0.142.0"
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive

      - name: Install Hugo CLI
        run: |
          wget -O ${{ runner.temp }}/hugo.deb \
            https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb
          sudo dpkg -i ${{ runner.temp }}/hugo.deb

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Build Hugo
        env:
          HUGO_ENVIRONMENT: production
          TZ: Asia/Tokyo
        run: hugo --gc --minify

      - name: Run Lighthouse CI
        uses: treosh/lighthouse-ci-action@v12
        with:
          configPath: "./lighthouserc.json"
          uploadArtifacts: true
```

### 10.6 ベースライン管理ルール

- ベースライン画像の**初回承認は人間のデザインレビューを必須**とする
- 意図的なデザイン変更があった場合のみベースラインを更新
- ベースライン更新時は PR で Before / After のスクリーンショットを添付し、変更意図を明記
- `npx playwright test --update-snapshots` でベースラインを再生成

---

## 11. デプロイチェックリスト

### 初回セットアップ

- [ ] GitHub リポジトリの Settings > Pages で「GitHub Actions」をソースに設定
- [ ] カスタムドメイン取得・DNS レコード設定
- [ ] CNAME ファイルを `static/` に配置
- [ ] 「Enforce HTTPS」を有効化
- [ ] Google Search Console にサイトを登録
- [ ] GA4 プロパティを作成し、トラッキングIDを設定
- [ ] `sitemap.xml` を Search Console に送信

### 各デプロイ時（自動）

- [ ] Hugo ビルド成功
- [ ] HTML/CSS/JS ミニファイ適用
- [ ] 画像の WebP 変換・リサイズ処理
- [ ] sitemap.xml 更新

### PR マージ前（自動）

- [ ] デザイントークン検証: カラー・タイポグラフィ・スペーシングが仕様値と一致
- [ ] レイアウト検証: レスポンシブ崩れなし・要素重なりなし・コンテンツ幅制限内
- [ ] コントラスト比: 全ページ・全モードで WCAG AA (4.5:1) 以上
- [ ] ビジュアルリグレッション: ベースラインとの差分なし or 意図的変更（人間レビュー済み）
- [ ] Lighthouse CI スコア全カテゴリ 90 以上

### 定期確認（月次）

- [ ] Lighthouse スコアチェック（Performance 95+）
- [ ] Core Web Vitals レポート確認
- [ ] ビジュアルリグレッションのベースライン見直し
- [ ] Search Console のインデックスカバレッジ確認
- [ ] GA4 でアクセス状況確認
