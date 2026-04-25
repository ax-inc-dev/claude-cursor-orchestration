---
name: review-qa
description: QA 観点で変更差分をレビューする。回帰マップ・リスクベース優先・欠陥パターンを扱い、受け入れ検証と探索観点を整理する。
---

## Purpose

回帰リスク・探索テスト観点・再現性・優先度付けを diff から検証し、リリース前に潰すべきギャップを重大度付きで返す。

## When to Use

- リリース前・フィーチャー完了時の QA 柱レビュー
- 並列レビューで QA 観点を担当するとき
- 変更が広範で回帰範囲が不明なとき
- マーケサイト/LP で E2E シナリオと実装の整合を確認するとき
- 欠陥の再現手順・優先度の妥当性を詰めるとき

## Review Checklist — CONCRETE items (QA)

**Regression map（回帰マップ）**
1. 変更点に **隣接する未テスト領域** を列挙（機能・画面・API・ジョブ）。
2. 過去に壊れやすかった領域（変更履歴・バグ DB）との重なりを確認。
3. データ移行・バックフィルがある場合は **移行前後** の代表データで検証可能か。

**Risk-based prioritization**
4. ユーザー影響・頻度・金銭・コンプライアンスでリスクをスコアし、テスト順を提案。
5. クリティカルパス（登録・ログイン・購入・課金等）を最優先で列挙。
6. 探索的テストの時間配分をリスクに比例させるか。

**Defect patterns（欠陥パターン）**
7. 境界値・オフバイワン・空・最大長・特殊文字・並列操作の組み合わせ。
8. 権限ロール行列（管理者/一般/ゲスト）とデータスコープの漏れ。
9. オフライン・リトライ・タイムアウト・二重送信の典型パターン。
10. ロケール・TZ・通貨（該当時）のずれ。
11. ログ・メトリクスで障害に気づけるか（該当時）。
12. **マーケサイト・LP**: `docs/site/e2e-scenarios.md` と Playwright 実装（または **`E2E実行`** 相当）が **主要導線・CTA** をカバーしているか。詳細は `~/.cursor/skills/site-e2e-playwright/SKILL.md`。実行委譲は **`/site-e2e-runner`** を含めてよい。
13. バグ報告に **再現手順・期待/実際・環境** が揃うよう、レビューで不足を指摘。
14. フレークしうる E2E（待ち・データ依存）を識別し、安定化案を要求。
15. パフォーマンス・負荷のスポット（該当時）はスモーク手順を定義できるか。
16. カオス/障害注入（該当時）の観点が必要か。
17. アクセシビリティのスモーク（キーボード）を QA 観点で拾う（詳細は FE へ）。
18. 変更のテストレベル（単体/集成/E2E）の適切な配分。
19. 受け入れ条件の「Given/When/Then」がレビュー可能な形で存在するか。
20. リリース後のロールバック・フィーチャーフラグ・段階的公開の検証。
21. 欠陥の重複（同一根因の別見え方）を疑う。
22. 探索テストのセッション目標（チャーター）を一文で提案できるか。

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

- 単体テストだけで主要導線を満足とする。
- E2E 不在のままクリティカルフローを承認する。
- 再現手順のないバグを優先度判断できない。
- 回帰範囲を曖昧にしたままリスク並べ替えをしない。
- マーケサイトで `docs/site/e2e-scenarios.md` と実装の突合をスキップする。

## Workflow (Codex)

1. **Read target**: diff・仕様・テスト・E2E シナリオ文書を特定。
2. **Skim**: 影響範囲とユーザーフローを俯瞰。
3. **Deep-read**: 回帰マップ → リスク優先 → 欠陥パターンを適用。
4. **Cite**: `file:line` またはシナリオ節。
5. **Grade**: 集計。
6. **Verdict**: Output Contract → `review-summary`。

## Machine Gate

レビュー本文の **最終行** は Output Contract の `review-summary` フェンス（キー固定: `grade`, `verdict`, `critical`, `high`, `medium`, `low`）とする。省略・キー名変更は禁止。
