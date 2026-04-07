#!/usr/bin/env bash
# =============================================================================
# Claude Code -> Cursor Agent Orchestrator
#
# Claude Code (this script's caller) dispatches tasks to cursor-agent CLI,
# streams back results in real-time, and can chain multiple tasks.
# =============================================================================

set -euo pipefail

CURSOR_AGENT="${CURSOR_AGENT_BIN:-$HOME/.local/bin/cursor-agent}"
DEFAULT_WORKSPACE="${CURSOR_WORKSPACE:-$(pwd)}"
DEFAULT_MODEL="${CURSOR_MODEL:-}"  # e.g. "composer-2-fast", leave empty for default
TIMEOUT="${CURSOR_TIMEOUT:-600}"   # seconds

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

usage() {
    cat <<EOF
Usage: orchestrator.sh <command> [options]

Commands:
  run       <prompt>              Run a task and stream output
  run-json  <prompt>              Run a task, output structured JSON result
  models                          List available models
  status                          Check auth status
  session   <chatId> <prompt>     Resume a session with new prompt
  help                            Show this help

Options:
  --workspace <path>    Working directory (default: current dir)
  --model <model>       Model to use (e.g. composer-2-fast)
  --force               Auto-approve all tool calls
  --plan                Use plan mode (read-only analysis)
  --timeout <seconds>   Timeout (default: 600)

Examples:
  ./orchestrator.sh run "Fix the failing tests in src/api/"
  ./orchestrator.sh run --model composer-2-fast --force "Refactor auth module"
  ./orchestrator.sh run-json "Add error handling to utils.ts"
  ./orchestrator.sh session abc123 "Now add tests for that change"
EOF
}

log() { echo -e "${BLUE}[orchestrator]${NC} $*" >&2; }
warn() { echo -e "${YELLOW}[orchestrator]${NC} $*" >&2; }
err() { echo -e "${RED}[orchestrator]${NC} $*" >&2; }
ok() { echo -e "${GREEN}[orchestrator]${NC} $*" >&2; }

check_auth() {
    if ! "$CURSOR_AGENT" status 2>&1 | grep -q "Logged in"; then
        err "cursor-agent is not logged in. Run: cursor-agent login"
        return 1
    fi
}

# Run a task with stream-json output, parse events in real-time
run_task() {
    local prompt="$1"
    local workspace="${2:-$DEFAULT_WORKSPACE}"
    local model="${3:-$DEFAULT_MODEL}"
    local force="${4:-false}"
    local mode="${5:-}"
    local resume="${6:-}"

    local args=(-p --output-format stream-json --workspace "$workspace" --trust)

    if [[ -n "$model" ]]; then
        args+=(--model "$model")
    fi

    if [[ "$force" == "true" ]]; then
        args+=(--force)
    fi

    if [[ -n "$mode" ]]; then
        args+=(--mode "$mode")
    fi

    if [[ -n "$resume" ]]; then
        args+=(--resume "$resume")
    fi

    args+=("$prompt")

    log "Dispatching to cursor-agent..."
    log "  Workspace: $workspace"
    log "  Model: ${model:-default}"
    log "  Prompt: ${prompt:0:100}..."

    # Run cursor-agent and process stream
    local tmpfile
    tmpfile=$(mktemp /tmp/cursor-orchestrator-XXXXXX.jsonl)
    local exit_code=0

    "$CURSOR_AGENT" "${args[@]}" 2>/dev/null > "$tmpfile" &
    local pid=$!

    # Watchdog timer
    (
        sleep "$TIMEOUT"
        if kill -0 "$pid" 2>/dev/null; then
            warn "Timeout reached (${TIMEOUT}s), killing cursor-agent"
            kill "$pid" 2>/dev/null
        fi
    ) &
    local watchdog=$!

    # Stream and parse events
    tail -f "$tmpfile" 2>/dev/null &
    local tail_pid=$!

    wait "$pid" || exit_code=$?

    kill "$watchdog" 2>/dev/null || true
    kill "$tail_pid" 2>/dev/null || true

    if [[ $exit_code -ne 0 ]]; then
        err "cursor-agent exited with code $exit_code"
    else
        ok "Task completed successfully"
    fi

    # Return the raw output for Claude Code to parse
    cat "$tmpfile"
    rm -f "$tmpfile"
    return $exit_code
}

# Run and return only the final JSON result
run_task_json() {
    local prompt="$1"
    local workspace="${2:-$DEFAULT_WORKSPACE}"
    local model="${3:-$DEFAULT_MODEL}"
    local force="${4:-false}"

    local args=(-p --output-format json --workspace "$workspace" --trust)

    if [[ -n "$model" ]]; then
        args+=(--model "$model")
    fi

    if [[ "$force" == "true" ]]; then
        args+=(--force)
    fi

    args+=("$prompt")

    log "Dispatching to cursor-agent (json mode)..."

    "$CURSOR_AGENT" "${args[@]}" 2>/dev/null
    return $?
}

# ---- Main ----
COMMAND="${1:-help}"
shift || true

WORKSPACE="$DEFAULT_WORKSPACE"
MODEL="$DEFAULT_MODEL"
FORCE="false"
MODE=""
RESUME=""
PROMPT=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --workspace) WORKSPACE="$2"; shift 2 ;;
        --model) MODEL="$2"; shift 2 ;;
        --force) FORCE="true"; shift ;;
        --plan) MODE="plan"; shift ;;
        --timeout) TIMEOUT="$2"; shift 2 ;;
        *)
            if [[ -z "$PROMPT" ]]; then
                PROMPT="$1"
            else
                PROMPT="$PROMPT $1"
            fi
            shift
            ;;
    esac
done

case "$COMMAND" in
    run)
        [[ -z "$PROMPT" ]] && { err "No prompt provided"; usage; exit 1; }
        run_task "$PROMPT" "$WORKSPACE" "$MODEL" "$FORCE" "$MODE" "$RESUME"
        ;;
    run-json)
        [[ -z "$PROMPT" ]] && { err "No prompt provided"; usage; exit 1; }
        run_task_json "$PROMPT" "$WORKSPACE" "$MODEL" "$FORCE"
        ;;
    models)
        "$CURSOR_AGENT" --list-models 2>&1
        ;;
    status)
        "$CURSOR_AGENT" status 2>&1
        ;;
    session)
        RESUME="$PROMPT"
        PROMPT="${*}"
        [[ -z "$RESUME" ]] && { err "No session ID provided"; exit 1; }
        [[ -z "$PROMPT" ]] && { err "No prompt provided"; exit 1; }
        run_task "$PROMPT" "$WORKSPACE" "$MODEL" "$FORCE" "$MODE" "$RESUME"
        ;;
    help|--help|-h)
        usage
        ;;
    *)
        err "Unknown command: $COMMAND"
        usage
        exit 1
        ;;
esac
