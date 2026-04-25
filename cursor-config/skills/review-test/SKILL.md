---
name: review-test
description: テストコードのレビュー。テストピラミッド・フレーク・ミューテーション・カバレッジゲート・契約テストを検証する。
---

## Purpose

テストの意味・フレーク・ピラミッド・契約を変更差分から検証し、虚偽の緑や重要分岐の未検証を重大度付きで返す。

## When to Use

- テスト追加・変更がある PR または並列レビュー
- 契約/API テスト・E2E の配置を見直すとき
- フレークや遅いテストが増えているとき
- カバレッジ閾値を変更するとき
- ミューテーションテストや契約テストを導入する場合

## Review Checklist — CONCRETE items (test quality)

**Test pyramid（ピラミッド）**
1. 単体・統合・E2E の比率が変更のリスクに見合うか。高コスト E2E の過剰化を指摘。
2. 重要なビジネスルールが単体で十分に縛られているか。

**Flakes（フレーク）**
3. 時間依存・`await` なし・共有可変状態・グローバル乱数・並列実行の競合。
4. ネットワーク・外部 I/O をモックせずに不安定なテストになっていないか。

**Mutation testing（ミューテーション）**
5. ミューテーションテストや同等の厳しさを導入している場合、アサーションが弱いかを確認。
6. 意味のあるアサーションか（`expect(true).toBe(true)` 等を禁止）。

**Coverage gates（カバレッジゲート）**
7. カバレッジ数値だけでなく **分岐・重要パス** がカバーされているか。
8. カバレッジ閾値を下げる変更の正当性（リスクの説明）。
9. 未カバーが Critical パスに触れていないか。

**Contract / API tests（契約）**
10. スキーマ・OpenAPI・consumer-driven contract（該当時）とテストが同期しているか。
11. 破壊的変更を検知する契約テストの有無。

**その他**
12. テストデータの決定性（シード・固定時刻・ファクトリ）。
13. モック過多による虚偽緑（実挙動と乖離）。
14. 統合テストの置き場（DB・コンテナ）と速度のトレードオフ。
15. テストの名前・Given-When-Then が意図を読ませるか。
16. セットアップ・ティアダウンの漏れ（リーク・汚染）。
17. スナップショットテストの過剰・メンテ負債。
18. テストの並列化・分離（ファイルシステム・DB のスコープ）。
19. 回帰のための最小テスト追加（YAGNI と両立）。
20. セキュリティ・認可の分岐は専用テストで触れているか（該当時）。
21. パフォーマンス/ベンチテストの扱い（該当時）。
22. テスト失敗時のメッセージがデバッグに役立つか。

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

- 実装追従のみのテストで重要分岐を抜かす。
- フレークを「たまに」で許容する。
- モックだらけで本番コードのパスを検証していない。
- カバレッジ % だけを見て安心する。
- 契約テストなしで API 変更を承認する。

## Workflow (Codex)

1. **Read target**: テストファイル・設定・カバレッジレポートを特定。
2. **Skim**: 何を守るテストか（対象製品コード）を列挙。
3. **Deep-read**: ピラミッド → フレーク・決定性 → 契約・カバレッジゲート → ミューテーション相当。
4. **Cite**: `file:line`。
5. **Grade**: 集計。
6. **Verdict**: Output Contract → `review-summary`。

## Machine Gate

レビュー本文の **最終行** は Output Contract の `review-summary` フェンス（キー固定: `grade`, `verdict`, `critical`, `high`, `medium`, `low`）とする。省略・キー名変更は禁止。
