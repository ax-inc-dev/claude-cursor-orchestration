---
name: review-app-product
description: 変更差分をプロダクト・アプリ利用者目線でレビューする。UX仮説・KPI・ファネル・リテンション・仕様充足を検証し、並列レビューのプロダクト柱として使う。
---

## Purpose

利用者価値・仕様充足・ビジネス妥当性を diff と根拠付きで検証し、重大度付きで返す。

## When to Use

- UI/フロー/コピー/権限/計測に触れる変更をレビューするとき
- 並列レビューで「プロダクト柱」を担当するとき
- 受入条件・ユーザーストーリーと実装の突合が必要なとき
- KPI・ファネル・リテンションへの影響を評価するとき
- ロールアウトやフィーチャーフラグで利用者影響を確認するとき

## Review Checklist — CONCRETE items (product / UX / business)

1. **UX 仮説**: 変更が解く利用者課題がコード・コピー・導線で一貫して表現されているか（仮説と実装の対応を `path:line` で示す）。
2. **KPI 連動**: 追うべき指標（活性・転換・エラー率など）とイベント/プロパティの対応が取れているか、取りこぼしがないか。
3. **ファネル**: 主要ステップ（認知→行動→完了）で離脱・不明点が増えないか、各画面の CTA が一貫しているか。
4. **リテンション**: 再訪・再実行を促す導線（通知設定、履歴、再開）が欠けていないか、該当時は根拠行を引用。
5. 受入条件・ユーザーストーリーと **コード上の分岐** が 1:1 で追えるか（不一致なら節・行で指摘）。
6. 初回 / 再訪 / 失敗 / 復帰の **主要ジャーニー** が通るか、分岐ごとに状態が定義されているか。
7. 空・ローディング・エラー・権限不足の **4 状態** が利用者に誤解を与えないか。
8. コピーが誤解・法務・信頼リスクを生まないか（該当時は文言の行を引用）。
9. イベント名・パラメータが分析要件と整合し、**ダブルカウント** や欠測がないか。
10. 既存画面との **操作・用語・レイアウト** の一貫性（逸脱は理由がコード上で分かるか）。
11. a11y（利用者向け）: SR で意味が通るか。FE と重複なら「FE 参照」。
12. 体感パフォーマンス: 初期表示・操作・大量データで詰まらないか。
13. フィーチャーフラグ/段階リリースのオフ・部分適用時の影響を説明できるか。
14. 競合・オフライン・重複送信などエッジ（該当時）。
15. 権限・ロール変更が既存導線を壊さないか。
16. エラーからの復帰（再試行・サポート・リセット）が明示されているか。
17. 計測なしの「雰囲気 OK」を避け、無ければ UNVERIFIED。
18. 仕様が無い場合、コメント/PR で受入の置き場が明示されているか。
19. 主要フローにデッドエンドが無いか。
20. 既存 KPI を歪めないか（例: クリックだけ改善し転換が落ちる等）。

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

- 仕様書が無いまま「雰囲気で OK」とする。
- KPI・ファネルと実装の対応を確認せずイベントだけ増やす。
- エラー時のドロップオフや復帰導線を見ない。
- プロダクト指摘を抽象的な形容詞だけで終える（必ず `path:line`）。
- 計測・仮説なしで A/B に格上げする。

## Workflow (Codex)

1. Read target → 2. Skim → 3. Deep-read（チェックリスト順・根拠行メモ）→ 4. Cite（`file:line`）→ 5. Grade → 6. Verdict + `review-summary`。

## Machine Gate

レビュー本文の **最終行** は Output Contract の `review-summary` フェンス（キー固定: `grade`, `verdict`, `critical`, `high`, `medium`, `low`）とする。省略・キー名変更は禁止。
