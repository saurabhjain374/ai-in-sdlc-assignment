# AI Augmentation Log

**Last regenerated:** 28 October 2026  
**Purpose:** Record where AI supported the assignment, which agent and tools are known, what the human decided, and how the result was checked.

## 1. How to read this log

`ai-augmentation-log.json` contains five structured JSONL records (one JSON object per line). Each record includes:

- **Activity date and timestamp:** The original activity date/time was not captured, so `activity_date` and `timestamp` are `null`. `log_regenerated_date` records when this log was regenerated; it is not the date the original activity happened.
- **Agent and model:** Recorded only when the existing notes support the detail. The code-review evaluation records GitHub Copilot Chat Ask and GPT-5.6 Luna. Other activities do not have a confirmed specific agent/model in the available notes.
- **Tools:** Lists only tools already documented in the notes. A `null` value means the historical tool list was not captured.
- **MCP servers:** Historical MCP usage was not captured for these activities. A `null` value means unknown, not that no MCP server was used.
- **Human decision and verification:** Summarizes what was reviewed or decided and what evidence was checked.
- **Limitations and artifacts:** Identifies gaps in the historical record and links each activity to relevant repository files.

## 2. Activities

### 2.1 Architecture documentation and architecture test

- **AI contribution:** Helped analyze the invoice approval flow, draft Mermaid architecture diagrams, and propose an architecture test.
- **Known tools:** Mermaid and `dotnet test`.
- **Human decision:** Checked diagrams against repository code, reviewed inferred details, and ensured proposed target components were not described as implemented.
- **Verification:** The recorded command was `dotnet test backend/InvoiceApp.sln --configuration Release`; the recorded result was 8/8 tests passed.
- **Artifacts:** `docs/architecture/`, `backend/InvoiceApp.sln`.
- **Metadata gap:** Exact activity date/time, specific agent/model, session reference, and MCP usage were not preserved.

### 2.2 PayEx submission reliability decision

- **AI contribution:** Helped compare reliability options, including durable submission state, transactional outbox processing, idempotency where supported, and reconciliation after ambiguous timeouts.
- **Human decision:** Reviewed operational trade-offs and conditions that could trigger reconsideration.
- **Verification:** Reviewed the ADR content.
- **Artifact:** `docs/decisions/ADR-001-payex-submission-reliability.md`.
- **Important limitation:** This is a design decision; it does not claim the proposed PayEx integration is implemented.
- **Metadata gap:** Exact activity date/time, specific agent/model, tools, session reference, and MCP usage were not preserved.

### 2.3 AI autonomy policy and risk audit

- **AI contribution:** Helped structure autonomy boundaries, human approval controls, and the Lethal Trifecta risk assessment.
- **Human decision:** Kept the proposed workflow read-only and prohibited autonomous production changes and external financial submissions.
- **Verification:** Reviewed the policy and risk documentation. Actual production permissions were not established by this review.
- **Artifacts:** `docs/policies/ai-autonomy-policy.md`, `ops/README.md`.
- **Metadata gap:** Exact activity date/time, specific agent/model, tools, session reference, and MCP usage were not preserved.

### 2.4 AI code-review evaluation

- **Recorded agent/tool:** GitHub Copilot Chat Ask.
- **Recorded model:** GPT-5.6 Luna.
- **AI contribution:** Reviewed fixed code-change cases for defects; prompt versions were compared and findings were evaluated against expected defects.
- **Human decision:** Reviewed adjudication, excluded incompatible Case 03 from primary metrics, and did not count unsupported findings.
- **Verification:** Results and adjudication are recorded in the evaluation CSV files and summarized in `ops/evals/summary.md`.
- **Artifacts:** `ops/evals/results.csv`, `ops/evals/adjudication.csv`, `ops/evals/summary.md`.
- **Limitations:** The evaluation sample is small and selected. This is a retrospective summary, not a complete prompt transcript. Exact activity date/time and MCP usage were not captured.

### 2.5 Measurement plan

- **AI contribution:** Helped define delivery metrics, evidence sources, and measurement limitations.
- **Known tools:** GitHub Actions and Git history.
- **Human decision:** Kept repository activity, fixture timings, CI results, and production performance as separate evidence categories.
- **Verification:** Measurement sources and limitations are documented in the plan.
- **Artifact:** `docs/measurement-plan.md`.
- **Metadata gap:** Exact activity date/time, specific agent/model, session reference, and MCP usage were not preserved.

## 3. Human oversight and accountability

AI outputs were treated as suggestions rather than automatically accepted facts. Human oversight included:

- Checking architecture claims against source code.
- Reviewing design trade-offs and operational risks.
- Checking test results and diagram rendering.
- Adjudicating evaluation findings and documenting fixture limitations.
- Separating implemented behavior from proposed future architecture.
- Keeping conclusions proportionate to the available evidence.

The author remains responsible for final decisions, validation, and claims made in the submission.

## 4. Historical metadata limitations

- The original activity timestamps and time zones were not captured in the available notes. They remain `null` rather than being guessed.
- The regeneration date is recorded separately and must not be mistaken for an activity timestamp.
- Agent/model/mode details are included only where supported by the existing notes.
- Historical MCP server usage, skills, sub-agents, and exact tool calls were not captured. Unknown fields do not prove that those capabilities were not used.
- The log is a retrospective summary, not an automatically generated, complete transcript of all AI activity.
- Validation evidence supports only the specific checks recorded; it does not establish production readiness by itself.

## 5. For future activities

Capture the activity date/time with timezone, agent and model, tools, MCP server/tool names, relevant prompts or session references where permitted, human decisions, verification evidence, and affected files at the time the work occurs. Do not backfill missing historical values from memory unless clearly labeled as an estimate.
