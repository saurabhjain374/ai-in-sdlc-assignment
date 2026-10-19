# ADR-001: Reliable PayEx Submission and Duplicate Prevention

- **Status:** Proposed
- **Date:** 2026-10-19
- **Decision owner:** Invoice Approval service team
- **Scope:** Submitting approved invoices to PayEx without creating duplicate external effects

## 1. Context

The Invoice Approval service is moving from an internal tool to a tier-2 service with 24x7 on-call support and published SLOs. The scenario anticipates approximately 40,000 invoices per month, with 60% arriving in the final three working days and a peak of around 80 approvals per minute.

The current implementation uses in-memory persistence. The PayEx integration and durable database are planned, not implemented. A PayEx request may time out after 30 seconds, and a timeout does not reliably mean that PayEx failed to process the request.

Approval actions must be auditable for seven years to support the planned SOC 2 Type II audit.

The core problem is that a network timeout can leave the service uncertain whether PayEx processed a submission. Blindly retrying can create a duplicate; never retrying can leave an invoice unprocessed.

## 2. Decision

**Prefer a transactional outbox with a durable submission record and a stable idempotency key, provided PayEx supports reliable idempotency semantics.**

The invoice decision, audit record, and outbox submission intent must be committed in one Azure SQL transaction. A background worker then submits the outbox item to PayEx.

Each logical submission receives a stable identifier. Retries reuse the same identifier; they must not generate a new key for the same logical submission. The worker records provider references and outcomes, and supports controlled retry and reconciliation.

A timeout is recorded as an **unknown outcome**, not as a confirmed failure. If PayEx does not support idempotency keys, the worker must reconcile the outcome with PayEx before attempting a potentially duplicate submission.

The outbox provides durable delivery, not magical exactly-once execution at the external provider. Duplicate-safe external effects depend on PayEx idempotency or an effective reconciliation protocol.

## 3. Options considered

### Option A — Idempotency key plus deduplication table

The API or submission component creates a stable idempotency key and persists it with a unique constraint. Duplicate requests with the same key return the existing submission result rather than creating a new logical submission.

**Advantages**
- Straightforward duplicate detection.
- Unique constraints can prevent concurrent duplicate records.
- Works well when PayEx supports idempotency keys.

**Disadvantages**
- A deduplication table alone does not atomically coordinate invoice approval and an external HTTP call.
- A crash between persisting local state and calling PayEx can leave the submission stranded.
- A timeout still requires safe retry or reconciliation.

**Assessment:** Necessary protection, but insufficient as the complete delivery mechanism.

### Option B — Transactional outbox plus background worker

The service writes the invoice decision, audit record, and outbox item in one database transaction. A worker delivers pending items and tracks attempts, outcomes, and provider references.

**Advantages**
- Prevents the database commit and submission intent from silently diverging.
- Supports durable retries, observability, and operational recovery.
- Separates approval latency from provider latency.
- Provides a clear queue of work for on-call engineers.

**Disadvantages**
- Adds worker deployment, outbox polling or dispatch, retry policies, monitoring, and operational procedures.
- Delivery is at least once; the worker can send the same item again after a crash.
- Requires PayEx idempotency or reconciliation to prevent duplicate external effects.

**Assessment:** Preferred, combined with stable submission identifiers and provider idempotency or reconciliation.

### Option C — Optimistic submission plus nightly reconciliation

The service attempts submission directly and uses a nightly job to compare local records against PayEx.

**Advantages**
- Less infrastructure initially.
- Reconciliation can detect missing or inconsistent records.

**Disadvantages**
- Duplicate or missing submissions can remain unresolved for hours.
- A nightly batch is poorly matched to a tier-2 service with 24x7 expectations.
- The system needs a way to identify provider-side outcomes and resolve ambiguous cases.
- Reconciliation becomes a critical operational dependency during month-end peaks.

**Assessment:** Useful as a complementary control, but not sufficient as the primary reliability strategy.

## 4. Failure analysis: 3 a.m. on the final working day of the month

Assume the worker submits an invoice, PayEx processes it, but the response times out.

1. Mark the attempt as `UnknownOutcome`; do not mark it as a definite failure.
2. Retain the outbox item and its original idempotency key.
3. If PayEx guarantees idempotent handling for that key, retry with the same key according to the documented retry policy.
4. If provider idempotency is unavailable or uncertain, query the provider using a stable merchant reference or supported reconciliation interface before resubmitting.
5. Alert on the age and count of unknown outcomes, retry backlog, and oldest pending outbox item.
6. If the provider cannot establish the outcome automatically, keep the item in a controlled exception state and require an auditable human decision.

The on-call runbook must explain how to identify affected invoices, inspect attempt history, safely retry, reconcile, and escalate. Operators must not manually create a fresh submission key simply to make a retry succeed.

## 5. Build and run costs

| Option | Build cost | Run cost | Main operational burden |
|---|---|---|---|
| Idempotency key + dedupe table | Medium | Low–medium | Key lifecycle, uniqueness, ambiguous outcomes |
| Transactional outbox + worker | High | Medium–high | Worker health, backlog, retries, dead letters, reconciliation |
| Direct submission + nightly reconciliation | Low initially | Medium–high over time | Delayed detection, batch failures, manual exception handling |

These are relative engineering estimates, not measured costs or vendor quotations. Actual cost depends on Azure configuration, PayEx contract capabilities, transaction volume, retention, and operational support requirements.

## 6. Controls and auditability

- Persist approval decisions and relevant submission state durably.
- Retain immutable or tamper-evident audit records for the required seven years, subject to approved retention and access policies.
- Enforce unique identifiers for logical submissions.
- Record attempt timestamps, outcomes, provider references, retry counts, and operator interventions.
- Use bounded retries with backoff and alerting; do not retry indefinitely without visibility.
- Avoid logging credentials, tokens, or sensitive payment data.
- Test duplicate delivery, concurrent workers, process crashes, provider timeouts, and recovery after restart.
- Verify PayEx's idempotency contract, key scope, retention period, and behavior when the same key is reused with a different payload before production.

## 7. Reconsideration triggers

Revisit this decision if:
- PayEx does not support idempotency and offers no reliable way to query submission outcomes.
- The provider's idempotency-key retention period is shorter than the maximum retry and reconciliation window.
- Transactional outbox complexity exceeds the team's support capacity and a managed delivery mechanism meets the same correctness requirements.
- Measured latency, backlog, failure rate, or SLO performance breaches agreed thresholds.
- Audit, legal, or security requirements change the retention or evidence model.

## 8. Challenge the preferred option

A plausible alternative recommendation is to use only an idempotency key plus a deduplication table because the current throughput—around 80 approvals per minute at peak—is modest and a worker introduces operational complexity.

That alternative is attractive if PayEx idempotency is strong and submission state can be coordinated safely. However, the deduplication table by itself does not guarantee that every committed approval will eventually be submitted. The outbox closes that local durability gap and provides a recoverable queue of work.

If the provider cannot deduplicate requests or support reconciliation, none of these options alone can guarantee exactly-once external effects across an ambiguous network failure. That limitation must be resolved with the provider or accepted explicitly as a business risk.

## 9. Where the agent was wrong or useless

- **A deduplication table alone is not enough.** It can stop duplicate local records but cannot guarantee delivery after a process crash between a database write and the provider call.
- **An outbox does not guarantee exactly-once PayEx execution.** It guarantees durable local intent and normally at-least-once delivery; external idempotency or reconciliation is still required.
- **A timeout is not a failure signal.** Retrying with a newly generated key can duplicate a payment or submission that PayEx already accepted.
- **Nightly reconciliation is not an adequate primary recovery mechanism** for a tier-2, 24x7 service when month-end work is concentrated and delayed resolution matters.
- **The cost comparison is qualitative.** Without actual Azure pricing, PayEx contract details, and measured failure rates, presenting numerical savings or a definitive total cost would be unjustified.

The final decision remains conditional on verifying PayEx's actual idempotency and reconciliation capabilities. A design review and failure-injection tests are required before production approval.

## 10. Validation required before implementation

- Confirm PayEx idempotency-key support, uniqueness scope, retention, and replay behavior.
- Confirm the provider's query/reconciliation capability for unknown outcomes.
- Agree on submission state transitions and operational ownership.
- Define retry limits, backlog alerts, unknown-outcome alerts, and escalation procedures.
- Test process termination after database commit, after provider acceptance, and before recording the response.
- Verify the audit-retention design against the seven-year requirement.
