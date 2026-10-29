#!/usr/bin/env python3
"""Append privacy-conscious GitHub Copilot hook events to a JSONL audit log.

The hook deliberately does not store prompt text, tool argument values, tool output,
credentials, or full local paths. Human decisions and verification still require review.
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "docs" / "ai-augmentation-events.jsonl"


def first(payload: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = payload.get(key)
        if value is not None:
            return value
    return None


def relative_cwd(value: Any) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return Path(value).resolve().relative_to(ROOT.resolve()).as_posix() or "."
    except (OSError, ValueError):
        return None


def build_record(payload: dict[str, Any]) -> dict[str, Any]:
    event_name = first(payload, "hook_event_name", "eventName", "event", "hookEventName")
    session_id = first(payload, "session_id", "sessionId")
    tool_name = first(payload, "tool_name", "toolName")
    tool_args = first(payload, "tool_input", "toolArgs", "tool_args")
    prompt = first(payload, "prompt", "user_prompt", "userPrompt")
    is_error = first(payload, "is_error", "isError", "tool_error")

    session_hash = None
    if isinstance(session_id, str) and session_id:
        session_hash = hashlib.sha256(session_id.encode("utf-8")).hexdigest()[:12]

    argument_keys = sorted(str(key) for key in tool_args.keys()) if isinstance(tool_args, dict) else []
    record = {
        "record_type": "copilot_hook_event",
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "event": str(event_name) if event_name else "unknown",
        "agent": "GitHub Copilot (hook configured in repository)",
        "model": None,
        "session_fingerprint": session_hash,
        "tool": str(tool_name) if isinstance(tool_name, (str, int, float)) else None,
        "tool_argument_keys": argument_keys,
        "tool_result_error": bool(is_error) if is_error is not None else None,
        "prompt_character_count": len(prompt) if isinstance(prompt, str) else None,
        "subagent_name": first(payload, "agent_name", "agentName", "subagent_name", "subagentName"),
        "working_directory": relative_cwd(first(payload, "cwd", "working_directory", "workingDirectory")),
        "prompt_content_recorded": False,
        "tool_arguments_recorded": False,
        "tool_output_recorded": False,
        "human_decision": None,
        "verification_evidence": None,
    }
    return record


def main() -> int:
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
        if not isinstance(payload, dict):
            payload = {}
        record = build_record(payload)
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    except Exception as exc:  # Logging must not block the user's agent action.
        print(f"AI augmentation logger warning: {type(exc).__name__}: {exc}", file=sys.stderr)
    # Copilot hooks expect JSON output; this logger makes no allow/deny decision.
    print("{}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
