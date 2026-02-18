# Homepage Requirements v2 - 詳細仕様書

> 本文書は6名のプロフェッショナルチーム（Creative Director, UI/UX Designer, Visual Designer, Hugo Developer, Content Strategist, DevOps Engineer）の設計成果を統合した、ホームページの包括的な仕様書です。
> 各セクションの詳細は個別ドキュメントを参照してください。

---

## 目次

1. [プロジェクト概要](#1-プロジェクト概要)
2. [コンセプト・ブランディング](#2-コンセプトブランディング)
3. [サイト構成・ページ設計](#3-サイト構成ページ設計)
4. [ビジュアルデザイン](#4-ビジュアルデザイン)
5. [コンテンツ戦略](#5-コンテンツ戦略)
6. [技術設計](#6-技術設計)
7. [DevOps・パフォーマンス](#7-devopsパフォーマンス)
8. [実装優先順位](#8-実装優先順位)
9. [参照ドキュメント](#9-参照ドキュメント)

---

## 1. プロジェクト概要

### 1.1 目的

アプリ開発会社のホームページを Hugo + GitHub Pages で構築する。アプリのPR、関連ソフトウェアのダウンロード、会社情報の発信を行う。

### 1.2 掲載アプリ

| アプリ名 | ステータス | プラットフォーム | 概要 |
|----------|-----------|----------------|------|
| **StillMotion** | 完成 | iOS / iPadOS / macOS / watchOS + ローカルサーバー | 画像と動画をシームレスに扱えるメディアビューア |
| **DayRhythm** | 開発中 | iOS / iPadOS / watchOS（予定） | サーカディアンリズム科学に基づくAI習慣化アプリ |

### 1.3 技術スタック

- **SSG**: Hugo（Extended版）
- **テーマ**: Blowfish（Tailwind CSS 3.0 ベース）
- **ホスティング**: GitHub Pages
- **CI/CD**: GitHub Actions
- **テーマ管理**: Hugo Modules（Go Modules ベース）

---

## 2. コンセプト・ブランディング

> 詳細: [creative_direction.md](./creative_direction.md)

### 2.1 全体コンセプト: "Quiet Craft"（静かなる技巧）

社名はyohaku（余白）。サイト名は「Less is More」。

その「Less is More」を発展させ、「削ぎ落とすこと自体に価値がある」という世界観。華美な装飾や過剰な演出を排し、プロダクトそのものの完成度で語るサイト。

**3つの柱:**

1. **Restraint（抑制）** - 必要なものだけを、必要なだけ
2. **Precision（精緻）** - 細部への徹底したこだわり
3. **Seamlessness（シームレス）** - 技術の複雑さをユーザーに感じさせない

### 2.2 社名・サイト名・タグライン

- **社名**: **yohaku**（余白）— 日本美術の「意図的な空白」を表す言葉。Less is Moreの哲学を凝縮した名前
- **サイト名**: **Less is More**
- **推奨タグライン**: 「**Less, but better.**」

### 2.3 トーン & マナー

| 要素 | 方針 |
|------|------|
| 声色 | 穏やかで誠実、しかし自信を持っている |
| 文体 | 簡潔・平易。専門用語は最小限に |
| リズム | 短い文を重ねる。体言止めも効果的に使う |
| 温度感 | 冷たすぎず、熱すぎず。感嘆符は原則使わない |

**DO**: 機能ではなく体験を語る。余白を怖がらない。
**DON'T**: 誇大表現（「革命的」「究極の」）。競合比較。緊急性の煽り。

### 2.4 デザイン方針: "Functional Minimalism"

- **余白を構造として使う** - 1画面に詰め込まない
- **アプリのスクリーンショットが主役** - 装飾よりプロダクトそのもの
- **タイポグラフィが骨格** - フォントウェイトで階層を表現
- **カラーは抑制的** - モノクロームベース + アプリごとのアクセント
- **アニメーションは「気づかれない」くらいで** - フェードイン程度の微細な動き

### 2.5 判断基準

迷ったときの問い:

1. これを取り除いても伝わるか？ → 伝わるなら取り除く
2. ユーザーは3秒以内にこのページの目的を理解できるか？
3. PaperModのブログを読んだ人が「同じ人が作った」と感じるか？
4. このアプリを使いたいと思えるか？

---

## 3. サイト構成・ページ設計

> 詳細: [ui_ux_design.md](./ui_ux_design.md)

### 3.1 サイトマップ

```
/                              トップページ
├── /apps/                     アプリ一覧
│   ├── /apps/stillmotion/     StillMotion 詳細
│   └── /apps/dayrhythm/       DayRhythm（Coming Soon）
├── /download/                 ダウンロード
│   └── /download/stillmotion-server/  StillMotion Server
├── /privacy/                  プライバシーポリシー
├── /terms/                    利用規約
└── /contact/                  お問い合わせ
```

- URL パターン: `/apps/{app-slug}/` で将来のアプリ追加に対応
- 多言語: `/ja/` `/en/` プレフィックス方式（Hugo i18n）

### 3.2 ページ構成

#### トップページ

| セクション | 内容 |
|-----------|------|
| Hero | サイト名 + タグライン + 余白。それだけ |
| Featured Apps | アプリカード一覧（アイコン + 名前 + 一行説明） |
| Footer | 共通フッター |

- ミニマル志向: 1〜2画面で完結

#### StillMotion 詳細ページ

| セクション | 内容 |
|-----------|------|
| App Hero | アイコン（大）+ アプリ名 + サブタイトル + プラットフォームバッジ |
| CTA Primary | App Store バッジ群（iOS/iPadOS/macOS） |
| Overview | アプリの概要説明（2〜3段落） |
| Features | 主要機能リスト（3〜6個、グリッド配置） |
| Screenshots | スクリーンショットギャラリー（デバイスごと）。**ライト/ダーク両方を用意し、サイトの表示モードに連動して切り替える** |
| Local Server | ローカルサーバー説明 + ダウンロードリンク |
| CTA Secondary | App Store バッジ再掲 |

#### DayRhythm（Coming Soon）

| セクション | 内容 |
|-----------|------|
| App Hero | アイコン + アプリ名 + 「Coming Soon」バッジ |
| Teaser | 簡単な紹介文 + 対応予定プラットフォーム |

#### ダウンロードページ

| セクション | 内容 |
|-----------|------|
| Header | ソフトウェア名 + バージョン |
| System Requirements | 対応OS・動作要件 |
| Download Links | macOS / Linux / Windows ダウンロードボタン（GitHub Releases からダウンロード） |
| Installation Guide | 簡潔なインストール手順（折りたたみ可） |

### 3.3 ナビゲーション

**ヘッダー**（項目を絞る）:
```
[Logo/サイト名]          [Apps]  [Contact]  [EN/JA]
```
- Privacy / Terms はフッターのみに配置

**フッター**（3カラム）:
```
Apps            Legal            Connect
StillMotion     Privacy Policy   Contact
DayRhythm       Terms of Use
```

**モバイル**: ハンバーガーメニュー、アニメーション 150〜200ms

### 3.4 レスポンシブ対応

**モバイルファースト**、`min-width` メディアクエリで段階的に拡張。

| ブレークポイント | 幅 | 対象 |
|----------------|-----|------|
| `sm` | 640px〜 | 大きめスマートフォン |
| `md` | 768px〜 | タブレット |
| `lg` | 1024px〜 | デスクトップ |
| `xl` | 1280px〜 | 大画面 |

### 3.5 CTA 戦略

- **1ページにつき主要CTAは1種類**
- App Store 公式バッジ使用（Apple ガイドライン準拠）
- アプリ詳細ページの**上部と下部**に App Store バッジ二重配置
- ローカルサーバーのダウンロードは控えめに（メインCTAを邪魔しない）

### 3.6 アクセシビリティ

- **WCAG 2.1 Level AA** 目標
- セマンティック HTML 徹底
- コントラスト比 4.5:1 以上
- キーボード操作対応
- `prefers-reduced-motion` 完全対応
- Lighthouse Accessibility 90+ 目標

---

## 4. ビジュアルデザイン

> 詳細: [visual-identity.md](./visual-identity.md)

### 4.1 アイコン分析

**StillMotion**: 角丸フレーム内に「山」+「再生ボタン」。ブルー系グラデーション（`#6EB3E6` 〜 `#A8D4F0`）、シアンアクセント（`#4DD9C0`）。幾何学的、クリーン。

**DayRhythm**: 螺旋/渦巻きの有機的モチーフ。ミント/ターコイズ（`#78CCBE`）基調。時間帯カラー（朝=オレンジ、昼=グリーン、夜=パープル）。温かみのある流動的デザイン。

### 4.2 カラーパレット

#### サイト共通

| 役割 | ライトモード | ダークモード |
|------|-------------|-------------|
| Background Primary | `#FAFAFA` | `#121212` |
| Background Secondary | `#FFFFFF` | `#1E1E1E` |
| Text Primary | `#1A1A1A` | `#F0F0F0` |
| Text Secondary | `#6B6B6B` | `#A0A0A0` |
| Border | `#E5E5E5` | `#333333` |
| Brand | `#4A9ECC` | `#5AAEDC` |
| Accent | `#4DD9C0` | `#5DE9D0` |

#### アプリ固有

| アプリ | Primary | Accent |
|-------|---------|--------|
| StillMotion | `#4A9ECC` (ブルー) | `#4DD9C0` (シアン) |
| DayRhythm | `#78CCBE` (ミント) | 朝 `#F0A050` / 昼 `#5EBB78` / 夜 `#8B6BB5` |

- ダークモード: `prefers-color-scheme` に追従（手動トグル不要）
- **アプリスクリーンショットの表示モード連動**: サイトがダークモードのときはアプリのダークモードのスクリーンショットを、ライトモードのときはライトモードのスクリーンショットを表示する。各スクリーンショットにつきライト版・ダーク版の2枚を用意し、`<picture>` + `prefers-color-scheme` メディアクエリ、またはJavaScriptによる切り替えで実装する

### 4.3 タイポグラフィ

| 用途 | フォント |
|------|---------|
| 見出し・本文 | Inter + Noto Sans JP |
| コード | JetBrains Mono |

**タイプスケール**: Major Third 比率（1.250）

| レベル | サイズ | ウェイト |
|--------|--------|---------|
| Display | 3.052rem | 700 |
| H1 | 2.441rem | 700 |
| H2 | 1.953rem | 600 |
| H3 | 1.563rem | 600 |
| Body | 1.0rem (16px) | 400 |

### 4.4 余白・グリッド

- **8px ベース**の10段階スペーシングシステム
- **12カラムグリッド**、最大幅 1200px、本文 720px
- ヒーローセクション: 全幅、最大限の余白（128px）

### 4.5 ビジュアルエレメント

- **角丸統一**: カード 8px、ボタン 4px、チップ 2px、アプリアイコン 22%
- **シャドウ**: ライトモードのみ微細に使用
- **UIアイコン**: Lucide Icons（ラインスタイル、1.5px ストローク）
- **アニメーション**: 120ms / 200ms / 350ms の3段階デュレーション

### 4.6 デザイントークン（CSS Custom Properties）

```css
:root {
  /* カラー */
  --color-bg-primary: #FAFAFA;
  --color-text-primary: #1A1A1A;
  --color-brand: #4A9ECC;
  --color-accent: #4DD9C0;

  /* タイポグラフィ */
  --font-heading: "Inter", "Noto Sans JP", -apple-system, sans-serif;
  --font-body: "Inter", "Noto Sans JP", -apple-system, sans-serif;
  --font-mono: "JetBrains Mono", "SF Mono", monospace;

  /* スペーシング */
  --space-4: 1rem;    /* 基本 */
  --space-8: 4rem;    /* セクション間 */
  --space-10: 8rem;   /* ヒーロー余白 */

  /* レイアウト */
  --content-max: 1200px;
  --content-text: 720px;

  /* アニメーション */
  --ease-out: cubic-bezier(0.22, 1, 0.36, 1);
  --duration-fast: 120ms;
  --duration-normal: 200ms;
  --duration-slow: 350ms;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-bg-primary: #121212;
    --color-text-primary: #F0F0F0;
    --color-brand: #5AAEDC;
    --color-accent: #5DE9D0;
  }
}
```

完全版は [visual-identity.md](./visual-identity.md) の付録を参照。

---

## 5. コンテンツ戦略

> 詳細: [content_strategy.md](./content_strategy.md)

### 5.1 トップページ

**ヘッドライン**: 「**画像も動画も、ひとつに。**」 / "**Images and Videos, United.**"

**サブヘッドライン**: 「7つのソース、20以上のフォーマット。画像も動画もシームレスに閲覧できるメディアビューア。」

### 5.2 StillMotion ページ

#### ヒーローセクション

```
画像も動画も、区別なく。

写真、RAW、MKV、WebM――20種類以上のフォーマットに対応。
7つのメディアソースをひとつのアプリで、シームレスに。

[App Store でダウンロード]
```

#### 主要機能（4つに絞り込み）

1. **シームレスなスライドショー** - 「画像と動画を混ぜて、連続再生。」
2. **タイル表示（有料）** - 「最大30枚を、1画面に。」
3. **デュアルエンジン動画再生** - 「再生できないフォーマットは、もうない。」
4. **7つのメディアソース** - 「保存場所を選ばない。」

#### 料金プラン

```
無料で始める。必要なら、もっと。
買い切り ¥800。サブスクなし。一度買えば、ずっと使える。
```

- 無料版 vs フルバージョン 比較表（詳細は content_strategy.md 参照）
- 「広告は一切ありません」を強調

### 5.3 ダウンロードページ（ローカルサーバー）

```
StillMotion Local Server
PCのメディアを、手元のデバイスで。
```

- macOS / Linux / Windows ダウンロードリンク（GitHub Releases から配布）
- 5ステップの簡易セットアップガイド

### 5.4 多言語方針

- **日本語をプライマリ**（開発者がネイティブ、主要ターゲット市場）
- 逐語翻訳を避け、各言語で自然なコピーライティング
  - 日本語: 体言止め・余韻型（「画像も動画も、ひとつに。」）
  - 英語: アクション指向・直接型（"No format left behind."）

### 5.5 SEO キーワード

**日本語主要キーワード**: メディアビューア iPhone / MKV 再生 iPhone / RAW 閲覧 iPhone / スライドショー アプリ / 広告なし 写真ビューア

**構造化データ**: SoftwareApplication（アプリ）、Organization（ホーム）、BreadcrumbList（パンくず）

---

## 6. 技術設計

> 詳細: [hugo_technical_architecture.md](./hugo_technical_architecture.md)

### 6.1 テーマ: Blowfish

**選定理由**:

- Tailwind CSS 3.0 ベースでブランドカスタマイズが容易
- ドロップダウンメニュー対応（アプリ増加時に階層化可能）
- カスタムセクションレイアウトが柔軟
- ダークモード・多言語対応が組み込み済み

**PaperMod を選ばない理由**: ドロップダウン非対応、カスタムセクションの柔軟性不足、ブログ特化

## 禁止事項

以下のことは遵守すること

- 連絡先をかかないこと

### 6.2 ディレクトリ構成

```
homepage/
├── hugo.toml
├── go.mod / go.sum            # Hugo Modules
├── .github/workflows/deploy.yml
├── assets/css/custom.css      # テーマカスタム CSS
├── content/
│   ├── ja/                    # 日本語（デフォルト）
│   │   ├── _index.md          # ホームページ
│   │   ├── apps/
│   │   │   ├── _index.md      # アプリ一覧
│   │   │   ├── stillmotion/   # Page Bundle
│   │   │   │   ├── index.md
│   │   │   │   └── images/
│   │   │   └── dayrhythm/
│   │   ├── downloads/
│   │   │   └── stillmotion/
│   │   └── legal/             # privacy, terms
│   └── en/                    # 英語（同一構造）
├── layouts/
│   ├── apps/                  # list.html, single.html
│   ├── downloads/             # list.html, single.html
│   ├── partials/              # app-card, download-button, etc.
│   └── shortcodes/            # app-store-badge, download-table, etc.
├── static/
│   └── images/                # ロゴ、OGP画像
├── releases/                  # GitHub Releases 用バイナリ（git管理外）
│   └── stillmotion-server/
│       └── v1.1/              # バージョンごとのバイナリ
├── i18n/                      # ja.yaml, en.yaml
└── data/apps/                 # アプリメタデータ
```

### 6.3 コンテンツタイプ

#### apps/ - Front Matter

```yaml
app:
  slug: "stillmotion"
  tagline: "画像も動画も、区別なく。"
  icon: "images/app-icon.png"
  platforms: [iOS, iPadOS, macOS, watchOS]
  appStoreUrl: "https://apps.apple.com/app/..."
  status: "released"   # released | coming_soon
  features:
    - title: "機能名"
      description: "説明"
      image: "images/feature1.png"
      imageDark: "images/feature1-dark.png"   # ダークモード用（省略時は image を使用）
```

#### downloads/ - Front Matter

```yaml
download:
  appSlug: "stillmotion"
  releases:
    - version: "1.1"
      githubRelease: "stillmotion-server-v1.1"  # GitHub Releases のタグ名
      files:
        - platform: "macOS (Apple Silicon)"
          filename: "StillMotion-Server-1.1.dmg"
          url: "https://github.com/{owner}/{repo}/releases/download/stillmotion-server-v1.1/StillMotion-Server-1.1.dmg"
          size: "5.9MB"
          note: "推奨。DMGインストーラー"
        - platform: "macOS (Intel)"
          filename: "stillmotion-server-darwin-amd64"
          url: "https://github.com/{owner}/{repo}/releases/download/stillmotion-server-v1.1/stillmotion-server-darwin-amd64"
          size: "7.1MB"
        - platform: "Linux (x86_64)"
          filename: "stillmotion-server-linux-amd64"
          url: "https://github.com/{owner}/{repo}/releases/download/stillmotion-server-v1.1/stillmotion-server-linux-amd64"
          size: "6.9MB"
        - platform: "Linux (ARM64)"
          filename: "stillmotion-server-linux-arm64"
          url: "https://github.com/{owner}/{repo}/releases/download/stillmotion-server-v1.1/stillmotion-server-linux-arm64"
          size: "6.6MB"
        - platform: "Windows (x86_64)"
          filename: "stillmotion-server-windows-amd64.exe"
          url: "https://github.com/{owner}/{repo}/releases/download/stillmotion-server-v1.1/stillmotion-server-windows-amd64.exe"
          size: "7.1MB"
        - platform: "Windows (ARM64)"
          filename: "stillmotion-server-windows-arm64.exe"
          url: "https://github.com/{owner}/{repo}/releases/download/stillmotion-server-v1.1/stillmotion-server-windows-arm64.exe"
          size: "6.6MB"
```

### 6.4 ショートコード

| ショートコード | 用途 |
|--------------|------|
| `app-store-badge` | App Store ダウンロードバッジ |
| `download-table` | ダウンロードファイルテーブル |
| `platform-list` | 対応プラットフォーム一覧 |

### 6.5 バイナリ配布（GitHub Releases）

StillMotion Local Server のバイナリファイルは **GitHub Releases** を通じて配布する。`static/downloads/` にバイナリを配置する方式は採用しない（Git リポジトリの肥大化を防ぐため）。

#### バイナリ管理

- ソースリポジトリ: `../StillMotion/LocalServer/` でビルド（`make all`）
- ビルド成果物を `releases/stillmotion-server/v{VERSION}/` にコピー
- `releases/` ディレクトリは `.gitignore` に追加し、Git 管理対象外とする
- GitHub Releases にアップロードして配布

#### 配布ファイル一覧（v1.1）

| プラットフォーム | ファイル名 | サイズ | 備考 |
|----------------|-----------|--------|------|
| macOS (Apple Silicon) | `StillMotion-Server-1.1.dmg` | 5.9MB | 推奨。DMGインストーラー |
| macOS (Apple Silicon) | `stillmotion-server-darwin-arm64` | 6.7MB | CLI バイナリ |
| macOS (Intel) | `stillmotion-server-darwin-amd64` | 7.1MB | CLI バイナリ |
| Linux (x86_64) | `stillmotion-server-linux-amd64` | 6.9MB | CLI バイナリ |
| Linux (ARM64) | `stillmotion-server-linux-arm64` | 6.6MB | Raspberry Pi 等 |
| Windows (x86_64) | `stillmotion-server-windows-amd64.exe` | 7.1MB | ダブルクリックで起動 |
| Windows (ARM64) | `stillmotion-server-windows-arm64.exe` | 6.6MB | ダブルクリックで起動 |

#### リリース手順

```bash
# 1. StillMotion LocalServer でビルド
cd ../StillMotion/LocalServer
make clean all

# 2. homepage リポジトリにコピー
cp build/* ../homepage/releases/stillmotion-server/v1.1/

# 3. GitHub Release を作成しバイナリをアップロード
gh release create stillmotion-server-v1.1 \
  --title "StillMotion Server v1.1" \
  --notes "StillMotion Local Server v1.1" \
  releases/stillmotion-server/v1.1/*
```

#### ダウンロード URL 形式

```
https://github.com/{owner}/{repo}/releases/download/stillmotion-server-v{VERSION}/{filename}
```

ダウンロードページの Hugo テンプレートでは、Front Matter の `download.releases[].files[].url` に上記 URL を設定し、直接 GitHub Releases からダウンロードさせる。

#### タグ命名規則

- `stillmotion-server-v{VERSION}` （例: `stillmotion-server-v1.1`）
- アプリ本体の App Store リリースとは独立したバージョニング

### 6.6 Hugo 設定概要（hugo.toml）

- テーマ: Blowfish（Hugo Modules 経由）
- デフォルト言語: `ja`、`hasCJKLanguage = true`
- ダークモード: `autoSwitchAppearance = true`
- ビルド: `minifyOutput = true`、`enableRobotsTXT = true`
- メニュー: Apps / Downloads / About（言語別）

完全な設定は [hugo_technical_architecture.md](./hugo_technical_architecture.md) セクション4を参照。

---

## 7. DevOps・パフォーマンス

> 詳細: [devops_performance_design.md](./devops_performance_design.md)

### 7.1 GitHub Actions デプロイ

- **トリガー**: main ブランチ push + 手動 `workflow_dispatch`
- **環境**: Hugo Extended + Go + Node.js
- **キャッシュ**: Hugo モジュール / npm / ビルドキャッシュの3層
- **タイムゾーン**: `TZ=Asia/Tokyo`

### 7.2 ドメイン

- **カスタムドメイン推奨**（会社ブランディングに必要）
- 個人ブログ（frkake.com）とは別ドメイン
- HTTPS 自動（Let's Encrypt、GitHub Pages 標準）

### 7.3 画像最適化

- Hugo Pipes による **WebP 自動変換** + PNG フォールバック
- レスポンシブ画像（320/640/960/1280px）`srcset` 生成
- `assets/` に配置して Hugo Pipes で処理

| 用途 | サイズ | フォーマット |
|------|--------|-------------|
| ヒーロー | 512px | WebP + PNG |
| カード | 256px | WebP + PNG |
| OGP | 1200x630 | PNG |
| favicon | 32px, 180px | ICO, PNG |

**ダーク/ライトモード画像切り替え**:
- アプリのスクリーンショット・機能紹介画像は、ライト版とダーク版の2バリエーションを用意
- 命名規則: `{name}.png`（ライト版） / `{name}-dark.png`（ダーク版）
- `<picture>` 要素 + `prefers-color-scheme` メディアクエリで切り替え（JS不要、CSSのみ）
- Hugo テンプレート/ショートコードで自動処理し、コンテンツ作成者の負担を最小化

### 7.4 パフォーマンス目標

| 指標 | 目標値 |
|------|--------|
| LCP | < 1.5s |
| INP | < 100ms |
| CLS | < 0.05 |
| Lighthouse 全カテゴリ | 95+ |
| Lighthouse SEO | 100 |

### 7.5 SEO 技術要件

- `sitemap.xml` 自動生成
- `robots.txt` テンプレート
- OGP メタタグ + Twitter Card
- JSON-LD 構造化データ（Organization, SoftwareApplication, BreadcrumbList）
- canonical URL
- hreflang（多言語対応）

### 7.6 デザイン品質検証

実装がデザイン仕様に忠実であること、そしてビジュアルとして完璧であることを保証する仕組み。
構文の正しさではなく、**見た目の正しさ**を検証の中心に据える。

#### 検証の哲学

- 「HTMLとして正しいか」ではなく「**デザインとして完璧か**」を問う
- デザイントークン（カラー、タイポグラフィ、スペーシング）が仕様通りに適用されているかを機械的に検証する
- 人間の目による最終レビューを省略しない

#### 1. デザイントークン検証（Playwright）

CSS の算出値がデザイン仕様（セクション 4 で定義）に一致するかを自動テストする。

| 検証項目 | 検証内容 |
|----------|---------|
| カラーパレット | 背景色・文字色・ブランドカラー・アクセントカラーが仕様値と一致 |
| ダークモード切替 | ライト/ダーク各モードで全カラートークンが正しく反映 |
| タイポグラフィ | フォントファミリー・ウェイト・サイズが各レベル（Display〜Body）で仕様通り |
| スペーシング | セクション間余白・コンテンツ幅・ヒーロー余白が 8px ベースの設計と一致 |
| 角丸 | カード (8px)・ボタン (4px)・チップ (2px) の border-radius が統一されている |
| コントラスト比 | テキスト/背景のコントラスト比が WCAG 2.1 AA（4.5:1 以上）を満たす |

#### 2. レイアウト構造検証（Playwright）

要素の配置・サイズ・間隔を数値で検証する。

| 検証項目 | 検証内容 |
|----------|---------|
| グリッド | コンテンツ最大幅 1200px、本文幅 720px を超えていない |
| レスポンシブ | 各ブレークポイント（375px / 768px / 1280px）でレイアウト崩れがない |
| 要素重なり | 要素同士がオーバーラップしていない |
| CTA配置 | App Store バッジがページ上部・下部の指定位置に存在する |
| ナビゲーション | ヘッダー項目数・フッター3カラム構造が仕様通り |

#### 3. ビジュアルリグレッションテスト（Playwright スクリーンショット比較）

ベースライン画像との差分を検出し、意図しないデザイン変更を防ぐ。

- **検証マトリクス**:

| 条件 | バリエーション |
|------|--------------|
| 表示モード | ライトモード / ダークモード |
| ビューポート | モバイル (375px) / タブレット (768px) / デスクトップ (1280px) |
| 言語 | 日本語 / 英語 |

- 差分が閾値（ピクセル差 0.1% 以上）を超えた場合、PR にスクリーンショットの差分画像を添付
- ベースライン画像の初回承認は**人間のデザインレビュー**を必須とする
- ベースライン更新時も PR レビューでスクリーンショットの変更意図を明記

#### 4. デザインレビュープロセス

自動テストでは捕捉できない「全体の美しさ・バランス・余白のリズム」を人間が確認する。

- **新規ページ追加時**: 全ビューポート × 全カラースキームのスクリーンショットを PR に添付し、レビュー
- **デザイン変更時**: Before / After のスクリーンショットを比較し、レビュー
- **判断基準**: セクション 2.5 の問い（「取り除いても伝わるか？」「3秒で目的を理解できるか？」）を適用

#### 検証対象ページ

| ページ | パス |
|--------|------|
| トップ | `/` |
| StillMotion 詳細 | `/apps/stillmotion/` |
| DayRhythm | `/apps/dayrhythm/` |
| ダウンロード | `/downloads/stillmotion/` |
| プライバシーポリシー | `/legal/privacy/` |
| お問い合わせ | `/contact/` |

### 7.7 分析ツール

- **GA4**（推奨）- App Store マーケティングとの統合、無料
- **Google Search Console** - 検索パフォーマンス
- production 環境のみでトラッキング読み込み

---

## 8. 実装優先順位

| 優先度 | タスク | 内容 |
|--------|--------|------|
| **P0** | プロジェクト初期化 | Hugo init, Blowfish テーマ導入, hugo.toml 設定 |
| **P0** | StillMotion ページ | apps/stillmotion のコンテンツとカスタムレイアウト |
| **P0** | ダウンロードページ | downloads/stillmotion のコンテンツとレイアウト |
| **P0** | GitHub Actions | デプロイパイプライン構築 |
| **P1** | トップページ | カスタムホームレイアウト（Hero + Featured Apps） |
| **P1** | ダークモード調整 | カラースキーム・CSS Custom Properties カスタマイズ |
| **P1** | 多言語対応 | 英語コンテンツ追加 |
| **P2** | 会社概要ページ | about/ コンテンツ |
| **P2** | 法的ページ | privacy/, terms/ コンテンツ |
| **P2** | お問い合わせ | contact/ ページ（mailto: リンク） |
| **P2** | デザイン検証CI | Lighthouse CI + Playwright ビジュアルリグレッションテスト導入 |
| **P3** | DayRhythm ページ | 開発完了後に Coming Soon → 詳細に切替 |
| **P3** | コンテンツ拡張 | ブログ、FAQ、スクリーンショットギャラリー |

---

## 9. 参照ドキュメント

| ドキュメント | 担当 | 内容 |
|------------|------|------|
| [creative_direction.md](./creative_direction.md) | Creative Director | コンセプト・ブランドメッセージ・トーン&マナー |
| [ui_ux_design.md](./ui_ux_design.md) | UI/UX Designer | サイトマップ・ページ構成・ナビゲーション・CTA |
| [visual-identity.md](./visual-identity.md) | Visual Designer | カラーパレット・タイポグラフィ・デザイントークン |
| [hugo_technical_architecture.md](./hugo_technical_architecture.md) | Hugo Developer | テーマ選定・ディレクトリ構成・設定・CI/CD |
| [content_strategy.md](./content_strategy.md) | Content Strategist | コピーライティング・SEO・多言語方針 |
| [devops_performance_design.md](./devops_performance_design.md) | DevOps Engineer | デプロイ・画像最適化・パフォーマンス・SEO技術 |

### アプリ参照資料

| 資料 | パス |
|------|------|
| StillMotion 機能詳細 | `../StillMotion/docs/features.md` |
| StillMotion App Store説明 | `../StillMotion/docs/apple_store_description.md` |
| StillMotion 販売計画 | `../StillMotion/docs/sales_plan.md` |
| StillMotion ローカルサーバー | `../StillMotion/LocalServer/README.md` |
| StillMotion アイコン | `assets/images/apps/stillmotion/` |
| DayRhythm 要件 | `../DayRhythmProject/docs/v2/requirements.md` |
| DayRhythm アイコン | `assets/images/apps/dayrhythm/` |
| 個人ブログ設定 | `../frkake.github.io/hugo.toml` |
