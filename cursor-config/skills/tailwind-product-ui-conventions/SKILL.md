---
name: tailwind-product-ui-conventions
description: プロダクト品質の Tailwind 運用。cn()、デザイントークン、任意値の抑制、タイポ階層、コンテナクエリの判断（全PJ共通）。
---

# Tailwind Product UI Conventions

## When to Use

- [site-build-orchestrator](../site-build-orchestrator/SKILL.md) Phase 2 以降の実装
- クラス列挙がページごとにバラバラになってきたときのリセット
- リポに **Google Stitch 形式の `DESIGN.md`**（例: [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) からコピー）がある → トークン・タイポの出典として **`Read`** **[design-md-reference](../design-md-reference/SKILL.md)** し、`DESIGN.md` と本 SKILL を両方満たすようマッピングする

## 規約

### レイアウト・スペーシング

- 余白は **限られたスケール**に寄せる（例：`4 / 6 / 8 / 12 / 16 / 24` のようにプロジェクトで一覧化）。**都度のピクセル任意値**は例外として理由をコメント or PR 説明に残す
- セクション縦リズムは **繰り返しパターン**でそろえる（`py-*` がセクションごとに無秩序に変わらないように）

### 色・タイポ

- 色とコントラストは **CSS 変数（デザイントークン）** 経由を優先。hex のベタ貼り乱用を避ける
- **見出しレベル（h1〜h3）と視覚スタイル**を一致させ、SEO/a11y と見た目を対応させる

### `cn()` / 条件クラス

- `clsx` + `tailwind-merge` の `cn()` パターンに寄せ、競合クラスを merge で解決する

### 任意値・レスポンシブ

- `w-[372px]` のような **任意値は必要最小限**。まず標準スケール・`max-w-*`・grid で足りないか検討
- **コンテナクエリ**（`@container`）：カード内でブレークポイントが変わるときに検討。ページ全体の `sm/md/lg` だけでは足りない **コンポーネント単位**の折り返しに使う

### アンチパターン

- 同じ UI を **微妙に違うクラス列**で複製しない（コンポーネント化または variant 化）
- 「とりあえず shadow や ring を足す」だけで階層をごまかさない

## 出力

実装フェーズでは **作業リポの** `docs/site/ui-brief.md` のトーンに沿い、新規ユーティリティを増やすなら **トークン側に寄せるか**を一言判断してからコードにする。
