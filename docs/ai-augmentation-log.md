@'
# AI Augmentation Log

## Purpose

This log records how AI tools were used during the AI-in-SDLC assignment,
the decisions made by the engineer, and the validation performed.
This is a retrospective record of the work completed; it is not a
verbatim transcript of every AI interaction.

## Entry 1 — Architecture documentation and architecture tests

- **Activity:** Document the current invoice approval architecture and
  the proposed target architecture.
- **AI assistance:** Helped structure architecture diagrams, explain
  the approval flow, and identify architectural boundaries and test ideas.
- **Engineer contribution:** Reviewed the diagrams and documentation
  against the repository's actual implementation and kept proposed
  components distinct from implemented components.
- **Validation:** Ran the solution's .NET test suite. Final Release
  validation passed 8 tests with 0 failures.
- **Outcome:** Architecture documentation and architecture test
  artifacts were added to the repository.

## Entry 2 — PayEx submission reliability ADR

- **Activity:** Evaluate approaches for reliable invoice submission
  to PayEx, including ambiguous timeouts and duplicate submissions.
- **AI assistance:** Helped compare idempotency and deduplication,
  transactional outbox processing, and optimistic submission with
  reconciliation.
- **Engineer contribution:** Considered failure recovery, operational
  complexity, and the consequences of a month-end failure. Selected
  the preferred approach and documented reconsideration triggers.
- **Validation:** Reviewed the decision against the assignment scenario
  and distinguished proposed target capabilities from implemented code.
- **Outcome:** ADR-001 was documented.

## Entry 3 — AI autonomy policy and risk audit

- **Activity:** Define appropriate autonomy for an invoice-incident
  triage workflow and assess the lethal-trifecta risk.
- **AI assistance:** Helped organize autonomy levels, approval controls,
  risk mitigations, and evidence required before increasing autonomy.
- **Engineer contribution:** Kept the initial autonomy level conservative,
  restricted production-changing actions, and documented review triggers.
- **Validation:** Checked the policy against the assignment scenario
  and recorded the risk decision and mitigations in the repository.
- **Outcome:** The autonomy policy and risk-audit documentation were added.

## Entry 4 — AI code-review evaluation

- **Activity:** Evaluate AI code-review findings against a fixed set
  of diffs, including defect cases and clean changes.
- **AI assistance:** GitHub Copilot Chat was used for code-review runs.
  The initial prompt was compared with a revised prompt while keeping
  the model and review mode unchanged for the prompt experiment.
- **Engineer contribution:** Reviewed findings against the code and
  available contracts, adjudicated true positives, false negatives,
  false positives, and true negatives, and excluded incompatible or
  unverified cases from the primary metrics.
- **Validation:** Recorded results and adjudications in CSV files,
  calculated metrics, and checked the comparable Run 4 counts.
- **Outcome:** Evaluation results and a prompt-comparison analysis
  were documented. The small sample size limits confidence in the
  measured improvement.

## Entry 5 — Measurement plan

- **Activity:** Define change lead time, change failure rate, and
  review turnaround time.
- **AI assistance:** Helped structure metric definitions and identify
  the evidence needed to calculate them.
- **Engineer contribution:** Inspected available Git history and checked
  the repository's GitHub Actions workflow history.
- **Validation:** Documented available repository-history timestamps
  and explicitly noted that they are not substitutes for actual
  pull-request, deployment, incident, or review timestamps.
- **Outcome:** The measurement plan records the evidence available
  and the limitations preventing unsupported baseline claims.

## Engineering principles applied

- AI suggestions were treated as proposals, not authoritative facts.
- Findings were checked against source code and available contracts.
- Incompatible test cases and unverified assumptions were not silently
  treated as confirmed defects.
- Proposed architecture was distinguished from implemented behavior.
- Automated test results and evaluation metrics were checked separately
  from AI-generated explanations.

## Evidence and limitations

This is a retrospective summary. It does not claim to contain every
prompt, response, timestamp, or intermediate edit. The repository's
artifacts, evaluation CSV files, Git history, and test output provide
supporting evidence for the activities described above.
'@ | Set-Content -Path "docs/ai-augmentation-log.md" -Encoding utf8