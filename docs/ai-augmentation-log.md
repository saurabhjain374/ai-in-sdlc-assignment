# AI Augmentation Log

**Last reviewed:** 27 October 2026  
**Purpose:** Record how AI supported the assignment, what was produced, how outputs were verified, and where human judgment was required.

## 1. Logging approach

This document provides a readable summary of AI-assisted development. The corresponding `ai-augmentation-log.json` contains structured task-level records.

The log is retrospective. Exact prompts, timestamps, agent configuration, and tool-call details are included only where evidence is available. Reconstructed task descriptions are summaries, not verbatim prompts.

## 2. AI-assisted activities

### 2.1 Architecture documentation and architecture test

- **AI contribution:** Helped analyze the invoice approval flow, draft Mermaid architecture diagrams, and propose a structural architecture test.
- **Artifacts:** As-built and target architecture diagrams, sequence diagrams, and architecture test.
- **Human intervention:** Checked diagrams against repository code, reviewed inferred details, ensured the proposed target was not presented as implemented, and verified that the diagrams rendered.
- **Validation evidence:** The solution test command was `dotnet test backend/InvoiceApp.sln --configuration Release`; the recorded result was 8/8 tests passed.
- **Outcome:** Completed, with implementation facts distinguished from proposed architecture.
- **Limitations:** The original prompts and exact AI session metadata were not preserved in the existing retrospective notes.

### 2.2 PayEx submission reliability decision

- **AI contribution:** Helped compare submission reliability options, including idempotency, a transactional outbox with a worker, and reconciliation after ambiguous timeouts.
- **Artifact:** `docs/decisions/ADR-001-payex-submission-reliability.md`.
- **Human intervention:** Reviewed trade-offs, operational failure scenarios, implementation effort, and conditions that could trigger reconsideration of the decision.
- **Outcome:** The ADR recommends durable submission state and a transactional outbox, with idempotency where supported by the external provider.
- **Limitation:** This is a design decision, not evidence that the proposed production integration has been implemented.

### 2.3 AI autonomy policy and risk audit

- **AI contribution:** Helped structure autonomy levels, human approval controls, evidence requirements, and the Lethal Trifecta risk analysis.
- **Artifacts:** AI autonomy policy and risk-audit documentation.
- **Human intervention:** Kept the proposed initial workflow read-only and prohibited autonomous production changes, database mutations, and external financial submissions.
- **Outcome:** A conservative policy with explicit escalation and review requirements.
- **Limitation:** The documented controls are proposed safeguards; actual production permissions and integrations require separate verification.

### 2.4 AI code-review evaluation

- **AI contribution:** Helped structure a fixed-case code-review experiment, refine the review prompt, and analyze defect-level results.
- **Tool and model recorded for the evaluation:** GitHub Copilot Chat Ask, GPT-5.6 Luna.
- **Artifacts:** `ops/evals/results.csv`, `ops/evals/adjudication.csv`, and `ops/evals/summary.md`.
- **Human intervention:** Reviewed defect adjudication, excluded the incompatible Case 03 fixture from primary metrics, excluded unsupported findings, and compared prompt versions on the original comparable cases.
- **Outcome:** The revised prompt showed promising results in the small evaluation set.
- **Limitation:** The results do not prove general improvement. The sample is small and selected, and the raw outputs remain separate from the adjudicated scores.

### 2.5 Measurement plan

- **AI contribution:** Helped define delivery and review metrics, potential evidence sources, and calculation methods.
- **Artifact:** `docs/measurement-plan.md`.
- **Human intervention:** Distinguished repository activity, scenario-provided pipeline timing data, and observed GitHub Actions results from production performance data.
- **Outcome:** A measurement plan that documents evidence sources and limitations rather than claiming unverified production improvements.
- **Limitation:** Repository activity and assignment CI results are not substitutes for verified production lead time or change-failure data.

## 3. Human oversight and accountability

AI outputs were treated as proposals, not automatically accepted as correct. Human review included:

- Checking architecture claims against source code.
- Reviewing design trade-offs and operational risks.
- Validating test results and diagram rendering.
- Adjudicating evaluation findings and documenting fixture limitations.
- Separating implemented behavior from proposed future architecture.
- Keeping conclusions proportionate to the available evidence.

The author remains responsible for final decisions, validation, and claims made in the submission.

## 4. Traceability and evidence

The structured JSONL log records known task details, relevant artifacts, human decisions, validation evidence, outcomes, and limitations.

Where historical interaction data was not captured, the log explicitly identifies the gap. It does not claim to be an automatically generated, complete transcript of all AI activity.

For future work, capture interaction records as close to the time of use as possible, preserve exact prompts when permitted, and retain relevant test output, session references, and commit references.

## 5. Logging limitations

- The existing notes do not contain a complete prompt-by-prompt transcript.
- Exact timestamps, model versions, execution modes, skills, sub-agents, and tool calls are not available for every activity.
- Absence of a recorded skill, sub-agent, or integration must not be interpreted as proof that none was used.
- Historical records are reconstructed summaries where explicitly indicated.
- Validation evidence supports only the specific checks recorded; it does not establish production readiness by itself.