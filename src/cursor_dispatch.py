#!/usr/bin/env python3
"""
cursor_dispatch.py - Claude Code <-> Cursor Agent bridge

Supports:
  - Single task dispatch
  - Parallel dispatch (multiple tasks simultaneously)
  - A2A-style bidirectional loop (auto-detect questions, respond, resume)

Usage:
    # Single task
    python3 cursor_dispatch.py "Fix the bug" --workspace /path

    # Parallel tasks (comma-separated or JSON array)
    python3 cursor_dispatch.py parallel --workspace /path \
      --tasks '["Implement auth in src/auth/", "Add tests in tests/"]'

    # A2A loop (auto-answers Cursor's questions via Claude Code LLM)
    python3 cursor_dispatch.py "Build auth system" --workspace /path --a2a

    # Utilities
    python3 cursor_dispatch.py --status
    python3 cursor_dispatch.py --models
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import re
import threading
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

CURSOR_AGENT = os.environ.get("CURSOR_AGENT_BIN", os.path.expanduser("~/.local/bin/cursor-agent"))
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# A2A question detection patterns
QUESTION_PATTERNS = [
    r'[？\?]\s*$',                       # ends with ? or ？
    r'(?:which|should|do you|would you|can you|shall|prefer)',  # EN question words
    r'(?:option\s*[1-9AB]|choice|alternative)',  # offering choices
    r'(?:confirm|clarify|decide|choose)',  # asking for decisions
    r'(?:ですか|でしょうか|ますか|しますか|どちらが|どれを|選んで)',  # JP question words
    r'(?:よいですか|いいですか|どうしますか|進めて)',  # JP decision words
]
QUESTION_RE = re.compile('|'.join(QUESTION_PATTERNS), re.IGNORECASE)


def parse_events(raw_output: str) -> List[dict]:
    """Parse JSONL output into event list."""
    events = []
    for line in raw_output.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return events


def extract_result(events: List[dict]) -> dict:
    """Extract structured result from parsed events."""
    text_chunks = []
    thinking_chunks = []
    tool_calls = []
    errors = []
    session_id = None
    has_question = False
    question_text = ""

    for event in events:
        etype = event.get("type", "")
        subtype = event.get("subtype", "")

        if etype == "system":
            session_id = event.get("session_id", session_id)

        elif etype == "assistant":
            msg = event.get("message", {})
            for block in msg.get("content", []):
                if block.get("type") == "text":
                    chunk = block.get("text", "")
                    if chunk.strip():
                        text_chunks.append(chunk)

        elif etype == "tool_call" and subtype == "started":
            tc = event.get("tool_call", {})
            for key in tc:
                if key.endswith("ToolCall") or key.endswith("_call"):
                    tool_calls.append({
                        "name": key,
                        "args": tc[key].get("args", {}),
                    })
                    break

        elif etype == "error":
            msg = event.get("message", "") or event.get("error", str(event))
            errors.append(msg)

        elif etype == "result":
            session_id = event.get("session_id", session_id)

    full_text = "".join(text_chunks)

    # Detect if Cursor is asking a question (A2A signal)
    if QUESTION_RE.search(full_text):
        # Extract the last paragraph as the question
        paragraphs = [p.strip() for p in full_text.split('\n\n') if p.strip()]
        if paragraphs:
            last = paragraphs[-1]
            if QUESTION_RE.search(last):
                has_question = True
                question_text = last

    return {
        "text": full_text,
        "thinking": "".join(thinking_chunks),
        "tool_calls": tool_calls,
        "errors": errors,
        "session_id": session_id or "",
        "has_question": has_question,
        "question_text": question_text,
    }


def run_task(prompt: str, workspace: str, model: Optional[str] = None,
             force: bool = True, mode: Optional[str] = None,
             resume: Optional[str] = None, timeout: int = 600,
             task_id: Optional[str] = None) -> dict:
    """Run a single task via cursor-agent. Returns structured result."""

    args = [CURSOR_AGENT, "-p", "--output-format", "stream-json",
            "--workspace", workspace, "--trust"]

    if force:
        args.append("--force")
    if model:
        args.extend(["--model", model])
    if mode:
        args.extend(["--mode", mode])
    if resume:
        args.extend(["--resume", resume])

    args.append(prompt)

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    uid = hashlib.md5(f"{prompt}{ts}".encode()).hexdigest()[:6]
    tid = task_id or uid
    log_file = LOG_DIR / f"session_{ts}_{tid}.jsonl"

    prefix = f"[{tid}]"
    print(f"{prefix} dispatch workspace={workspace}", file=sys.stderr)
    print(f"{prefix} model={model or 'default'}", file=sys.stderr)
    print(f"{prefix} prompt={prompt[:100]}...", file=sys.stderr)

    try:
        proc = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

        raw_lines = []
        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue
            raw_lines.append(line)

            # Write to log
            with open(log_file, "a") as f:
                f.write(line + "\n")

            # Real-time status to stderr
            try:
                event = json.loads(line)
                etype = event.get("type", "")
                subtype = event.get("subtype", "")

                if etype == "system":
                    print(f"{prefix} [system] session={event.get('session_id', '')}", file=sys.stderr)
                elif etype == "assistant":
                    msg = event.get("message", {})
                    for block in msg.get("content", []):
                        if block.get("type") == "text":
                            txt = block.get("text", "").strip()
                            if txt:
                                # Show first 80 chars of each assistant chunk
                                print(f"{prefix} {txt[:80]}{'...' if len(txt)>80 else ''}", file=sys.stderr)
                elif etype == "tool_call" and subtype == "started":
                    tc = event.get("tool_call", {})
                    for key in tc:
                        if key.endswith("ToolCall") or key.endswith("_call"):
                            a = tc[key].get("args", {})
                            desc = a.get("path", "") or a.get("command", "")
                            print(f"{prefix} [tool] {key} {desc[:60]}", file=sys.stderr)
                            break
                elif etype == "result":
                    dur = event.get("duration_ms", 0)
                    print(f"{prefix} [done] {dur}ms", file=sys.stderr)
            except json.JSONDecodeError:
                pass

        proc.wait(timeout=timeout)
        exit_code = proc.returncode

    except subprocess.TimeoutExpired:
        proc.kill()
        raw_lines.append(json.dumps({"type": "error", "message": f"Timeout after {timeout}s"}))
        exit_code = -1
    except Exception as e:
        raw_lines.append(json.dumps({"type": "error", "message": str(e)}))
        exit_code = -2

    events = parse_events("\n".join(raw_lines))
    result = extract_result(events)
    result["success"] = exit_code == 0 and len(result["errors"]) == 0
    result["exit_code"] = exit_code
    result["log_file"] = str(log_file)
    result["event_count"] = len(events)
    result["task_id"] = tid

    return result


# =============================================================================
# Parallel dispatch
# =============================================================================

def run_parallel(tasks: List[dict], workspace: str, model: Optional[str] = None,
                 force: bool = True, max_workers: int = 4, timeout: int = 600) -> dict:
    """
    Run multiple tasks in parallel.

    tasks: list of {"prompt": str, "task_id": str (optional)}
    Returns: {"results": [...], "summary": {...}}
    """
    results = []
    print(f"[parallel] Dispatching {len(tasks)} tasks with max_workers={max_workers}", file=sys.stderr)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {}
        for i, task in enumerate(tasks):
            prompt = task if isinstance(task, str) else task.get("prompt", "")
            tid = f"t{i}" if isinstance(task, str) else task.get("task_id", f"t{i}")
            future = executor.submit(
                run_task,
                prompt=prompt,
                workspace=workspace,
                model=model,
                force=force,
                timeout=timeout,
                task_id=tid,
            )
            future_map[future] = tid

        for future in as_completed(future_map):
            tid = future_map[future]
            try:
                result = future.result()
                results.append(result)
                status = "OK" if result["success"] else "FAIL"
                print(f"[parallel] {tid} -> {status}", file=sys.stderr)
            except Exception as e:
                results.append({
                    "task_id": tid,
                    "success": False,
                    "errors": [str(e)],
                    "text": "",
                })

    # Summary
    succeeded = sum(1 for r in results if r.get("success"))
    failed = len(results) - succeeded
    questions = [r for r in results if r.get("has_question")]

    return {
        "results": results,
        "summary": {
            "total": len(results),
            "succeeded": succeeded,
            "failed": failed,
            "has_questions": len(questions),
            "question_tasks": [{"task_id": r["task_id"], "question": r["question_text"]} for r in questions],
        },
    }


# =============================================================================
# A2A bidirectional loop
# =============================================================================

def run_a2a_loop(prompt: str, workspace: str, model: Optional[str] = None,
                 force: bool = True, timeout: int = 600,
                 max_rounds: int = 5,
                 answer_callback=None) -> dict:
    """
    A2A-style bidirectional loop.

    1. Dispatch task to Cursor
    2. If Cursor asks a question, generate an answer and resume
    3. Repeat until Cursor finishes without questions or max_rounds reached

    answer_callback: function(question_text, context) -> str
        If None, uses a default strategy that picks the first/recommended option.
    """
    rounds = []
    current_prompt = prompt
    session_id = None

    for round_num in range(max_rounds):
        print(f"\n[a2a] === Round {round_num + 1}/{max_rounds} ===", file=sys.stderr)

        result = run_task(
            prompt=current_prompt,
            workspace=workspace,
            model=model,
            force=force,
            resume=session_id,
            timeout=timeout,
            task_id=f"a2a_r{round_num}",
        )

        session_id = result.get("session_id") or session_id
        rounds.append({
            "round": round_num + 1,
            "prompt": current_prompt,
            "result": result,
        })

        if not result.get("has_question") or not result.get("success"):
            print(f"[a2a] Completed in {round_num + 1} round(s)", file=sys.stderr)
            break

        # Cursor asked a question - generate answer
        question = result["question_text"]
        print(f"[a2a] Cursor asks: {question[:120]}", file=sys.stderr)

        if answer_callback:
            answer = answer_callback(question, result["text"])
        else:
            answer = generate_default_answer(question, result["text"])

        print(f"[a2a] Answering: {answer[:120]}", file=sys.stderr)
        current_prompt = answer

    return {
        "rounds": rounds,
        "total_rounds": len(rounds),
        "final_session_id": session_id,
        "final_result": rounds[-1]["result"] if rounds else {},
        "completed": not rounds[-1]["result"].get("has_question") if rounds else False,
    }


def generate_default_answer(question: str, context: str) -> str:
    """
    Generate a default answer when Cursor asks a question.
    Strategy: Pick the first/recommended option, or say 'proceed with your best judgment'.
    """
    q_lower = question.lower()

    # If offering numbered options, pick option 1
    if re.search(r'option\s*1|1\)', q_lower):
        return "Option 1 please. Proceed with that approach."

    # If asking yes/no
    if re.search(r'\b(should|shall|do you want|would you like)\b', q_lower):
        return "Yes, proceed."

    # If asking about technology choice
    if re.search(r'\b(which|what)\s+(library|framework|approach|method|pattern)\b', q_lower):
        return "Use the most standard/common approach for this project. Proceed with your best judgment."

    # Default: tell Cursor to decide
    return "Proceed with your best judgment. Choose the most standard and maintainable approach."


# =============================================================================
# Utilities
# =============================================================================

def check_status():
    """Check cursor-agent auth status."""
    result = subprocess.run(
        [CURSOR_AGENT, "status"],
        capture_output=True, text=True, timeout=15,
    )
    output = result.stdout + result.stderr
    clean = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', output).strip()
    return {"status": clean, "logged_in": "Logged in" in clean}


def list_models():
    """List available models."""
    result = subprocess.run(
        [CURSOR_AGENT, "--list-models"],
        capture_output=True, text=True, timeout=15,
    )
    output = result.stdout + result.stderr
    clean = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', output).strip()
    return {"models": clean}


# =============================================================================
# CLI
# =============================================================================

def main():
    # Detect if first positional arg is "parallel"
    is_parallel = len(sys.argv) > 1 and sys.argv[1] == "parallel"

    if is_parallel:
        parser = argparse.ArgumentParser(description="Parallel dispatch")
        parser.add_argument("command")  # "parallel"
        parser.add_argument("--tasks", required=True, help="JSON array of tasks")
        parser.add_argument("--workspace", "-w", default=os.getcwd())
        parser.add_argument("--model", "-m", help="Model name")
        parser.add_argument("--no-force", action="store_true")
        parser.add_argument("--max-workers", type=int, default=4)
        parser.add_argument("--timeout", type=int, default=600)
        args = parser.parse_args()

        try:
            tasks = json.loads(args.tasks)
        except json.JSONDecodeError:
            tasks = [t.strip() for t in args.tasks.split(",") if t.strip()]

        result = run_parallel(
            tasks=tasks,
            workspace=args.workspace,
            model=args.model,
            force=not args.no_force,
            max_workers=args.max_workers,
            timeout=args.timeout,
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    # Single / A2A mode
    parser = argparse.ArgumentParser(
        description="Claude Code <-> Cursor Agent bridge (parallel + A2A)",
    )
    parser.add_argument("prompt", nargs="*", default=[], help="Task prompt")
    parser.add_argument("--workspace", "-w", default=os.getcwd(), help="Working directory")
    parser.add_argument("--model", "-m", help="Model name")
    parser.add_argument("--resume", "-r", help="Resume session ID")
    parser.add_argument("--mode", choices=["plan", "ask"], help="Execution mode")
    parser.add_argument("--no-force", action="store_true", help="Don't auto-approve tools")
    parser.add_argument("--timeout", type=int, default=600, help="Timeout in seconds")
    parser.add_argument("--status", action="store_true", help="Check auth status")
    parser.add_argument("--models", action="store_true", help="List available models")
    parser.add_argument("--a2a", action="store_true", help="Enable A2A bidirectional loop")
    parser.add_argument("--a2a-max-rounds", type=int, default=5, help="Max A2A rounds")
    parser.add_argument("--a2a-answer", help="Custom answer for all A2A questions")
    args = parser.parse_args()

    if args.status:
        print(json.dumps(check_status(), indent=2))
        return
    if args.models:
        print(json.dumps(list_models(), indent=2))
        return

    if not args.prompt:
        parser.print_help()
        sys.exit(1)

    prompt = " ".join(args.prompt)
    force = not args.no_force

    if args.a2a:
        callback = None
        if args.a2a_answer:
            callback = lambda q, c: args.a2a_answer

        result = run_a2a_loop(
            prompt=prompt,
            workspace=args.workspace,
            model=args.model,
            force=force,
            timeout=args.timeout,
            max_rounds=args.a2a_max_rounds,
            answer_callback=callback,
        )
    else:
        result = run_task(
            prompt=prompt,
            workspace=args.workspace,
            model=args.model,
            force=force,
            mode=args.mode,
            resume=args.resume,
            timeout=args.timeout,
        )

    print(json.dumps(result, indent=2, ensure_ascii=False))
    success = result.get("success", result.get("completed", False))
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
