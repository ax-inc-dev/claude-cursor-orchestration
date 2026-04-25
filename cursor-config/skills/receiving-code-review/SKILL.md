---
name: receiving-code-review
description: レビュー指摘を受けた作者向け。重大度トリアージ・反論パターン・バッチ処理で、検証ファーストに実装順序を決める。GitHub インラインに限らず文書改稿・議事・一括応答にも対応する。
---

## Purpose

指摘を **検証してから** 実装し、Critical/High/Medium/Low と YES/WITH EDITS/NO の対応をはっきりさせ、並列レビュー結果を安全に統合する。**Acceptance channel** と **Review target type** で返信経路とコミット要否を切り替える。

## When to Use

- GitHub/GitLab のレビューコメント・インライン指摘を受け取った直後
- 複数レビュアー・並列 `review-*` の結果を統合するとき
- 指摘が曖昧・疑義があり、実装前に整理が必要なとき
- コンサル成果物の改稿レビュー、文書ベースの承認、会議での指摘整理のあと
- 感謝表現ではなく技術的応答で進めたいとき（本スキルの禁止事項を維持）

## Review Checklist — CONCRETE items (author receiving feedback)

**Acceptance channel（受理・返信の経路・必須）**

次のいずれか **一つ** を宣言する:

- `github-inline` — PR コメントスレッド
- `pr-description` — PR 本文の更新・チェックリスト
- `doc-revision` — 成果物・仕様書の改稿と版管理
- `meeting-minutes` — 会議・承認ミーティングの結論を反映
- `batch-response` — 単一のまとめ返信（メール・ドキュメント・チャット）

**Review target type（依頼側 `requesting-code-review` と整合）**

- `code-pr` | `consulting-deliverable` | `document` | `design-plan` のいずれかを明示。

**Severity triage（重大度トリアージ）**

1. 各指摘を Critical/High/Medium/Low に再ラベルし、**Rubric** と整合するか確認（Technical 列と Business/Strategy 列のどちらで根拠づけるかを意識）。
2. **≥1 Critical** または **≥2 High** はリリース／納品前にブロック扱い（方針）。
3. セキュリティ・データ損失・認可は他より先に並べる（`review-security` / `review-test` 優先）。

**Rebuttal pattern（反論パターン）**

4. 指摘が誤りのとき: 事実（テスト・仕様・行番号）で反論し、感情語を使わない。
5. 証拠が足りないとき: 「UNVERIFIED: [不足]」と書き、確認手順を提案。
6. スコープ外のとき: 仕様・Issue へのリンクで却下理由を一行で。

**Batch handling（バッチ処理）**

7. 複数指摘は **理解できたものから** ではなく、**依存関係と重大度** で順序付け。
8. `target_type = code-pr` のときは可能なら **最小コミット単位** で直し、その都度テスト。文書のみのときは版またはセクション単位で同様に。
9. 並列 8 本の結果をマージするとき、**衝突する指摘** を表にし、採用/却下を明示。

**既存ルールの維持**

10. 曖昧な項目は実装せず、先に質問する。
11. 外部レビュアーは疑義を持って検証する（プロジェクトの前提を確認）。
12. YAGNI: 使われていないコードへの「正しい実装」要求は grep で確認してから判断。
13. `channel = github-inline` のときは GitHub の **インラインスレッド** に返信（トップレベル一括ではない）。他チャネルではその経路の作法に合わせる。
14. 感謝・賞賛表現は禁止（行動とコード・文書で示す）。**検証ファースト** を最優先。

**WITH EDITS 時**

15. レビューで求められた **必須修正リスト** を応答に転記し、チェックボックスで潰す。
16. 結論が YES / WITH EDITS / NO のどれに相当するかを自分でラベル付け。

**フォローアーティファクト**

17. `target_type = code-pr` のとき: **`followup_artifact`** に、次のコミットで使う予定の **コミットタイトル**（例: `fix: address review on authz`）を含める。Conventional Commits を推奨。
18. `target_type` が `code-pr` 以外のとき: **`followup_artifact`** に改稿版のファイルパス・版・議事録リンク・承認記録など、次の成果物の **到達可能な参照** を書く（コミットタイトルは不要）。

## Anti-Bias Guardrails

1. Read the actual code/content FIRST. Do not output a verdict before reading.
2. Every finding must cite file + line or plan section. No abstract prose.
3. Cite evidence, not vibes. Phrases like "looks clean" / "seems fine" are forbidden — quote evidence or admit uncertainty.
4. If you cannot verify, say "UNVERIFIED: [reason]" instead of assuming OK.
5. Forbidden phrases when concluding: "probably fine", "seems good", "should work". Use verifiable assertions.
6. Review length must be at least 20% of target length when target > 500 LOC, or ≥ target length when smaller.
7. Do NOT grade above B if any rubric-triggering finding exists.
8. End with the mandatory machine gate JSON block for THIS skill (review-summary / review-briefing / acceptance-plan as specified in Machine Gate section) — DO NOT omit, DO NOT vary the keys.

## Output Contract (Author response plan)

**grade の代わりに、受理計画（acceptance plan）を出す。** 見出し順は固定。

## Acceptance channel / Review target type

- channel: …
- target_type: …

## 指摘サマリ（出所別）

- レビュアー / ツール / 並列スキル名 — 件数

## 重大度マッピング

- [Critical] … → 対応方針（実装 / 反論 / 要確認）

## 採用する修正（順序付き）

1. … — `file` または §節 — 依存関係

## 反論・却下（理由付き）

- 指摘: … — 理由: … — 証拠: `path:line` または節

## テスト / 検証計画

- コマンドと期待結果（該当時）

## 結論（マージ・納品可否の自己判断）

- YES / WITH EDITS / NO — 一行理由

## acceptance-plan（機械可読・必須）

```acceptance-plan
{"channel": "github-inline", "target_type": "code-pr", "accepted": ["fix idor on line 42"], "deferred": ["refactor naming nits"], "rejected_with_reason": ["split service: not used in codebase per grep"], "followup_artifact": "fix: address security review on resource access"}
```

```acceptance-plan
{"channel": "doc-revision", "target_type": "consulting-deliverable", "accepted": ["clarify KPI chain in §4"], "deferred": [], "rejected_with_reason": [], "followup_artifact": "slides v3 in /deliverables/2026-04-deck-v3.pdf"}
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

- 一部だけ直して残りを曖昧にする。
- 感情表現で指摘の検証を置き換える。
- 重大度を無視して楽な指摘から手を付ける。
- 並列レビュー結果を突合せずに部分的にマージする。
- `followup_artifact` が実内容と無関係、または `target_type = code-pr` なのにコミットタイトルが無い。

## Workflow (Codex)

1. **Read target**: 全コメント・`review-summary` 群・CI・文書版を読む。
2. **Skim**: カテゴリ（バグ・スタイル・設計・ビジネス整合）に分類。
3. **Deep-read**: 各指摘をコードまたは文書で検証（同意/不同意/要追加情報）。
4. **Cite**: 応答に `path:line` または節を付ける。
5. **Plan**: `acceptance-plan` を埋め、実装・改稿順を確定。
6. **Gate**: `acceptance-plan` JSON を出力。

## Machine Gate

応答の **最終** は次のフェンス。**言語タグは必ず `acceptance-plan`。** トップレベルキーは次の6つのみ（省略・改名禁止）: `channel`, `target_type`, `accepted`, `deferred`, `rejected_with_reason`, `followup_artifact`。

- `channel`: `github-inline` | `pr-description` | `doc-revision` | `meeting-minutes` | `batch-response`
- `target_type`: `code-pr` | `consulting-deliverable` | `document` | `design-plan`
- `accepted` / `deferred` / `rejected_with_reason`: 文字列の配列
- `followup_artifact`: 単一文字列。`target_type = code-pr` のときは次コミット予定タイトルを含める。それ以外は次版・リンク等。

```acceptance-plan
{"channel": "github-inline", "target_type": "code-pr", "accepted": ["fix idor on line 42"], "deferred": ["refactor naming nits"], "rejected_with_reason": ["split service: not used in codebase per grep"], "followup_artifact": "fix: address security review on resource access"}
```
