# Visual Identity Guide - iidatakumi Homepage

## 1. アイコン分析

### StillMotion
- **モチーフ**: 角丸の画面フレーム内に「山」のシルエットと「再生ボタン」を組み合わせた構成。写真（静止画・山）と動画（再生ボタン）の融合を表現。
- **ライトモード**: 柔らかいブルーグラデーション背景（#6EB3E6 〜 #A8D4F0）。フレームは白、山はソフトブルー、再生ボタンはシアン/ターコイズ（#4DD9C0）。清潔感と信頼感。
- **ダークモード**: 深いネイビー背景（#1A2E4A 〜 #2D4A6E）。同じモチーフをやや明るいブルー系で表現。暗所での視認性を確保。
- **Tinted（モノクロ）**: 黒背景に白のラインアート。山と再生ボタンがアウトラインで描かれ、ミニマルな印象。
- **デザイン特徴**: 幾何学的、クリーンなライン、角丸のフレーム。プロフェッショナルかつ親しみやすい。

### DayRhythm
- **モチーフ**: 螺旋（スパイラル/渦巻き）形状。一日のリズム・サイクル・流れを有機的な曲線で表現。
- **ライトモード**: ミント/ターコイズ背景（#78CCBE）に白いスパイラル。穏やかさと活力の共存。
- **ダークモード**: ダークチャコール背景（#3A3A3C）に白いスパイラル。落ち着きと集中。
- **Tinted（カラー）**: ダーク背景にブルー→グリーンのグラデーションスパイラル。アプリの時間帯カラー（朝=オレンジ、昼=グリーン、夜=パープル）を示唆。
- **デザイン特徴**: 有機的曲線、流動的、手描き感のあるストローク。人間的で温かみがある。

### 共通分析
- 両アプリとも「白いモチーフ on カラー背景」というパターンを共有
- シンプルな単一モチーフでアプリの本質を表現するミニマルアプローチ
- ライト/ダーク両対応の設計思想が一貫

---

## 2. カラーパレット

### 2.1 サイト共通カラー

#### プライマリカラー
サイト全体の基調色。両アプリのアイコンから抽出した「信頼・清潔・静謐」の印象を統合。

| 役割 | ライトモード | ダークモード | 用途 |
|------|-------------|-------------|------|
| Background Primary | `#FAFAFA` | `#121212` | ページ背景 |
| Background Secondary | `#FFFFFF` | `#1E1E1E` | カード・セクション背景 |
| Background Tertiary | `#F5F5F5` | `#2A2A2A` | コードブロック・引用背景 |
| Text Primary | `#1A1A1A` | `#F0F0F0` | 見出し・本文 |
| Text Secondary | `#6B6B6B` | `#A0A0A0` | 補足テキスト・キャプション |
| Text Tertiary | `#999999` | `#707070` | プレースホルダー・無効テキスト |
| Border | `#E5E5E5` | `#333333` | 区切り線・カード枠 |
| Border Subtle | `#F0F0F0` | `#252525` | 微細な区切り |

#### セカンダリカラー（ブランドカラー）
両アプリアイコンの青系統を統合した、サイトのブランドアイデンティティ。

| 名前 | 値 | 用途 |
|------|-----|------|
| Brand | `#4A9ECC` | リンク、CTAボタン、アクティブ状態 |
| Brand Hover | `#3A8BBB` | ホバー状態 |
| Brand Light | `#E8F4FA` | ライトモード：ハイライト背景 |
| Brand Dark | `#1A3A50` | ダークモード：ハイライト背景 |

#### アクセントカラー
控えめに使用し、重要な要素を際立たせる。

| 名前 | 値 | 用途 |
|------|-----|------|
| Accent | `#4DD9C0` | StillMotionの再生ボタン由来。成功状態、ポジティブ表示 |
| Warning | `#E8A44A` | 注意・警告 |
| Error | `#D45B5B` | エラー表示 |

### 2.2 アプリ固有カラーアクセント

#### StillMotion
| 名前 | 値 | 用途 |
|------|-----|------|
| SM Primary | `#4A9ECC` | メインブルー（アイコン背景由来） |
| SM Accent | `#4DD9C0` | シアン/ターコイズ（再生ボタン由来） |
| SM Gradient Start | `#6EB3E6` | グラデーション開始 |
| SM Gradient End | `#A8D4F0` | グラデーション終了 |
| SM Dark BG | `#1A2E4A` | ダークモード固有背景 |

#### DayRhythm
| 名前 | 値 | 用途 |
|------|-----|------|
| DR Primary | `#78CCBE` | メインミント（アイコン背景由来） |
| DR Morning | `#F0A050` | 朝のオレンジ |
| DR Afternoon | `#5EBB78` | 昼のグリーン |
| DR Night | `#8B6BB5` | 夜のパープル |
| DR Dark BG | `#3A3A3C` | ダークモード固有背景 |

### 2.3 CSS Custom Properties 定義

```css
:root {
  /* サイト共通 */
  --color-bg-primary: #FAFAFA;
  --color-bg-secondary: #FFFFFF;
  --color-bg-tertiary: #F5F5F5;
  --color-text-primary: #1A1A1A;
  --color-text-secondary: #6B6B6B;
  --color-text-tertiary: #999999;
  --color-border: #E5E5E5;
  --color-border-subtle: #F0F0F0;
  --color-brand: #4A9ECC;
  --color-brand-hover: #3A8BBB;
  --color-brand-bg: #E8F4FA;
  --color-accent: #4DD9C0;

  /* StillMotion */
  --color-sm-primary: #4A9ECC;
  --color-sm-accent: #4DD9C0;
  --color-sm-gradient-start: #6EB3E6;
  --color-sm-gradient-end: #A8D4F0;

  /* DayRhythm */
  --color-dr-primary: #78CCBE;
  --color-dr-morning: #F0A050;
  --color-dr-afternoon: #5EBB78;
  --color-dr-night: #8B6BB5;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-bg-primary: #121212;
    --color-bg-secondary: #1E1E1E;
    --color-bg-tertiary: #2A2A2A;
    --color-text-primary: #F0F0F0;
    --color-text-secondary: #A0A0A0;
    --color-text-tertiary: #707070;
    --color-border: #333333;
    --color-border-subtle: #252525;
    --color-brand: #5AAEDC;
    --color-brand-hover: #6ABEEC;
    --color-brand-bg: #1A3A50;
    --color-accent: #5DE9D0;

    --color-sm-primary: #5AAEDC;
    --color-sm-accent: #5DE9D0;
    --color-sm-gradient-start: #3A8BBB;
    --color-sm-gradient-end: #5AAEDC;

    --color-dr-primary: #88DCCE;
    --color-dr-morning: #FFBA6A;
    --color-dr-afternoon: #6ECB88;
    --color-dr-night: #9B7BC5;
  }
}
```

---

## 3. タイポグラフィ

### 3.1 フォントスタック

#### 見出し（Headings）
```css
--font-heading: "Inter", "Noto Sans JP", -apple-system, BlinkMacSystemFont, sans-serif;
```
- **Inter**: 幾何学的で洗練されたサンセリフ。StillMotionのクリーンなラインと親和性が高い。Google Fonts で無料利用可。
- **Noto Sans JP**: 日本語の見出しに使用。Interとのウェイトバランスが良好。

#### 本文（Body）
```css
--font-body: "Inter", "Noto Sans JP", -apple-system, BlinkMacSystemFont, sans-serif;
```
- 見出しと同一ファミリーで統一感を維持。ウェイトで差別化。

#### UIテキスト / コード
```css
--font-mono: "JetBrains Mono", "SF Mono", "Fira Code", monospace;
```
- 開発者ポートフォリオとしての技術的信頼感を演出。

### 3.2 タイプスケール

モジュラースケール比率: **1.250**（Major Third）。ミニマルで均整の取れたスケール。

| レベル | サイズ (rem) | ウェイト | 行間 | 用途 |
|--------|-------------|---------|------|------|
| Display | 3.052 | 700 | 1.1 | ヒーローセクション見出し |
| H1 | 2.441 | 700 | 1.2 | ページタイトル |
| H2 | 1.953 | 600 | 1.25 | セクション見出し |
| H3 | 1.563 | 600 | 1.3 | サブセクション |
| H4 | 1.25 | 500 | 1.35 | カード見出し |
| Body Large | 1.125 | 400 | 1.6 | リード文 |
| Body | 1.0 | 400 | 1.7 | 本文（16px基準） |
| Body Small | 0.875 | 400 | 1.6 | 補足テキスト |
| Caption | 0.75 | 400 | 1.5 | キャプション・注釈 |

### 3.3 フォントウェイト

| ウェイト | 値 | 用途 |
|---------|-----|------|
| Regular | 400 | 本文 |
| Medium | 500 | 小見出し、強調テキスト |
| Semibold | 600 | セクション見出し |
| Bold | 700 | ページ見出し、CTA |

### 3.4 レターススペーシング

| 要素 | letter-spacing |
|------|---------------|
| Display / H1 | -0.02em |
| H2 / H3 | -0.01em |
| Body | 0em |
| Caption | 0.02em |
| 日本語全般 | 0.04em |

---

## 4. 余白・グリッドシステム

### 4.1 スペーシングスケール

8pxベースのスペーシングシステム。ミニマルデザインでは十分な余白が重要。

| トークン | 値 | 用途 |
|---------|-----|------|
| `--space-1` | 4px | アイコンとラベルの間隔 |
| `--space-2` | 8px | インライン要素間 |
| `--space-3` | 12px | 密接な要素間 |
| `--space-4` | 16px | リスト項目間 |
| `--space-5` | 24px | カード内パディング |
| `--space-6` | 32px | セクション内要素間 |
| `--space-7` | 48px | セクション間（小） |
| `--space-8` | 64px | セクション間（中） |
| `--space-9` | 96px | セクション間（大） |
| `--space-10` | 128px | ヒーロー前後の余白 |

### 4.2 グリッドシステム

```
最大コンテンツ幅: 1200px
コンテンツ幅（本文）: 720px
カラム数: 12
ガター: 24px
左右マージン: 24px (mobile) / 48px (tablet) / auto (desktop)
```

#### ブレイクポイント

| 名前 | 値 | カラム |
|------|-----|--------|
| Mobile | < 640px | 4 |
| Tablet | 640px - 1024px | 8 |
| Desktop | > 1024px | 12 |

### 4.3 セクションレイアウト方針

- **ヒーローセクション**: 全幅、最大限の余白（`--space-10`）
- **アプリ紹介セクション**: コンテンツ幅内、左右対称のカード配置
- **テキストセクション**: 720px幅、読みやすさを最優先
- **フッター**: 全幅、控えめなスペーシング

---

## 5. ビジュアルエレメント

### 5.1 アプリアイコンの使用ガイドライン

- **推奨サイズ**: 64px, 96px, 128px（Webでの表示用）
- **角丸**: iOS準拠の `border-radius: 22.37%`（連続角丸）、CSS近似では `border-radius: 22%` を使用
- **余白**: アイコン周囲に最低アイコンサイズの25%の余白を確保
- **背景**: アイコンを単色背景に置く場合、アイコン色と背景色のコントラスト比 4.5:1 以上を確保

### 5.2 装飾要素の方針

「Less is More」の原則に従い、装飾要素は最小限にする。

- **区切り線**: 1px、`--color-border` 使用。使用は最小限に
- **カード**: `border: 1px solid var(--color-border)` または `box-shadow` のいずれか（併用しない）
- **角丸**: 統一して `8px`（カード）, `4px`（ボタン・入力欄）, `2px`（チップ・バッジ）
- **シャドウ**: ライトモードのみ、微細に使用
  - Small: `0 1px 3px rgba(0, 0, 0, 0.06)`
  - Medium: `0 4px 12px rgba(0, 0, 0, 0.08)`
  - ダークモードではシャドウ不使用、border で代替

### 5.3 スクリーンショット・写真

- **アプリスクリーンショット**: デバイスフレーム内に表示。フレームはミニマルなワイヤーフレーム風
- **画像の角丸**: `8px`（カードと同じ）
- **画像比率**: 16:9（横長）または 9:19.5（iPhone風縦長）
- **フィルター**: なし。アプリ画面はありのままを表示

### 5.4 アイコン（UI）

- **スタイル**: ラインアイコン、ストローク幅 1.5px
- **サイズ**: 20px (default), 16px (small), 24px (large)
- **ライブラリ推奨**: Lucide Icons（軽量、ミニマル、MITライセンス）
- **カラー**: `currentColor` を使用し、テキストカラーに追従

---

## 6. アニメーション・トランジション

### 6.1 基本方針

「気づかないほど自然な動き」を目指す。過度なアニメーションはミニマルの本質に反する。

### 6.2 イージング関数

```css
--ease-out: cubic-bezier(0.22, 1, 0.36, 1);    /* 主要トランジション */
--ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);  /* 対称的な動き */
--ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1); /* 控えめなバウンス（特殊用途のみ） */
```

### 6.3 デュレーション

| トークン | 値 | 用途 |
|---------|-----|------|
| `--duration-fast` | 120ms | ホバー、フォーカス、色変化 |
| `--duration-normal` | 200ms | 展開、トグル、フェード |
| `--duration-slow` | 350ms | ページ遷移、モーダル開閉 |

### 6.4 トランジション定義

```css
/* ホバー・インタラクション */
--transition-color: color var(--duration-fast) var(--ease-out);
--transition-bg: background-color var(--duration-fast) var(--ease-out);
--transition-opacity: opacity var(--duration-normal) var(--ease-out);
--transition-transform: transform var(--duration-normal) var(--ease-out);
```

### 6.5 スクロールアニメーション

- **ファーストビュー**: コンテンツは即座に表示。遅延ローディングアニメーションは不使用
- **スクロール連動**: `fade-in-up` のみ使用可。移動量は `12px` 以下、duration は `350ms`
- **`prefers-reduced-motion`**: すべてのアニメーションを無効化する対応を必須とする

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### 6.6 ページ遷移

- Hugo の標準ページ遷移（フルリロード）を基本とする
- 必要に応じて View Transitions API を検討（ブラウザサポート考慮）
- 遷移時は `opacity` のフェードのみ。スライドやズームは不使用

### 6.7 ダークモード切替

- `prefers-color-scheme` に追従（手動トグル不要、システム設定に委任）
- CSS Custom Properties による即座の切替（トランジション不要）

---

## 付録: デザイントークンまとめ

```css
:root {
  /* Colors - documented above */

  /* Typography */
  --font-heading: "Inter", "Noto Sans JP", -apple-system, BlinkMacSystemFont, sans-serif;
  --font-body: "Inter", "Noto Sans JP", -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: "JetBrains Mono", "SF Mono", "Fira Code", monospace;

  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-5: 1.5rem;
  --space-6: 2rem;
  --space-7: 3rem;
  --space-8: 4rem;
  --space-9: 6rem;
  --space-10: 8rem;

  /* Borders */
  --radius-sm: 2px;
  --radius-md: 4px;
  --radius-lg: 8px;
  --radius-icon: 22%;

  /* Shadows (light mode only) */
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);

  /* Animation */
  --ease-out: cubic-bezier(0.22, 1, 0.36, 1);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
  --duration-fast: 120ms;
  --duration-normal: 200ms;
  --duration-slow: 350ms;

  /* Layout */
  --content-max: 1200px;
  --content-text: 720px;
  --grid-gutter: 1.5rem;
}
```
