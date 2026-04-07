---
name: create-cursor-skill
description: >-
  Authors reusable Agent Skills (SKILL.md) for personal (~/.cursor/skills/) or
  project (.cursor/skills/) scope. Use when the user wants to create, split, or
  refactor a skill; standardize skill shape; or migrate repeated chat prompts
  into a skill. Complements Cursor's built-in create-skill in skills-cursor.
---

# Create Cursor Skill（ユーザースキル作成）

個人用・プロジェクト用の **Agent Skill**（`SKILL.md`）を、短く・発見しやすく・再利用しやすい形で書くための手順。

## When to Use

- 同じ指示をチャットで繰り返している → **スキル化**して再利用する
- ワークフロー・判断基準・ドメイン手順をエージェントに固定したい
- 既存スキルを分割・統合し、**500 行以内**と参照の深さを守りたい
- 「トリガー語」と「何をするか」を description に落とし込みたい

## Relationship to Built-ins

- Cursor 同梱の一般的ガイドは `~/.cursor/skills-cursor/create-skill` を参照してよい（**`skills-cursor` への新規作成はしない**）。
- 本スキルは **あなたのホーム正本**（`~/.cursor/skills/`）向けに、下記の**型**と抽象チェックリストを固定する。

## Canonical Shape（型）

新規 `SKILL.md` は次の骨格から外さない。長文化したら **セクションごとに `reference.md` 等へ退避**（参照は SKILL から **1 ホップ**）。

```markdown
---
name: my-skill
description: Short description of what this skill does and when to use it.
---

# My Skill

Detailed instructions for the agent.（必要なら1〜2文で目的を書く）

## When to Use

- Use this skill when...
- This skill is helpful for...

## Instructions

- Step-by-step guidance for the agent
- Domain-specific conventions
- Best practices and patterns
- 要件が曖昧なら、利用可能なら質問ツールでユーザーに確認する
```

### description（フロントマター）の型

- **三人称**で書く（システムに注入される前提）。
- **WHAT（できること）+ WHEN（いつ発動するか）** を同一文字列に含める。
- トリガー語（ファイル種別・ツール名・業務キーワード）を具体的に入れる。
- `name` は **64 文字以内・英小文字・ハイフン**。

## Instructions（作成フロー）

1. **保存場所を決める**
   - 全プロジェクト共通 → `~/.cursor/skills/<skill-name>/SKILL.md`
   - リポジトリ共有 → `<repo>/.cursor/skills/<skill-name>/SKILL.md`
2. **1 スキル＝1 つの焦点**。別問題なら別ディレクトリに分割し、親 SKILL からリンクだけ張る。
3. **エージェントが既に知っている一般論は書かない**。プロジェクト固有の例外・ゲート・パス・禁止事項だけを優先する。
4. **コードや規約の全文は貼らない**。正本ファイルへのパスを書き、「必要時に Read」と指示する。
5. **長い例・API 表・チェックリスト大全**は `reference.md` / `examples.md` に分離。SKILL には「最短手順 + リンク」だけ残す。
6. **SKILL.md は 500 行以内**を上限とし、超えるなら分割か progressive disclosure。
7. **用語を統一**（同一概念に別名を混在させない）。
8. 最後に **自己チェック**（下記 Checklist）。

## Abstract Patterns（横展開の考え方）

どんなドメインでも次に分解すると保守しやすい。

| パターン | SKILL に残すもの | 別ファイルへ |
|----------|------------------|--------------|
| 手順型 | フェーズ見出し + チェックリストの導入 1 行 | 詳細手順・長いコマンド列 |
| 判断型 | 分岐の質問と結論の型 | 例外表・境界事例の列挙 |
| テンプレ型 | 出力フォーマットのミニ版 | 完全なサンプル群 |
| ツール型 | いつ何を実行/Read するか | スクリプト実装本体 |

## Anti-Patterns（避ける）

- Windows 形式パス、時限付きの手順を本文に直書き（劣化しやすい）
- 「どれでも可」な選択肢だらけ（デフォルトを 1 つ決め、逃げ道だけ書く）
- めったに起きないエッジケースだけのために本文を膨らませる

## Checklist（完成前）

- [ ] `description` に WHAT + WHEN + トリガー語がある（三人称）
- [ ] `## When to Use` と `## Instructions` があり、重複がない
- [ ] SKILL.md が 500 行以内（超えるなら参照ファイルへ）
- [ ] 長文の規約・コードは **参照パス**にした（コピペしていない）
- [ ] 参照は SKILL から **1 段階**（深いネストを作っていない）
