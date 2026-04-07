---
name: site-e2e-playwright
description: マーケサイト向け E2E。Playwright CLI、Cursor エージェントのターミナル実行、Playwright MCP（user-playwright）の使い分け。docs/site/e2e-scenarios.md を単一の真実にする（全PJ共通）。
---

# Site E2E + Playwright（全PJ共通）

## When to Use

- ユーザーが **`E2E実行`** と合図したとき
- [site-build-orchestrator](../site-build-orchestrator/SKILL.md) の実装後、受け入れを機械的に確認するとき
- Subagent **`site-e2e-runner`** が従う手順の正本

## 単一の真実

- **`docs/site/e2e-scenarios.md`** — シナリオ・Given-When-Then・回帰チェックリスト  
- リポに Playwright がある場合は **`e2e/`** または **`tests/e2e/`** 等の既存規約に **シナリオ ID または見出し**で対応づけを書く（本 SKILL の「対応表」節）

## 実行経路（優先順）

### A. Playwright CLI（本命・CI とも一致させやすい）

1. プロジェクトルートで `package.json` に `@playwright/test` または `playwright` があるか確認。
2. **dev サーバー**が必要なら、別ターミナルまたは `webServer` in `playwright.config` で起動済みにする。
3. エージェントは Cursor の **Agent チャットからターミナルツール**でコマンド実行する（実行環境は Cursor の **エージェント用シェル／サンドボックス設定**に従う。失敗時はユーザーへ同コマンドの手元実行を依頼）。
4. 標準コマンド例（プロジェクトの scripts に合わせて置換）:
   - `npx playwright test`
   - `npx playwright test --grep "@smoke"`
   - プレビュー URL だけ触る場合: `npx playwright test --config=playwright.config.ts`（中で `baseURL` を環境変数化）

### B. Playwright MCP（`user-playwright` / `playwright`）

CLI 不在、或いは **探索的に** `e2e-scenarios.md` をなぞるとき。

1. MCP ツールのスキーマを **`mcps/user-playwright/tools/*.json`** 等で確認してから `call_mcp_tool` する。
2. **サーバー名**: `user-playwright`（環境により表示名は `playwright`）。
3. 典型フロー: `browser_navigate` → `browser_snapshot` → `browser_click` / `browser_type` → 必要なら `browser_take_screenshot`。  
4. **シナリオごと**に結果を簡潔に記録し、最後に **パス / 失敗 / 未実施** を一覧にする。

### C. 手動

自動化が無い場合でも、`e2e-scenarios.md` のチェックリストを **人が潰す**前提で、エージェントは手順と期待結果だけ出す。

## Cursor エージェント環境について

- **ターミナル経由の Playwright**は、Cursor が Agent に与える **隔離・権限制約**の影響を受ける（ネットワーク禁止・特定パス読み取り専用等）。**失敗したら**ログを貼り、ユーザー側のローカル or CI で再現させる。
- MCP ブラウザは **別プロセス**のことが多く、CLI と同じ `baseURL` を明示して揃える。

## `e2e-scenarios.md` に書くとよい追加欄

各シナリオに次を任意で追加:

- `Playwright`: ファイル名 + `test.describe` / テスト名、または `@tag`
- `MCP`: 主要ステップの一行要約

## 完了の宣言

**テストを実際に実行**し、終了コード（または MCP 相当の証跡）と要約を出してから「パス」と言う。ホームに `verification-before-completion` SKILL があればそれにも従う。

## 参考

- Playwright: https://playwright.dev  
- Cursor Subagents: https://cursor.com/docs/subagents.md  
