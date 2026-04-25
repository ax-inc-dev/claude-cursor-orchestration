---
name: review-frontend
description: フロントエンド変更のレビュー。WCAG 2.1 の観点に沿って a11y・状態・バンドルを検証し、UI 差分と仕様プロセスの整合を扱う。
---

## Purpose

UI 実装の正しさ・アクセシビリティ・状態管理・バンドル影響を diff から検証し、利用者体験と実装のギャップを重大度付きで返す。

## When to Use

- コンポーネント・ページ・スタイルの差分があるとき
- 並列レビューで UI 柱を担当するとき
- キーボード・スクリーンリーダー・フォーカスが絡むとき
- データ取得・キャッシュ・ストリーミングを変更するとき
- `docs/ux-design/`・`docs/site/`・`DESIGN.md` との整合を確認するとき

## Review Checklist — CONCRETE items (frontend + WCAG 2.1)

**WCAG 2.1（4 原則を明示スキャン）**

- **Perceivable**: 代替テキスト、キャプション、レイアウト適応、色以外の手がかり、コントラスト。
- **Operable**: キーボード、時間制限、発作配慮、ナビ・フォーカス可視化、入力モダリティ。
- **Understandable**: 言語、予測可能な挙動、入力支援・エラー識別・ラベル。
- **Robust**: 適合マークアップ、名前・役割・値（ARIA 等）。

**追加の具体項目**

1. UI/フローに効くのに `docs/ux-design/` 等・Figma 更新が無い場合は **仕様プロセス違反**（Medium+、既存ルール維持）。
2. セマンティック HTML: 見出し階層、ボタン vs リンク、リストの妥当性。
3. キーボードのみで主要フローが完走するか（Tab 順・ショートカット・フォーカストラップ）。
4. フォーカス管理: モーダル開閉・ルート遷移後のフォーカス移動。
5. ラベル: `label`/`aria-label`/`aria-labelledby` が入力と結びついているか。
6. 動く UI: `prefers-reduced-motion` への配慮、アニメーションの一時停止相当。
7. 状態の単一情報源: 重複 state・派生可能な state の二重管理がないか。
8. 再レンダリング: メモ化・依存配列・リスト key の妥当性。
9. データ取得の重複・ウォーターフォール・キャッシュキーの衝突。
10. エラー境界・フォールバック UI・部分失敗の表示。
11. Suspense・ストリーミング・Server Components（該当時）の境界。
12. バンドル: 動的 import・重い依存の遅延・ツリーシェイク。
13. 画像: サイズ・`loading`・適切なフォーマット。
14. CSP・サードパーティスクリプト（該当時）のリスク。
15. i18n: 伸長・日付・複数形（該当時）。
16. ルーティング: 404/403、戻るボタン整合。
17. フォーム: バリデーションタイミング、エラー近傍表示。
18. デザインシステム・トークン・`cn()` 整合。
19. ターゲットサイズ十分か。
20. ライブリージョン・ステータス（該当時）。
21. カスタム role/aria-* が WAI-ARIA パターンに沿うか。
22. Web Vitals 悪化がないか（該当時）。

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

- 見た目だけ確認し、キーボードと SR での意味を読まない。
- a11y を「後回し」で Critical を見逃す。
- 巨大バンドルや重依存を性能レビューで触れない。
- 仕様プロセス無視の UI 先行を許容する。
- WCAG カテゴリに言及せず「なんとなく問題なさそう」とする。

## Workflow (Codex)

1. Read target → 2. Skim → 3. Deep-read（WCAG 4 原則→仕様プロセス→バンドル）→ 4. Cite（`file:line`）→ 5. Grade → 6. Verdict + `review-summary`。

## Machine Gate

レビュー本文の **最終行** は Output Contract の `review-summary` フェンス（キー固定: `grade`, `verdict`, `critical`, `high`, `medium`, `low`）とする。省略・キー名変更は禁止。
