# Architecture deliverables

## As-built summary

The current application is an ASP.NET Core API with a static UI, session middleware, API controllers, a domain service, and an in-memory repository. `Program.cs` registers `SessionStore` and binds `IInvoiceRepository` to `InMemoryInvoiceRepository`. `ApprovalService` enforces `Draft -> PendingApproval -> Approved|Rejected`; an approval records the approver and UTC decision timestamp, while rejection also records a reason.

## Evidence map

| Element / relationship | Source evidence |
|---|---|
| ASP.NET Core host, static UI and middleware pipeline | `backend/src/InvoiceApp.Api/Program.cs`: builder, `UseDefaultFiles`, `UseStaticFiles`, `UseMiddleware<SessionAuthMiddleware>`, `MapControllers`, `Run` |
| Session store and middleware | `backend/src/InvoiceApp.Api/Program.cs`: `AddSingleton<SessionStore>()`, `UseMiddleware<SessionAuthMiddleware>()` |
| Invoice endpoints | `backend/src/InvoiceApp.Api/Controllers/InvoicesController.cs`: list/get/create/submit/delete actions |
| Approval endpoints and role restriction | `backend/src/InvoiceApp.Api/Controllers/ApprovalsController.cs`: approve/reject routes and `[RequireRole("Approver", "Admin")]` |
| Session identity passed to decision service | `backend/src/InvoiceApp.Api/Controllers/ApprovalsController.cs`: `HttpContext.GetSession().Username` |
| State transitions and decision metadata | `backend/src/InvoiceApp.Domain/ApprovalService.cs`: `Submit`, `Approve`, `Reject`, `EnsurePending` |
| Repository contract | `backend/src/InvoiceApp.Domain/IInvoiceRepository.cs` |
| In-memory repository and methods | `backend/src/InvoiceApp.Api/InMemoryInvoiceRepository.cs`: `InMemoryInvoiceRepository : IInvoiceRepository`, `GetById`, `Add`, `Update`, `Remove` |
| Repository implementation selected by DI | `backend/src/InvoiceApp.Api/Program.cs`: `AddSingleton<IInvoiceRepository, InMemoryInvoiceRepository>()` |
| Domain entity/status | `backend/src/InvoiceApp.Domain/Invoice.cs` and `InvoiceStatus.cs` |
| Test framework | `backend/tests/InvoiceApp.Tests/ApprovalServiceTests.cs`; project conventions in `AGENTS.md` |

## Inferred elements

- A human or browser/client calls the HTTP API. The repository defines routes, but does not establish a specific deployed caller.
- The API process hosts the static UI because `Program.cs` configures default and static files; actual production hosting topology is not shown.
- In-memory changes are not durable across process restart. No database transaction, external payment call, or production message publication is implemented in the inspected code.
- The target diagrams are proposals. `ops/README.md` and `AGENTS.md` explicitly warn that database, message topic and PayEx are planned and do not exist in code.

## Target-state design note

The proposed outbox pattern atomically records the invoice decision, audit event, and intent to submit. A worker delivers at least once. An outbox alone does **not** guarantee exactly-once effects at PayEx: use provider-supported idempotency with a stable key, or reconcile ambiguous outcomes before any resubmission. A timeout means the result is unknown, not necessarily failed.
