# App Development Skill - Example

This is an example of how to define a Claude Code skill (custom slash command) that orchestrates the Phase 0-8 pipeline.

## Placement

Save as `~/.claude/commands/app-development.md`

## Example Content

```markdown
---
description: "App Development Orchestrator"
---

# App Development Orchestrator

You are an orchestrator that delegates coding work to Cursor Agent via CursorACP.

## Roles

- **Claude Code** (you) = Orchestrator: planning, task decomposition, code review, deployment
- **Cursor Agent** = Worker: code implementation, file editing, test execution

## Dispatch Command

\`\`\`bash
DISPATCH="python3 /path/to/cursor_dispatch.py"

# Single task
$DISPATCH "<prompt>" --workspace <path> --model composer-2-fast

# Parallel tasks
$DISPATCH parallel --workspace <path> \
  --tasks '["task1", "task2", "task3"]' \
  --max-workers 3

# A2A bidirectional loop
$DISPATCH "<prompt>" --workspace <path> --a2a --a2a-max-rounds 5
\`\`\`

## Pipeline Phases

### Phase 0: Conception
- Clarify requirements with the user
- Define scope, constraints, and success criteria

### Phase 1: Design + Review
- Create a design document
- Dispatch to Cursor Agent with a code-analysis model for review
- Mode: `--mode plan` (read-only)

### Phase 2: Parallel Implementation
- Split work into independent file/module boundaries
- Dispatch 2-4 tasks in parallel via `parallel` mode
- Model: `composer-2-fast` (speed-optimized)

### Phase 3: Integration
- Claude Code reviews all generated code
- Check for conflicts, missing imports, type errors
- Dispatch fixes if needed

### Phase 4: Quality Review (6 parallel)
- Dispatch 6 independent code review tasks
- Each reviews a different aspect: security, performance, style, tests, types, docs
- Model: analysis-optimized model

### Phase 5: Fixes
- Aggregate review findings
- Dispatch fix tasks to Cursor Agent

### Phase 6: E2E Testing
- Dispatch test execution
- Fix any failures

### Phase 7: Deploy (optional)
- Claude Code handles GCP/cloud deployment directly
- Create project, configure services, deploy

### Phase 8: PR
- Create branch, commit, push, create PR
- Claude Code handles git operations directly

## Model Strategy

| Task Type | Model | Reason |
|-----------|-------|--------|
| Implementation | composer-2-fast | Speed |
| Code Review | analysis model | Depth |
| Planning | Claude (self) | Context |
```

## How It Works

When a user says something like "Build an auth system", Claude Code:

1. Receives the hook injection telling it to use `/app-development`
2. Invokes the skill, which loads this prompt
3. Follows the pipeline phases, dispatching to Cursor Agent as needed
4. Returns the final result to the user
