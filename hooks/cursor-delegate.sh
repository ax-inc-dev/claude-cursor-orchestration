#!/bin/bash
# =============================================================================
# cursor-delegate.sh - Claude Code UserPromptSubmit Hook
#
# Automatically delegates coding tasks to Cursor Agent via CursorACP bridge.
# If cursor-agent CLI is NOT installed, exits silently (graceful fallback).
# =============================================================================

# Graceful fallback: if cursor-agent CLI is not installed, do nothing
if [ ! -f "$HOME/.local/bin/cursor-agent" ]; then
  exit 0
fi

# Resolve the plugin root (directory containing this script's parent)
PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DISPATCH="${PLUGIN_ROOT}/src/cursor_dispatch.py"

# Inject delegation instruction into Claude Code's context
cat <<HOOKEOF
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "CURSOR AGENT DELEGATION ACTIVE: When this task involves writing, editing, or generating code (including creating files, refactoring, fixing bugs, adding features), you MUST use the /app-development skill to orchestrate the full development flow. This skill dispatches coding work to Cursor Agent via CursorACP (python3 ${DISPATCH}) and follows a structured Phase 0-8 pipeline: conception → design review → parallel implementation → integration → quality review → fixes → E2E → deploy → PR. For read-only analysis, planning, reviews, and non-code tasks, handle them yourself directly without the skill."
  }
}
HOOKEOF
