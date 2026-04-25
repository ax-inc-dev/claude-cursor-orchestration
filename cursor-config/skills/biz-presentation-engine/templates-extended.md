# テンプレート参照: 拡張パターン 26-43

> B2B提案に必須のリッ���テンプレート。SKILL.md のCSS基盤・JS基盤と組み合わせて使用する。

### 26. swot-analysis（SWOT分析）
**構造:** 2×2グリッド。各象限を色分け（S=青, W=赤系, O=緑, T=オレンジ）。各セルにタイトル + 3〜5箇条書き。
**テーマ:** `white` or `light`
**レイアウト:** `display: grid; grid-template-columns: 1fr 1fr; gap: 4px;` 各セルは `biz-card` + 左上にアイコン/ラベル
**アニメーション:** 各象限を `scale-in d1〜d4` で順次出現

```html
<section class="slide" data-theme="white">
  <h2 class="slide-title fade-in" style="text-align: center;">SWOT分析</h2>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 4px; max-width: 1000px; margin: var(--gap) auto 0;">
    <div class="scale-in d1" style="background: var(--c-primary-light); border-radius: var(--radius-lg) 0 0 0; padding: var(--gap);">
      <h3 style="color: var(--c-primary); font-weight: 900;">S — 強み</h3>
      <ul style="margin-top: var(--gap-sm); font-size: var(--size-body); list-style: disc; padding-left: 20px;"><li>項目1</li><li>項目2</li></ul>
    </div>
    <div class="scale-in d2" style="background: #FEE2E2; border-radius: 0 var(--radius-lg) 0 0; padding: var(--gap);">
      <h3 style="color: #DC2626; font-weight: 900;">W — 弱み</h3>
      <ul style="margin-top: var(--gap-sm); font-size: var(--size-body); list-style: disc; padding-left: 20px;"><li>項目1</li></ul>
    </div>
    <div class="scale-in d3" style="background: #D1FAE5; border-radius: 0 0 0 var(--radius-lg); padding: var(--gap);">
      <h3 style="color: #059669; font-weight: 900;">O — 機会</h3>
      <ul style="margin-top: var(--gap-sm); font-size: var(--size-body); list-style: disc; padding-left: 20px;"><li>項目1</li></ul>
    </div>
    <div class="scale-in d4" style="background: #FEF3C7; border-radius: 0 0 var(--radius-lg) 0; padding: var(--gap);">
      <h3 style="color: #D97706; font-weight: 900;">T — 脅威</h3>
      <ul style="margin-top: var(--gap-sm); font-size: var(--size-body); list-style: disc; padding-left: 20px;"><li>項目1</li></ul>
    </div>
  </div>
</section>
```

### 27. roadmap（ロードマップ）
**構造:** 横軸に四半期/月、縦にカテゴリ（スイムレーン）。各レーンにカラーバーで期間を表示。「現在」の縦線。
**テーマ:** `white` or `light`
**レイアウト:** CSSグリッド `grid-template-columns: 120px repeat(4, 1fr)` で5列。左端にカテゴリラベル、残り4列が Q1〜Q4。
**アニメーション:** 各行を `slide-in-left d1〜d4` で順次

```html
<section class="slide" data-theme="white">
  <h2 class="slide-title fade-in" style="text-align: center;">ロードマップ 2026</h2>
  <div style="max-width: 1100px; margin: var(--gap) auto 0;">
    <!-- ヘッダー行 -->
    <div class="fade-in" style="display: grid; grid-template-columns: 120px repeat(4, 1fr); gap: 2px; margin-bottom: 4px;">
      <div></div>
      <div style="text-align: center; font-family: var(--font-mono); font-size: var(--size-small); color: var(--c-text-muted); padding: 8px;">Q1</div>
      <div style="text-align: center; font-family: var(--font-mono); font-size: var(--size-small); color: var(--c-text-muted); padding: 8px;">Q2</div>
      <div style="text-align: center; font-family: var(--font-mono); font-size: var(--size-small); color: var(--c-text-muted); padding: 8px;">Q3</div>
      <div style="text-align: center; font-family: var(--font-mono); font-size: var(--size-small); color: var(--c-text-muted); padding: 8px;">Q4</div>
    </div>
    <!-- スイムレーン行 -->
    <div class="slide-in-left d1" style="display: grid; grid-template-columns: 120px repeat(4, 1fr); gap: 2px; margin-bottom: 4px;">
      <div style="font-weight: 700; font-size: var(--size-small); display: flex; align-items: center;">フェーズ1</div>
      <div style="background: var(--c-primary); border-radius: 6px; height: 40px; grid-column: 2 / 4;"></div>
      <!-- 空セルは省略 -->
    </div>
    <!-- 追加の行... -->
  </div>
</section>
```

### 28. org-chart（組織図）
**構造:** 最上部にCEO、下に2〜3階層。各ノードは丸アバター+名前+肩書き。CSSのflexboxで階層を表現し、ノード間を `::after` の縦線/横線で接続。
**テーマ:** `white` or `light`
**アニメーション:** 上から順に `fade-in d1〜d4`

```html
<section class="slide" data-theme="white">
  <h2 class="slide-title fade-in" style="text-align: center;">組織体制</h2>
  <div style="display: flex; flex-direction: column; align-items: center; gap: var(--gap); margin-top: var(--gap);">
    <!-- トップ -->
    <div class="scale-in d1" style="text-align: center;">
      <div style="width: 80px; height: 80px; border-radius: 50%; background: var(--c-primary); color: white; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 24px; margin: 0 auto;">CEO</div>
      <p style="font-weight: 700; margin-top: 8px;">山田太郎</p>
      <p style="font-size: var(--size-small); color: var(--c-text-muted);">代表取締役</p>
    </div>
    <div style="width: 2px; height: 20px; background: var(--c-border);"></div>
    <!-- 2階層目 -->
    <div class="fade-in d2" style="display: flex; gap: calc(var(--gap) * 2); position: relative;">
      <div style="position: absolute; top: -10px; left: 25%; right: 25%; height: 2px; background: var(--c-border);"></div>
      <div style="text-align: center;"><div style="width: 60px; height: 60px; border-radius: 50%; background: var(--c-primary-light); color: var(--c-primary); display: flex; align-items: center; justify-content: center; font-weight: 700; margin: 0 auto;">営</div><p style="font-weight: 600; margin-top: 4px; font-size: var(--size-small);">営業部</p></div>
      <div style="text-align: center;"><div style="width: 60px; height: 60px; border-radius: 50%; background: var(--c-primary-light); color: var(--c-primary); display: flex; align-items: center; justify-content: center; font-weight: 700; margin: 0 auto;">開</div><p style="font-weight: 600; margin-top: 4px; font-size: var(--size-small);">開発部</p></div>
      <div style="text-align: center;"><div style="width: 60px; height: 60px; border-radius: 50%; background: var(--c-primary-light); color: var(--c-primary); display: flex; align-items: center; justify-content: center; font-weight: 700; margin: 0 auto;">管</div><p style="font-weight: 600; margin-top: 4px; font-size: var(--size-small);">管理部</p></div>
    </div>
  </div>
</section>
```

### 29. case-study（導入事例）★重要
**構造:** 上部にクライアントロゴ/社名 + 業種バッジ。3セクション横並び: 課題(赤系)→ソリューション(青系)→成果(緑系)。成果セクションに大きなカウントアップ数値。
**テーマ:** `white` or `light`
**アニメーション:** `slide-in-left` → `fade-in` → `slide-in-right`

```html
<section class="slide" data-theme="light">
  <div class="section-label"><div><span class="section-label-en">Case Study</span>導入事例</div></div>
  <div class="fade-in" style="text-align: center; margin-bottom: var(--gap);">
    <span style="background: var(--c-primary-light); color: var(--c-primary); padding: 4px 16px; border-radius: 999px; font-size: var(--size-small); font-weight: 600;">製造業</span>
    <h2 class="slide-title" style="margin-top: var(--gap-xs);">株式会社○○ 様</h2>
  </div>
  <div class="three-col" style="align-items: stretch;">
    <div class="biz-card slide-in-left d1" style="border-top: 3px solid #EF4444;">
      <h3 style="color: #EF4444; font-weight: 700;">課題</h3>
      <ul style="margin-top: var(--gap-sm); font-size: var(--size-body); list-style: disc; padding-left: 16px;"><li>月60時間のリサーチ業務</li><li>外注費が年間1000万円</li></ul>
    </div>
    <div class="biz-card fade-in d2" style="border-top: 3px solid var(--c-primary);">
      <h3 style="color: var(--c-primary); font-weight: 700;">解決策</h3>
      <ul style="margin-top: var(--gap-sm); font-size: var(--size-body); list-style: disc; padding-left: 16px;"><li>AIエージェント導入</li><li>業務フロー再設計</li></ul>
    </div>
    <div class="biz-card slide-in-right d3" style="border-top: 3px solid #10B981; text-align: center;">
      <h3 style="color: #10B981; font-weight: 700;">成果</h3>
      <div style="font-size: var(--size-display); font-weight: 900; color: #10B981; margin-top: var(--gap-sm);" class="countup" data-target="83" data-suffix="%">0%</div>
      <p style="font-weight: 600;">業務工数削減</p>
    </div>
  </div>
</section>
```

### 30. matrix-quadrant（マトリクス/ポジショニングマップ）
**構造:** XY軸の十字線で4象限。各象限にラベル。バブル（円）でアイテムをプロット。自社位置をハイライト。
**テーマ:** `white`
**レイアウト:** 相対配置の正方形エリアに十字線（CSS ::before/::after）+ absolute配置のバブル
**アニメーション:** 各バブルを `scale-in d1〜d6`

```html
<section class="slide" data-theme="white">
  <h2 class="slide-title fade-in" style="text-align: center;">ポジショニングマップ</h2>
  <div class="fade-in d1" style="position: relative; width: 600px; height: 500px; margin: var(--gap) auto 0;">
    <!-- 軸 -->
    <div style="position: absolute; left: 50%; top: 0; bottom: 0; width: 2px; background: var(--c-border);"></div>
    <div style="position: absolute; top: 50%; left: 0; right: 0; height: 2px; background: var(--c-border);"></div>
    <!-- 軸ラベル -->
    <span style="position: absolute; top: -20px; left: 50%; transform: translateX(-50%); font-size: var(--size-small); color: var(--c-text-muted);">高品質</span>
    <span style="position: absolute; bottom: -20px; left: 50%; transform: translateX(-50%); font-size: var(--size-small); color: var(--c-text-muted);">低品質</span>
    <span style="position: absolute; left: -40px; top: 50%; transform: translateY(-50%); font-size: var(--size-small); color: var(--c-text-muted);">低価格</span>
    <span style="position: absolute; right: -40px; top: 50%; transform: translateY(-50%); font-size: var(--size-small); color: var(--c-text-muted);">高価格</span>
    <!-- バブル（自社=ハイライト） -->
    <div class="scale-in d2" style="position: absolute; top: 15%; right: 20%; width: 80px; height: 80px; border-radius: 50%; background: var(--c-primary); color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: var(--size-small); animation: glow-pulse 3s infinite;">自社</div>
    <div class="scale-in d3" style="position: absolute; top: 30%; left: 20%; width: 60px; height: 60px; border-radius: 50%; background: var(--c-border); display: flex; align-items: center; justify-content: center; font-size: var(--size-label);">A社</div>
    <!-- 他のバブル... -->
  </div>
</section>
```

### 31. pyramid-diagram（ピラミッド図）
**構造:** 3〜5段の台形レイヤー。上に行くほど幅が狭い。各レイヤーにラベル+説明。
**テーマ:** `white` or `light`

```html
<section class="slide" data-theme="white">
  <h2 class="slide-title fade-in" style="text-align: center;">サービス体系</h2>
  <div style="display: flex; flex-direction: column; align-items: center; gap: 4px; margin-top: var(--gap);">
    <div class="fade-in d1" style="width: 30%; padding: 16px; background: var(--c-primary); color: white; text-align: center; border-radius: 8px 8px 0 0; font-weight: 700;">戦略コンサル</div>
    <div class="fade-in d2" style="width: 55%; padding: 16px; background: var(--c-primary); opacity: 0.8; color: white; text-align: center; font-weight: 700;">AI導入支援</div>
    <div class="fade-in d3" style="width: 75%; padding: 16px; background: var(--c-primary); opacity: 0.6; color: white; text-align: center; font-weight: 700;">e-learning研修</div>
    <div class="fade-in d4" style="width: 100%; padding: 16px; background: var(--c-primary); opacity: 0.4; color: white; text-align: center; border-radius: 0 0 8px 8px; font-weight: 700;">情報発信・メディア</div>
  </div>
</section>
```

### 32. hub-and-spoke（ハブ＆スポーク図）
**構造:** 中央に大きな円（コアサービス/製品）。周囲にCSS `position: absolute` で6個の小円を等間隔に配置。中央→各ノードに破線を接続。
**テーマ:** `white` or `light`
**アニメーション:** 中央 `scale-in`、周囲 `fade-in d1〜d6`

```html
<section class="slide" data-theme="white">
  <h2 class="slide-title fade-in" style="text-align: center;">サービスエコシステム</h2>
  <div style="position: relative; width: 500px; height: 500px; margin: var(--gap) auto 0;">
    <!-- 中央ハブ -->
    <div class="scale-in" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 140px; height: 140px; border-radius: 50%; background: var(--c-primary); color: white; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: var(--size-h3); box-shadow: var(--shadow-elevated);">コア</div>
    <!-- スポーク（上） -->
    <div class="fade-in d1" style="position: absolute; top: 5%; left: 50%; transform: translateX(-50%); text-align: center;">
      <div style="width: 70px; height: 70px; border-radius: 50%; background: var(--c-primary-light); color: var(--c-primary); display: flex; align-items: center; justify-content: center; font-weight: 700; margin: 0 auto;">営業</div>
    </div>
    <!-- 右上 -->
    <div class="fade-in d2" style="position: absolute; top: 20%; right: 5%; text-align: center;">
      <div style="width: 70px; height: 70px; border-radius: 50%; background: var(--c-primary-light); color: var(--c-primary); display: flex; align-items: center; justify-content: center; font-weight: 700; margin: 0 auto;">開発</div>
    </div>
    <!-- 他のスポークも同様に配置... -->
  </div>
</section>
```

### 33. cycle-diagram（サイクル図/PDCA）
**構造:** 4〜6ステップを円周上に配置。ステップ間を曲線矢印で接続。中央にサイクル名。
**テーマ:** `white`
**レイアウト:** hub-and-spokeと同様のabsolute配置。矢印はCSS `border` + `transform: rotate()` か SVG arc。

```html
<section class="slide" data-theme="white">
  <h2 class="slide-title fade-in" style="text-align: center;">PDCAサイクル</h2>
  <div style="position: relative; width: 450px; height: 450px; margin: var(--gap) auto 0;">
    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-family: var(--font-mono); font-size: var(--size-h3); color: var(--c-text-muted);">PDCA</div>
    <!-- 上: Plan -->
    <div class="scale-in d1" style="position: absolute; top: 0; left: 50%; transform: translateX(-50%);">
      <div style="width: 100px; height: 100px; border-radius: 50%; background: var(--c-primary); color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; font-weight: 700;">
        <span style="font-size: 24px;">P</span><span style="font-size: 10px;">計画</span>
      </div>
    </div>
    <!-- 右: Do / 下: Check / 左: Act を同様に配置 -->
    <!-- 矢印はSVGオーバーレイで曲線を描画 -->
  </div>
</section>
```

### 34. waterfall-chart（ウォーターフォールチャート）
**構造:** 開始値から増減を経て最終値に至る浮動棒グラフ。増加=青、減少=赤、合計=濃い青。
**テーマ:** `white` or `light`
**レイアウト:** flexbox横並び。各バーを `position: relative` + `margin-top` で浮動表現。
**アニメーション:** 各バーを `fade-in d1〜d6`

```html
<section class="slide" data-theme="white">
  <h2 class="slide-title fade-in" style="text-align: center;">コスト構造分析</h2>
  <div class="fade-in d1" style="display: flex; align-items: flex-end; justify-content: center; gap: 8px; height: 350px; margin-top: var(--gap); max-width: 900px; margin-left: auto; margin-right: auto; border-bottom: 2px solid var(--c-border); padding-bottom: 8px;">
    <div style="text-align: center; width: 100px;">
      <div style="height: 250px; background: var(--c-primary); border-radius: 6px 6px 0 0; display: flex; align-items: flex-end; justify-content: center; color: white; font-weight: 700; padding-bottom: 8px;">¥500万</div>
      <p style="font-size: var(--size-small); margin-top: 4px;">売上</p>
    </div>
    <div style="text-align: center; width: 100px;">
      <div style="height: 80px; margin-top: 170px; background: #EF4444; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700;">-¥80万</div>
      <p style="font-size: var(--size-small); margin-top: 4px;">人件費</p>
    </div>
    <!-- 追加バー... -->
    <div style="text-align: center; width: 100px;">
      <div style="height: 150px; background: var(--c-primary-dark); border-radius: 6px 6px 0 0; display: flex; align-items: flex-end; justify-content: center; color: white; font-weight: 700; padding-bottom: 8px;">¥300万</div>
      <p style="font-size: var(--size-small); margin-top: 4px;">利益</p>
    </div>
  </div>
</section>
```

### 35. bento-grid（ベントーグリッド）★重要
**構造:** 非対称グリッド（一部セルが2倍サイズ）。各セルにメトリクス、ミニチャート、テキスト、画像などを混在配置。2026年最新トレンド。
**テーマ:** `white` or `light`
**レイアウト:** `display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: auto auto;` で一部セルに `grid-column: span 2` や `grid-row: span 2`

```html
<section class="slide" data-theme="light">
  <h2 class="slide-title fade-in" style="text-align: center;">事業サマリー</h2>
  <div style="display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: auto auto; gap: var(--gap-sm); max-width: 1100px; margin: var(--gap) auto 0;">
    <div class="biz-card fade-in d1" style="grid-column: span 2; display: flex; align-items: center; gap: var(--gap);">
      <div><p style="font-size: var(--size-small); color: var(--c-text-muted);">年間売上</p><div style="font-size: var(--size-h1); font-weight: 900; color: var(--c-primary);" class="countup" data-target="12" data-suffix="億円">0億円</div></div>
      <div style="flex: 1; height: 60px; background: linear-gradient(90deg, var(--c-primary-light), var(--c-primary)); border-radius: 8px; opacity: 0.3;"></div>
    </div>
    <div class="biz-card fade-in d2" style="text-align: center;">
      <p style="font-size: var(--size-small); color: var(--c-text-muted);">顧客満足度</p>
      <div style="font-size: var(--size-display); font-weight: 900; color: var(--c-accent);" class="countup" data-target="98" data-suffix="%">0%</div>
    </div>
    <div class="biz-card fade-in d3" style="text-align: center;">
      <p style="font-size: var(--size-small); color: var(--c-text-muted);">従業員数</p>
      <div style="font-size: var(--size-h1); font-weight: 900;" class="countup" data-target="150" data-suffix="名">0名</div>
    </div>
    <div class="biz-card fade-in d4" style="grid-column: span 2;">
      <p style="font-size: var(--size-small); color: var(--c-text-muted);">主要サービス</p>
      <div style="display: flex; gap: var(--gap-sm); margin-top: var(--gap-xs);">
        <span style="background: var(--c-primary-light); color: var(--c-primary); padding: 6px 16px; border-radius: 999px; font-size: var(--size-small); font-weight: 600;">AI研修</span>
        <span style="background: var(--c-primary-light); color: var(--c-primary); padding: 6px 16px; border-radius: 999px; font-size: var(--size-small); font-weight: 600;">開発支援</span>
        <span style="background: var(--c-primary-light); color: var(--c-primary); padding: 6px 16px; border-radius: 999px; font-size: var(--size-small); font-weight: 600;">コンサルティング</span>
      </div>
    </div>
  </div>
</section>
```

### 36. gantt-chart（ガントチャート）
**構造:** 左にタスク名、上に月/週の軸。各タスクに横棒バー（bar-animate使用）。マイルストーンにダイヤマーク。
**テーマ:** `white`
**レイアウト:** CSSグリッド `grid-template-columns: 150px repeat(12, 1fr)` 左列タスク名 + 12列（月）。
**アニメーション:** 各バーを `bar-animate` で伸長

```html
<section class="slide" data-theme="white">
  <h2 class="slide-title fade-in" style="text-align: center;">プロジェクト計画</h2>
  <div class="fade-in d1" style="max-width: 1100px; margin: var(--gap) auto 0; overflow-x: auto;">
    <div style="display: grid; grid-template-columns: 130px repeat(6, 1fr); gap: 2px; min-width: 800px;">
      <!-- ヘッダー -->
      <div style="font-weight: 700; font-size: var(--size-small);">タスク</div>
      <div style="text-align: center; font-family: var(--font-mono); font-size: var(--size-label); color: var(--c-text-muted);">4月</div>
      <div style="text-align: center; font-family: var(--font-mono); font-size: var(--size-label); color: var(--c-text-muted);">5月</div>
      <div style="text-align: center; font-family: var(--font-mono); font-size: var(--size-label); color: var(--c-text-muted);">6月</div>
      <div style="text-align: center; font-family: var(--font-mono); font-size: var(--size-label); color: var(--c-text-muted);">7月</div>
      <div style="text-align: center; font-family: var(--font-mono); font-size: var(--size-label); color: var(--c-text-muted);">8月</div>
      <div style="text-align: center; font-family: var(--font-mono); font-size: var(--size-label); color: var(--c-text-muted);">9月</div>
      <!-- 行 -->
      <div style="font-size: var(--size-small); display: flex; align-items: center;">要件定義</div>
      <div style="grid-column: 2 / 4; background: var(--c-primary); border-radius: 4px; height: 28px;" class="bar-animate" data-width="100%"></div>
      <div style="grid-column: 4 / 8;"></div>
      <!-- 追加行... -->
    </div>
  </div>
</section>
```

### 37. kpi-dashboard（KPIダッシュボード）
**構造:** 4〜6個のメトリクスカード。各カードに数値、トレンド矢印（↑緑/↓赤）、前期比。ミニスパークラインはCSSグラデーションで表現。
**テーマ:** `light`
**レイアウト:** `three-col` or `four-col` グリッド

```html
<section class="slide" data-theme="light">
  <h2 class="slide-title fade-in" style="text-align: center;">月次KPIレポート</h2>
  <div class="three-col fade-in d1" style="margin-top: var(--gap);">
    <div class="biz-card" style="text-align: center;">
      <p style="font-size: var(--size-small); color: var(--c-text-muted);">MRR</p>
      <div style="font-size: var(--size-h1); font-weight: 900; color: var(--c-primary);" class="countup" data-target="850" data-prefix="¥" data-suffix="万">¥0万</div>
      <p style="color: #10B981; font-weight: 700; font-size: var(--size-small);">&#x25B2; +12.3% <span style="color: var(--c-text-muted); font-weight: 400;">vs 前月</span></p>
      <div style="height: 30px; margin-top: var(--gap-xs); background: linear-gradient(90deg, var(--c-primary-light) 0%, var(--c-primary) 100%); border-radius: 4px; opacity: 0.3;"></div>
    </div>
    <div class="biz-card" style="text-align: center;">
      <p style="font-size: var(--size-small); color: var(--c-text-muted);">解約率</p>
      <div style="font-size: var(--size-h1); font-weight: 900; color: #10B981;" class="countup" data-target="2" data-suffix=".1%">0%</div>
      <p style="color: #10B981; font-weight: 700; font-size: var(--size-small);">&#x25BC; -0.5pt <span style="color: var(--c-text-muted); font-weight: 400;">vs 前月</span></p>
    </div>
    <div class="biz-card" style="text-align: center;">
      <p style="font-size: var(--size-small); color: var(--c-text-muted);">NPS</p>
      <div style="font-size: var(--size-h1); font-weight: 900; color: var(--c-accent);" class="countup" data-target="72">0</div>
      <p style="color: #EF4444; font-weight: 700; font-size: var(--size-small);">&#x25BC; -3 <span style="color: var(--c-text-muted); font-weight: 400;">vs 前月</span></p>
    </div>
  </div>
</section>
```

### 38. problem-solution（課題と解決策）★重要
**構造:** before-afterと似ているが、論理構造が異なる。左に「現状の課題」（灰/赤トーン）、右に「私たちの解決策」（青/緑トーン）。課題側に×マーク、解決側に✓マーク。
**テーマ:** `white`（パディングなし、左右で色分け）

```html
<section class="slide" data-theme="white" style="padding: 0;">
  <div style="display: grid; grid-template-columns: 1fr 1fr; height: 100%;">
    <div class="slide-in-left" style="background: #F9FAFB; padding: var(--slide-padding); display: flex; flex-direction: column; justify-content: center;">
      <span style="font-family: var(--font-mono); font-size: var(--size-label); color: var(--c-text-muted); letter-spacing: 0.1em;">PROBLEM</span>
      <h3 style="font-size: var(--size-h2); font-weight: 900; margin-top: var(--gap-xs); color: #EF4444;">現状の課題</h3>
      <div style="margin-top: var(--gap); display: flex; flex-direction: column; gap: var(--gap-sm);">
        <div style="display: flex; gap: var(--gap-sm); align-items: start;"><span style="color: #EF4444; font-size: 20px; flex-shrink: 0;">&#x2717;</span><p>課題1の詳細説明</p></div>
        <div style="display: flex; gap: var(--gap-sm); align-items: start;"><span style="color: #EF4444; font-size: 20px; flex-shrink: 0;">&#x2717;</span><p>課題2の詳細説明</p></div>
      </div>
    </div>
    <div class="slide-in-right d2" style="background: var(--c-primary-light); padding: var(--slide-padding); display: flex; flex-direction: column; justify-content: center;">
      <span style="font-family: var(--font-mono); font-size: var(--size-label); color: var(--c-primary); letter-spacing: 0.1em;">SOLUTION</span>
      <h3 style="font-size: var(--size-h2); font-weight: 900; margin-top: var(--gap-xs); color: var(--c-primary);">私たちの解決策</h3>
      <div style="margin-top: var(--gap); display: flex; flex-direction: column; gap: var(--gap-sm);">
        <div style="display: flex; gap: var(--gap-sm); align-items: start;"><span style="color: #10B981; font-size: 20px; flex-shrink: 0;">&#x2713;</span><p>解決策1の詳細説明</p></div>
        <div style="display: flex; gap: var(--gap-sm); align-items: start;"><span style="color: #10B981; font-size: 20px; flex-shrink: 0;">&#x2713;</span><p>解決策2の詳細説明</p></div>
      </div>
    </div>
  </div>
</section>
```

### 39. customer-journey（カスタマージャーニーマップ）
**構造:** 横に5〜7ステージ。各ステージにアイコン + 名前 + タッチポイント。上部にSVGの感情曲線（折れ線グラフ）。
**テーマ:** `white`
**レイアウト:** 上半分にSVG折れ線、下半分に `display: grid; grid-template-columns: repeat(5, 1fr)` のステージカード

```html
<section class="slide" data-theme="white">
  <h2 class="slide-title fade-in" style="text-align: center;">カスタマージャーニー</h2>
  <!-- 感情曲線 -->
  <svg class="fade-in d1" viewBox="0 0 500 100" style="width: 80%; max-width: 900px; margin: var(--gap-sm) auto; display: block; height: 80px;">
    <line x1="0" y1="50" x2="500" y2="50" stroke="var(--c-border)" stroke-width="1" stroke-dasharray="4"/>
    <polyline points="0,70 100,30 200,60 300,20 400,25 500,15" fill="none" stroke="var(--c-primary)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
  <!-- ステージ -->
  <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: var(--gap-sm); max-width: 1100px; margin: 0 auto;">
    <div class="fade-in d2" style="text-align: center; padding: var(--gap-sm);">
      <div style="font-size: 28px;">&#x1F50D;</div>
      <h4 style="font-weight: 700; margin-top: 4px;">認知</h4>
      <p style="font-size: var(--size-small); color: var(--c-text-muted); margin-top: 4px;">広告・SNS経由で知る</p>
    </div>
    <div class="fade-in d3" style="text-align: center; padding: var(--gap-sm);"><div style="font-size: 28px;">&#x1F4CB;</div><h4 style="font-weight: 700; margin-top: 4px;">検討</h4><p style="font-size: var(--size-small); color: var(--c-text-muted); margin-top: 4px;">資料請求・比較</p></div>
    <div class="fade-in d4" style="text-align: center; padding: var(--gap-sm);"><div style="font-size: 28px;">&#x1F4B3;</div><h4 style="font-weight: 700; margin-top: 4px;">購入</h4><p style="font-size: var(--size-small); color: var(--c-text-muted); margin-top: 4px;">契約・導入</p></div>
    <div class="fade-in d5" style="text-align: center; padding: var(--gap-sm);"><div style="font-size: 28px;">&#x1F4BB;</div><h4 style="font-weight: 700; margin-top: 4px;">利用</h4><p style="font-size: var(--size-small); color: var(--c-text-muted); margin-top: 4px;">日常利用・サポート</p></div>
    <div class="fade-in d6" style="text-align: center; padding: var(--gap-sm);"><div style="font-size: 28px;">&#x2B50;</div><h4 style="font-weight: 700; margin-top: 4px;">推奨</h4><p style="font-size: var(--size-small); color: var(--c-text-muted); margin-top: 4px;">口コミ・紹介</p></div>
  </div>
</section>
```

### 40. venn-diagram（ベン図）
**構造:** 2〜3個の半透明円を重ねて配置。各円にラベル、重なり部分にキーワード。
**テーマ:** `white`

```html
<section class="slide" data-theme="white">
  <h2 class="slide-title fade-in" style="text-align: center;">私たちの強み</h2>
  <div style="position: relative; width: 500px; height: 400px; margin: var(--gap) auto 0;">
    <div class="scale-in d1" style="position: absolute; top: 0; left: 10%; width: 280px; height: 280px; border-radius: 50%; background: rgba(59,130,182,0.2); border: 2px solid var(--c-primary); display: flex; align-items: center; justify-content: center; padding-bottom: 60px;"><span style="font-weight: 700; color: var(--c-primary);">テクノロジー</span></div>
    <div class="scale-in d2" style="position: absolute; top: 0; right: 10%; width: 280px; height: 280px; border-radius: 50%; background: rgba(245,166,35,0.2); border: 2px solid var(--c-accent); display: flex; align-items: center; justify-content: center; padding-bottom: 60px;"><span style="font-weight: 700; color: var(--c-accent);">ビジネス</span></div>
    <div class="scale-in d3" style="position: absolute; bottom: 0; left: 50%; transform: translateX(-50%); width: 280px; height: 280px; border-radius: 50%; background: rgba(16,185,129,0.2); border: 2px solid #10B981; display: flex; align-items: center; justify-content: center; padding-top: 60px;"><span style="font-weight: 700; color: #10B981;">デザイン</span></div>
    <!-- 中央の重なり -->
    <div class="blur-in d4" style="position: absolute; top: 45%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 8px 20px; border-radius: 999px; font-weight: 900; font-size: var(--size-h3); box-shadow: var(--shadow-elevated);">AX</div>
  </div>
</section>
```

### 41. checklist-status（チェックリスト/進捗一覧）
**構造:** 縦リスト。各行にステータスバッジ（完了=緑、進行中=青、未着手=灰）+ タスク名 + 担当者 + 進捗バー。
**テーマ:** `white`

```html
<section class="slide" data-theme="white">
  <h2 class="slide-title fade-in" style="text-align: center;">プロジェクト進捗</h2>
  <div style="max-width: 800px; margin: var(--gap) auto 0;">
    <div class="fade-in d1" style="display: flex; align-items: center; gap: var(--gap-sm); padding: var(--gap-sm) 0; border-bottom: 1px solid var(--c-border);">
      <span style="background: #10B981; color: white; padding: 2px 10px; border-radius: 999px; font-size: var(--size-label); font-weight: 600; min-width: 60px; text-align: center;">完了</span>
      <span style="flex: 1; font-weight: 600;">要件定義</span>
      <div style="width: 120px; height: 6px; background: var(--c-border); border-radius: 3px; overflow: hidden;"><div class="bar-animate" data-width="100%" style="height: 100%; background: #10B981; border-radius: 3px;"></div></div>
    </div>
    <div class="fade-in d2" style="display: flex; align-items: center; gap: var(--gap-sm); padding: var(--gap-sm) 0; border-bottom: 1px solid var(--c-border);">
      <span style="background: var(--c-primary); color: white; padding: 2px 10px; border-radius: 999px; font-size: var(--size-label); font-weight: 600; min-width: 60px; text-align: center;">進行中</span>
      <span style="flex: 1; font-weight: 600;">設計・開発</span>
      <div style="width: 120px; height: 6px; background: var(--c-border); border-radius: 3px; overflow: hidden;"><div class="bar-animate" data-width="60%" style="height: 100%; background: var(--c-primary); border-radius: 3px;"></div></div>
    </div>
    <div class="fade-in d3" style="display: flex; align-items: center; gap: var(--gap-sm); padding: var(--gap-sm) 0; border-bottom: 1px solid var(--c-border);">
      <span style="background: var(--c-border); color: var(--c-text-muted); padding: 2px 10px; border-radius: 999px; font-size: var(--size-label); font-weight: 600; min-width: 60px; text-align: center;">未着手</span>
      <span style="flex: 1; font-weight: 600;">テスト・検証</span>
      <div style="width: 120px; height: 6px; background: var(--c-border); border-radius: 3px;"></div>
    </div>
  </div>
</section>
```

### 42. logo-wall（導入企業ロゴ一覧）
**構造:** 4×3グリッドにクライアントロゴ（テキスト代替可）。ホバーで影が強まる。
**テーマ:** `white` or `light`

```html
<section class="slide" data-theme="white">
  <h2 class="slide-title fade-in" style="text-align: center;">導入企業</h2>
  <p class="fade-in" style="text-align: center; color: var(--c-text-muted);">業種・規模を問わず多くの企業様にご利用いただいています</p>
  <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--gap-sm); max-width: 900px; margin: var(--gap) auto 0;">
    <div class="biz-card scale-in d1" style="display: flex; align-items: center; justify-content: center; min-height: 80px; font-weight: 700; color: var(--c-text-muted);">企業A</div>
    <div class="biz-card scale-in d2" style="display: flex; align-items: center; justify-content: center; min-height: 80px; font-weight: 700; color: var(--c-text-muted);">企業B</div>
    <!-- 8〜12個 -->
  </div>
</section>
```

### 43. number-highlight（数字ハイライト）
**構造:** 3〜4個の超大型数値を横並び。装飾的なアンダーライン + ラベル。stats-highlightよりもタイポグラフィ重視でクリーンなデザイン。
**テーマ:** `blue` or `dark-blue`

```html
<section class="slide" data-theme="blue">
  <div class="center-content">
    <h2 class="fade-in" style="font-family: var(--font-mono); font-size: var(--size-body); letter-spacing: 0.15em; opacity: 0.7;">KEY NUMBERS</h2>
    <div style="display: flex; gap: calc(var(--gap) * 2); margin-top: var(--gap); flex-wrap: wrap; justify-content: center;">
      <div class="fade-in d1" style="text-align: center;">
        <div style="font-size: clamp(56px, 7vw, 100px); font-weight: 900; line-height: 1;" class="countup" data-target="500" data-suffix="+">0+</div>
        <div style="width: 40px; height: 3px; background: var(--c-accent); margin: 8px auto;"></div>
        <p style="font-size: var(--size-body); opacity: 0.8;">導入企業数</p>
      </div>
      <div class="fade-in d2" style="text-align: center;">
        <div style="font-size: clamp(56px, 7vw, 100px); font-weight: 900; line-height: 1;" class="countup" data-target="98" data-suffix="%">0%</div>
        <div style="width: 40px; height: 3px; background: var(--c-accent); margin: 8px auto;"></div>
        <p style="font-size: var(--size-body); opacity: 0.8;">継続率</p>
      </div>
      <div class="fade-in d3" style="text-align: center;">
        <div style="font-size: clamp(56px, 7vw, 100px); font-weight: 900; line-height: 1;" class="countup" data-target="47000" data-suffix="h">0h</div>
        <div style="width: 40px; height: 3px; background: var(--c-accent); margin: 8px auto;"></div>
        <p style="font-size: var(--size-body); opacity: 0.8;">年間削減時間</p>
      </div>
    </div>
  </div>
</section>
```

---
