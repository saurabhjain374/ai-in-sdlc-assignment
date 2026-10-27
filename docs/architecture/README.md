# Architecture overview

This page explains what the application does today, what the diagrams propose for the future, and how the diagrams were checked against the code.

## 1. Current application (as built)

The application has:
- A small web UI served by an ASP.NET Core API.
- Session middleware for sign-in and user identity.
- API controllers for invoice and approval requests.
- `ApprovalService`, which applies the invoice approval rules.
- An in-memory repository that stores invoices while the application is running.

The main invoice flow is:

`Draft -> PendingApproval -> Approved or Rejected`

When an invoice is approved, the app records who approved it and the UTC decision time. When it is rejected, it also records the reason.

**Important:** The current repository is in memory. Its data is not durable across an application restart. The inspected code does not implement a database, PayEx payment submission, or production message publishing.

## 2. Diagrams

The Mermaid source files are:

- **As-built containers:** [as-built-containers.mmd](as-built-containers.mmd)
- **As-built approval flow:** [as-built-approval-sequence.mmd](as-built-approval-sequence.mmd)
- **Proposed target containers:** [target-containers.mmd](target-containers.mmd)
- **Proposed target approval flow:** [target-approval-sequence.mmd](target-approval-sequence.mmd)

The two as-built diagrams describe the current code. The two target diagrams show a **proposed design only**. Azure SQL, the outbox, a background worker, a message topic, and PayEx integration are not implemented.

## 3. Evidence from the code

| What the diagram shows | Where to verify it |
|---|---|
| App startup, static UI and middleware | `backend/src/InvoiceApp.Api/Program.cs` |
| Invoice API routes | `backend/src/InvoiceApp.Api/Controllers/InvoicesController.cs` |
| Approval routes and role checks | `backend/src/InvoiceApp.Api/Controllers/ApprovalsController.cs` |
| Approval rules and state changes | `backend/src/InvoiceApp.Domain/ApprovalService.cs` |
| Invoice repository interface | `backend/src/InvoiceApp.Domain/IInvoiceRepository.cs` |
| In-memory repository implementation | `backend/src/InvoiceApp.Api/InMemoryInvoiceRepository.cs` |
| Invoice data and status values | `backend/src/InvoiceApp.Domain/Invoice.cs` and `InvoiceStatus.cs` |
| Approval service tests | `backend/tests/InvoiceApp.Tests/ApprovalServiceTests.cs` |

## 4. What we inferred

These points are reasonable conclusions from the code, but are not proof of the deployed production setup:

- A person or client calls the HTTP API; the code does not identify a specific deployed caller.
- The API serves the static UI, but the production hosting setup is not shown.
- In-memory data can be lost when the process restarts.
- The database, message topic and PayEx integration belong to the proposed target design, not the current application.

## 5. Important reliability decision for the proposed design

The proposed design uses an **outbox**: the application saves the invoice decision, audit event and request to submit in one database transaction. A background worker then sends the saved request.

This supports recovery, but does **not by itself guarantee exactly-once processing** at PayEx. The worker may need to retry after a timeout, even when PayEx has already processed the invoice.

To reduce duplicate-payment risk:
1. Use the same stable request reference for retries if PayEx supports duplicate protection.
2. Otherwise, check PayEx's status before resending a request whose outcome is unknown.
3. Ask a person to investigate if the result still cannot be confirmed.

A timeout means **the result is unknown**; it does not automatically mean the submission failed.

See [ADR-001: Making PayEx Invoice Submissions Reliable](../decisions/ADR-001-payex-submission-reliability.md) for the full decision and alternatives.

## 6. Architecture test

Run the architecture test with:

```bash
dotnet test backend/InvoiceApp.sln --configuration Release
```

The test in `backend/tests/InvoiceApp.Tests/ArchitectureTests.cs` checks that the Domain assembly does not directly depend on `InvoiceApp.Api` or `Microsoft.AspNetCore` assemblies.

This verifies **one dependency rule only**. Passing it does not prove that every architecture requirement is met.
