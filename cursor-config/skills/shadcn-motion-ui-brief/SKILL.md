---
name: shadcn-motion-ui-brief
description: shadcn/ui と Motion を使うマーケ・コーポ向け UI の判断基準。a11y・motion・セクション構造・コンポーネント再利用のブリーフ作成用（全PJ共通）。
---

# shadcn/ui + Motion UI Brief

## When to Use

- [site-build-orchestrator](../site-build-orchestrator/SKILL.md) の Phase 2
- 「リッチにしたいが安っぽくなった」「動きが気持ち悪い」と言われたときの見直し
- **`DESIGN.md`（Stitch / awesome-design-md）**で色・タイポ・Elevation が既に固定されている → **[design-md-reference](../design-md-reference/SKILL.md)** と併読し、Motion はそのトーンに従い **過剰にならない**よう調整する

## 原則

1. **見た目のリッチさより情報の階層**（見出しレベル・余白・1 画面の主メッセージは 1 つに近づける）
2. **shadcn/ui** は Radix 由来の **フォーカス・キーボード**を活かす。`div` + `onClick` だけの Primary 操作を増やさない
3. **Motion** は補助。ヒーロー・初回ビューポート以外は **控えめ**

## セクション構造（B2B LP のデフォルト例）

案件で差し替えてよい。**作業リポの** `docs/site/ui-brief.md` に採用可否と理由を書く。

1. Hero（価値提案・主 CTA・補助リンク）
2. 信頼の帯（ロゴ／数値のいずれか）
3. 課題共感 → 解決の骨子
4. サービス／プロセス
5. 事例・証拠
6. FAQ / 反論処理
7. 終結 CTA

## shadcn/ui

- **優先**: `Button` / `Card` / `Accordion` / `NavigationMenu` / `Sheet`（モバイル）など、設計に合うプリミティブから選ぶ
- **1 画面あたりの variant 濫用を避ける**（ボタンサイズ・カード種類は理由のない増殖を禁止）
- **Dialog / Sheet** は Escape・フォーカストラップを壊さない（可能なら既存コンポーネントを維持）

## Motion（Framer Motion 想定）

- **`prefers-reduced-motion: reduce`** のときは **アニメなしまたは即時表示**（ユーザーの OS 設定を尊重）
- **viewport 入場**: 一度きり（`whileInView` 等）を基本。無限リピートで注目を奪わない
- **stagger**: 子の間隔は短く（目安 50〜100ms 級）。遅延の積み上げで操作可能時間を遅らせない
- **`layout` アニメ**: CLS（レイアウトシフト）やジャークの原因になりやすい。**必要箇所のみ**、検証してから

## 出力（`docs/site/ui-brief.md` 向け）

- 採用セクション一覧と **各セクションで許可する motion の種類**（なし / フェード / 軽いスライド 等）
- **禁止**: 自動再生の派手なパララックス、ヒーロー以外での長い stagger 連打
- プロジェクトで shadcn の CLI や registries を使う場合は、そのリポの公式ドキュメントに従う（本 Skill はブリーフ専用）

## 関連

- トークン・ユーティリティ規約: [tailwind-product-ui-conventions](../tailwind-product-ui-conventions/SKILL.md)
