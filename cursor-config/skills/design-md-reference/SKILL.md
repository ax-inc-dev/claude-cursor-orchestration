---
name: design-md-reference
description: >-
  Uses Google Stitch–format DESIGN.md as the UI contract: VoltAgent
  awesome-design-md (https://github.com/VoltAgent/awesome-design-md.git)
  presets or custom DESIGN.md, token mapping to Tailwind/shadcn, conflict
  rules vs docs/site or docs/ux-design. Use when the user clones or copies
  from awesome-design-md, adds DESIGN.md, picks a preset site, or wants
  strong agent-readable UI reference without Figma. Always Read this SKILL
  before reading preset DESIGN.md files per global-agent-workflow.mdc.
---

# DESIGN.md リファレンス（Stitch 形式・エージェント向け）

## When to Use

- ユーザーが **DESIGN.md** をリポに置いた、または **VoltAgent [awesome-design-md](https://github.com/VoltAgent/awesome-design-md)** から特定サイトの一式を **clone / コピー**した
- **Figma が無い／未完**でも、タイポ・色・余白・Elevation をエージェント可読な平面テキストで固定したい
- 実装前に **ビジュアル基準**（ライト/ダーク）を `preview.html` で確認したい

グローバルルール **`~/.cursor/rules/global-agent-workflow.mdc`**（技能表の **DESIGN.md / awesome-design-md** 行）および **`~/.cursor/CURSOR_GLOBAL_RULES.md`**（DESIGN.md・awesome-design-md 節）でも本 SKILL が必読として指されている。

## awesome-design-md リポジトリ（Git 正本）

| 項目 | 値 |
|------|-----|
| **clone URL** | **`https://github.com/VoltAgent/awesome-design-md.git`** |
| **プリセットのパス** | リポジトリ内 **`design-md/<サイト名>/`** に **`DESIGN.md`**、`preview.html`、`preview-dark.html` など |
| **推奨ローカル置き場（例）** | `~/.cursor/third-party/awesome-design-md`（初回だけ `git clone`。更新は `git pull --ff-only`） |
| **作業プロジェクトでの使い方** | 選んだサイトフォルダから **`DESIGN.md`（＋任意で preview）** を **`docs/design/`** またはリポルートへコピー。エージェントは **作業リポ上のパス**を主に `Read`（clone 直参照でも可だが、チーム共有ならコピーを推奨） |

個々の **`design-md/*/DESIGN.md` はスキルファイルではない**。エージェント向けの**手順と優先ルール**は **本 `SKILL.md`** にあり、各プリセットは **データ（Read 対象の Markdown）** として扱う。

## What DESIGN.md Is

- [Google Stitch — DESIGN.md 概要](https://stitch.withgoogle.com/docs/design-md/overview/)
- [フォーマット仕様](https://stitch.withgoogle.com/docs/design-md/format/)
- **AGENTS.md** がビルド手順、**DESIGN.md** が見た目・トーンの契約、という役割分け（リポに両方あれば両方 `Read`）

各プリセット（awesome-design-md）には通常:

| ファイル | 用途 |
|----------|------|
| `DESIGN.md` | エージェントが Read する正本（9 セクション構成が多い） |
| `preview.html` / `preview-dark.html` | スウォッチ・タイポのビジュアル確認（人間・ブラウザ MCP） |

## Instructions

1. **正本の場所を決める**  
   - リポルートの `DESIGN.md` か、`docs/design/DESIGN.md` など **1 箇所**に固定。散在させない。  
   - ユーザーが「このサイトのトーン」と言ったら、awesome-design-md 内の **該当ディレクトリ**から `DESIGN.md` と preview をコピー。

2. **`Read` の順**  
   - まず **DESIGN.md 全文**（セクション構造: Visual Theme / Color / Typography / Components / Layout / Elevation / Do-Don'ts / Responsive / Agent Prompt Guide）。  
   - 既存の **`tailwind-product-ui-conventions`** と **`shadcn-motion-ui-brief`**（サイト系なら `docs/site/ui-brief.md`）を読み、**衝突するルール**を列挙する。

3. **トークンを実装へ写す**  
   - 色・フォント・シャドウは **CSS 変数または Tailwind theme** に落とし、コンポーネントは **shadcn の variant / cn()** で寄せる。  
   - DESIGN.md の数値は **推奨デフォルト**として使い、プロジェクトの a11y・ブランド制約があればそちらを優先（ユーザーに一言確認）。

4. **優先順位（矛盾時）**  
   1. ユーザー明示  
   2. プロジェクト既存の **`docs/site/*`** または **`docs/ux-design/*`**（承認済み設計）  
   3. ルート／`docs/design/` の **DESIGN.md**  
   - 食い違いは PR か返信で「どちらを正にするか」1 行だけ確認。

5. **プレビュー**  
   - `preview.html` がある場合、必要ならブラウザで開き、実装後の画面と **セマンティック対応**（Primary / Surface / 見出し階層）を突き合わせる。スクリーンショット比較は任意。

6. **著作権・ブランド**  
   - awesome-design-md は公開 UI からの抽出で **インスピレーション用**。そのままロゴ・固有名を製品に流用しない。社内ブランドがある場合は DESIGN.md を **自社トークンに差し替え**た版を正とする。

## Relationship to Other Skills

- **サイト制作**: `site-build-orchestrator` / Phase 2 の `ui-brief.md` と併用可。DESIGN.md を **トークン正本**、`ui-brief` を **プロジェクト固有コピー・CTA** にするとぶつかりにくい。
- **Figma 派**: `figma-mcp-design-orchestrator` と両立。Figma 実装時は DESIGN.md を「フォールバック／モードボード」にしない。ユーザーがどちらを主にするか決める。
- **Tailwind**: `tailwind-product-ui-conventions` を必ず併読し、任意値乱発を避ける。

## Checklist

- [ ] `DESIGN.md` のパスがプロジェクトで合意されている
- [ ] Color / Typography / Elevation がコード側トークンに対応づけがある
- [ ] 既存 `docs/site` または `docs/ux-design` との矛盾を解消した（またはユーザー確認済み）
- [ ] `preview.html` がある場合、主要サーフェスを一度は目視または MCP で確認した
