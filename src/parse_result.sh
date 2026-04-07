#!/usr/bin/env bash
# =============================================================================
# parse_result.sh - Parse cursor-agent stream-json output
#
# Usage: cat session.jsonl | ./parse_result.sh
#        ./parse_result.sh < session.jsonl
#
# Extracts: final text, tool calls made, files modified, errors
# =============================================================================

set -uo pipefail

TEXT=""
TOOLS=()
ERRORS=()

while IFS= read -r line; do
    [[ -z "$line" ]] && continue

    # Try to extract event type
    type=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('type',''))" 2>/dev/null || echo "")

    case "$type" in
        "text"|"assistant")
            chunk=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('content','') or d.get('text','') or d.get('delta',''))" 2>/dev/null || echo "")
            TEXT="${TEXT}${chunk}"
            ;;
        "tool_call"|"tool")
            tool_name=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('name','') or d.get('tool',''))" 2>/dev/null || echo "")
            if [[ -n "$tool_name" ]]; then
                TOOLS+=("$tool_name")
            fi
            ;;
        "error")
            error_msg=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('message','') or d.get('error',''))" 2>/dev/null || echo "")
            ERRORS+=("$error_msg")
            ;;
        "result")
            result_text=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('text','') or d.get('content',''))" 2>/dev/null || echo "")
            if [[ -n "$result_text" ]]; then
                TEXT="${TEXT}${result_text}"
            fi
            # Extract session ID if available
            session_id=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('sessionId','') or d.get('chatId',''))" 2>/dev/null || echo "")
            ;;
    esac
done

# Output structured summary
cat <<EOF
{
  "text": $(python3 -c "import json; print(json.dumps('''$TEXT'''))" 2>/dev/null || echo "\"$TEXT\""),
  "tools_used": $(python3 -c "import json; print(json.dumps([$(printf '"%s",' "${TOOLS[@]}" 2>/dev/null || echo "")]))" 2>/dev/null || echo "[]"),
  "errors": $(python3 -c "import json; print(json.dumps([$(printf '"%s",' "${ERRORS[@]}" 2>/dev/null || echo "")]))" 2>/dev/null || echo "[]"),
  "session_id": "${session_id:-}"
}
EOF
