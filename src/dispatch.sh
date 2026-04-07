#!/usr/bin/env bash
# =============================================================================
# dispatch.sh - Simplified single-shot task dispatcher for Claude Code
#
# Usage (from Claude Code's Bash tool):
#   ./dispatch.sh "Fix the bug in auth.ts" /path/to/workspace [model]
#
# Returns structured output that Claude Code can parse.
# =============================================================================

set -uo pipefail

CURSOR_AGENT="${CURSOR_AGENT_BIN:-$HOME/.local/bin/cursor-agent}"
PROMPT="${1:?Usage: dispatch.sh <prompt> [workspace] [model]}"
WORKSPACE="${2:-$(pwd)}"
MODEL="${3:-}"
LOG_DIR="${CURSORACP_LOG_DIR:-$(dirname "$0")/../logs}"

mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SESSION_LOG="$LOG_DIR/session_${TIMESTAMP}.jsonl"

# Build args
ARGS=(-p --output-format stream-json --workspace "$WORKSPACE" --trust --force)

if [[ -n "$MODEL" ]]; then
    ARGS+=(--model "$MODEL")
fi

ARGS+=("$PROMPT")

echo "=== DISPATCH START ===" >&2
echo "Time: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >&2
echo "Workspace: $WORKSPACE" >&2
echo "Model: ${MODEL:-default}" >&2
echo "Prompt: $PROMPT" >&2
echo "Log: $SESSION_LOG" >&2
echo "=== STREAMING ===" >&2

# Run and tee to log
"$CURSOR_AGENT" "${ARGS[@]}" 2>/dev/null | tee "$SESSION_LOG"
EXIT_CODE=${PIPESTATUS[0]}

echo "" >&2
echo "=== DISPATCH END (exit: $EXIT_CODE) ===" >&2

exit $EXIT_CODE
