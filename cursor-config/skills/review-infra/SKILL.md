---
name: review-infra
description: インフラ・デプロイ・IaC・CI の変更レビュー。IaC・ネットワーク・IAM・可観測性・DR・コストを横断して検証する。
---

## Purpose

IaC・ネットワーク・権限・秘密・可観測性・事業継続・コストを変更差分から検証し、運用事故と権限逸脱を重大度付きで返す。

## When to Use

- Terraform/Pulumi/CloudFormation・K8s manifest・Helm 等の変更があるとき
- CI/CD・パイプライン・デプロイフックを触るとき
- VPC・ファイアウォール・LB・DNS を変更するとき
- IAM・サービスアカウント・OIDC を追加/変更するとき
- 監視・アラート・SLO・バックアップを変更するとき

## Review Checklist — CONCRETE items (infra / ops)

**IaC**
1. リソース定義が環境間で意図せず分岐していないか（コピペ乖離）。
2. `terraform plan` / 差分レビューに相当する確認が取れる記述か（手順が SKILL 上で UNVERIFIED なら明示）。
3. 状態ファイル・ロック・リモートバックエンドの取り扱いが安全か。
4. モジュール境界と再利用が過度に広い権限を隠していないか。

**Network**
5. サブネット・SG/Firewall・ルートで **最小公開** か。0.0.0.0/0 の意味付け。
6. プライベートリンク/VPC ピアリング/egress のデータ経路が意図通りか。
7. WAF・DDoS 保護（該当時）のギャップ。

**IAM**
8. 最小権限: ロール・ポリシーが action/resource にスコープされているか。
9. サービスアカウント・ワークロード ID・キーレス運用の妥当性。
10. 特権昇格・横展開の経路（AssumeRole チェーン）が説明可能か。

**Observability**
11. メトリクス・ログ・トレースの欠損がないか。アラート条件と SLO/SLI の対応。
12. ダッシュボード更新とオーナーシップ（誰がオンコールか）。
13. ログの保持・PII・暗号化（保管時・転送時）。

**DR (Disaster Recovery)**
14. バックアップ頻度・RPO/RTO・リストア手順の検証可能性。
15. マルチ AZ/リージョン戦略とフェイルオーバー（該当時）。
16. ステートフルデータの復旧演習の匂い（未検証なら UNVERIFIED）。

**Cost**
17. コスト急増の要因（スケール・データ転送・ストレージ階層・未使用リソース）。
18. 予算アラート・タグ付け・チャージバック（該当時）。

**その他**
19. 秘密情報がリポに平文でないか（Secret Manager / sealed 等）。
20. 環境分離（dev/stage/prod）と blast radius。
21. パイプラインの承認・サプライチェーン（該当時: 署名・SBOM）。
22. ロールバック手順とフラグ・段階的リリース。

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

- 本番と検証の設定コピペで権限過多を見逃す。
- オブザーバビリティ欠如（デプロイ後に気づけない）。
- ネットワークを広く開けたまま「後で締める」。
- DR 未検証を「あるはず」で済ませる。
- コスト影響を読まずにスケール設定だけ変更する。

## Workflow (Codex)

1. **Read target**: IaC・manifest・workflow ファイルを列挙。
2. **Skim**: 環境・権限・ネットワークの入口を掴む。
3. **Deep-read**: IaC → network → IAM → observability → DR → cost の順。
4. **Cite**: `file:line`。
5. **Grade**: 集計。
6. **Verdict**: Output Contract → `review-summary`。

## Machine Gate

レビュー本文の **最終行** は Output Contract の `review-summary` フェンス（キー固定: `grade`, `verdict`, `critical`, `high`, `medium`, `low`）とする。省略・キー名変更は禁止。
