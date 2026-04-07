#!/bin/bash
# =============================================================================
# cursor-delegate.sh - Claude Code UserPromptSubmit Hook
#
# This hook runs every time the user submits a prompt to Claude Code.
# If cursor-agent CLI is installed, it injects a delegation instruction
# so that coding tasks are automatically routed to Cursor Agent.
#
# If cursor-agent is NOT installed, the hook exits silently and
# Claude Code handles everything directly (graceful fallback).
#
# Setup:
#   1. Place this file somewhere accessible (e.g. ~/.claude-code/hooks/)
#   2. Add to ~/.claude/settings.json:
#      {
#        "hooks": {
#          "UserPromptSubmit": [{
#            "hooks": [{
#              "type": "command",
#              "command": "/path/to/cursor-delegate.sh"
#            }]
#          }]
#        }
#      }
# =============================================================================

# Graceful fallback: if cursor-agent CLI is not installed, do nothing
if [ ! -f "$HOME/.local/bin/cursor-agent" ]; then
  exit 0
fi

# Inject delegation instruction into Claude Code's context
cat <<'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "CURSOR AGENT DELEGATION ACTIVE: When this task involves writing, editing, or generating code (including creating files, refactoring, fixing bugs, adding features), you MUST use the /app-development skill to orchestrate the full development flow. This skill dispatches coding work to Cursor Agent via CursorACP (python3 /path/to/cursor_dispatch.py) and follows a structured Phase 0-8 pipeline: conception → design review → parallel implementation → integration → quality review → fixes → E2E → deploy → PR. For read-only analysis, planning, reviews, and non-code tasks, handle them yourself directly without the skill."
  }
}
EOF
