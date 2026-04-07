---
name: site-build-orchestrator
description: LP・コーポレート・サービスページのサイト制作（全PJ共通）。Skill + Subagent で Phase 委譲。戦略→設計→（計画承認）→実装→監査→E2E（Playwright / MCP）。
---

# Site Build Orchestrator（ユーザー共通）

## When to Use

- ユーザーが LP / コーポレート / サービスページ / ランディングの新規・刷新を依頼したとき
- Use **proactively**: Agent はサイト系の依頼で **まず本 SKILL を Read** し、続けて **Subagent 委譲**を検討する

本 Skill・Subagent は **`~/.cursor/skills/`**（および **`~/.cursor/superpowers/skills/`** の process 系）と **`~/.cursor/agents/`** を参照し、**どのワークスペースでも**利用可能。

### Skill パス解決（Read 前に必ず適用）

1. `<workspace>/.cursor/skills/<dir>/SKILL.md`
2. `~/.cursor/skills/<dir>/SKILL.md`
3. `~/.cursor/superpowers/skills/<dir>/SKILL.md`

以下の **`<dir>`** はすべてこの順で解決する（表記の `~/.cursor/skills/` は「ユーザ側の主たる置き場」の意味で、2 が無ければ 3）。

`<SUBAGENT-STOP>`  
親エージェントは **本 SKILL を Read したうえで**、Phase に応じて **`~/.cursor/agents/`** の Subagent へ **Task 委譲**する。渡すプロンプトに必ず含める: **(1) ワークスペースルート** **(2) `docs/site` のパス（または project-slug サブフォルダ）** **(3) ユーザーが述べた目的 1 文** **(4) いま何 Phase か**。  
サブエージェント定義の全文を貼り付けず、**役割名 + 上記コンテキスト**でよい。  
`</SUBAGENT-STOP>`

## グローバル Subagent（全PJ・正本 `~/.cursor/agents/`）

| Phase | Subagent ファイル | slash 例 | 役割 |
|-------|-------------------|-----------|------|
| 0–3 設計のみ | `site-design-planner.md` | `/site-design-planner` | `docs/site/*` のみ編集。実装禁止。 |
| 4 実装 | `site-frontend-implementer.md` | `/site-frontend-implementer` | **`計画承認` 後のみ**。`docs/site` を真実としてコード化。 |
| 5 監査 | `site-quality-auditor.md` | `/site-quality-auditor` | 読み取り中心。`review-*` SKILL と突合。 |
| **E2E** | **`site-e2e-runner.md`** | **`/site-e2e-runner`** | **`E2E実行`** または実装直後。Playwright CLI + 任意で MCP **`user-playwright`**。 |

**委譲の流れ（Orchestrator pattern）**

1. 親 Agent: 本 SKILL を Read → **`/site-design-planner`** に **目的・ルート・slug** を渡す。  
2. ユーザーが **`計画承認`** と返すまで Phase 4 に進めない。  
3. **`/site-frontend-implementer`**（計画承認済みを明示）。  
4. **`/site-quality-auditor`** で監査（ルールのレビューラウンドに従う）。  
5. ユーザーが **`E2E実行`** したとき（または実装・監査後に E2E を任せるとき）**`/site-e2e-runner`**。手順の正本は **`~/.cursor/skills/site-e2e-playwright/SKILL.md`**。

親が Subagent を使わない場合でも、**Phase 順とゲートは本 SKILL に従う**。

## 成果物テンプレ（初回のみ）

- **正本**: `~/.cursor/templates/docs-site/`  
- 作業リポ: `mkdir -p docs/site && cp -R ~/.cursor/templates/docs-site/* docs/site/`

## 絶対ゲート（ルールの優先順）

1. **ワークスペース**に `.cursor/rules/agent-workflow.mdc` があれば **最優先**。なければ **`~/.cursor/rules/global-agent-workflow.mdc`**。
2. **`計画承認` があるまで** Phase 4（実装）に進めない。
3. `計画承認` 後は **設計完了 → テスト実装 → プロダクト実装 → 静的 → 自動テスト** を短縮しない（ルールファイルのゲート順）。
4. レビュー SKILL: ワークスペース `.cursor/skills/review-*` を優先、無ければ **`~/.cursor/skills/review-*`**。
5. **E2E**: **`docs/site/e2e-scenarios.md`** に沿い、**`~/.cursor/skills/site-e2e-playwright/SKILL.md`** を参照。CLI 優先、補助として MCP **`user-playwright`**。ユーザーの **`E2E実行`** で Phase E2E 開始。

## 成果物（プロジェクトルート相対）

| ファイル | 役割 |
|----------|------|
| `docs/site/PRD.md` | 目的・スコープ・成功指標 |
| `docs/site/ia-decision-map.md` | 戦略・IA・意思決定マップ |
| `docs/site/section-copy.md` | コピー・CTA |
| `docs/site/ui-brief.md` | UI / Motion / Tailwind |
| `docs/site/e2e-scenarios.md` | 受け入れ・E2E（Playwright / MCP 対応表を書く） |

## Phase 0 — 目的の固定

（`site-design-planner`）目的 1 文、`docs/site` 初期化。

## Phase 1 — 戦略・IA

1. **`Read`**: `~/.cursor/skills/b2b-site-strategy-and-ia/SKILL.md`  
2. `docs/site/PRD.md`, `docs/site/ia-decision-map.md`

## Phase 2 — コピー・UI ブリーフ

1. **`Read`**: `~/.cursor/skills/shadcn-motion-ui-brief/SKILL.md`, `~/.cursor/skills/tailwind-product-ui-conventions/SKILL.md`  
2. `docs/site/section-copy.md`, `docs/site/ui-brief.md`

## Phase 3 — テスト指示

1. 任意で **`Read`**: **`writing-plans`** と **`site-e2e-playwright`**（上記「Skill パス解決」。`writing-plans` は多くの環境で `superpowers` 側のみ）  
2. `docs/site/e2e-scenarios.md` → **ユーザー確認 → `計画承認` を待つ**

## Phase 4 — 実装

1. 任意で **`Read`**: **`test-driven-development`**（パス解決同上。未 clone の場合は `~/.cursor/superpowers` を `git clone` するか、リポに TDD 方針を別途書く）  
2. `docs/site/*` に従い実装（`site-frontend-implementer`）。**Playwright スペック**は `e2e-scenarios.md` と突き合わせて追加・更新する。

## Phase 5 — 監査

- **`site-quality-auditor`**。コア 4 + `review-frontend` + 任意で **`review-test`**（E2E 変更時）。

## Phase E2E — Playwright / MCP

- ユーザー **`E2E実行`** または親の委譲で **`/site-e2e-runner`**。  
- **`Read` 必須**: `~/.cursor/skills/site-e2e-playwright/SKILL.md`

## 参考

- Agent: https://www.cursor.com/blog/agent-best-practices  
- Subagents: https://cursor.com/docs/subagents.md  
