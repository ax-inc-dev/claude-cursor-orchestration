---
name: review-architecture
description: 全体構成と設計思想に照らして変更差分をレビューする。結合・進化・シーム・統合を検証し、レイヤ責務と依存方向を並列レビューのアーキ柱として扱う。
---

## Purpose

モジュール境界・依存・進化性・統合点を diff と設計文脈から検証し、重大度付きで返す。

## When to Use

- 新モジュール・パッケージ・公開 API 面が増えるとき
- レイヤ跨ぎ・大規模リファクタ・ドメイン境界の変更があるとき
- ADR・規約・既存パターンとの整合を確認するとき
- デプロイ単位やチーム境界に影響するとき
- 並列レビューで「アーキテクチャ柱」を担当するとき

## Review Checklist — CONCRETE items (architecture)

1. **結合度 (coupling)**: 変更が不要なモジュールまで引きずっていないか。安定した抽象に対して依存が一方向か。
2. **凝集度**: 1 モジュールの責務が単一か。God object / 万能サービス化していないか。
3. **進化 (evolution)**: 将来の拡張に対し、変更が局所化するか。破壊的変更の波及範囲は説明可能か。
4. **シーム (seams)**: テスト・置換・段階的リリースのための境界（インターフェース・ファサード）が明確か。
5. **統合 (integration)**: 外部システム・BFF・メッセージ・同期 API の接続点で契約と失敗モードが定義されているか。
6. データ所有者と一貫性境界（集約・トランザクションの置き場）がコード上で追えるか。
7. 依存方向が内→外か。循環依存の匂い（間接 import、型の逆参照）がないか。
8. 公開インターフェースの安定性: バージョニング・非推奨・互換レイヤの必要性。
9. 拡張ポイントと過度な抽象のバランス（YAGNI との両立）。
10. 横断関心（ログ・認可・メトリクス）の置き場が一貫し、ドメインが汚染されていないか。
11. 非機能（可用性・スケール・レイテンシ）要件と構造の整合。
12. 既存 ADR・ディレクトリ規約・命名と矛盾しないか（逸脱なら理由がコードまたは文書で追えるか）。
13. テスト容易性: スタブ可能な境界、決定的なファクトリ、フレークしにくい構造か。
14. **デプロイ単位 / リリース独立性**: サービス・モジュールを独立リリースできるか、共有 DB による暗黙結合がないか。
15. 設定・環境差分が構造に漏れすぎていないか（環境分岐の爆発）。
16. フィーチャーフラグや段階的移行のための分岐が一箇所にまとまっているか。
17. ドメインイベント / 副作用の発火点が追跡可能か。
18. 読み取り/書き込みモデルの混線（CQRS 要否）。
19. サブシステム間のエラー伝播・リトライ境界の明確さ。
20. チーム分割（境界コンテキスト）に耐えるか、共有カーネル肥大化がないか。
21. レガシー接続（アダプタ）が明示され、新コードが侵食していないか。
22. ドキュメント/README の構造説明と実装の乖離（Medium 以上）。

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

- 「きれい」など感情語で境界の曖昧さをごまかす。
- ドメイン無視の技術最適化だけで責務を割り切る。
- 統合点の失敗モード・整合性を読まずに合格にする。
- 循環依存を「今は動く」で許容する。
- ADR や規約を確認せずに新パターンを増やす。

## Workflow (Codex)

1. Read target → 2. Skim → 3. Deep-read（結合・進化・シーム・統合）→ 4. Cite → 5. Grade → 6. Verdict + `review-summary`。

## Machine Gate

レビュー本文の **最終行** は Output Contract の `review-summary` フェンス（キー固定: `grade`, `verdict`, `critical`, `high`, `medium`, `low`）とする。省略・キー名変更は禁止。
