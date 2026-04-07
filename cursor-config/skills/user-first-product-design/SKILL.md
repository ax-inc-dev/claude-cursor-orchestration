---
name: user-first-product-design
description: アプリ・Web 製品のユーザーファースト設計の正本。目的・タスク・認知負荷・エラー・Accessibility を先に固定してから UI/Figma/実装に進む（全PJ共通）。
---

# User-First Product Design

## When to Use

- **すべてのアプリケーション／プロダクト UI** を触る前（Figma・コード・要件のいずれでも）
- [figma-mcp-design-orchestrator](../figma-mcp-design-orchestrator/SKILL.md) の **Phase 0**
- 機能一覧だけ決まっていて **誰が何のために使うか**が薄いときの再出発

## フロントエンド実装との順序（全PJ）

**顧客／ユーザーファーストで体験と画面の契約を先に決め、内部構造はその後。**  
コンポーネント設計・リポジトリのフォルダ構成・グローバル状態・API の振り分けを **UI 設計より前**に始めると、見た目・タスク・a11y が後付けになり品質が落ちやすい。

- **アプリ系**: 本 SKILL → `product-ui-ux-design`（および **`/product-ui-ux-designer`**）で `docs/ux-design/` 等を埋めてから実装。
- **マーケサイト系**: `site-build-orchestrator` と **`/site-design-planner`** で `docs/site/*` を埋め、**`計画承認`** 後に **`/site-frontend-implementer`**。
- **トークンが DESIGN.md で固定されている場合**: [design-md-reference](../design-md-reference/SKILL.md) を併読。

グローバルルールの単一記述: **`~/.cursor/rules/global-agent-workflow.mdc`**（「フロントエンド実装の順序」）、人間向け要約: **`~/.cursor/CURSOR_GLOBAL_RULES.md`**。

## 原則（優先順）

1. **ユーザーの成果（Outcome）** が先。機能や画面数は後。
2. **主要タスク**（理想は 1 セッション 1 主目的）を文章化してからワイヤーやフレームを作る。
3. **圧倒的に使いやすいか**は「学習コストが低いか・迷わないか・ミスから戻れるか・待たされないか」で測る。主観「かっこいい」だけにしない。
4. **アプリの目的**（事業目的・成功指標）とユーザーの目的の **接点** を明示する。一致していなければ設計を疑う。
5. **Accessibility**：色だけに頼らない情報、`focus` / キーボード、コントラスト、動き（`prefers-reduced-motion`）を後回しにしない。

## 設計前チェックリスト（出力前に自分で埋める）

| 問い | 答え |
|------|------|
| 主ユーザーは誰か（1 手で書けるか） | |
| その人が「今日ここで達成したいこと」は | |
| 失敗・離脱が一番コスト高いのはどの操作か | |
| 初見が **3 秒**で理解すべきことは | |
| 絶対に誤操作させたくない操作と、その防止 | |
| オフライン・遅延・権限不足のときの振る舞い | |

## 成果物（リポに残すなら）

プロジェクトルートに `docs/design/` を推奨（テンプレは `~/.cursor/templates/docs-design/`）。

- **誰の・何のための UI か**を一文で
- **タスクフロー**（箇条書きでよい）
- **非対象**（やらないこと／後回し）

## よくあるアンチパターン

- スクリーン一覧から入る（タスクが見えない）
- 全ロールに同じ画面上詰め込み（意思決定者と実行者を混在）
- エラーを「Something went wrong」で丸める
- デザインシステムの見た目だけ真似して **情報の優先順位**が崩れる

## 接続

- **Figma で形にする**前に本 Skill を完了させる。  
- Figma MCP 作業は [figma-mcp-design-orchestrator](../figma-mcp-design-orchestrator/SKILL.md) へ。

## 参考（外部）

- [Nielsen Norman — usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)（ヒューリスティクス演習に利用可）
