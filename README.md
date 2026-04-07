# Claude Code + Cursor Agent Orchestration (CursorACP)

**Claude Code をオーケストレーター、Cursor Agent を実装ワーカーとして連携させるエージェントオーケストレーションシステム**

<p align="center">
  <img src="docs/architecture-overview.svg" alt="Architecture Overview" width="800">
</p>

## TL;DR

- Claude Code（Anthropic CLI）が **設計・レビュー・デプロイ判断** を担当
- Cursor Agent（Cursor CLI）が **コード実装・テスト・ファイル編集** を担当
- Python ブリッジ (`cursor_dispatch.py`) が両者を繋ぎ、並列実行・A2A対話・セッション管理を提供
- Claude Code の Hook 機構でコーディングタスクを **自動的に** Cursor Agent に委譲

---

## 目次

- [なぜこの構成なのか](#なぜこの構成なのか)
- [コスト・速度・コンテキストの最適化](#コスト速度コンテキストの最適化)
- [アーキテクチャ](#アーキテクチャ)
- [セットアップ（自動）](#セットアップ自動)
- [Cursor エコシステムとの連携](#cursor-エコシステムとの連携)
- [パイプライン（Phase 0-8）](#パイプラインphase-0-8)
- [CursorACP ブリッジの3つのモード](#cursoracp-ブリッジの3つのモード)
- [自動委譲の仕組み（Hook）](#自動委譲の仕組みhook)
- [メリット・デメリット](#メリットデメリット)
- [ファイル構成](#ファイル構成)
- [使い方の例](#使い方の例)
- [License](#license)

---

## なぜこの構成なのか

AI コーディングエージェントは単体でも強力ですが、**得意分野が異なります**：

| 能力 | Claude Code | Cursor Agent |
|------|-------------|--------------|
| 長文コンテキスト理解・設計 | ★★★★★ | ★★★ |
| コードレビュー・品質判断 | ★★★★★ | ★★★ |
| ファイル編集・リファクタリング | ★★★ | ★★★★★ |
| IDE統合・LSP連携 | ★★ | ★★★★★ |
| GCP/インフラ操作 | ★★★★ | ★★ |
| 並列タスク実行 | ★★★★ | ★★★★★ |

**一つのエージェントにすべてを任せる** のではなく、**それぞれの強みを活かして協調** させることで、より高品質なアウトプットを高速に得られます。

---

## コスト・速度・コンテキストの最適化

この構成の最大のメリットの一つは、**Claude Code (Opus) のコンテキストウィンドウを劇的に節約** できることです。

### コンテキスト削減効果

通常、Claude Code 単体で開発する場合：

```
ユーザー指示       →  コード読み取り  →  コード生成  →  テスト実行  →  修正
       ↓                  ↓                ↓              ↓           ↓
  Opus コンテキスト: [全部ここに積まれる ─────────────────────────────── 200K tokens]
```

CursorACP 構成の場合：

```
  Claude Code (Opus):  [設計] ─── [指示出し] ─── [結果レビュー]  → ~20-40K tokens
  Cursor Agent:        ──────── [実装の全詳細] ──────────────────  → Cursor側で処理
```

| シナリオ | Opus 単体 | CursorACP 構成 | 削減率 |
|---------|-----------|---------------|--------|
| 小規模機能追加 | ~50K tokens | ~15K tokens | **70%** |
| 中規模機能（3ファイル） | ~120K tokens | ~30K tokens | **75%** |
| 大規模開発（10+ファイル） | ~180K tokens（上限に迫る） | ~40K tokens | **78%** |

**なぜこれほど削減できるのか：**

1. **ファイル内容を Opus が読まない** — Cursor Agent が LSP/IDE 経由でファイルを直接操作するので、Opus のコンテキストにコード全文が載らない
2. **生成コードが Opus を通らない** — コード生成は Cursor 側で完結。Opus には「成功/失敗」と要約だけが返る
3. **テスト実行ログが Opus を通らない** — テスト出力も Cursor 側で処理される

### コスト比較

| 項目 | Claude Code 単体 | CursorACP 構成 |
|------|-----------------|---------------|
| **Opus API** | ~$15/M input, ~$75/M output | 設計・レビューのみ → **1/3〜1/4 に削減** |
| **Cursor** | 使わない | Pro $20/月（定額） |
| **Composer 2 Fast** | — | Cursor Pro に含まれる（追加課金なし） |
| **合計（中規模開発）** | Opus だけで $3-5/タスク | Opus $0.8-1.5 + Cursor $20/月 |

**ポイント：** Cursor の Composer 2 Fast は **Cursor Pro ($20/月) に含まれる定額制** なので、実装をいくら投げてもコストは変わりません。Opus の従量課金を設計・レビューだけに絞ることで、全体コストを大幅に抑えられます。

### Opus の自律性 + Cursor の速度 = いいとこ取り

```
┌─── Opus の強み（そのまま活かす）─────────────────┐
│ - 200K コンテキストでプロジェクト全体を俯瞰      │
│ - 複雑な設計判断・アーキテクチャ決定              │
│ - 自律的にタスク分割・優先順位付け                │
│ - コードレビューで潜在バグ・セキュリティ問題発見  │
│ - git/GCP/インフラを直接操作                      │
└─────────────────────────────────────────────────┘
         ↕ cursor_dispatch.py（指示と結果だけ）
┌─── Cursor の強み（委譲して活かす）──────────────┐
│ - Composer 2 Fast: 超高速コード生成（定額制）    │
│ - LSP統合: 型チェック・インポート解決が正確      │
│ - IDE統合: リアルタイムのシンタックスエラー検出  │
│ - 並列実行: 複数エージェントが同時にコード生成   │
│ - $20/月定額: 何回呼んでも追加コストなし         │
└─────────────────────────────────────────────────┘
```

Opus の 200K コンテキストを **設計と判断** に使い、Cursor の高速・安価な実装力で **コード生成** を行う。これが「いいとこ取り」の本質です。

---

## アーキテクチャ

```
┌─────────────────────────────────────────────────────┐
│                    ユーザー                           │
│              「認証機能を作って」                       │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              Claude Code (Orchestrator)               │
│                                                       │
│  ┌─────────┐  ┌──────────┐  ┌─────────────────────┐ │
│  │ Hook    │→│ Skill     │→│ Phase Pipeline       │ │
│  │ (auto   │  │ (/app-   │  │ 0: Conception       │ │
│  │ detect) │  │ develop- │  │ 1: Design + Review  │ │
│  │         │  │ ment)    │  │ 2: Implementation   │ │
│  └─────────┘  └──────────┘  │ 3: Integration      │ │
│                              │ 4: Quality Review   │ │
│                              │ 5: Fixes            │ │
│                              │ 6: E2E Testing      │ │
│                              │ 7: GCP Deploy       │ │
│                              │ 8: PR               │ │
│                              └────────┬────────────┘ │
└───────────────────────────────────────┼──────────────┘
                                        │
                    python3 cursor_dispatch.py
                                        │
                                        ▼
┌─────────────────────────────────────────────────────┐
│              CursorACP Bridge (Python)                │
│                                                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │ Single   │  │ Parallel │  │ A2A Bidirectional│   │
│  │ Task     │  │ Tasks    │  │ Loop             │   │
│  └─────┬────┘  └────┬─────┘  └────────┬─────────┘   │
│        │             │                 │              │
│        └─────────────┼─────────────────┘              │
│                      │                                │
│              cursor-agent CLI                         │
│              (JSONL stream)                            │
└──────────────────────┼────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│              Cursor Agent (Worker)                     │
│                                                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │ Code     │  │ File     │  │ Tool             │   │
│  │ Generate │  │ Edit     │  │ Execution        │   │
│  └──────────┘  └──────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## セットアップ（自動）

### 前提条件

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (CLI) がインストール済み
- [Cursor](https://cursor.sh/) Pro/Business プラン（$20/月〜）
- Python 3.10+

### ワンコマンドセットアップ

```bash
# 1. cursor-agent CLI をインストール（まだの場合）
curl https://cursor.com/install -fsSL | bash
cursor-agent login

# 2. このリポジトリを clone して setup.sh を実行
git clone https://github.com/bunta-ishiwata/claude-cursor-orchestration.git
cd claude-cursor-orchestration
./setup.sh
```

`setup.sh` が自動的に以下を行います：
- cursor-agent / Claude Code / Python の存在確認
- Hook スクリプトの配置（`~/.claude-code/hooks/cursor-delegate.sh`）
- `~/.claude/settings.json` への Hook 登録（既存設定を壊さずマージ）
- `/app-development` スキルの配置（`~/.claude/commands/app-development.md`）

**Claude Code に依頼する場合：**
```
> このリポジトリの setup.sh を実行して
```
Claude Code が自分でスクリプトを読んで実行してくれます。

### 手動セットアップ

自動セットアップがうまくいかない場合は [docs/skill-example.md](docs/skill-example.md) を参照。

---

## Cursor エコシステムとの連携

このシステムは Cursor の豊富なエコシステムを活用しています。

### cursor-agent CLI（公式）

[Cursor 公式 CLI](https://cursor.com/docs/cli/overview)。ターミナルから Cursor の AI エージェントを呼び出せます。

```bash
# 3つのモード
cursor-agent "Fix the bug"                    # Agent モード（デフォルト）: ファイル編集・コマンド実行
cursor-agent --mode plan "How to refactor?"   # Plan モード: 設計のみ、コード変更なし
cursor-agent --mode ask "Explain this code"   # Ask モード: 読み取り専用分析
```

| 特徴 | 説明 |
|------|------|
| **Agent モード** | ファイル編集、ターミナル実行、マルチファイル操作を自律的に実行 |
| **Plan モード** | コード変更なしで設計・分析。CursorACP の Phase 1 で活用 |
| **Ask モード** | 読み取り専用。コードの説明や調査に使用 |
| **Cloud Handoff** | `&` プレフィックスでローカル→クラウドに移行。オフラインでも継続実行 |
| **Session Resume** | `--resume <session_id>` で中断したセッションを再開。A2A ループの核心技術 |

### ACP（Agent Client Protocol）

[ACP](https://agentcommunicationprotocol.dev/) は JetBrains と Zed が策定した**オープン標準プロトコル**。AI エージェントとエディタの通信を標準化します。

- Cursor は ACP を公式サポート → JetBrains IDE（IntelliJ, PyCharm 等）でも Cursor エージェントが動作
- CursorACP はこの ACP 対応 CLI を介して Claude Code と Cursor を橋渡し

### Cursor Agent（IDE 内蔵）

Cursor 3 で全面刷新された**エージェントファースト**のインターフェース：

- **マルチファイル編集** — プロジェクト全体を理解した上でファイル横断の変更
- **並列エージェント** — 複数エージェントが同時に異なるリポジトリ/ワークツリーで作業
- **Memory 機能** — 過去の実行から学習し、繰り返し使うほど精度向上
- **MCP 対応** — 外部ツール（DB、API、ブラウザ等）を MCP 経由で利用可能

### Cursor Skills / Superpowers

Cursor は独自の **Skills** フレームワークを持ち、開発ワークフローを定義できます：

- **Skills** — `~/.cursor/skills/` に配置する構造化ワークフロー定義。コンテキストに応じて自動トリガー
  - レビュー系: セキュリティ、アーキテクチャ、フロントエンド、バックエンド
  - 開発系: TDD、デバッグ、プランニング
  - スキル自体の作成: `create-cursor-skill`

- **[Superpowers](https://cursor.com/marketplace)** — Cursor プラグインマーケットプレイスで配布される開発フレームワーク
  - スペック策定 → 計画 → TDD（RED-GREEN-REFACTOR）→ サブエージェント駆動開発
  - `/add-plugin superpowers` で Cursor に追加可能

### Cursor Plugin Marketplace

Cursor 3 で追加された**プラグインマーケットプレイス**：
- MCP サーバー、Skills、サブエージェントをワンクリックインストール
- VS Code 拡張との互換性も維持（Open VSX Registry 経由）
- チーム向けプライベートマーケットプレイスも構築可能

> **Note:** CursorACP はこれらの Cursor エコシステムの上に構築されています。Cursor 側で Skills や Superpowers を設定しておくと、委譲されたタスクの品質がさらに向上します。

---

## パイプライン（Phase 0-8）

開発タスクが委譲されると、以下のフェーズを順に実行します：

| Phase | 担当 | 内容 | モデル |
|-------|------|------|--------|
| **0. Conception** | Claude Code | 要件整理・ヒアリング | Claude Opus |
| **1. Design + Review** | Claude Code → Cursor | 設計書作成 + Codex レビュー | Codex High |
| **2. Implementation** | Cursor Agent (並列) | コード実装 | Composer 2 Fast |
| **3. Integration** | Claude Code | 統合確認・コンフリクト解決 | Claude Opus |
| **4. Quality Review** | Cursor Agent (6並列) | コード品質レビュー | Codex High |
| **5. Fixes** | Cursor Agent | レビュー指摘の修正 | Composer 2 Fast |
| **6. E2E Testing** | Cursor Agent | テスト実行・修正 | Composer 2 Fast |
| **7. GCP Deploy** | Claude Code | GCP プロジェクト作成・デプロイ | Claude Opus |
| **8. PR** | Claude Code | ブランチ整理・PR 作成 | Claude Opus |

### フェーズ間の役割分担イメージ

```
Claude Code:  ████░░░░░░████░░░░░░░░░░████░░░░░░████████
Cursor Agent: ░░░░████████░░░░████████████████████░░░░░░░░
              Ph0  Ph1  Ph2  Ph3  Ph4  Ph5  Ph6  Ph7  Ph8
```

---

## CursorACP ブリッジの3つのモード

### 1. Single Task Mode

一つのタスクを一つの Cursor Agent セッションで実行。

```bash
python3 cursor_dispatch.py "Fix the failing tests in src/auth/" \
  --workspace /path/to/project \
  --model composer-2-fast
```

**出力（JSON）：**
```json
{
  "success": true,
  "text": "Fixed 3 failing tests...",
  "tool_calls": [{"name": "editFile", "path": "src/auth/test_login.py"}],
  "session_id": "abc123",
  "has_question": false
}
```

### 2. Parallel Mode

独立した複数タスクを同時実行。ファイル競合を避けるため、事前にタスク分割が重要。

```bash
python3 cursor_dispatch.py parallel \
  --workspace /path/to/project \
  --tasks '["Implement auth in src/auth/", "Add tests in tests/", "Update docs in docs/"]' \
  --max-workers 3 \
  --model composer-2-fast
```

**出力（JSON）：**
```json
{
  "results": [...],
  "summary": {
    "total": 3,
    "succeeded": 3,
    "failed": 0,
    "has_questions": 0
  }
}
```

### 3. A2A (Agent-to-Agent) Bidirectional Loop

Cursor Agent が質問を返した場合、Claude Code が自動回答してセッションを再開。

```bash
python3 cursor_dispatch.py "Build a complete REST API" \
  --workspace /path/to/project \
  --a2a \
  --a2a-max-rounds 5
```

**フロー：**
```
Round 1: Claude → "Build REST API" → Cursor
         Cursor → "TypeScript or Python?" → Claude
Round 2: Claude → "TypeScript" → Cursor
         Cursor → "Express or Fastify?" → Claude  
Round 3: Claude → "Fastify" → Cursor
         Cursor → (completes task, no question)
→ Done in 3 rounds
```

**質問検出の仕組み：**
```python
QUESTION_PATTERNS = [
    r'[？\?]\s*$',                    # 末尾が ? or ？
    r'(?:which|should|do you|would)',  # 英語の質問パターン
    r'(?:ですか|でしょうか|ますか)',      # 日本語の質問パターン
    r'(?:option\s*[1-9]|choice)',      # 選択肢の提示
]
```

---

## 自動委譲の仕組み（Hook）

Claude Code の Hook 機構を使って、**ユーザーが意識することなく** コーディングタスクを Cursor Agent に委譲します。

```
ユーザー: 「認証機能を追加して」
    │
    ▼
┌───────────────────────────────────┐
│ UserPromptSubmit Hook             │
│ cursor-delegate.sh が実行される    │
│                                   │
│ cursor-agent CLI が存在する？      │
│   Yes → 委譲指示を注入            │
│   No  → 何もしない（フォールバック）│
└───────────────────┬───────────────┘
                    │
                    ▼
┌───────────────────────────────────┐
│ Claude Code                       │
│ 「コーディングタスクだ」と判断     │
│ → /app-development スキルを起動   │
│ → Phase 0-8 パイプライン開始      │
└───────────────────────────────────┘
```

**ポイント：**
- `cursor-agent` がインストールされていない環境では、Hook は何もせず Claude Code が単体で処理
- 分析・計画・レビューなど非コーディングタスクは Claude Code が直接処理
- コーディングタスクのみ Cursor Agent に委譲

---

## メリット・デメリット

### メリット

| メリット | 説明 |
|---------|------|
| **Opus コンテキスト 70-80% 削減** | 実装の詳細が Opus のコンテキストを消費しない。設計とレビューだけに集中 → 200K トークンを有効活用 |
| **コスト最適化** | 実装は Cursor Pro 定額（$20/月）に含まれる Composer 2 Fast で処理。Opus の従量課金を 1/3〜1/4 に削減 |
| **Opus の自律性はそのまま** | 設計判断・タスク分割・優先順位付け・コードレビュー・デプロイ判断は全て Opus が自律的に実行 |
| **Cursor の高速実装** | Composer 2 Fast は高速・LSP統合・型チェック連携。IDE の恩恵をフル活用したコード生成 |
| **専門性の分離** | Claude Code は設計・レビュー、Cursor は実装に集中。それぞれの得意領域を最大活用 |
| **並列実行による高速化** | 独立したタスクを複数の Cursor Agent で同時実行。3-4タスク並列で大幅な時間短縮 |
| **品質の二重チェック** | Claude Code が設計、Cursor が実装、Claude Code がレビューという三段階で品質担保 |
| **フォールバック** | cursor-agent が未インストールなら Claude Code 単体で処理。環境に依存しない |
| **A2A 対話** | エージェント間で自動的に質問→回答→再開。人間の介入なしに曖昧さを解決 |
| **完全なログ** | 全セッションの JSONL ログ。デバッグ・監査・改善に活用可能 |

### デメリット

| デメリット | 説明 |
|-----------|------|
| **セットアップの複雑さ** | Claude Code + Cursor + cursor-agent CLI + Hook + Skill の設定が必要。初期構築コストが高い |
| **コスト** | 2つのAIサービスのAPI利用料が発生。設計レビュー（Claude）+ 実装（Cursor）で単体より高額 |
| **デバッグの難しさ** | 問題発生時、Claude Code 側か Cursor Agent 側かの切り分けが必要。ログを追う手間 |
| **cursor-agent CLI への依存** | Cursor 公式 CLI（ACP 対応）に依存。バージョンアップで破壊的変更の可能性あり |
| **並列実行のファイル競合** | 同じファイルを複数タスクが同時編集するとコンフリクト。事前のタスク分割設計が重要 |
| **A2A の不確実性** | 質問検出が正規表現ベース。複雑な質問や想定外の形式を見逃す可能性 |
| **レイテンシ** | エージェント間の通信（CLI呼び出し + JSONL パース）にオーバーヘッド。小さなタスクでは割に合わない |
| **Cursor の認証管理** | `cursor-agent login` によるセッション管理が必要。トークン期限切れのハンドリング |

### 向いているケース / 向いていないケース

**向いているケース：**
- 中〜大規模の新機能開発（Phase 0-8 のフルパイプラインが活きる）
- 複数の独立したファイル/モジュールを同時に作成するタスク
- 品質が重要なプロダクションコード（二重レビュー体制）
- GCP デプロイまで一気通貫で行いたい場合

**向いていないケース：**
- 1ファイルのバグ修正や小さな変更（オーバーヘッドが大きい）
- Cursor のサブスクリプションがない環境
- ネットワークが不安定な環境（2つのAI APIへの接続が必要）
- 実験的・探索的なコーディング（対話的にやる方が効率的）

---

## ファイル構成

```
.
├── README.md                          # このファイル
├── setup.sh                           # ワンコマンド自動セットアップ
├── src/
│   ├── cursor_dispatch.py             # メインブリッジ（Single/Parallel/A2A）
│   ├── orchestrator.sh                # Bash ラッパー（リアルタイム出力）
│   ├── dispatch.sh                    # 簡易ディスパッチャー
│   └── parse_result.sh               # JSONL パーサー
├── hooks/
│   └── cursor-delegate.sh            # Claude Code Hook スクリプト
├── skills/
│   └── app-development-example.md    # スキル定義の例
└── docs/
    ├── architecture-overview.svg      # アーキテクチャ図
    ├── sequence-diagram.md            # シーケンス図
    └── skill-example.md              # スキル設定ガイド
```

---

## 使い方の例

### 基本的な使い方（自動委譲）

Hook を設定済みなら、Claude Code に普通に話しかけるだけ：

```
> 認証機能を追加して

Claude Code が自動的に:
1. 要件を整理（Phase 0）
2. 設計書を作成（Phase 1）
3. Cursor Agent に実装を委譲（Phase 2）
4. コードをレビュー（Phase 4）
5. PR を作成（Phase 8）
```

### 手動でブリッジを使う

```bash
# 単一タスク
python3 src/cursor_dispatch.py "Fix auth bug" -w /my/project

# 並列タスク
python3 src/cursor_dispatch.py parallel \
  --tasks '["Add login", "Add tests", "Update docs"]' \
  -w /my/project --max-workers 3

# A2A ループ
python3 src/cursor_dispatch.py "Build REST API" \
  -w /my/project --a2a --a2a-max-rounds 5

# ステータス確認
python3 src/cursor_dispatch.py --status
```

---

## 技術的な詳細

### JSONL イベントストリーム

cursor-agent CLI は以下の形式でイベントをストリーム出力します：

```jsonc
// 初期化
{"type":"system","subtype":"init","session_id":"...","model":"Composer 2 Fast"}

// ツール呼び出し
{"type":"tool_call","subtype":"started","tool_call":{"editToolCall":{"args":{"path":"src/auth.ts"}}}}

// 完了
{"type":"result","subtype":"success","duration_ms":10703,"usage":{"inputTokens":1386,"outputTokens":512}}
```

### セッション再開（Resume）

A2A ループの核心技術。session_id を使って Cursor Agent のコンテキストを保持したまま対話を継続：

```bash
# 初回タスク → session_id を取得
result=$(python3 cursor_dispatch.py "Build API" -w /project)
session_id=$(echo $result | jq -r '.session_id')

# 追加指示で再開
python3 cursor_dispatch.py "Add rate limiting too" \
  --resume $session_id -w /project
```

---

## License

MIT

---

## Contributing

Issues や PR を歓迎します。特に以下の改善に興味があります：

- 質問検出の精度向上（現在は正規表現ベース）
- ファイル競合の自動検出・解決
- より多くのデプロイターゲット（AWS, Vercel, etc.）
- cursor-agent CLI のバージョン互換性管理
