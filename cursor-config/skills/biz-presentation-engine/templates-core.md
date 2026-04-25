# テンプレート参照: 基本パターン 1-25

> 各テンプレートのHTMLコード。SKILL.md のCSS基盤・JS基盤と組み合わせて使用する。

### 1. cover-title（表紙）
ロゴ + 大タイトル + サブタイトル + バッジ3つ + 右に写真エリア。
背景は白 + 左上に青い装飾丸。

```html
<section class="slide" data-theme="white">
  <div class="deco-circle" style="width: 500px; height: 500px; top: -200px; left: -100px; background: var(--c-primary);"></div>
  <div class="two-col-60-40" style="position: relative; z-index: 1;">
    <div class="slide-in-left">
      <p class="catch-text fade-in" style="font-size: var(--size-h1); color: var(--c-text);">
        生産性10倍の<br>企業のAIプロ育成なら
      </p>
      <h1 class="fade-in d1" style="font-size: var(--size-display); font-weight: 900; margin: var(--gap-sm) 0;">
        <span style="color: #888;">AX</span><span style="color: var(--c-text);">CAMP</span>
      </h1>
      <div class="fade-in d2" style="display: inline-block; background: var(--c-primary); color: white; padding: 6px 24px; border-radius: var(--radius-sm); font-size: var(--size-body); font-weight: 700;">
        チームプラン
      </div>
      <p class="fade-in d3" style="margin-top: var(--gap-sm); font-size: var(--size-body); color: var(--c-text-muted);">
        ~業務を自動化するAIプロ人材チームを育成するeラーニング研修~
      </p>
      <div class="divider fade-in d3" style="margin: var(--gap) 0;"></div>
      <div class="fade-in d4" style="display: flex; gap: var(--gap); flex-wrap: wrap;">
        <div class="badge-medal"><div class="badge-medal-label">伴走支援実績</div><div class="badge-medal-value">83%削減</div><div class="badge-medal-note">※弊社社内実績</div></div>
        <div class="badge-medal"><div class="badge-medal-label">AI化伴走実績</div><div class="badge-medal-value">1,112件</div><div class="badge-medal-note">※2025年末実績</div></div>
        <div class="badge-medal"><div class="badge-medal-label">助成金最大</div><div class="badge-medal-value">75%OFF</div><div class="badge-medal-note">※チーム研修</div></div>
      </div>
    </div>
    <div class="slide-in-right d2" style="border-radius: var(--radius-xl); overflow: hidden; aspect-ratio: 3/4; max-height: 70vh;">
      <div class="photo-placeholder" style="background: linear-gradient(135deg, #D1E8F0, #A8D0E0);">
        写真エリア
      </div>
    </div>
  </div>
  <div class="slide-footer">&copy; 2026 Company Name. All Right Reserved.</div>
</section>
```

### 2. contents（目次）
青グラデーション背景 + 番号付きリスト。右下に装飾用ビルアイコン。

```html
<section class="slide" data-theme="blue">
  <div style="max-width: 800px;">
    <h2 class="fade-in" style="font-family: var(--font-mono); font-size: var(--size-display); font-weight: 300; letter-spacing: 0.1em;">CONTENTS</h2>
    <div style="margin-top: var(--gap);">
      <div class="fade-in d1" style="display: flex; align-items: baseline; gap: var(--gap); padding: var(--gap-sm) 0; border-bottom: 1px solid rgba(255,255,255,0.15);">
        <span style="font-family: var(--font-mono); font-size: var(--size-h2); font-weight: 300;">01</span>
        <div><h3 style="font-size: var(--size-h2); font-weight: 700;">わたし達について</h3><p style="font-size: var(--size-body); opacity: 0.7;">自己紹介 / 会社の沿革</p></div>
      </div>
      <div class="fade-in d2" style="display: flex; align-items: baseline; gap: var(--gap); padding: var(--gap-sm) 0; border-bottom: 1px solid rgba(255,255,255,0.15);">
        <span style="font-family: var(--font-mono); font-size: var(--size-h2); font-weight: 300;">02</span>
        <div><h3 style="font-size: var(--size-h2); font-weight: 700;">AI活用で実現する未来</h3><p style="font-size: var(--size-body); opacity: 0.7;">AIで出来ること / 具体的な活用事例</p></div>
      </div>
      <!-- 03, 04... -->
    </div>
  </div>
  <!-- 右下に薄い装飾アイコン（SVGやCSS図形でビルやグリッドパターン） -->
</section>
```

### 3. section-divider（セクション区切り）
青グラデーション背景。中央に大きな半透明の番号 + タイトル。左右に縦書きの英字テキスト装飾。

```html
<section class="slide" data-theme="blue">
  <!-- 左の縦テキスト -->
  <div style="position: absolute; left: 24px; top: 50%; transform: translateY(-50%) rotate(180deg); writing-mode: vertical-rl; font-family: var(--font-mono); font-size: var(--size-label); letter-spacing: 0.3em; opacity: 0.4;">
    COMPANY INTRODUCTION
  </div>
  <!-- 右の縦テキスト -->
  <div style="position: absolute; right: 24px; top: 50%; transform: translateY(-50%); writing-mode: vertical-rl; font-family: var(--font-mono); font-size: var(--size-label); letter-spacing: 0.3em; opacity: 0.4;">
    COMPANY INTRODUCTION
  </div>
  <!-- 左右の縦線 -->
  <div style="position: absolute; left: 60px; top: 10%; bottom: 10%; width: 1px; background: rgba(255,255,255,0.15);"></div>
  <div style="position: absolute; right: 60px; top: 10%; bottom: 10%; width: 1px; background: rgba(255,255,255,0.15);"></div>

  <div class="center-content" style="position: relative;">
    <div class="scale-in" style="font-size: clamp(150px, 20vw, 300px); font-weight: 900; opacity: 0.1; font-family: var(--font-heading); position: absolute; line-height: 1;">01</div>
    <p class="fade-in" style="font-family: var(--font-mono); font-size: var(--size-body); letter-spacing: 0.15em; position: relative;">About Company</p>
    <h2 class="fade-in d1" style="font-size: var(--size-h1); font-weight: 900; position: relative;">わたし達について</h2>
  </div>
</section>
```

### 4. profile（自己紹介）
左に大きな写真エリア（青い丸背景で切り抜き風）、右に肩書き・名前・経歴・実績。

```html
<section class="slide" data-theme="light">
  <div class="section-label"><div><span class="section-label-en">Profile</span>自己紹介</div></div>
  <div class="two-col-40-60" style="margin-top: var(--gap);">
    <div class="slide-in-left" style="position: relative;">
      <div style="width: 100%; aspect-ratio: 3/4; background: linear-gradient(135deg, var(--c-grad-start), var(--c-grad-end)); border-radius: var(--radius-xl) var(--radius-xl) 0 var(--radius-xl); overflow: hidden;">
        <div class="photo-placeholder">写真エリア</div>
      </div>
    </div>
    <div class="slide-in-right d1">
      <p style="font-size: var(--size-body); color: var(--c-text-muted);">株式会社AX 代表取締役</p>
      <h2 style="font-size: var(--size-display); font-weight: 900; margin: var(--gap-xs) 0;">石綿 文太</h2>
      <p style="font-size: var(--size-body); line-height: 1.8; margin-top: var(--gap-sm);">
        経歴テキスト。18歳で起業。現在31歳で...
      </p>
      <div class="divider" style="margin: var(--gap) 0;"></div>
      <ul style="list-style: none; display: flex; flex-direction: column; gap: var(--gap-xs);">
        <li style="font-size: var(--size-body); display: flex; align-items: center; gap: var(--gap-xs);"><span style="color: var(--c-primary);">&#x2022;</span> 実績1</li>
        <li style="font-size: var(--size-body); display: flex; align-items: center; gap: var(--gap-xs);"><span style="color: var(--c-primary);">&#x2022;</span> 実績2</li>
      </ul>
    </div>
  </div>
</section>
```

### 5. vision-statement（ビジョン）
背景に半透明の写真/パターン + 中央にVISIONラベル + 超大きなテキスト + 英訳。

```html
<section class="slide" data-theme="blue">
  <div class="section-label" style="color: rgba(255,255,255,0.7);"><div><span class="section-label-en">Vision</span>ビジョン</div></div>
  <div class="center-content">
    <div class="fade-in" style="border: 1px solid rgba(255,255,255,0.3); border-radius: var(--radius-sm); padding: 6px 20px; font-family: var(--font-mono); font-size: var(--size-small); letter-spacing: 0.1em;">VISION</div>
    <h2 class="blur-in d1" style="font-size: var(--size-display); font-weight: 900; margin-top: var(--gap);">
      1000万時間を解放し、<br>世界の創造性を爆発させる
    </h2>
    <p class="fade-in d2" style="font-size: var(--size-body); opacity: 0.7; margin-top: var(--gap-sm); font-family: var(--font-mono);">
      Free up 10 million hours and unleash the world's creativity
    </p>
  </div>
</section>
```

### 6. timeline（横型タイムライン）
白背景。上に見出し、中央に横棒のタイムライン。上下交互にイベントを配置。

```html
<section class="slide" data-theme="white">
  <div class="section-label"><div><span class="section-label-en">History</span>沿革</div></div>
  <h2 class="slide-title fade-in" style="text-align: center; margin-bottom: var(--gap);">主要トピック</h2>
  <div class="fade-in d1" style="position: relative; padding: 60px 0;">
    <!-- 横線 -->
    <div style="position: absolute; top: 50%; left: 5%; right: 5%; height: 2px; background: var(--c-border);"></div>
    <!-- タイムラインアイテム（上下交互） -->
    <div style="display: flex; justify-content: space-between; position: relative;">
      <div style="text-align: center; width: 16%;">
        <div style="margin-bottom: 40px;">
          <h4 style="font-size: var(--size-h3); font-weight: 700;">AIライティング導入</h4>
          <p style="font-size: var(--size-small); color: var(--c-text-muted);">説明テキスト</p>
        </div>
        <div style="width: 12px; height: 12px; background: var(--c-primary); border-radius: 50%; margin: 0 auto;"></div>
        <p style="font-family: var(--font-mono); font-size: var(--size-small); color: var(--c-primary); margin-top: 8px;">2022.6</p>
      </div>
      <!-- 下に配置するアイテム -->
      <div style="text-align: center; width: 16%; padding-top: 80px;">
        <div style="width: 12px; height: 12px; background: var(--c-primary); border-radius: 50%; margin: 0 auto;"></div>
        <p style="font-family: var(--font-mono); font-size: var(--size-small); color: var(--c-primary); margin-top: 8px;">2024.6</p>
        <div style="margin-top: 12px;">
          <h4 style="font-size: var(--size-h3); font-weight: 700;">AI自動化検証開始</h4>
          <p style="font-size: var(--size-small); color: var(--c-text-muted);">説明テキスト</p>
        </div>
      </div>
      <!-- 以下交互に繰り返し -->
    </div>
  </div>
</section>
```

### 7. two-col-text-image（2カラム: テキスト + 画像/図解）
左にテキスト（セクションラベル + 見出し + 本文 + リスト）、右にカード/画像。

```html
<section class="slide" data-theme="white">
  <div class="section-label"><div><span class="section-label-en">AI Future</span>AI活用で実現する未来</div></div>
  <div class="two-col" style="margin-top: var(--gap);">
    <div class="slide-in-left">
      <h2 class="slide-title">AIエージェント：<span class="text-accent">ゴールまで自律的に動くAI</span></h2>
      <p class="slide-subtitle" style="margin-top: var(--gap-sm);">「答えるだけのAI」から「仕事を終わらせるAI」への進化</p>
    </div>
    <div class="slide-in-right d2">
      <div class="biz-card" style="padding: var(--gap);">
        <!-- 図解をここに配置 -->
      </div>
    </div>
  </div>
</section>
```

### 8. three-cards（3カラムカード）
見出し + 3つのカード。各カードにアイコン + タイトル + 数値 + 説明リスト。

```html
<section class="slide" data-theme="light">
  <div class="section-label"><div><span class="section-label-en">Results</span>AI活用で実現する未来</div></div>
  <h2 class="slide-title fade-in" style="text-align: center;">AI導入で最初にROIが出るのは<br><span class="text-primary">「経費の削減」</span>です</h2>
  <div class="three-col" style="margin-top: var(--gap);">
    <div class="biz-card fade-in d1" style="text-align: center;">
      <div class="icon-circle"><!-- SVGアイコン --></div>
      <h3 style="font-size: var(--size-h3); font-weight: 700;">システム開発外注費</h3>
      <p class="text-primary" style="font-size: var(--size-h3); font-weight: 900;">1,000万円以上が0円に</p>
      <ul style="text-align: left; margin-top: var(--gap-sm); list-style: disc; padding-left: 20px; font-size: var(--size-body); color: var(--c-text-muted);">
        <li>広告代理店</li><li>制作会社</li><li>記事制作会社</li>
      </ul>
    </div>
    <div class="biz-card fade-in d2" style="text-align: center;"><!-- 同様 --></div>
    <div class="biz-card fade-in d3" style="text-align: center;"><!-- 同様 --></div>
  </div>
</section>
```

### 9. icon-grid（五角形ダイアグラム等）
中央に人物シルエット、周囲に5つのアイコン付きステップを配置。CSS positionで実現。

```html
<section class="slide" data-theme="white">
  <div class="section-label"><div><span class="section-label-en">AI Pro</span>AIプロ人材とは？</div></div>
  <h2 class="slide-title fade-in" style="text-align: center;">「AIプロ人材」は業務をAIで再設計できる</h2>
  <div class="fade-in d1" style="position: relative; width: 600px; height: 500px; margin: var(--gap) auto 0;">
    <!-- 中央のシルエット（CSS or SVG） -->
    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 200px; height: 300px; background: linear-gradient(180deg, var(--c-primary-light), transparent); border-radius: 100px 100px 0 0; display: flex; align-items: center; justify-content: center;">
      <!-- SVG人物シルエット -->
    </div>
    <!-- 五角形の5つのポイント -->
    <div class="scale-in d1" style="position: absolute; top: 0; left: 50%; transform: translateX(-50%); text-align: center;">
      <div class="icon-circle" style="width: 60px; height: 60px;"><!-- SVG --></div>
      <p style="font-weight: 700; font-size: var(--size-small); margin-top: 4px;">01. 業務フロー理解</p>
    </div>
    <!-- 右上、右下、左下、左上に同様に配置 -->
  </div>
</section>
```

### 10. before-after（Before / After比較）
左半分がBefore（白背景）、右半分がAfter（アクセントカラー背景）。

```html
<section class="slide" data-theme="white" style="padding: 0;">
  <div class="section-label" style="top: var(--slide-padding); left: var(--slide-padding); z-index: 2;"><div><span class="section-label-en">Internal performance</span>3つのAI革命</div></div>
  <div style="display: grid; grid-template-columns: 1fr 1fr; height: 100%;">
    <!-- Before側 -->
    <div class="slide-in-left" style="padding: var(--slide-padding); padding-top: calc(var(--slide-padding) + 40px); display: flex; flex-direction: column; justify-content: center;">
      <div style="display: inline-block; background: var(--c-text); color: white; padding: 8px 32px; border-radius: 999px; font-size: var(--size-h3); font-weight: 700; margin-bottom: var(--gap);">Before</div>
      <div style="display: flex; flex-direction: column; gap: var(--gap);">
        <div style="display: flex; align-items: center; gap: var(--gap-sm);">
          <span style="color: var(--c-text-muted); font-size: 24px;">&times;</span>
          <div><span style="font-size: var(--size-h2); font-weight: 900;">月60時間</span><span style="font-size: var(--size-body);">のリサーチ</span><br><span style="font-size: var(--size-small); color: var(--c-text-muted);">コピー作成・配信設計など入稿が...</span></div>
        </div>
        <!-- 他の項目 -->
      </div>
    </div>
    <!-- After側 -->
    <div class="slide-in-right d2" style="background: var(--c-accent); color: white; padding: var(--slide-padding); padding-top: calc(var(--slide-padding) + 40px); display: flex; flex-direction: column; justify-content: center;">
      <div style="display: inline-block; background: white; color: var(--c-text); padding: 8px 32px; border-radius: 999px; font-size: var(--size-h3); font-weight: 700; margin-bottom: var(--gap);">After</div>
      <div style="display: flex; flex-direction: column; gap: var(--gap);">
        <div style="display: flex; align-items: center; gap: var(--gap-sm);">
          <span style="font-size: 24px;">&#x25CE;</span>
          <div><span style="font-size: var(--size-h2); font-weight: 900;">たったの5分</span><span style="font-size: var(--size-body);">に短縮！</span></div>
        </div>
        <!-- 他の項目 -->
      </div>
    </div>
  </div>
</section>
```

### 11. comparison-table（競合比較テーブル）
白背景。見出し + 横幅いっぱいのテーブル。推奨列にハイライト。

```html
<section class="slide" data-theme="white">
  <h2 class="slide-title fade-in" style="text-align: center;">競合比較</h2>
  <div class="fade-in d1" style="max-width: 1000px; margin: var(--gap) auto 0;">
    <table style="width: 100%; border-collapse: collapse; font-size: var(--size-body);">
      <thead>
        <tr style="border-bottom: 2px solid var(--c-primary);">
          <th style="padding: 16px; text-align: left;"></th>
          <th style="padding: 16px; text-align: center;">一般的なAI研修</th>
          <th style="padding: 16px; text-align: center; background: var(--c-primary-light); border-radius: var(--radius-sm) var(--radius-sm) 0 0; color: var(--c-primary); font-weight: 900;">AX CAMP</th>
          <th style="padding: 16px; text-align: center;">社内独学</th>
        </tr>
      </thead>
      <tbody>
        <tr style="border-bottom: 1px solid var(--c-border);">
          <td style="padding: 16px; font-weight: 700;">AIエージェント開発</td>
          <td style="padding: 16px; text-align: center; color: var(--c-danger);">&#x2717;</td>
          <td style="padding: 16px; text-align: center; background: var(--c-primary-light); color: var(--c-primary); font-weight: 900;">&#x2713;</td>
          <td style="padding: 16px; text-align: center; color: var(--c-danger);">&#x2717;</td>
        </tr>
        <!-- 他の行 -->
      </tbody>
    </table>
  </div>
</section>
```

### 12. stats-highlight（数値ハイライト）
大きなカウントアップ数値 + ラベル。3列 or 1列。

```html
<section class="slide" data-theme="light">
  <div class="center-content">
    <h2 class="slide-title fade-in">導入実績</h2>
    <div class="three-col fade-in d1" style="margin-top: var(--gap);">
      <div class="biz-card" style="text-align: center;">
        <div style="font-size: var(--size-display); font-weight: 900; color: var(--c-primary);" class="countup" data-target="83" data-suffix="%">0%</div>
        <p style="font-size: var(--size-body); font-weight: 600;">業務工数削減</p>
      </div>
      <div class="biz-card" style="text-align: center;">
        <div style="font-size: var(--size-display); font-weight: 900; color: var(--c-primary);" class="countup" data-target="1112" data-suffix="件">0件</div>
        <p style="font-size: var(--size-body); font-weight: 600;">AI化伴走実績</p>
      </div>
      <div class="biz-card" style="text-align: center;">
        <div style="font-size: var(--size-display); font-weight: 900; color: var(--c-accent);" class="countup" data-target="75" data-suffix="%OFF">0%OFF</div>
        <p style="font-size: var(--size-body); font-weight: 600;">助成金最大</p>
      </div>
    </div>
  </div>
</section>
```

### 13. donut-stats（ドーナツグラフ + テキスト）
左にSVGドーナツ + 中央数値、右にテキスト説明。

```html
<section class="slide" data-theme="white">
  <div class="two-col">
    <div class="fade-in" style="text-align: center;">
      <svg viewBox="0 0 120 120" style="width: 220px; height: 220px;">
        <circle cx="60" cy="60" r="50" fill="none" stroke="var(--c-border)" stroke-width="10"/>
        <circle cx="60" cy="60" r="50" fill="none" stroke="var(--c-accent)" stroke-width="10"
          stroke-linecap="round" transform="rotate(-90 60 60)"
          class="donut-animate" data-dash="93 100" />
        <text x="60" y="55" text-anchor="middle" font-family="var(--font-heading)" font-size="22" font-weight="900" fill="var(--c-text)">
          <tspan class="countup" data-target="93" data-suffix="%">0%</tspan>
        </text>
        <text x="60" y="72" text-anchor="middle" font-size="8" fill="var(--c-text-muted)">削減費用</text>
      </svg>
    </div>
    <div class="slide-in-right d1">
      <h2 class="slide-title">人件費93%削減</h2>
      <p class="slide-subtitle">月600万円 → 月40万円に</p>
    </div>
  </div>
</section>
```

### 14. process-flow（横ステップフロー with 写真）
見出し + 横に4つのステップ。各ステップに写真 + 矢印 + タイトル + 説明。

```html
<section class="slide" data-theme="white">
  <div class="section-label"><div><span class="section-label-en">Flow</span>導入の流れ</div></div>
  <h2 class="slide-title fade-in" style="text-align: center;">AX CAMP 受講の流れ</h2>
  <div class="four-col fade-in d1" style="margin-top: var(--gap); align-items: start;">
    <div style="text-align: center;">
      <div style="aspect-ratio: 16/9; border-radius: var(--radius-md); overflow: hidden; margin-bottom: var(--gap-sm);">
        <div class="photo-placeholder">写真</div>
      </div>
      <!-- 矢印バー -->
      <div style="background: linear-gradient(90deg, var(--c-primary), var(--c-primary)); color: white; padding: 8px 16px; border-radius: var(--radius-sm); font-weight: 700; font-size: var(--size-small); margin-bottom: var(--gap-sm);">ヒアリング・契約</div>
      <p style="font-size: var(--size-small); color: var(--c-text-muted); text-align: left;">
        AIコンサルタントが業務をヒアリングし、AI化の難易度や実装工数の見積もりを行います。
      </p>
    </div>
    <!-- 2〜4番目のステップも同様 -->
  </div>
</section>
```

### 15. pentagon-diagram
→ パターン9 (icon-grid) と同じ。中央の人物 + 5つのアイコン付きポイント。

### 16. impact-message（インパクトメッセージ）
アクセントカラー背景にフルスクリーンの大きな白文字。

```html
<section class="slide" data-theme="accent-light">
  <div class="center-content">
    <h2 class="blur-in" style="font-size: var(--size-display); font-weight: 900; line-height: 1.3;">
      リサーチ/制作/営業の<br>「3つのAI革命」<br>お見せします。
    </h2>
  </div>
  <div class="slide-footer" style="color: rgba(255,255,255,0.6);">&copy; Company Name</div>
</section>
```

### 17. service-showcase（サービス紹介）
見出し + 左にラップトップ風モック（中にスクリーンショット）、右にバッジ3つ。

```html
<section class="slide" data-theme="blue">
  <div class="section-label" style="color: rgba(255,255,255,0.7);"><div><span class="section-label-en">Service</span>自社サービス</div></div>
  <h2 class="slide-title fade-in" style="text-align: center;">AIエージェントを作れるようになる<br>法人向けAIプロ人材育成支援をやっています</h2>
  <div class="two-col fade-in d1" style="margin-top: var(--gap);">
    <div>
      <!-- ラップトップモック -->
      <div style="background: #222; border-radius: 12px 12px 0 0; padding: 8px 8px 0; box-shadow: var(--shadow-elevated);">
        <div style="aspect-ratio: 16/10; background: white; border-radius: 4px 4px 0 0; overflow: hidden;">
          <div class="photo-placeholder" style="border-radius: 0;">スクリーンショット</div>
        </div>
      </div>
      <div style="background: #333; height: 12px; border-radius: 0 0 8px 8px; margin: 0 20px;"></div>
    </div>
    <div style="display: flex; flex-direction: column; align-items: center; gap: var(--gap-sm);">
      <p style="font-size: var(--size-h2); font-weight: 900;">生産性10倍の<br>企業のAIプロ育成なら</p>
      <div style="display: flex; gap: var(--gap-sm); flex-wrap: wrap; justify-content: center;">
        <div class="badge-medal" style="width: 100px; height: 100px;"><div class="badge-medal-label" style="font-size: 8px;">伴走支援実績</div><div class="badge-medal-value" style="font-size: 18px;">83%削減</div></div>
        <div class="badge-medal" style="width: 100px; height: 100px;"><div class="badge-medal-label" style="font-size: 8px;">AI化伴走</div><div class="badge-medal-value" style="font-size: 18px;">1,112件</div></div>
        <div class="badge-medal" style="width: 100px; height: 100px;"><div class="badge-medal-label" style="font-size: 8px;">助成金最大</div><div class="badge-medal-value" style="font-size: 18px;">75%OFF</div></div>
      </div>
    </div>
  </div>
</section>
```

### 18. pricing-table（料金プラン）
3列の料金プラン。おすすめにハイライト + ラベル。

```html
<section class="slide" data-theme="light">
  <h2 class="slide-title fade-in" style="text-align: center;">プランと料金</h2>
  <div class="three-col fade-in d1" style="margin-top: var(--gap); align-items: start;">
    <div class="biz-card" style="text-align: center;">
      <p style="font-family: var(--font-mono); font-size: var(--size-label); letter-spacing: 0.2em; color: var(--c-text-muted);">LIGHT</p>
      <div style="font-size: var(--size-h1); font-weight: 900; color: var(--c-primary); margin: var(--gap-sm) 0;">
        <span class="countup" data-target="30" data-prefix="¥" data-suffix="万/月">¥0万/月</span>
      </div>
      <ul style="list-style: none; text-align: left;">
        <li style="padding: 8px 0; border-bottom: 1px solid var(--c-border); font-size: var(--size-body);"><span style="color: var(--c-success);">&#x2713;</span> e-learning受講</li>
        <li style="padding: 8px 0; border-bottom: 1px solid var(--c-border); font-size: var(--size-body);"><span style="color: var(--c-success);">&#x2713;</span> 月1回のQ&A</li>
      </ul>
    </div>
    <div class="biz-card" style="text-align: center; border: 2px solid var(--c-primary); transform: scale(1.05); position: relative;">
      <div style="position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: var(--c-primary); color: white; padding: 4px 16px; border-radius: 999px; font-size: var(--size-label); font-weight: 700;">RECOMMENDED</div>
      <p style="font-family: var(--font-mono); font-size: var(--size-label); letter-spacing: 0.2em; color: var(--c-primary); margin-top: 8px;">TEAM</p>
      <div style="font-size: var(--size-h1); font-weight: 900; color: var(--c-primary); margin: var(--gap-sm) 0;">
        <span class="countup" data-target="80" data-prefix="¥" data-suffix="万/月">¥0万/月</span>
      </div>
      <ul style="list-style: none; text-align: left;">
        <li style="padding: 8px 0; border-bottom: 1px solid var(--c-border); font-size: var(--size-body);"><span style="color: var(--c-success);">&#x2713;</span> チーム研修(最大20名)</li>
        <!-- ... -->
      </ul>
    </div>
    <div class="biz-card" style="text-align: center;"><!-- ENTERPRISE --></div>
  </div>
</section>
```

### 19. demo-screenshot（実演/スクリーンショット大画面）
上にラベル付きバー、中央にスクリーンショット。

```html
<section class="slide" data-theme="white" style="padding: 0;">
  <div style="display: flex; flex-direction: column; height: 100%;">
    <div class="fade-in" style="display: flex; align-items: center; gap: var(--gap-sm); padding: 12px var(--slide-padding); background: linear-gradient(90deg, var(--c-primary-dark), var(--c-primary));">
      <span style="background: var(--c-accent); color: white; padding: 4px 12px; border-radius: var(--radius-sm); font-weight: 900; font-size: var(--size-small);">実演</span>
      <span style="color: white; font-weight: 700; font-size: var(--size-h3);">SEO記事生成エージェント</span>
    </div>
    <div class="scale-in d1" style="flex: 1; padding: var(--gap); display: flex; align-items: center; justify-content: center;">
      <div style="width: 90%; max-width: 1100px; aspect-ratio: 16/9; border-radius: var(--radius-lg); overflow: hidden; box-shadow: var(--shadow-elevated);">
        <div class="photo-placeholder" style="border-radius: 0;">スクリーンショット</div>
      </div>
    </div>
  </div>
</section>
```

### 20. closing-contact（締め + 連絡先）

```html
<section class="slide" data-theme="dark-blue">
  <div class="center-content">
    <h2 class="blur-in" style="font-size: var(--size-display); font-weight: 900;">THANK YOU</h2>
    <p class="fade-in d1" style="font-size: var(--size-h3); margin-top: var(--gap-sm); opacity: 0.8;">
      ご質問・ご相談はお気軽にどうぞ
    </p>
    <div class="fade-in d2" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--gap); margin-top: var(--gap); text-align: center; max-width: 600px;">
      <div><p style="font-family: var(--font-mono); font-size: var(--size-label); opacity: 0.6; letter-spacing: 0.1em;">EMAIL</p><p style="font-size: var(--size-body);">info@example.com</p></div>
      <div><p style="font-family: var(--font-mono); font-size: var(--size-label); opacity: 0.6; letter-spacing: 0.1em;">WEB</p><p style="font-size: var(--size-body);">example.com</p></div>
      <div><p style="font-family: var(--font-mono); font-size: var(--size-label); opacity: 0.6; letter-spacing: 0.1em;">TEL</p><p style="font-size: var(--size-body);">03-XXXX-XXXX</p></div>
    </div>
    <p class="fade-in d3" style="margin-top: var(--gap); font-family: var(--font-mono); font-size: var(--size-label); opacity: 0.5;">&copy; 2026 Company Name. All Rights Reserved.</p>
  </div>
</section>
```

---

### 拡張パターン（21〜25）— web-presentation由来

### 21. versus（VS対決比較）
中央にグローパルスのVSバッジ。左右に対比するカード。

```html
<section class="slide" data-theme="white">
  <div style="display: grid; grid-template-columns: 1fr auto 1fr; gap: var(--gap); align-items: center; max-width: 1100px; width: 100%;">
    <div class="biz-card slide-in-left" style="padding: var(--gap);">
      <h3 style="font-size: var(--size-h2); font-weight: 900;">他社AI研修</h3>
      <p style="color: var(--c-text-muted); margin: var(--gap-sm) 0;">研修がゴール</p>
      <ul style="list-style: none;"><li style="padding: var(--gap-xs) 0; border-bottom: 1px solid var(--c-border);">座学中心</li><li style="padding: var(--gap-xs) 0; border-bottom: 1px solid var(--c-border);">フォローなし</li></ul>
    </div>
    <div class="scale-in d1" style="text-align: center;">
      <div style="font-family: var(--font-heading); font-size: var(--size-h1); font-weight: 900; color: var(--c-accent); width: 100px; height: 100px; border: 3px solid var(--c-accent); border-radius: 50%; display: flex; align-items: center; justify-content: center; animation: glow-pulse 2s ease-in-out infinite;">VS</div>
    </div>
    <div class="biz-card slide-in-right d2" style="padding: var(--gap); border-color: var(--c-primary);">
      <h3 style="font-size: var(--size-h2); font-weight: 900; color: var(--c-primary);">自社サービス</h3>
      <p style="color: var(--c-text-muted); margin: var(--gap-sm) 0;">成果がゴール</p>
      <ul style="list-style: none;"><li style="padding: var(--gap-xs) 0; border-bottom: 1px solid var(--c-border);">超実践型</li><li style="padding: var(--gap-xs) 0; border-bottom: 1px solid var(--c-border);">AI顧問で伴走</li></ul>
    </div>
  </div>
</section>
```

### 22. funnel（ファネル図）
上から下に狭まる段階表示。カウントアップ付き。

```html
<section class="slide" data-theme="light">
  <h2 class="slide-title fade-in" style="text-align: center;">コンバージョンファネル</h2>
  <div style="display: flex; flex-direction: column; align-items: center; gap: 4px; margin-top: var(--gap); max-width: 800px; margin-left: auto; margin-right: auto;">
    <div class="fade-in d1" style="width: 100%; display: flex; justify-content: space-between; padding: 16px 24px; border-radius: 8px; background: var(--c-primary); color: white; font-weight: 700;"><span>認知</span><span class="countup" data-target="10000" data-suffix="人">0人</span></div>
    <div class="fade-in d2" style="width: 75%; display: flex; justify-content: space-between; padding: 16px 24px; border-radius: 8px; background: var(--c-primary); opacity: 0.85; color: white; font-weight: 700;"><span>興味</span><span class="countup" data-target="3000" data-suffix="人">0人</span></div>
    <div class="fade-in d3" style="width: 55%; display: flex; justify-content: space-between; padding: 16px 24px; border-radius: 8px; background: var(--c-primary); opacity: 0.7; color: white; font-weight: 700;"><span>検討</span><span class="countup" data-target="800" data-suffix="人">0人</span></div>
    <div class="fade-in d4" style="width: 40%; display: flex; justify-content: space-between; padding: 16px 24px; border-radius: 8px; background: var(--c-accent); color: white; font-weight: 700;"><span>成約</span><span class="countup" data-target="200" data-suffix="人">0人</span></div>
  </div>
</section>
```

### 23. vertical-timeline（縦タイムライン）
左に線+ドット、右にイベント。沿革の別表現。

```html
<section class="slide" data-theme="white">
  <h2 class="slide-title fade-in" style="text-align: center;">沿革</h2>
  <div style="position: relative; padding-left: 40px; max-width: 700px; margin: var(--gap) auto 0;">
    <div style="position: absolute; left: 8px; top: 0; bottom: 0; width: 2px; background: var(--c-border);"></div>
    <div class="fade-in d1" style="position: relative; padding-bottom: var(--gap);">
      <div style="position: absolute; left: -40px; top: 4px; width: 18px; height: 18px; border-radius: 50%; background: var(--c-primary); border: 3px solid white;"></div>
      <p style="font-family: var(--font-mono); font-size: var(--size-label); color: var(--c-primary);">2022.06</p>
      <h3 style="font-size: var(--size-h3); font-weight: 700;">AIライティング導入</h3>
      <p style="font-size: var(--size-body); color: var(--c-text-muted);">SEO事業でAI活用を開始</p>
    </div>
    <!-- 繰り返し -->
  </div>
</section>
```

### 24. quote-testimonial（引用・お客様の声）
大きな引用符 + ブラーインのテキスト + 出典。

```html
<section class="slide" data-theme="blue">
  <div class="center-content">
    <div class="fade-in" style="font-size: 120px; opacity: 0.15; font-family: serif; line-height: 1;">"</div>
    <blockquote class="blur-in d1" style="font-family: var(--font-heading); font-size: var(--size-h1); font-weight: 500; line-height: 1.5; font-style: italic; max-width: 800px;">
      AIを導入して、チームの生産性が劇的に変わりました
    </blockquote>
    <p class="fade-in d2" style="margin-top: var(--gap); font-size: var(--size-body); opacity: 0.8;">田中太郎 / 株式会社○○ 代表取締役</p>
  </div>
</section>
```

### 25. faq（アコーディオン風Q&A）
details/summaryでクリック開閉。

```html
<section class="slide" data-theme="white">
  <h2 class="slide-title fade-in" style="text-align: center;">よくあるご質問</h2>
  <div style="max-width: 800px; margin: var(--gap) auto 0;">
    <details class="fade-in d1" style="border-bottom: 1px solid var(--c-border);">
      <summary style="padding: var(--gap-sm) 0; font-size: var(--size-h3); font-weight: 700; cursor: pointer; list-style: none; display: flex; justify-content: space-between;">Q. 研修期間はどのくらいですか？<span style="color: var(--c-primary);">+</span></summary>
      <div style="padding: 0 0 var(--gap-sm); font-size: var(--size-body); color: var(--c-text-muted); line-height: 1.7;">A. 基本プランは3ヶ月です。カスタマイズも可能です。</div>
    </details>
    <!-- 繰り返し -->
  </div>
</section>
```

---
