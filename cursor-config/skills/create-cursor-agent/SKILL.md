---
name: create-cursor-agent
description: >-
  Authors Cursor Rules (.cursor/rules/*.mdc) and custom Subagents
  (.cursor/agents/*.md or ~/.cursor/agents). Use when creating or refactoring
  rules/subagents, splitting large rules, choosing subagent vs skill, setting
  model/readonly/background, or replacing repeated delegation prompts.
---

# Create Cursor Rules & Subagents（ルール・サブエージェント作成）

**Cursor Rules**（`.cursor/rules/*.mdc`）は会話への恒久コンテキスト。**カスタムサブエージェント**（`.cursor/agents/*.md` または `~/.cursor/agents/*.md`）は親エージェントが **Task で委任**する専門役割。どちらも短く・実行可能・スコープ明確に書く。

## When to Use（このスキル自体）

- ルール／サブエージェントの新規作成・分割・`description` 改善
- **サブエージェントかスキルか**の線引きを説明・設計したい
- 親が毎回載せるべきコンテキスト（サブエージェントは履歴を見ない）を整理したい

## Skill パス解決（サブエージェント・ルール設計の共通正本）

`Read` する前に、**次の順で最初に存在するパス**を使う。本文に「フルパスだけ」を書いて **`~/.cursor/skills/` に無い process 系**を参照抜けさせないこと。

1. **`<workspace>/.cursor/skills/<dir>/SKILL.md`**（リポ独自・チーム共有）
2. **`~/.cursor/skills/<dir>/SKILL.md`**（ユーザ正本）
3. **`~/.cursor/superpowers/skills/<dir>/SKILL.md`**（Superpowers / 汎用プロセス系。例: `writing-plans`, `test-driven-development`, `dispatching-parallel-agents`, `systematic-debugging`）

**プラグインキャッシュ配下**（ハッシュ変動）は、サブエージェント定義に**書かない**。Figma 等は orchestrator／`figma-canvas-builder` が `Glob` 手順を保持する。

**禁止**: 存在しないディレクトリを「正本」として書くだけにする（例: `~/.cursor/skills/writing-plans` が未展開のまま）。上記解決順を必ず書くか、実体のある場所へ symlink / 複製する。

## Subagent とは（Cursor 公式モデルに準拠）

- **専用コンテキスト**で動き、結果を親に返す。長い調査やノイズの多い出力を親から切り離せる。
- **並列実行**可（複数 Task）。コードの別領域を同時に進められる。
- **常に空のコンテキストから開始**。過去の親チャット履歴にはアクセスしない → **委任プロンプトに必要な事実・パス・制約を親が含める**。
- エディター / CLI / Cloud Agents で利用可能。

### フォアグラウンドとバックグラウンド

| モード | 挙動 | 向いていること |
|--------|------|----------------|
| フォアグラウンド | 完了まで親が待機、結果をすぐ返す | 順次・出力が直ちに必要なタスク |
| バックグラウンド | すぐ戻り、サブエージェントが独立実行 | 長時間・並列ワークストリーム |

フロントマターで `is_background: true` とする（下記）。

### 組み込みサブエージェント（設定不要）

親が適宜起動。**Explore**（広い探索・並列検索）、**Bash**（冗長なシェル出力の分離）、**Browser**（DOM スナップショット等のノイズ分離）。カスタム定義は不要。

## Subagent vs Skill（使い分け）

| サブエージェント向き | スキル向き |
|----------------------|------------|
| 長時間リサーチで **コンテキストを分けたい** | **単一用途**（changelog 生成、format など） |
| **複数ワークストリームを並列** | **手早く繰り返し**できればよい |
| **多段・専門知識**が要るタスク | **一発**で済む手順 |
| **独立して検証**したい | **別ウィンドウ不要** |

単一目的でコンテキスト分離も不要なら **Skill** やスラッシュコマンドを優先する。

## ファイルの場所と優先順位

| 種類 | パス | スコープ |
|------|------|----------|
| プロジェクト | `.cursor/agents/` | 当該リポのみ |
| 互換 | `.claude/agents/`, `.codex/agents/` | 当該リポのみ |
| ユーザー | `~/.cursor/agents/` | ユーザーの全プロジェクト |

**名前衝突**: プロジェクトが**ユーザー**より優先。`.cursor/` が `.claude/` / `.codex/` より優先。

チーム共有するなら **`.cursor/agents/` をリポにコミット**するのが一般的。

## サブエージェント定義の型（Markdown + YAML）

```markdown
---
name: security-auditor
description: Security specialist. Use when implementing auth, payments, or sensitive data.
model: inherit
readonly: true
is_background: false
---

（本文プロンプト：役割・手順・出力形式。簡潔に。）
```

### フロントマター欄

| フィールド | 必須 | デフォルト | 説明 |
|------------|------|------------|------|
| `name` | 推奨 | ファイル名から導出 | 表示・識別。小文字・ハイフン。 |
| `description` | 推奨 | — | **委任のトリガー**。Task がこれを読み要否判断。**具体的な WHEN** とパターン語（`Use proactively` / `Use when ...`）を書く。 |
| `model` | 任意 | `inherit` | `inherit`（親と同じ） / `fast`（探索・検証・大量処理向け） / 特定モデル ID。 |
| `readonly` | 任意 | `false` | `true` で編集・状態変更系シェル等が制限される。 |
| `is_background` | 任意 | `false` | `true` でバックグラウンド実行。 |

**モデル**: 深い推論は `inherit`、速度・コスト重視の捜査・検証は `fast`。組織制限・Max Mode・プランで**フォールバック**することがある。

自動委任を促すなら `description` に **いつ委任するか**を明示する（例: `Use proactively for ...`）。

## 呼び出し

- **明示**: プロンプトで `/agent-name`（例: `/verifier confirm the auth flow`）または自然文で「○○ subagent を使って」。
- **並列**: 1 メッセージ内で複数 Task → 同時実行されやすい。
- **再開**: 実行ごとに agent ID が返る。`Resume agent <id> and ...` で継続（長時間・バックグラウンド後も可）。

## 通用 Best Practices（ルール＋サブエージェント）

1. **1 サブエージェント＝1 責務**。「汎用 helper」を量産しない。
2. **`description` を最重視** — ここが委任の成否を決める。実際に投げて呼ばれるか試す。
3. **本文は簡潔** — 長大プロンプトは焦点をぼかす。詳細は Skill / ドキュメント参照。
4. **500 行以内** — ルール・定義が肥大化したら**分割**し、参照はパスで。
5. **ファイル参照を優先** — 規約全文は貼らない。正本パス + 「必要時 Read」。
6. **Hooks** — サブエージェントに**構造化出力ファイル**を書かせる場合、後処理の一貫性は hooks 検討。

### Cursor Rule（.mdc）の型（リマインダ）

```markdown
---
description: ...
globs: "**/*.ts"
alwaysApply: false
---
# ...
```

## Avoid（ルール・サブエージェント共通）

| 避ける | 代わり |
|--------|--------|
| スタイルガイド全文 | Linter。ルールには設定ファイルへの参照のみ |
| 一般 CLI の網羅リスト | 案件固有の既定コマンドだけ |
| 「一般的なタスク用」など**曖昧な description** | **具体的なシーン**（例: OAuth 実装時） |
| サブエージェントだらけ（似た役割が数十本） | **まず 2〜3 本**に絞り、明確な差分があるときだけ追加 |
| 単一目的・分離不要なのにサブエージェント | **Skill / スラッシュコマンド** |
| コードベースの重複貼付 | 正本パスを参照 |

## よくあるパターン（設計ヒント）

- **Verifier**: 完了報告を**疑って**テスト・実装確認。`model: fast` も選択肢。
- **Orchestrator（親）**: Planner → Implementer → Verifier のように**構造化された引き継ぎ**を明示。
- **Debugger / Test-runner**: 再現・根因・再実行までを手順化。test-runner は「proactively」を description に。

## パフォーマンス・コスト（目安）

- サブエージェントは**それぞれ**トークンを消費。並列 n 本 ≒ 概ね n 倍に近い負荷になりうる。
- **単純・短時間**はメインの方が速いこともある。利点は**分離・並列・専門化**。
- オーバーヘッド：**起動時にコンテキストを取りにいく**コストあり。

## Instructions（作成フロー）

1. **Rules か Subagent か**を上表で決める。
2. サブエージェントなら **`description` に WHEN を具体化**（自動委任なら proactive フレーズ検討）。
3. **`model` / `readonly` / `is_background`** を用途に合わせる。
4. 本文は **手順・出力形式・禁止**を短く。長文は Skill や `docs/` へ。
5. 親向けメモ: 委任時は**履歴にない前提**でコンテキストを渡す。
6. **Checklist** で仕上げ。

## Checklist

- [ ] 1 ファイル＝1 焦点。汎用「helper」量産になっていない
- [ ] `description` に **具体的なトリガー**（必要なら proactive）
- [ ] 本文が過長でない（参照で済ませている）
- [ ] Rules: `description` / `globs` / `alwaysApply` が意図と一致
- [ ] Subagent: `model` / `readonly` / `is_background` が意図と一致
- [ ] 単一目的タスクを無理にサブエージェント化していない（Skill 候補ではないか）
