# ADR-001: Making PayEx Invoice Submissions Reliable

**Status:** Proposed — not yet implemented

## 1. Context?

Our Invoice Approval service is currently used internally. We plan to make it a business-critical service that must run 24 hours a day, 7 days a week.

The service will send approved invoices to PayEx for payment processing.

We expect around 40,000 invoices per month, with most activity happening during the last three working days of the month. At peak times, around 80 approvals may happen per minute.

We need to make sure that:
- Every approved invoice is safely recorded.
- An invoice is not accidentally submitted to PayEx twice.
- Failed or delayed submissions can be recovered.
- We can explain what happened to an invoice, even months or years later.

**The main question:** What should happen if our application sends an invoice to PayEx but does not receive a response?

## 2. What options did we consider?

### Option A: Check for duplicates before sending

Before sending an invoice, the application checks whether it has already been submitted.

- **Advantage:** Simple to understand and may prevent duplicate submissions.
- **Disadvantage:** If the application stops unexpectedly, the invoice could still be missed. Checking our own records alone cannot always tell us whether PayEx processed the invoice.

### Option B: Save the invoice request and send it in the background

The application first saves the submission request in its database. A separate background process then sends it to PayEx.

- **Advantage:** The request is saved before sending, so it can be retried or investigated if something goes wrong.
- **Disadvantage:** This requires additional database records and a background process. We must also handle cases where PayEx processes a request but our application does not receive the response.

### Option C: Send directly and check later

The application sends the invoice directly to PayEx and checks for missing or failed submissions later.

- **Advantage:** Less work to set up initially.
- **Disadvantage:** Problems may remain unnoticed until the later check. Recovering missing or duplicate submissions can be harder.

## 3. What do we recommend?

**We recommend Option B: Save the request first, then send it through a background process.**

This gives us a reliable record of what needs to be sent and helps us recover if the application or network fails.

We will also use a consistent reference for each invoice submission so that retries can be recognised as the same request.

Where PayEx supports duplicate protection using this reference, we should use it. If PayEx does not support this, we must check PayEx's records before resending a request whose outcome is unknown.

**Important:** Saving the request first makes our process more reliable, but it does not by itself guarantee that PayEx will process an invoice only once.

## 9. Where the Agent Was Wrong or Useless?

The AI suggested saving invoice requests in a database before sending them to PayEx. This was useful for recovering requests after a failure, but the suggestion did not fully address the risk of duplicate processing.

For example, PayEx might process an invoice successfully, but our application might not receive the response. Sending the invoice again without checking could cause it to be processed twice.

The AI's initial suggestion was therefore incomplete. We identified this gap and clarified that retries must use PayEx's duplicate-protection feature where supported, or check the submission status before resending.

This review helped us distinguish between recovering a saved request and preventing duplicate processing.

## 4. Failure Scenario: PayEx Does Not Respond?

Imagine it is 3 a.m. on the last working day of the month. Our application sends an invoice to PayEx, but the request times out.

A timeout does not mean the submission failed. PayEx might have processed the invoice but failed to send a response back.

We will handle this as follows:

1. **Keep the record:** The original request remains safely saved in our database.
2. **Do not assume failure:** Mark the outcome as unknown until we have enough information.
3. **Check before resending:** If PayEx supports duplicate protection, retry using the same reference. Otherwise, check PayEx's records before sending again.
4. **Raise an alert if needed:** If the outcome cannot be confirmed, notify the support team.
5. **Resolve carefully:** If the system cannot safely determine what happened, a person must investigate before the invoice is resubmitted.

This approach reduces the risk of losing an invoice or processing it twice.

## 5. What will this cost us?

| Area | What is required? |
|---|---|
| Development | Additional database records and a background process |
| Testing | Tests for timeouts, retries, application restarts and duplicate submissions |
| Support | Monitoring, alerts and a process for investigating unresolved submissions |
| Audit | Keeping records of submission attempts, responses and final outcomes |

These additions require more work than sending invoices directly. However, they make the service easier to support and safer to operate as a business-critical system.

## 6. How will we monitor and track submissions?

The proposed solution should keep a record of:
- Which invoice was submitted and when.
- How many times a submission was attempted.
- What response PayEx returned.
- Whether the final outcome is successful, failed or still unknown.
- How an unresolved submission was investigated and resolved.

We should also alert the support team when submissions keep failing or remain unresolved for too long.

These records will help with troubleshooting, customer queries and future audit requirements.

## 7. Why isn't checking for duplicates enough?

Checking our own database is useful, but it cannot always tell us what happened at PayEx.

For example, PayEx may successfully process an invoice while our application loses the response. Our database could still show that the outcome is unknown.

If we simply send the invoice again, PayEx might process it twice.

That is why we need **both** a reliable way to save and retry requests, and a safe way to handle duplicate submissions. PayEx's support for duplicate protection will determine how we implement the second part.

## 8. When should we review this decision?

We should review this decision if:
- PayEx provides new or different duplicate-protection features.
- The expected invoice volume increases significantly.
- The business introduces stricter recovery or availability requirements.
- The proposed design proves too costly or difficult to operate.

## 10. What must be confirmed before implementation?

Before we build this solution, we must confirm:

- Whether PayEx supports a unique reference that prevents the same invoice from being processed twice.
- How we can check the status of a submission when a request times out.
- How long submission and audit records must be retained.
- How alerts, retries and unresolved submissions will be handled by the support team.
- How the solution will be tested before it becomes business-critical.

**Final decision:** Save each submission request first, process it in the background, and handle retries carefully. Never assume that a timeout means the invoice was not processed. Confirm PayEx's duplicate-protection capabilities before deciding how to safely resend uncertain submissions.