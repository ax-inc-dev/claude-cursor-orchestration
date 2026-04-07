# Cursor オーケストレーション用バンドル

このディレクトリは、**Cursor エディタ側**でオーケストレーション（開発ゲート・並列レビュー・サイト／プロダクト設計フロー）を再現するための設定ファイル集です。リポジトリをクローンしたユーザーが、手元の `~/.cursor/` に同じ構成を置けるようにしています。

バンドル内のパスは **`~/`（ホームディレクトリ）基準**に正規化済みです。特定ユーザー名の絶対パスは含みません。

---

## ディレクトリ構成

```
cursor-config/
├── README.md                 # 本ファイル
├── skills/<skill-name>/SKILL.md   # Agent Skills（20 件）
├── agents/*.md               # Subagent 定義（7 件）
└── rules/
    ├── CURSOR_GLOBAL_RULES.md      # グローバル方針・ゲート・レビュー表
    └── global-agent-workflow.mdc   # 常時適用ルール（ワークフロー表）
```

---

## インストール方法

### A. `setup.sh` を使う（推奨）

リポジトリルートで `./setup.sh` を実行すると、**Step 6** で次が `~/.cursor/` にコピーされます。

- `cursor-config/skills/*` → `~/.cursor/skills/<name>/SKILL.md`
- `cursor-config/agents/*.md` → `~/.cursor/agents/`
- `cursor-config/rules/CURSOR_GLOBAL_RULES.md` → `~/.cursor/CURSOR_GLOBAL_RULES.md`
- `cursor-config/rules/global-agent-workflow.mdc` → `~/.cursor/rules/global-agent-workflow.mdc`

**既に同名ファイルがある場合は上書き前に確認**されます（対話プロンプト）。

### B. 手動コピー

1. `skills` 各フォルダを `~/.cursor/skills/` にマージ（各 `SKILL.md` を同名ディレクトリへ）。
2. `agents/*.md` を `~/.cursor/agents/` へ。
3. `CURSOR_GLOBAL_RULES.md` を `~/.cursor/` へ。
4. `global-agent-workflow.mdc` を `~/.cursor/rules/` へ。

Cursor の **Settings → Rules** で、短いユーザールールを登録する場合は `CURSOR_GLOBAL_RULES.md` 末尾の「設定に貼る短い文」を参照してください。

---

## スキル一覧とカテゴリ

| カテゴリ | 件数 | スキル ID | 用途の要約 |
|---------|------|-----------|------------|
| **レビュー** | 8 | `review-app-product`, `review-security`, `review-qa`, `review-architecture`, `review-frontend`, `review-backend`, `review-infra`, `review-test` | 変更差分の観点別レビュー。並列レビュー（アプリ／セキュリティ／QA／アーキ）の前に該当 SKILL を `Read`。 |
| **デザイン（プロダクト／Figma／DESIGN.md）** | 4 | `user-first-product-design`, `product-ui-ux-design`, `design-md-reference`, `figma-mcp-design-orchestrator` | コード前の体験設計、UI/UX 設計、`DESIGN.md` 契約、Figma MCP の進行。 |
| **サイト制作** | 4 | `site-build-orchestrator`, `site-e2e-playwright`, `b2b-site-strategy-and-ia`, `shadcn-motion-ui-brief` | LP/コーポの IA・実装オーケストレーション、Playwright E2E、B2B 戦略、shadcn + Motion のブリーフ。 |
| **オーサリング** | 2 | `create-cursor-skill`, `create-cursor-agent` | 再利用可能な Skill / Subagent 定義の作成・整理。 |
| **特化** | 2 | `biz-presentation-engine`, `tailwind-product-ui-conventions` | 法人向け HTML スライド、Tailwind ベースのプロダクト UI 規約。 |

**注:** `using-superpowers` や `brainstorming` など、このバンドル外のスキルへの参照が `global-agent-workflow.mdc` に含まれる場合があります。必要に応じて [Superpowers](https://github.com/obra/superpowers) 等を別途インストールしてください。

---

## Subagent（`agents/`）と使いどころ

| ファイル | いつ使うか |
|----------|------------|
| `figma-ux-spec-lead.md` | Figma を直接操作せず、`docs/design/` などに UX 仕様・要件を整理するとき。 |
| `figma-canvas-builder.md` | Figma MCP でキャンバス操作（`use_figma` 等）するとき。**事前に `figma-use` SKILL を Glob+Read** する前提。 |
| `product-ui-ux-designer.md` | アプリ・ダッシュボード系の **設計のみ**（実装禁止でワイヤー・IA・状態設計を任せるとき）。成果物は多くの場合 `docs/ux-design/`。 |
| `site-design-planner.md` | マーケ／コーポサイトの **設計計画のみ**。ユーザーの **`計画承認`** まで実装に進まない。 |
| `site-frontend-implementer.md` | **`計画承認` 後**のフロント実装。`docs/site/*` 等を契約として実装。 |
| `site-quality-auditor.md` | 実装後の品質・整合性の **読み取り中心の監査**。 |
| `site-e2e-runner.md` | ユーザーが **`E2E実行`** と合図したときの Playwright E2E。`site-e2e-playwright` SKILL と連携。 |

チャットや Composer からは、各ファイル先頭で定義されている **Subagent 名**（例: `/site-design-planner`）で起動できます。

---

## ルールファイル（`rules/`）

| ファイル | 役割 |
|----------|------|
| **`CURSOR_GLOBAL_RULES.md`** | Cursor の運用の「正本」に相当：日本語応答、CLI はエージェント実行、秘密情報、**開発ゲート**（設計→テスト→実装→静的→自動テスト→多ラウンドレビュー→E2E→PR）、チャット合図、レビュー用スキルへのパス表、Superpowers 利用方針。Cursor 設定に貼る **短いルール文** もここに記載。 |
| **`global-agent-workflow.mdc`** | `alwaysApply: true` を想定。**Superpowers の場所**、`~/.cursor/skills/` への参照、状況別に読む SKILL の表、プロダクト UI/UX・Figma・サイト制作・Subagent の対応表、フロント実装順序（設計先行）、4 並列レビュー合図など、エージェントの日常動作を束ねる。 |

---

## このリポジトリとの関係

- **クローン先のプロジェクト**用の `.cursor/rules` や `AGENTS.md` は、案件ごとに別途置く想定です。
- 本バンドルは **ユーザー環境全体で共有する `~/.cursor/`** 向けです。`setup.sh` がリポジトリ付属の正本からホームへ展開します。

アップデート時は、リポジトリの `cursor-config/` を `git pull` したうえで `setup.sh` を再実行するか、差分のみ手動コピーしてください。
