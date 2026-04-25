---
name: review-backend
description: バックエンド変更の追加レビュー。API 契約・冪等性・トランザクション・N+1 を中心に、サーバー・API・DB 層の差分を検証する。
---

## Purpose

API 契約・整合性・信頼性・性能をサーバー差分から検証し、重大度付きで返す。

## When to Use

- REST/GraphQL/gRPC・バッチ・ワーカー・DB スキーマ変更があるとき
- 認可・トランザクション・冪等性が絡むとき
- パフォーマンス（N+1・インデックス）を疑うとき
- 並列レビューでサーバー柱を担当するとき
- 外部連携・キュー・非同期処理の境界を確認するとき

## Review Checklist — CONCRETE items (backend)

1. **API 契約**: リクエスト/レスポンススキーマ・型・必須フィールドが文書と実装で一致するか（破壊的変更はバージョン・非推奨の扱い）。
2. **後方互換**: 既存クライアントが壊れないか。デフォルト・未知フィールドの扱い。
3. **ステータスコードとエラーモデル**: 4xx/5xx の使い分け、エラーコード・`request_id` の一貫性。
4. **入力検証**: 境界値・型・長さ・列挙・Unicode。拒否理由が安全側か。
5. **認可**: リソース単位のチェックが各ハンドラで抜けていないか（IDOR の匂い）。
6. **トランザクション境界**: どの操作が同一トランザクションか、失敗時のロールバック範囲。
7. **孤立レベル / ロック**: 競合・デッドロック・読み取り一貫性の要件に合っているか。
8. **冪等性**: 再送・リトライで二重課金・二重作成が起きないか（キー・ユニーク制約）。
9. **重試**: リトライ可能なエラーと不可能なエラーの区別、バックオフ。
10. **N+1**: ORM・ループ内クエリ、関連ロード、バッチ化の必要性。
11. **インデックス**: 新クエリに必要なインデックス、既存インデックスの無効化リスク。
12. **クエリ計画の匂い**: フルスキャン・ソートコスト・大きな `IN` 句。
13. **マイグレーション**: ダウンタイム・ロック・バックフィル・ロールバック手順。
14. **タイムアウト / キャンセル**: クライアント・DB・外部 API のキャンセル伝播。
15. **レート制限**: 乱用・DoS に対する防御（該当時）。
16. **ログと PII**: 秘密・トークン・個人情報がログに出ないか。
17. **非同期 / メッセージ**: 重複配送・少なくとも一度配信での整合性、デッドレター。
18. **外部 API 障害**: サーキットブレーカー・フォールバック・部分失敗の扱い。
19. **時刻・タイムゾーン**: 集計・締め処理のずれ、DST。
20. **同時実行**: 楽観/悲観ロック、バージョン列の有無。
21. セキュリティ重複は security に任せる旨を明示し、BE（契約・整合性）に集中。
22. オブザーバビリティ: エラー率・レイテンシを境界で計測できるか。

## Anti-Bias Guardrails

1. Read the actual code/content FIRST. Do not output a verdict before reading.
2. Every finding must cite file + line or plan section. No abstract prose.
3. Cite evidence, not vibes. Phrases like "looks clean" / "seems fine" are forbidden — quote evidence or admit uncertainty.
4. If you cannot verify, say "UNVERIFIED: [reason]" instead of assuming OK.
5. Forbidden phrases when concluding: "probably fine", "seems good", "should work". Use verifiable assertions.
6. Review length must be at least 20% of target length when target > 500 LOC, or ≥ target length when smaller.
7. Do NOT grade above B if any rubric-triggering finding exists.
8. End with the mandatory machine gate JSON block for THIS skill (review-summary / review-briefing / acceptance-plan as specified in Machine Gate section) — DO NOT omit, DO NOT vary the keys.

## Output Contract

## 総合評価: A / B / C / D
- A: 即プロダクション投入可（0 Critical, 0 High, 0 Medium）
- B: 軽微修正で出せる（0 Critical, 0 High, ≤3 Medium）
- C: Critical/High 指摘あり、修正必須
- D: 根本設計問題、やり直し推奨

## 強み (3-5 bullets, 具体参照付き)
- 強み1 — file:line or section
...

## 重大な問題 (Critical/High)
- [Critical] path/file.ts:42 — 指摘と修正提案
- [High] docs/plan.md §3.2 — 指摘と修正提案

## 改善推奨 (Medium/Low, ROI高い順)
- [Medium] ... — ...
- [Low] ... — ...

## 結論: YES / WITH EDITS / NO
**WITH EDITS** — 一行理由（例: Critical なし、High 2件修正で出荷可）

```review-summary
{"grade": "B", "verdict": "WITH EDITS", "critical": 0, "high": 0, "medium": 2, "low": 3}
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

- Happy path のみ読み、エラーパスとトランザクションを確認しない。
- エラーを握りつぶして 200 を返す。
- OpenAPI と実装のズレを放置する。
- N+1 を「後で直す」でレビューを通す。
- 冪等性なしの決済・在庫・作成 API を見逃す。

## Workflow (Codex)

1. Read target → 2. Skim → 3. Deep-read（契約→認可→TX→冪等→クエリ）→ 4. Cite → 5. Grade → 6. Verdict + `review-summary`。

## Machine Gate

レビュー本文の **最終行** は Output Contract の `review-summary` フェンス（キー固定: `grade`, `verdict`, `critical`, `high`, `medium`, `low`）とする。省略・キー名変更は禁止。
