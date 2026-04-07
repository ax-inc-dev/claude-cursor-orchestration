---
name: figma-mcp-design-orchestrator
description: Figma MCP で「設計を Figma 上で完結」させる進行役。ユーザーファースト成果物→Canvas/MCP 実行。figma-use 必須・公式付属 Skill 連携（全PJ共通）。
---

# Figma MCP Design Orchestrator（全PJ共通）

## When to Use

- ユーザーが **Figma で画面／デザインシステム／LP を作り切りたい**、`figma.com` URL を渡した、**コードより先にデザイン**を固めたいとき
- Use **proactively**：Figma・デザインハンドオフ・Make・FigJam に触れる前に本 SKILL を Read

## 絶対順序（Web・チュートリアルと Figma 公式 INSTRUCTIONS の準拠）

1. **`Read`**: [user-first-product-design](../user-first-product-design/SKILL.md) — **外形（Figma）に入る前に**アウトカムとタスクを固定する。  
2. **成果物**（任意）: `docs/design/ux-brief.md` 等に落とす — テンプレは **`~/.cursor/templates/docs-design/`**  
3. **Figma MCP** の **読み取り／デザイン→コード**なら **`get_design_context`** を中核に（節「Design-to-code」）。  
4. **Figma への書き込み**（変数・コンポーネント・オートレイアウト・キャンバス編集）は **`use_figma` のみ**。**その前に必ず `figma-use` Skill を全文 Read**（公式 MANDATORY）。  
5. **Web ページを初めて Figma に取り込む**用途は **`generate_figma_design`**。既存フレームの更新・同期は基本 **`use_figma`**（公式 INSTRUCTIONS の使い分け）。  
6. コンポーネントを増やす前に **`search_design_system`**（既存を流用）。

## Figma 付属 Skill の場所（この Mac）

プラグインキャッシュはハッシュで変わり得る。**必ず** 次を `Glob` で探してから `Read` すること。

- 優先パターン: `~/.cursor/plugins/cache/**/figma-use/SKILL.md`
- 同ディレクトリの `figma-generate-design` / `figma-implement-design` / `figma-code-connect-components` など

| やりたいこと | 読む Skill（最低限） | MCP ツールの目安 |
|-------------|---------------------|-----------------|
| キャンバスに書く・変数・コンポーネント | **figma-use** | `use_figma`（`skillNames: "figma-use"`） |
| コード／説明から **画面全体**を Figma に | **figma-use** + **figma-generate-design** | `use_figma` + `search_design_system`、必要なら `generate_figma_design` |
| Figma から **コード実装** | **figma-implement-design** | `get_design_context` |
| コード ↔ コンポーネント対応 | **figma-code-connect-components** | Code Connect 系ツール |

`call_mcp_tool` の **server** は環境により **`plugin-figma-figma`**（identifier）。利用前に MCP ディスクリプタでサーバー名を確認する。

## URL から fileKey / nodeId

公式パース（INSTRUCTIONS 準拠）:

- `figma.com/design/:fileKey/:fileName?node-id=1-2` → `nodeId` は **`1:2`**（ハイフンをコロンに）
- ブランチ URL: `.../design/:fileKey/branch/:branchKey/...` → **`fileKey` には branchKey を使う**
- `figma.com/make/...` → Make ファイルキー
- `figma.com/board/...` → FigJam（`get_figjam` 等）

## デザイン・ファイルのベストプラクティス（調査ソースの合意）

- **Auto Layout** を前提に（読みやすい階層・実装時の一貫性）
- **Variables／トークン**で色・余白・角丸・タイポを持つ（ハードコード地獄を避ける）
- **コンポーネント**で再利用。増殖前に **`search_design_system`**
- 巨大フレームを避け、**セクション単位**で `use_figma` を分割（figma-use の「小ステップ」）
- **Design-to-code** で返ったコードは **参照用**。プロジェクトのスタック・既存 DS に合わせて改める（公式 INSTRUCTIONS）

## Subagent 委譲（全PJ `~/.cursor/agents/`）

| 段階 | Subagent | slash |
|------|-----------|-------|
| UX 仕様のみ（Figma 触らない） | `figma-ux-spec-lead` | `/figma-ux-spec-lead` |
| キャンバス構築・変数・コンポーネント | `figma-canvas-builder` | `/figma-canvas-builder` |

親エージェントは **Task にワークスペースルート・Figma URL・fileKey・対象ページ名・user-first の要約**を渡す。

`<SUBAGENT-STOP>`  
`figma-canvas-builder` に **figma-use の全文**を貼らない。**「fileKey」「やること」「参照フレーム名」**と **figma-use を Read 済み**で委譲する。  
`</SUBAGENT-STOP>`

## Design-to-code（実装フェーズ）

1. `get_design_context(fileKey, nodeId, ...)` — スクリーンショットは **デフォルトで残す**（`excludeScreenshot` はユーザーが省けと言ったときのみ）  
2. Code Connect・注釈・CSS 変数ヒントを優先し、**プロジェクトのコンポーネント**にマッピング  
3. 実装 Skill: **figma-implement-design** を Read

## 参考リンク

- Cursor × Figma MCP の補助説明例: [Builder.io — Figma MCP Server](https://www.builder.io/blog/figma-mcp-server)  
- 「トークン準備がコード品質を決める」系の記事群と整合（設計前に変数化）
