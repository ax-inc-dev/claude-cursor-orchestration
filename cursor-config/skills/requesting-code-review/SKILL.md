---
name: requesting-code-review
description: レビュー依頼者（作者）が依頼パッケージを整え、差分定義・リスク・観点・環境を揃える。コード PR に限らずコンサル成果物・文書・設計計画にも使い、各 review-* スキルの共通出力契約に接続する。
---

## Purpose

レビュー依頼側が **対象の定義・リスク仮説・見てほしい観点・環境** を揃え、レビュアーが `review-*` スキルの **同一 Output Contract** で応答できる入力を作る。`Review target type` により git 差分必須か文書パス必須かを切り替える。

## When to Use

- タスク完了・マージ前・複雑バグ修正のあと
- 並列で `review-app-product` … `review-test` を回す前の **依頼パケット** を作るとき
- `subagent-driven-development` の各タスク後にレビューを挟むとき
- 大きな diff や長文成果物でレビュアーが迷わないよう **ブリーフィング** が必要なとき
- コンサル成果物・設計計画・単一文書のレビューを依頼するとき
- `requesting-code-review/code-reviewer.md` テンプレを埋める前に品質ゲートとする

## Review Checklist — CONCRETE items (author prep / briefing quality)

**Review target type（ブリーフィング先頭で宣言・必須）**

次のいずれか **一つ** を明示する（ドロップダウン相当）:

- `code-pr` — バージョン管理されたコード差分
- `consulting-deliverable` — 提案書・戦略メモ・納品ドキュメント等
- `document` — 単一文書・仕様・ポリシー
- `design-plan` — 設計案・IA・画面設計・実装前計画

**`target_type = code-pr` のとき — git / 差分（以下はすべて必須）**

1. **BASE / HEAD**（または比較範囲）を明示。`git diff BASE..HEAD` が再現できること。
2. **対象 SHA** を本文に書く（レビュアーが同じ範囲を読むため）。
3. **diff の定義**: 「含む／含まない」（生成物、ロックファイルのみ等）を一行で宣言。
4. **diff 統計**（`git diff --stat` 相当）を本文に要約し、`review-briefing` の `key_metrics` にも反映（行数・ファイル数など。厳密な `est_loc` 単一フィールドは不要）。

**`target_type` が `code-pr` 以外のとき — 文書・成果物（git 差分に代わる必須フィールド）**

1. **document_path**: ファイルパス・Notion/ Drive の一意参照など、レビュー対象への到達方法。
2. **scope_sections**: レビュー範囲（章・スライド番号・セクション ID・見出しリスト）。
3. **affected_kpis**: 影響しうる KPI・意思決定・前提（該当なしは「なし」と明示）。
4. **audience**: 想定読者・承認者を一文で。

**Reviewer briefing（全 target type 共通）**

5. **何を実装・記述したか** をファイル名／節ベースで列挙（ストーリー1段落 + 箇条書き）。
6. **計画・Issue・ADR** へのリンクまたは節番号。
7. **リスク仮説**: セキュリティ・データ・パフォーマンス・ビジネス仮説で不安がある箇所を `path` または節付きで列挙。
8. **見てほしい観点**: 並列時は `review-security` / `review-test` 等、スキル名単位でリクエスト。
9. **環境**: 再現に必要な env・フィーチャーフラグ・シードデータ（コード PR のとき中心。文書のみなら N/A 可）。
10. **既知の妥協点** と理由（技術負債・文案未確定など）。
11. **テスト実行結果** の要約（コマンド + 成否）。未実行・対象外なら UNVERIFIED / N/A と書く。
12. **セキュリティ/UX/ビジネス整合** の懸念を作者側で先にメモ（ゼロなら「なし」と明示）。
13. 並列レビュー時、各 `review-*` に **共通の重大度ラベル（Critical/High/Medium/Low）** と、各スキル Machine Gate どおりの **`review-summary`**（本スキルは **`review-briefing`**）を出すよう依頼文に含める。
14. レビュアーが **読む順序**（エントリポイント・章順）を提案。
15. 外部依存（API・ステージング）が必要なら接続方法を記載。
16. ロールバックやフィーチャーフラグの有無（該当時）。
17. スクリーンショットや録画が有効なら添付ポイントを指定（該当時）。
18. レビュー期限・優先度（ブロッカーか）を一文で。
19. `code-reviewer.md` を使う場合でも、出力は各 `review-*` と **同一の構造化フォーマット** を要求する（旧 Important/Minor は使わない）。
20. 依頼文に **質問のないレビュアー** が迷わないよう、曖昧語を排除。

## Anti-Bias Guardrails

1. Read the actual code/content FIRST. Do not output a verdict before reading.
2. Every finding must cite file + line or plan section. No abstract prose.
3. Cite evidence, not vibes. Phrases like "looks clean" / "seems fine" are forbidden — quote evidence or admit uncertainty.
4. If you cannot verify, say "UNVERIFIED: [reason]" instead of assuming OK.
5. Forbidden phrases when concluding: "probably fine", "seems good", "should work". Use verifiable assertions.
6. Review length must be at least 20% of target length when target > 500 LOC, or ≥ target length when smaller.
7. Do NOT grade above B if any rubric-triggering finding exists.
8. End with the mandatory machine gate JSON block for THIS skill (review-summary / review-briefing / acceptance-plan as specified in Machine Gate section) — DO NOT omit, DO NOT vary the keys.

## Output Contract (Author → Reviewers)

**総合評価の代わりに、依頼パケットとブリーフィングを出力する。** 見出し順は固定。

## Review target type

- `code-pr` | `consulting-deliverable` | `document` | `design-plan`

## 依頼サマリ（1段落）

- 目的・背景・マージ先または承認フロー

## 対象の定義

**`code-pr` の場合**

- BASE: `<sha>` / HEAD: `<sha>`
- 含む: … / 含まない: …
- diff 統計要約: …

**`code-pr` 以外の場合**

- document_path: …
- scope_sections: …
- affected_kpis: …
- audience: …

## 実装・記述ハイライト（file:line または section 粒度の箇条書き）

- …

## リスク・懸念（作者メモ）

- [area] path/file または §節 — なぜ不安か

## レビュー観点リクエスト（並列時はスキル名を列挙）

- review-security: …
- review-qa: …

## 検証・環境

- テスト: コマンド + 結果要約（対象外は N/A）
- 環境変数 / フラグ: …

## review-briefing（機械可読・必須）

`target_type` は上記と同一値。`key_metrics` は型に応じた追加情報の **辞書**（例: `code-pr` なら `base`, `head`, `sha`, `diff_stats`；それ以外なら `document_path`, `scope_sections`, `affected_kpis`, `audience` を反映）。`est_loc` のような単一必須フィールドは置かない。

```review-briefing
{"target_type": "code-pr", "scope": "...", "risk_areas": ["..."], "reviewers_needed": ["review-security", "review-backend"], "key_metrics": {"base": "...", "head": "...", "sha": "...", "diff_stats": "12 files, +340 -120"}}
```

```review-briefing
{"target_type": "consulting-deliverable", "scope": "...", "risk_areas": ["..."], "reviewers_needed": ["review-app-product", "review-architecture"], "key_metrics": {"document_path": "...", "scope_sections": ["§3", "Slides 10-15"], "affected_kpis": ["CAC payback"], "audience": "CFO + product lead"}}
```

## Scoring Rubric

| Severity | Definition — Technical | Definition — Business/Strategy |
|----------|------------------------|----------------------------------|
| Critical | Ship-blocking: data loss, security breach, outage risk, legal violation | Fundamental misreading of client business, data numbers wrong at >20% magnitude, strategy that harms client economics |
| High | Incorrect behavior affecting key user flow / KPI | KPI mis-definition, broken causal logic (e.g. AI-KPI not connected to economic value), framework mis-use, missing strategic selection |
| Medium | Quality, maintainability, minor performance | Incomplete scenarios, unclear responsible party, placeholder ratio >30% |
| Low | Style, nice-to-have, docs polish | Minor inconsistencies, stylistic variation |

The Verdict decision tree and Grade map apply regardless of which column (Technical vs Business/Strategy) grounds a finding.

Verdict decision tree:

- ≥1 Critical → verdict "NO"
- ≥2 High OR ≥6 total issues → verdict "NO"
- 0 Critical, 0 High, ≤3 Medium → verdict "WITH EDITS"
- 0 Critical, 0 High, 0 Medium → verdict "YES"

Grade map:

- A: 0 Critical, 0 High, 0 Medium
- B: 0 Critical, 0 High, ≤3 Medium
- C: ≥1 Critical OR ≥2 High OR ≥4 Medium
- D: ≥2 Critical OR fundamental architectural issue

## Common Pitfalls

- 文脈なしの「見て」だけで終わる。
- `code-pr` なのに範囲（BASE/HEAD）が不明でレビュアーが別 diff を読む。
- 文書レビューで `document_path` / `scope_sections` がなくレビュー範囲が曖昧。
- 並列レビューで共通の重大度・出力形式を指定しない。
- テスト結果を書かずに「動いてるはず」とする（該当時）。
- `key_metrics` と本文の対象定義が矛盾する。

## Workflow (Codex)

1. Read target → 2. Skim → 3. Deep-read（チェックリスト・証跡）→ 4. Cite → 5. Assemble → 6. Gate `review-briefing`。

## Machine Gate

依頼文の **最終** は次のフェンス。**言語タグは必ず `review-briefing`。** トップレベルキーは次の5つのみ（省略・改名禁止）: `target_type`, `scope`, `risk_areas`, `reviewers_needed`, `key_metrics`。

- `target_type`: `code-pr` | `consulting-deliverable` | `document` | `design-plan`
- `scope`: 文字列
- `risk_areas`: 文字列の配列
- `reviewers_needed`: 文字列の配列（`review-*` 名など）
- `key_metrics`: JSON オブジェクト（`code-pr` なら base/head/sha/diff_stats 等、それ以外なら document_path/scope_sections/affected_kpis/audience 等を格納。`est_loc` 必須ではない）

```review-briefing
{"target_type": "code-pr", "scope": "feature X in checkout", "risk_areas": ["payments idempotency"], "reviewers_needed": ["review-security", "review-backend"], "key_metrics": {"base": "abc1234", "head": "def5678", "sha": "def5678", "diff_stats": "8 files, +210 -45"}}
```
