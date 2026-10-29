# Automatic AI Augmentation Logging

## What this adds

The repository includes a GitHub Copilot hook configuration at `.github/hooks/ai-augmentation-logging.json`. It invokes `scripts/ai_augmentation_logger.py` at selected agent lifecycle events and appends one JSON object per event to `docs/ai-augmentation-events.jsonl`.

The event log captures timestamps, event names, available tool names, tool-argument *keys* (not values), a hashed session fingerprint, and limited status metadata. It deliberately does **not** store prompt text, tool argument values, tool outputs, credentials, or full local paths.

## Enable and verify in VS Code

1. Open this repository in VS Code and trust the workspace only if you trust its contents.
2. Make sure the active agent session target is **Copilot** and that agent hooks are enabled/available in your VS Code version.
3. Confirm Python is available. On Windows the hook uses `py -3`; other platforms use `python`.
4. Start a new Copilot agent session and submit a harmless test prompt.
5. Use a tool once, then finish the session.
6. Check whether `docs/ai-augmentation-events.jsonl` was created and contains timestamped events.

A hook file existing in the repository does not prove it executed. Verify the generated event file in your actual VS Code session. Hooks are a VS Code preview feature and may be restricted by organization policy.

## Important limitations

- This is event-level automation, not a complete transcript of AI reasoning or every model response.
- The model name is not inferred when the hook payload does not provide it.
- Human decisions, whether a suggestion was accepted, and verification evidence cannot reliably be inferred from lifecycle events. Add those details during review; do not fabricate them.
- Historical activities are not backfilled. The existing retrospective log remains separate from this new live event log.
- The generated JSONL file may contain activity metadata. Review it before committing or sharing it.
- Hook execution must be tested in the environment where the agent runs; local VS Code, CLI, and cloud agents can support different event payloads.

## Demo explanation

"Earlier I maintained a retrospective summary. I have now added Copilot lifecycle hooks that automatically record available activity metadata as the agent runs. Sensitive prompt and tool contents are excluded, and human decisions and verification remain explicit review responsibilities."
