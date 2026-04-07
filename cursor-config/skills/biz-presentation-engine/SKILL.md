---
name: biz-presentation-engine
description: 法人向けHTMLプレゼンスライドの実装エンジン。Claude Codeから指示書（アウトライン＋テンプレート指定＋カラー＋コンテンツ）を受け取り、単一HTMLファイルとして実装する。43種テンプレート＋14種アニメーション。トリガー：プレゼン実装、スライドHTML生成、提案資料コーディング。
---

# Biz Presentation Engine — HTMLスライド実装エンジン

> Claude Codeからの指示書に従い、法��向け提案資料を単一HTMLファイルとして実装する。
> このスキルは**実装専門**。企画・構成設計はClaude Code側が担当する。

## 入力フォーマット

Claude Codeから以下の指示書を受け取る:

```
## 指示書
- タイトル: {プレゼンタイトル}
- ファイル名: {output.html}
- カラー: primary={#hex}, accent={#hex} (または「デフォルト青」)
- ロゴ/会社名: {テキスト}

## スライド構成
1. [cover-title] テーマ:dark-blue — タイトル「...」サブ「...」バッジ3つ
2. [contents] テーマ:blue — 目次5項目
3. [section-divider] テーマ:blue — 01 わたし達について
4. [profile] テーマ:light — 名前「...」肩書き「...」
...
```

## 実装ルール

### 必須要件
1. **単一HTMLファイル**で完結（Google Fonts CDN・Unsplash画像URLのみ外部依存可）
2. **横スクロールデッキ**形式。キーボード(←→)、クリック、タッチスワイプ対応
3. 全スライドに `data-theme` 属性 + `data-slide-title` 属性でテーマ・タイトル指定
4. `F`キーでフルスクリーン切替
5. プログレスバー（上部）＋スライドカウンター（右下）
6. **アジェンダメニュー**（左上☰ボタン→サイドパネル→クリックでスライド遷移）

### 画像・図解ルール

**Unsplash API で画像取得（推奨）:**
指示書で画像が必要な箇所には、Unsplash APIで適切なキーワードの画像URLを取得してimgタグに埋め込む。

```bash
# ステップ1: キーワード検索して画像情報を取得
curl -s "https://api.unsplash.com/search/photos?query=KEYWORD&per_page=1&orientation=landscape" \
  -H "Authorization: Client-ID <YOUR_UNSPLASH_ACCESS_KEY>" \
  | python3 -c "
import sys,json
r=json.load(sys.stdin)
if r['results']:
    p=r['results'][0]
    print('URL:', p['urls']['regular'])
    print('DOWNLOAD:', p['links']['download_location'])
    print('PHOTOGRAPHER:', p['user']['name'])
    print('PROFILE:', p['user']['links']['html'])
"

# ステップ2: download endpointを必ず叩く（Unsplashガイドライン必須）
curl -s "DOWNLOAD_LOCATION_URL" \
  -H "Authorization: Client-ID <YOUR_UNSPLASH_ACCESS_KEY>" > /dev/null
```

**Unsplashガイドライン準拠（必須）:**
1. **ホットリンク**: 画像URLはUnsplashのURLをそのまま使う（ダウンロードして埋め込まない）
2. **download endpoint**: 画像をスライドに使用する際、必ず `download_location` URLにリクエストを送る
3. **クレジット表示**: 画像を使った箇所に以下のクレジットを必ず表示する
   ```html
   <p class="unsplash-credit">
     Photo by <a href="PROFILE_URL?utm_source=ax_slides&utm_medium=referral" target="_blank">PHOTOGRAPHER_NAME</a>
     on <a href="https://unsplash.com?utm_source=ax_slides&utm_medium=referral" target="_blank">Unsplash</a>
   </p>
   ```
4. **クレジットCSS**:
   ```css
   .unsplash-credit { font-size: 10px; color: rgba(255,255,255,0.5); position: absolute; bottom: 8px; right: 12px; }
   .unsplash-credit a { color: inherit; text-decoration: underline; }
   ```
   ※白背景スライドの場合は `color: rgba(0,0,0,0.3)` に

- キーワード例: ビジネス→"business meeting", テック→"technology abstract", データ→"data analytics dashboard"
- 表紙、自己紹介、Before/After、実績ページなど写真が映えるスライドで使用
- テーブルや図解メインのスライドでは不要
- Unsplashのブランディング（ロゴ等）はスライド内に使用しない

**SVG図解を積極使用:**
- テキストだけのスライドにせず、SVGで図解・フロー・ダイアグラムを積極的に作成する
- ハブ&スポーク、フロー図、ピラミッド、サイクル図等は全てSVGで描画
- 背景装飾（ワイヤーフレーム球体、立方体、幾何学パターン）もSVGで
- SVGアニメーション（@keyframes回転、stroke-dasharray描画等）で動きをつける

### カラーシステム（デフォルト: コーポレートブルー）

指示書でカラー指定がある場合は `:root` の値を差し替える。

```css
:root {
  --c-primary: #3B82B6;
  --c-primary-dark: #1E5A8A;
  --c-primary-light: #E8F4F8;
  --c-grad-start: #5B9BD5;
  --c-grad-end: #8EC5E8;
  --c-accent: #F5A623;
  --c-accent-dark: #E8941A;
  --c-white: #FFFFFF;
  --c-text: #1A1A2E;
  --c-text-muted: #6B7280;
  --c-border: #E5E7EB;
  --c-bg: #F8FAFC;
  --c-success: #10B981;
  --c-danger: #EF4444;
}
```

### テーマバリエーション（6種）

| data-theme | 背景 | テキスト | 用途 |
|------------|------|---------|------|
| `white` | #FFFFFF | #1A1A2E | コンテンツ主体 |
| `light` | #F8FAFC | #1A1A2E | データ・図解 |
| `blue` | linear-gradient(135deg, grad-start, grad-end) | #FFFFFF | セクション区切り、目次 |
| `dark-blue` | linear-gradient(135deg, #1E3A5F, #2C5F8A) | #FFFFFF | 表紙、インパクト |
| `accent` | var(--c-accent) | #FFFFFF | CTA、強調 |
| `accent-light` | linear-gradient(135deg, #F5C563, #F5A623) | #FFFFFF | インパクトメッセージ |

### 禁止事項（法人提案資料）
- ダーク（黒背景）テーマは使わない。白ベース基本
- 蛍光色やネオンカラー禁止
- パーティクルやグリッド背景禁止（ビジネスに不適切）
- 英語だけの見出し禁止（日本語ファースト）
- フォントサイズ14px未満禁止
- 全スライド同一テーマ禁止（テーマを交互に使う）
- テキストだけのスライド3枚以上連続禁止
- **自社の内部メモ・戦略的示唆を先方向けスライドに含めない**（例：「○○社への示唆」「こちらの狙い」等は絶対NG）
- **ネガティブ表現を避ける**。先方の課題を指摘する際はポジティブに言い換える（例：「意思決定が遅い」→「より迅速な意思決定を実現」、「人材不足」→「AI活用の定着がこれから」）
- **見出しはセールスライティングを意識**。機能説明ではなくベネフィット訴求型にする（例：「技術ケイパビリティ」→「なぜ"使える"AIが作れるのか」）

### デザインバランスルール（★必読）
- **カード型レイアウトを3枚以上連続させない**。テーブル、バーチャート、フロー図、Before/After等を挟んでバリエーションを出す
- **two-colで左右の高さが揃わない場合**: align-items: start にして上揃えにする。中央揃え(center)にすると片方が浮く
- **見出し(slide-title)は全スライドで同一font-sizeに統一**。インラインstyleで個別に上書き禁止
- **見出しは日本語15文字以内**。2行に折れる見出しは必ず短縮し、詳細はsubtitleに移す
- **slide-titleとslide-subtitleのサイズに明確な差をつける**。titleはvar(--size-h2)、subtitleはvar(--size-body)
- **section-label（左上）と見出しの間に十分な余白**を確保。padding-top: clamp(80px,10vh,100px)
- **four-colのカード内テキストは短く**。改行で崩れるなら文字を減らす。word-break: keep-allを適用
- **テーブルヘッダーのテキストは1行で収まる長さに**。列幅%を明示指定する
- **43種のテンプレートを積極的に使い分ける**。bento-grid、problem-solution、hub-and-spoke、funnel等を混ぜてビジュアルの単調さを防ぐ

### テーマの流れ推��パターン
```
表紙(white/dark-blue) → 目次(blue) → 区切り(blue) → コンテンツ(white) →
コンテンツ(light) → 区切り(blue) → 比較(white) → インパクト(accent) →
データ(light) → 区切り(blue) → サービス(blue) → 料金(light) → 締め(dark-blue)
```

---

## HTML基本構造

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>プレゼンタイトル</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700;900&family=Inter:wght@300;400;600;700;900&display=swap" rel="stylesheet">
  <style>/* 全CSS */</style>
</head>
<body>
  <div class="progress-bar"><div class="progress-fill"></div></div>
  <div class="slide-counter"><span class="current-num">1</span> / <span class="total-num">20</span></div>
  <!-- アジェンダメニュー（左上ハンバーガー） -->
  <button class="agenda-toggle" aria-label="アジェンダ">☰</button>
  <nav class="agenda-panel" id="agendaPanel">
    <button class="agenda-close" aria-label="閉じる">✕</button>
    <h3 class="agenda-panel-title">AGENDA</h3>
    <ul class="agenda-list" id="agendaList">
      <!-- JSで自動生成: 各スライドのdata-slide-titleからリスト生成 -->
    </ul>
  </nav>
  <div class="agenda-overlay" id="agendaOverlay"></div>
  <button class="nav-btn nav-prev">&lsaquo;</button>
  <button class="nav-btn nav-next">&rsaquo;</button>
  <div class="deck">
    <section class="slide" data-theme="dark-blue" data-slide-title="表紙">...</section>
    <section class="slide" data-theme="blue" data-slide-title="目次">...</section>
    <!-- 各スライドに data-slide-title 属性を必ず付ける -->
  </div>
  <script>/* 全JS */</script>
</body>
</html>
```

---

## CSS基盤（必須実装）

```css
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

:root {
  --font-heading: 'Inter', 'Noto Sans JP', sans-serif;
  --font-body: 'Noto Sans JP', 'Inter', sans-serif;
  --font-mono: 'Inter', monospace;
  --size-display: clamp(42px, 5vw, 80px);
  --size-h1: clamp(32px, 3.5vw, 56px);
  --size-h2: clamp(24px, 2.5vw, 40px);
  --size-h3: clamp(18px, 1.6vw, 26px);
  --size-body: clamp(15px, 1.3vw, 20px);
  --size-small: clamp(12px, 1vw, 16px);
  --size-label: clamp(10px, 0.8vw, 13px);
  --slide-padding: clamp(40px, 5vw, 80px);
  --gap: clamp(20px, 2.5vw, 40px);
  --gap-sm: clamp(8px, 1vw, 16px);
  --gap-xs: clamp(4px, 0.5vw, 8px);
  /* カラーは上記カラーシステム参照 */
  --c-primary: #3B82B6;
  --c-primary-dark: #1E5A8A;
  --c-primary-light: #E8F4F8;
  --c-grad-start: #5B9BD5;
  --c-grad-end: #8EC5E8;
  --c-accent: #F5A623;
  --c-accent-dark: #E8941A;
  --c-white: #FFFFFF;
  --c-text: #1A1A2E;
  --c-text-muted: #6B7280;
  --c-border: #E5E7EB;
  --c-bg: #F8FAFC;
  --c-success: #10B981;
  --c-danger: #EF4444;
  --shadow-card: 0 2px 12px rgba(0,0,0,0.08);
  --shadow-card-hover: 0 8px 30px rgba(0,0,0,0.12);
  --shadow-elevated: 0 4px 20px rgba(0,0,0,0.1);
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;
}

html { overflow: hidden; }
body {
  font-family: var(--font-body);
  background: var(--c-bg);
  color: var(--c-text);
  overflow: hidden;
  height: 100vh; width: 100vw;
  line-height: 1.7;
  -webkit-font-smoothing: antialiased;
}

.deck { display: flex; width: max-content; height: 100vh; transition: transform 0.7s cubic-bezier(0.25, 0.46, 0.45, 0.94); }
.slide { width: 100vw; height: 100vh; flex-shrink: 0; display: flex; flex-direction: column; justify-content: center; padding: var(--slide-padding); position: relative; overflow: hidden; }

/* プログレスバー */
.progress-bar { position: fixed; top: 0; left: 0; width: 100%; height: 3px; background: rgba(0,0,0,0.05); z-index: 100; }
.progress-fill { height: 100%; background: var(--c-primary); transition: width 0.5s ease; width: 0%; }

/* スライドカウンター */
.slide-counter { position: fixed; bottom: 24px; right: 32px; font-family: var(--font-mono); font-size: var(--size-small); color: var(--c-text-muted); z-index: 100; background: rgba(255,255,255,0.9); padding: 4px 12px; border-radius: var(--radius-sm); }

/* アジェンダメニュー */
.agenda-toggle { position: fixed; top: 16px; left: 16px; width: 40px; height: 40px; border-radius: var(--radius-sm); background: rgba(255,255,255,0.9); border: 1px solid var(--c-border); font-size: 20px; cursor: pointer; z-index: 200; color: var(--c-text); display: flex; align-items: center; justify-content: center; box-shadow: var(--shadow-card); transition: all 0.3s; }
.agenda-toggle:hover { background: var(--c-primary); color: #fff; }
.agenda-panel { position: fixed; top: 0; left: -360px; width: 340px; height: 100vh; background: #fff; box-shadow: 4px 0 24px rgba(0,0,0,0.12); z-index: 300; padding: 24px; overflow-y: auto; transition: left 0.35s cubic-bezier(0.25,0.46,0.45,0.94); }
.agenda-panel.open { left: 0; }
.agenda-close { position: absolute; top: 16px; right: 16px; background: none; border: none; font-size: 20px; cursor: pointer; color: var(--c-text-muted); }
.agenda-panel-title { font-family: var(--font-mono); font-size: var(--size-label); letter-spacing: 0.15em; color: var(--c-text-muted); margin-bottom: 24px; margin-top: 8px; }
.agenda-list { list-style: none; }
.agenda-list li { padding: 12px 0; border-bottom: 1px solid var(--c-border); cursor: pointer; font-size: var(--size-body); font-weight: 500; transition: color 0.2s; display: flex; align-items: center; gap: 12px; }
.agenda-list li:hover { color: var(--c-primary); }
.agenda-list li .agenda-num { font-family: var(--font-mono); font-size: var(--size-small); color: var(--c-primary); min-width: 28px; }
.agenda-list li.active { color: var(--c-primary); font-weight: 700; }
.agenda-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.3); z-index: 250; opacity: 0; pointer-events: none; transition: opacity 0.3s; }
.agenda-overlay.open { opacity: 1; pointer-events: auto; }

/* ナビボタン */
.nav-btn { position: fixed; top: 50%; transform: translateY(-50%); width: 44px; height: 44px; border-radius: 50%; background: rgba(255,255,255,0.9); border: 1px solid var(--c-border); font-size: 24px; cursor: pointer; z-index: 100; color: var(--c-text); transition: all 0.3s; display: flex; align-items: center; justify-content: center; box-shadow: var(--shadow-card); }
.nav-btn:hover { background: var(--c-primary); color: white; }
.nav-prev { left: 16px; }
.nav-next { right: 16px; }

/* --- テーマ --- */
.slide[data-theme="white"] { background: var(--c-white); color: var(--c-text); --local-bg: var(--c-white); --local-text: var(--c-text); --local-text-muted: var(--c-text-muted); --local-primary: var(--c-primary); --local-accent: var(--c-accent); --local-border: var(--c-border); --local-card-bg: var(--c-white); --local-card-border: var(--c-border); }
.slide[data-theme="light"] { background: var(--c-bg); color: var(--c-text); --local-bg: var(--c-bg); --local-text: var(--c-text); --local-text-muted: var(--c-text-muted); --local-primary: var(--c-primary); --local-accent: var(--c-accent); --local-border: var(--c-border); --local-card-bg: var(--c-white); --local-card-border: var(--c-border); }
.slide[data-theme="blue"] { background: linear-gradient(135deg, var(--c-grad-start), var(--c-grad-end)); color: var(--c-white); --local-bg: transparent; --local-text: var(--c-white); --local-text-muted: rgba(255,255,255,0.7); --local-primary: var(--c-white); --local-accent: var(--c-accent); --local-border: rgba(255,255,255,0.2); --local-card-bg: rgba(255,255,255,0.1); --local-card-border: rgba(255,255,255,0.2); }
.slide[data-theme="dark-blue"] { background: linear-gradient(135deg, #1E3A5F, #2C5F8A); color: var(--c-white); --local-bg: #1E3A5F; --local-text: var(--c-white); --local-text-muted: rgba(255,255,255,0.7); --local-primary: var(--c-white); --local-accent: var(--c-accent); --local-border: rgba(255,255,255,0.15); --local-card-bg: rgba(255,255,255,0.08); --local-card-border: rgba(255,255,255,0.15); }
.slide[data-theme="accent"] { background: var(--c-accent); color: var(--c-white); --local-bg: var(--c-accent); --local-text: var(--c-white); --local-text-muted: rgba(255,255,255,0.8); --local-primary: var(--c-white); --local-accent: var(--c-white); --local-border: rgba(255,255,255,0.3); --local-card-bg: rgba(255,255,255,0.15); --local-card-border: rgba(255,255,255,0.3); }
.slide[data-theme="accent-light"] { background: linear-gradient(135deg, #F5C563, #F5A623); color: var(--c-white); --local-bg: transparent; --local-text: var(--c-white); --local-text-muted: rgba(255,255,255,0.8); --local-primary: var(--c-white); --local-accent: var(--c-white); --local-border: rgba(255,255,255,0.3); --local-card-bg: rgba(255,255,255,0.15); --local-card-border: rgba(255,255,255,0.3); }

/* --- 共通コンポ���ネント --- */
.section-label { position: absolute; top: var(--slide-padding); left: var(--slide-padding); display: flex; align-items: center; gap: var(--gap-sm); font-size: var(--size-small); font-weight: 500; color: var(--local-text-muted); }
.section-label::before { content: ''; width: 3px; height: 20px; background: var(--local-primary); border-radius: 2px; }
.section-label-en { font-family: var(--font-mono); font-size: var(--size-label); letter-spacing: 0.1em; display: block; margin-bottom: 2px; }
.slide-title { font-family: var(--font-heading); font-size: var(--size-h1); font-weight: 900; line-height: 1.3; letter-spacing: -0.02em; }
.slide-subtitle { font-size: var(--size-h3); color: var(--local-text-muted); margin-top: var(--gap-sm); line-height: 1.6; }
.catch-text { font-family: var(--font-heading); font-size: var(--size-display); font-weight: 900; line-height: 1.2; }
.text-primary { color: var(--c-primary); }
.text-accent { color: var(--c-accent); }
.biz-card { background: var(--local-card-bg); border: 1px solid var(--local-card-border); border-radius: var(--radius-lg); padding: var(--gap); box-shadow: var(--shadow-card); transition: transform 0.3s, box-shadow 0.3s; }
.biz-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-card-hover); }
.badge-medal { display: inline-flex; align-items: center; justify-content: center; flex-direction: column; text-align: center; width: 130px; height: 130px; border-radius: 50%; border: 3px solid var(--c-accent); background: linear-gradient(135deg, #FFF8E7, #FFF2D0); box-shadow: 0 2px 12px rgba(245,166,35,0.2); padding: 12px; }
.badge-medal-label { font-size: var(--size-label); font-weight: 500; color: var(--c-accent-dark); }
.badge-medal-value { font-size: clamp(24px, 2.5vw, 36px); font-weight: 900; color: var(--c-accent-dark); line-height: 1.1; }
.photo-placeholder { width: 100%; height: 100%; background: linear-gradient(135deg, var(--c-primary-light), #D1E8F0); border-radius: var(--radius-lg); display: flex; align-items: center; justify-content: center; color: var(--c-text-muted); font-size: var(--size-small); overflow: hidden; }
.photo-placeholder img { width: 100%; height: 100%; object-fit: cover; }
.icon-circle { width: 80px; height: 80px; border-radius: 50%; background: var(--c-primary-light); display: flex; align-items: center; justify-content: center; margin: 0 auto var(--gap-sm); }
.icon-circle svg { width: 40px; height: 40px; stroke: var(--c-primary); fill: none; stroke-width: 1.5; }
.divider { width: 100%; height: 1px; background: var(--local-border); margin: var(--gap-sm) 0; }
.slide-footer { position: absolute; bottom: 20px; right: 32px; font-size: var(--size-label); color: var(--local-text-muted); font-family: var(--font-mono); letter-spacing: 0.05em; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: var(--gap); align-items: center; width: 100%; max-width: 1200px; }
.two-col-60-40 { display: grid; grid-template-columns: 6fr 4fr; gap: var(--gap); align-items: center; width: 100%; max-width: 1200px; }
.two-col-40-60 { display: grid; grid-template-columns: 4fr 6fr; gap: var(--gap); align-items: center; width: 100%; max-width: 1200px; }
.three-col { display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--gap); width: 100%; max-width: 1200px; }
.four-col { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--gap); width: 100%; max-width: 1200px; }
.center-content { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; width: 100%; }

/* --- 3D背景アニメーション（表紙やインパクトスライドで使用） --- */
@keyframes sphere-spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes cube-spin { from { transform: translateY(-50%) rotate(0deg); } to { transform: translateY(-50%) rotate(360deg); } }
.bg-sphere { animation: sphere-spin 30s linear infinite; }
.bg-cube { animation: cube-spin 40s linear infinite; }
/* 背景画像オーバーレイ（Unsplash等） */
.slide-bg-cover { position: relative; }
.slide-bg-cover::before { content: ''; position: absolute; inset: 0; background-image: var(--bg-img); background-size: cover; background-position: center; opacity: var(--bg-opacity, 0.08); z-index: 0; }
.slide-bg-cover > * { position: relative; z-index: 1; }

/* --- アニメーション（14種+3D） --- */
.fade-in { opacity: 0; transform: translateY(20px); transition: opacity 0.6s ease, transform 0.6s ease; }
.fade-in.visible { opacity: 1; transform: translateY(0); }
.slide-in-left { opacity: 0; transform: translateX(-40px); transition: opacity 0.6s ease, transform 0.6s ease; }
.slide-in-left.visible { opacity: 1; transform: translateX(0); }
.slide-in-right { opacity: 0; transform: translateX(40px); transition: opacity 0.6s ease, transform 0.6s ease; }
.slide-in-right.visible { opacity: 1; transform: translateX(0); }
.scale-in { opacity: 0; transform: scale(0.85); transition: opacity 0.5s ease, transform 0.5s ease; }
.scale-in.visible { opacity: 1; transform: scale(1); }
.blur-in { opacity: 0; filter: blur(8px); transition: opacity 0.6s ease, filter 0.6s ease; }
.blur-in.visible { opacity: 1; filter: blur(0); }
.flip-in { opacity: 0; transform: perspective(800px) rotateY(-30deg); transition: opacity 0.8s ease, transform 0.8s ease; }
.flip-in.visible { opacity: 1; transform: perspective(800px) rotateY(0); }
.d1 { transition-delay: 0.1s; } .d2 { transition-delay: 0.2s; } .d3 { transition-delay: 0.3s; }
.d4 { transition-delay: 0.4s; } .d5 { transition-delay: 0.5s; } .d6 { transition-delay: 0.6s; }
.countup { font-family: var(--font-heading); font-weight: 900; }
.bar-animate { width: 0; transition: width 1s cubic-bezier(0.25, 0.46, 0.45, 0.94); }
.donut-animate { stroke-dasharray: 0 100; transition: stroke-dasharray 1.5s cubic-bezier(0.25, 0.46, 0.45, 0.94); }
@keyframes typing { from { width: 0; } to { width: 100%; } }
@keyframes blink-caret { 50% { border-color: transparent; } }
.typing-text { overflow: hidden; white-space: nowrap; border-right: 2px solid var(--c-primary); animation: typing 2s steps(30) forwards, blink-caret 0.75s step-end infinite; width: 0; }
@keyframes glow-pulse { 0%,100% { box-shadow: 0 0 5px var(--c-primary); } 50% { box-shadow: 0 0 20px var(--c-primary), 0 0 40px var(--c-primary); } }
@keyframes pulse-ring { 0% { transform: scale(0.8); opacity: 0.8; } 100% { transform: scale(1.5); opacity: 0; } }
@keyframes float-particle { 0%,100% { transform: translateY(0); opacity: 0.3; } 50% { transform: translateY(-20px); opacity: 0.7; } }
```

---

## JavaScript基盤（必須実装）

```javascript
const deck = document.querySelector('.deck');
const slides = document.querySelectorAll('.slide');
const progressFill = document.querySelector('.progress-fill');
const currentNum = document.querySelector('.current-num');
const totalNum = document.querySelector('.total-num');
let current = 0;
const total = slides.length;
totalNum.textContent = total;

function updateUI() {
  currentNum.textContent = current + 1;
  progressFill.style.width = ((current + 1) / total * 100) + '%';
  const theme = slides[current]?.dataset.theme || 'white';
  const isDark = ['blue', 'dark-blue', 'accent', 'accent-light'].includes(theme);
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.style.background = isDark ? 'rgba(255,255,255,0.15)' : 'rgba(255,255,255,0.9)';
    btn.style.color = isDark ? '#fff' : '#1A1A2E';
    btn.style.borderColor = isDark ? 'rgba(255,255,255,0.2)' : '#E5E7EB';
  });
  const counter = document.querySelector('.slide-counter');
  counter.style.background = isDark ? 'rgba(255,255,255,0.15)' : 'rgba(255,255,255,0.9)';
  counter.style.color = isDark ? 'rgba(255,255,255,0.8)' : '#6B7280';
}

function triggerAnimations(slide) {
  slide.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right, .scale-in, .blur-in, .flip-in').forEach(el => el.classList.add('visible'));
  slide.querySelectorAll('.bar-animate').forEach(el => { el.style.width = el.dataset.width; });
  slide.querySelectorAll('.donut-animate').forEach(el => { el.style.strokeDasharray = el.dataset.dash; });
  slide.querySelectorAll('.countup').forEach(el => {
    const target = parseFloat(el.dataset.target);
    const suffix = el.dataset.suffix || '';
    const prefix = el.dataset.prefix || '';
    const sep = el.dataset.sep !== 'false';
    const duration = 1200;
    const start = performance.now();
    function update(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const val = Math.round(target * eased);
      el.textContent = prefix + (sep ? val.toLocaleString() : val) + suffix;
      if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
  });
}

function resetAnimations(slide) {
  slide.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right, .scale-in, .blur-in, .flip-in').forEach(el => el.classList.remove('visible'));
  slide.querySelectorAll('.bar-animate').forEach(el => { el.style.width = '0'; });
  slide.querySelectorAll('.donut-animate').forEach(el => { el.style.strokeDasharray = '0 100'; });
}

function goTo(index) {
  if (index === current) { triggerAnimations(slides[current]); return; }
  const prev = current;
  current = Math.max(0, Math.min(index, total - 1));
  deck.style.transform = `translateX(-${current * 100}vw)`;
  updateUI();
  if (prev !== current) resetAnimations(slides[prev]);
  setTimeout(() => triggerAnimations(slides[current]), 100);
}

document.querySelector('.nav-next').addEventListener('click', () => goTo(current + 1));
document.querySelector('.nav-prev').addEventListener('click', () => goTo(current - 1));
document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); goTo(current + 1); }
  if (e.key === 'ArrowLeft') { e.preventDefault(); goTo(current - 1); }
  if (e.key === 'f' || e.key === 'F') {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen();
    else document.exitFullscreen();
  }
});
let touchStartX = 0;
document.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; });
document.addEventListener('touchend', e => {
  const diff = touchStartX - e.changedTouches[0].clientX;
  if (Math.abs(diff) > 50) goTo(current + (diff > 0 ? 1 : -1));
});

// === アジェンダメニュー ===
const agendaPanel = document.getElementById('agendaPanel');
const agendaOverlay = document.getElementById('agendaOverlay');
const agendaList = document.getElementById('agendaList');
function buildAgenda() {
  agendaList.innerHTML = '';
  slides.forEach((s, i) => {
    const title = s.dataset.slideTitle || ('Slide ' + (i + 1));
    const li = document.createElement('li');
    li.innerHTML = '<span class="agenda-num">' + String(i + 1).padStart(2, '0') + '</span><span>' + title + '</span>';
    li.addEventListener('click', () => { goTo(i); closeAgenda(); });
    agendaList.appendChild(li);
  });
  updateAgendaActive();
}
function updateAgendaActive() {
  agendaList.querySelectorAll('li').forEach((li, i) => li.classList.toggle('active', i === current));
}
function openAgenda() { agendaPanel.classList.add('open'); agendaOverlay.classList.add('open'); }
function closeAgenda() { agendaPanel.classList.remove('open'); agendaOverlay.classList.remove('open'); }
document.querySelector('.agenda-toggle').addEventListener('click', () => {
  agendaPanel.classList.contains('open') ? closeAgenda() : openAgenda();
});
agendaOverlay.addEventListener('click', closeAgenda);
document.querySelector('.agenda-close').addEventListener('click', closeAgenda);
// goToを拡張: アジェンダのアクティブ状態も更新
const _origGoTo = goTo;
// 注: goTo内でupdateAgendaActive()を呼ぶか、goTo後にupdateAgendaActive()を呼ぶ

buildAgenda();
goTo(0);
```

**注意**: goTo関数の末尾に `updateAgendaActive();` を追加すること。
または、上記の `buildAgenda()` の後に `goTo(0)` を呼ぶ構成にする。
各スライドの `<section>` には必ず `data-slide-title="スライド名"` 属性を付けること。

---

## テンプレート一覧（43種）

テンプレートのHTMLコードは参照ファイルを Read すること:
- [templates-core.md](templates-core.md) — 基本パターン 1-25
- [templates-extended.md](templates-extended.md) — 拡張パターン 26-43

| # | パターン名 | カテゴリ | 用途 |
|---|-----------|---------|------|
| 1 | cover-title | 表紙 | ロゴ + 大タイトル + サブ + バッジ + 写真 |
| 2 | contents | 目次 | セクション番号付き目次 |
| 3 | section-divider | 区切り | 大きなセクション番号 + タイトル |
| 4 | profile | 紹介 | 写真 + 肩書き + 経歴 + 実績バッジ |
| 5 | vision-statement | コンテンツ | 中央に大きなステートメント |
| 6 | timeline | コンテンツ | 横型タイムライン |
| 7 | two-col-text-image | コンテンツ | 2カラム: テキスト + 画像 |
| 8 | three-cards | コンテンツ | 3カラムカード |
| 9 | icon-grid | コンテンツ | アイコン + テキストのグリッド |
| 10 | before-after | 比較 | 左Before右After |
| 11 | comparison-table | 比較 | 競合比較テーブル |
| 12 | stats-highlight | データ | 大きな数値 + カウントアップ |
| 13 | donut-stats | データ | ドーナツグラフ + テキスト |
| 14 | process-flow | フロー | 横方向ステップフロー |
| 15 | pentagon-diagram | フロー | 中央 + 5ノードダイアグラム |
| 16 | impact-message | CTA | フルスクリーン大文字 |
| 17 | service-showcase | サービス | ラップトップモック + バッジ |
| 18 | pricing-table | 料金 | 料金プラン比較 |
| 19 | demo-screenshot | 実演 | スクリーンショット大画面 |
| 20 | closing-contact | CTA | 締め + 連絡先 |
| 21 | versus | 比較 | VS対決比較 |
| 22 | funnel | データ | ファネル図 |
| 23 | vertical-timeline | フロー | 縦タイムライン |
| 24 | quote-testimonial | 引用 | お客様の声 |
| 25 | faq | Q&A | アコーディオンQ&A |
| 26 | swot-analysis | データ | SWOT分析4象限 |
| 27 | roadmap | フロー | ロードマップ（四半期） |
| 28 | org-chart | コンテンツ | 組織図 |
| 29 | case-study | コンテンツ | 導入事例（課題→解決→成果） |
| 30 | matrix-quadrant | データ | ポジショニングマップ |
| 31 | pyramid-diagram | コンテンツ | ピラミッド図 |
| 32 | hub-and-spoke | コンテンツ | ハブ&スポーク図 |
| 33 | cycle-diagram | フロー | サイクル図/PDCA |
| 34 | waterfall-chart | データ | ウォーターフォールチャート |
| 35 | bento-grid | コンテンツ | ベントーグリッド |
| 36 | gantt-chart | データ | ガントチャート |
| 37 | kpi-dashboard | データ | KPIダッシュボード |
| 38 | problem-solution | コンテンツ | 課題と解決策 |
| 39 | customer-journey | フロー | カスタマージャーニー |
| 40 | venn-diagram | コンテンツ | ベン図 |
| 41 | checklist-status | コンテンツ | 進捗チェックリスト |
| 42 | logo-wall | 信頼 | 導入企業ロゴ一覧 |
| 43 | number-highlight | データ | ���字ハイライト |

---

## セルフレビュー＆リファインプロセス（実装完了後に必ず実行）

HTMLファイルの生成が完了したら、以下の3段階のレビューを**必ず自分で実行**し、問題があれば修正してから完了報告すること。
このプロセスを飛ばして完了とすることは**絶対に禁止**。

### STEP 1: 機能チェック（grepで確認）

以下をgrepで確認する:
- `<section class="slide"` の数が `total-num` の数値と一致するか
- `triggerAnimations` 関数内で `.fade-in, .slide-in-left, .slide-in-right, .scale-in, .blur-in` に `.visible` を追加する処理があるか
- `.countup` のカウントアップ処理があるか
- `.bar-animate` のバーアニメーション処理があるか
- Fキーフルスクリーンの `requestFullscreen` があるか
- 外部CSSファイルや外部JSファイルのlinkがないか（Google Fontsのみ例外）

### STEP 2: デザイン品質チェック（★最重要）

生成したHTMLの全スライドを読み返し、以下を1つずつ確認する。1つでも問題があればSTEP 3で修正する。

**テキストの階層・バランス（最頻出の問題）:**
- [ ] slide-title（見出し）のfont-sizeが全スライドで統一されている（インラインstyleで個別に上書きしていないか）
- [ ] 見出しが**1行に収まる長さ**である。日本語15文字以内が目安。2行に折れる見出しは必ず短縮する
- [ ] slide-titleとslide-subtitleのサイズに**明確な差**がある（見出しは大きく太く、サブは小さく薄く）
- [ ] カード内のテキストが改行で崩れていない。特にthree-col/four-colの狭いカード内のh3やpを確認
- [ ] テーブルヘッダーのテキストが**1行に収まっている**。折れる場合はテキストを短縮するか列幅%を調整

**レイアウト・配置:**
- [ ] 全スライドのコンテンツが**水平方向にセンタリング**されている（max-width + margin: 0 auto）
- [ ] section-label（左上ラベル）とslide-title（見出し）が**被っていない**。padding-topが十分にあるか確認
- [ ] two-colの左右カラムの**開始位置が揃っている**（align-items: start推奨）
- [ ] three-col/four-colのカードの**高さが揃っている**（min-heightで統一）
- [ ] フローチャートの各ステップに**十分な幅**がある。テキストが縦1文字ずつになっていないか

**テーマ・色:**
- [ ] テーマがwhite/light交互に配置されている（3枚以上同一テーマが連続しない）
- [ ] ダーク（黒背景 #000〜#1a1a2e）テーマが使われていない

**アニメーション:**
- [ ] 各スライドに**最低1つ**のアニメーションクラスが付いている
- [ ] fade-in**以外**のアニメーション（scale-in, slide-in-left, slide-in-right等）も使われている
- [ ] 遅延クラス（.d1〜.d6）で要素が**順番に出現する**ようになっている

### STEP 3: セルフリファイン

STEP 2で問題が見つかった場合:
1. 問題箇所をgrepやreadで特定
2. editで修正を適用
3. 修正後にもう一度STEP 2を再実行
4. 全チェック項目がOKになるまで繰り返す（**最大3ループ**）

**よくある問題と修正パターン:**

| 問題 | 原因 | 修正方法 |
|------|------|----------|
| 見出しが2行に折れる | テキストが長い | 15文字以内に短縮。詳細はsubtitleへ |
| カード内テキスト崩れ | カード幅不足 | テキスト短縮。またはgridカラム数を減らす |
| section-labelと見出し被り | padding-top不足 | .slideのpadding-topをclamp(80px,10vh,100px)に |
| 左右カラム高さ不揃い | align-items: center | align-items: startに変更 |
| テーブルヘッダー折れ | テキスト長い | テキスト短縮＋列幅%指定 |
| フロー要素の文字崩れ | max-widthが狭い | 固定幅を削除、gridの1frに任せる。または2段構成に |
| 全部fade-inだけ | バリエーション不足 | scale-in, slide-in-left/rightを混ぜる |
| 同じテーマ3連続 | テーマ指定ミス | white/lightを交互に配置 |

### 完了報告

STEP 1-3が全て完了し、STEP 2のチェック項目が全てOKになったら、以下の形式で報告する:

```
## セルフレビュー結果
- STEP 1 機能チェック: OK（スライド数: XX, アニメーション処理: 確認済）
- STEP 2 デザイン品質: OK（問題0件 / 修正X件適用済）
- STEP 3 リファイン: X回ループで完了
```
