# Sequence Diagrams

## 1. Basic Flow (Single Task)

```
User          Claude Code         Hook              CursorACP           Cursor Agent
 │                │                 │                   │                    │
 │  "Fix bug"     │                 │                   │                    │
 ├───────────────>│                 │                   │                    │
 │                │  UserPromptSubmit                   │                    │
 │                ├────────────────>│                   │                    │
 │                │  "DELEGATION    │                   │                    │
 │                │   ACTIVE"       │                   │                    │
 │                │<────────────────┤                   │                    │
 │                │                 │                   │                    │
 │                │  python3 cursor_dispatch.py         │                    │
 │                ├───────────────────────────────────>│                    │
 │                │                 │                   │  cursor-agent CLI  │
 │                │                 │                   ├───────────────────>│
 │                │                 │                   │  JSONL stream      │
 │                │                 │                   │<───────────────────┤
 │                │                 │  result JSON      │                    │
 │                │<───────────────────────────────────┤                    │
 │  "Done!"       │                 │                   │                    │
 │<───────────────┤                 │                   │                    │
```

## 2. Parallel Execution

```
Claude Code                CursorACP                 Cursor Agent(s)
 │                            │                          │
 │  parallel --tasks [A,B,C]  │                          │
 ├───────────────────────────>│                          │
 │                            │  ThreadPoolExecutor      │
 │                            │                          │
 │                            ├──── Task A ─────────────>│ Agent 1
 │                            ├──── Task B ─────────────>│ Agent 2
 │                            ├──── Task C ─────────────>│ Agent 3
 │                            │                          │
 │                            │<──── Result A ───────────┤
 │                            │<──── Result B ───────────┤
 │                            │<──── Result C ───────────┤
 │                            │                          │
 │  summary: 3/3 succeeded    │                          │
 │<───────────────────────────┤                          │
```

## 3. A2A Bidirectional Loop

```
Claude Code         CursorACP              Cursor Agent
 │                     │                      │
 │  "Build REST API"   │                      │
 ├────────────────────>│                      │
 │                     ├─────────────────────>│  Round 1
 │                     │  "TypeScript or      │
 │                     │   Python?"           │
 │                     │<─────────────────────┤
 │                     │                      │
 │                     │  Question detected!  │
 │                     │  Auto-answer:        │
 │                     │  "TypeScript"        │
 │                     │                      │
 │                     ├─── resume session ──>│  Round 2
 │                     │  "Express or         │
 │                     │   Fastify?"          │
 │                     │<─────────────────────┤
 │                     │                      │
 │                     │  Auto-answer:        │
 │                     │  "Fastify"           │
 │                     │                      │
 │                     ├─── resume session ──>│  Round 3
 │                     │  (task complete,     │
 │                     │   no question)       │
 │                     │<─────────────────────┤
 │                     │                      │
 │  completed: true    │                      │
 │  rounds: 3          │                      │
 │<────────────────────┤                      │
```

## 4. Full Phase 0-8 Pipeline

```
User          Claude Code              CursorACP / Cursor Agent
 │                │                          │
 │  "Build auth"  │                          │
 ├───────────────>│                          │
 │                │                          │
 │                │ ── Phase 0: Conception ──│
 │  "Requirements │                          │
 │   confirmed?"  │                          │
 │<───────────────┤                          │
 │  "Yes"         │                          │
 ├───────────────>│                          │
 │                │                          │
 │                │ ── Phase 1: Design ──────│
 │                │  (Claude designs)        │
 │                ├── review request ────────>│  (Codex model)
 │                │<── review result ─────────┤
 │                │                          │
 │                │ ── Phase 2: Implement ───│
 │                ├── parallel [auth, test] ─>│  (Composer Fast x2)
 │                │<── results ───────────────┤
 │                │                          │
 │                │ ── Phase 3: Integrate ───│
 │                │  (Claude reviews code)   │
 │                │                          │
 │                │ ── Phase 4: Quality ─────│
 │                ├── parallel [6 reviews] ──>│  (Codex x6)
 │                │<── review results ────────┤
 │                │                          │
 │                │ ── Phase 5: Fixes ───────│
 │                ├── fix tasks ─────────────>│  (Composer Fast)
 │                │<── fixed ─────────────────┤
 │                │                          │
 │                │ ── Phase 6: E2E ─────────│
 │                ├── run tests ─────────────>│
 │                │<── test results ──────────┤
 │                │                          │
 │                │ ── Phase 7: Deploy ──────│
 │                │  (Claude runs gcloud)    │
 │                │                          │
 │                │ ── Phase 8: PR ──────────│
 │                │  (Claude runs git/gh)    │
 │                │                          │
 │  "PR created:  │                          │
 │   github.com/  │                          │
 │   .../pull/42" │                          │
 │<───────────────┤                          │
```
