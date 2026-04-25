---
name: review-security
description: 変更差分のセキュリティレビュー。OWASP Top 10 を起点に認証・認可・秘密・入力・依存関係を検証する。
---

## Purpose

OWASP 系・認証認可・機密・サプライチェーンを diff から検証し、悪用可能な欠陥を重大度付きで返す。

## When to Use

- 並列レビューのセキュリティ柱として常に 1 本走らせるとき
- 認証・認可・秘密・入力・依存更新を触るとき
- API 公開・ファイルアップロード・管理画面を変更するとき
- インフラと重なる場合は **infra スキル** と役割分担し、重複は明示する

## Review Checklist — CONCRETE items (security + OWASP Top 10 2021)

**OWASP Top 10 2021（各項目に少なくとも 1 つの検証を当てる）**

1. **A01 Broken Access Control**: オブジェクト ID 直指定・権限昇格・管理 API の認可抜け。多テナント境界。
2. **A02 Cryptographic Failures**: 不適切な暗号化・鍵管理・ハードコード秘密・TLS 設定の欠落（該当時）。
3. **A03 Injection**: SQL/NoSQL/OS/LDAP インジェクション、テンプレートインジェクション、コマンド注入。
4. **A04 Insecure Design**: 脅威モデルなしの設計（レート制限なし・無制限リトライ等）。セキュアデフォルトの欠如。
5. **A05 Security Misconfiguration**: デバッグ有効・デフォルト認証情報・過剰エラー詳細・CORS 設定ミス。
6. **A06 Vulnerable and Outdated Components**: 依存の既知 CVE・EOL ライブラリ・ロックファイル未更新。
7. **A07 Identification and Authentication Failures**: 認証バイパス・弱いパスワードポリシー・セッション固定・MFA 不足（該当時）。
8. **A08 Software and Data Integrity Failures**: 署名なし更新・サプライチェーン・CI の信頼境界。
9. **A09 Security Logging and Monitoring Failures**: 認可失敗・認証失敗の記録漏れ、アラート不在、改ざん耐性。
10. **A10 Server-Side Request Forgery (SSRF)**: 内部メタデータ・内ネットワークへの任意リクエスト。

**追加**
11. シークレット管理: Secret Manager / env、リポに平文なし。
12. CORS / CSRF（該当時）の整合性。
13. クライアント露出（API キー・トークン）を禁止。
14. ファイルアップロード: MIME/拡張子・サイズ・ストレージパストラバーサル。
15. レート制限・ブルートフォース対策（該当時）。
16. SBOM / 既知 CVE の匂い（スキャン結果が無ければ UNVERIFIED）。
17. ログへのトークン・PII 混入。
18. 認可とビジネスロジックの二重チェック（クライアントのみの制限禁止）。
19. サードパーティスクリプト・サブリソース整合性（該当時）。
20. コンテナ/イメージのユーザー権限・read-only root（該当時）。
21. 依存の固定バージョンと更新方針。
22. セキュリティヘッダー（CSP/HSTS 等、該当時）。

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

- 「フレームワークが守る」前提で認可を読まない。
- ログにトークンや秘密を出してしまう。
- IDOR（他ユーザーデータ参照）を見逃す。
- 依存更新を見ずに「問題なさそう」とする。
- OWASP 項目を列挙せずに抽象的な指摘だけにする。

## Workflow (Codex)

1. **Read target**: 認証・認可・入力・依存・設定ファイルを特定。
2. **Skim**: エントリポイントとデータ境界。
3. **Deep-read**: A01→A10 の順に当てはめ、追加チェックを続ける。
4. **Cite**: `file:line` と OWASP 項目を対応。
5. **Grade**: 集計。
6. **Verdict**: Output Contract → `review-summary`。

## Machine Gate

レビュー本文の **最終行** は Output Contract の `review-summary` フェンス（キー固定: `grade`, `verdict`, `critical`, `high`, `medium`, `low`）とする。省略・キー名変更は禁止。
