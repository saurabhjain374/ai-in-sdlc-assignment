# AI Augmentation Log

**Date:** 2026-10-21

This log summarizes how AI assistance was used during the assignment. It is a retrospective summary, not a verbatim transcript of every prompt or interaction.

## 1. Architecture documentation and tests

- **AI assistance:** Helped map the existing invoice approval flow, identify relevant source files and symbols, draft Mermaid diagrams, and propose a structural architecture test.
- **Human verification:** Checked the diagrams against repository source files and symbols, confirmed all four Mermaid diagrams render, and ran the architecture test with the solution tests.
- **Outcome:** Documented the as-built architecture, distinguished inferred details from verified implementation, proposed a target architecture without presenting it as implemented, and added a runnable structural architecture test.

## 2. PayEx submission reliability ADR

- **AI assistance:** Helped compare idempotency and deduplication, transactional outbox with a worker, and optimistic submission with reconciliation.
- **Human verification:** Reviewed the trade-offs, including ambiguous timeouts, month-end operational failure, build effort, and reconsideration triggers.
- **Outcome:** ADR recommends a transactional outbox and durable submission state, with idempotency where the external provider supports it.

## 3. AI autonomy policy and risk audit

- **AI assistance:** Helped define autonomy levels, approval controls, evidence requirements, and the lethal-trifecta risk analysis.
- **Human verification:** Kept the initial autonomy level conservative because two of six engineers are new, and prohibited production mutations and external submission by the agent.
- **Outcome:** A read-only-first policy with explicit escalation and review controls.

## 4. Evaluation experiment

- **AI assistance:** Helped structure the fixed-case review experiment, refine the review prompt, and calculate defect-level evaluation metrics.
- **Human verification:** Reviewed adjudication decisions, excluded the incompatible Case 03 fixture and unverified findings, and compared the original prompt with the revised prompt while holding the model and review mode fixed.
- **Outcome:** A documented baseline and revised-prompt comparison. The sample is small and selected, so the results indicate a possible improvement rather than proof of general effectiveness.

## 5. Measurement plan

- **AI assistance:** Helped define lead time, change failure rate, and review turnaround, including potential data sources and calculation methods.
- **Human verification:** Distinguished repository activity and scenario-provided pipeline fixtures from four verified successful live GitHub Actions runs and unavailable production performance measurements.
- **Outcome:** A measurement plan with explicit evidence limitations. Live CI results are reported separately from production metrics; unavailable production measurements are not represented as zero or as verified results.

## Limitations

This is a retrospective summary rather than a complete prompt-by-prompt transcript. AI-generated suggestions were treated as proposals and checked against repository evidence where applicable. Final decisions, exclusions, and submission claims remain the author's responsibility.