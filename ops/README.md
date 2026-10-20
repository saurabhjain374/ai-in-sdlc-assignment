# Operations material

Evidence packs and artefacts for working on this service the way you would in
production. Nothing here runs as part of the application or its tests.

| Folder | What it holds |
| --- | --- |
| `incidents/INC-2041` | Approvals slow and failing. Logs, metrics and the deploy diff for a completed incident window. |
| `incidents/INC-2047` | Approved invoices not triggering notifications. A live incident, read-only output only. |
| `pipeline` | The service's full CI pipeline and per-step timings for the last 20 runs. |
| `evals` | Ten fixed review cases and a results template. |

## A note on the scenario

The invoice approval service in this repository is an internal tool. The
material here assumes the version of it that is going to production: a
24x7 on-call rotation, a database, a message topic, and an integration with
an external payment provider called PayEx. None of that is in the code yet,
which is the point — the diagrams, decisions and policies have to be made
before it is.

Names, hosts and figures are invented. No real system, customer or vendor
appears anywhere in this folder.

## No answers here

These packs deliberately do not state what the root cause is, which cases
contain defects, or which pipeline changes are safe. Working that out is the
exercise. If you are facilitating rather than participating, the answers are
in the session runbook, not in the repository.

## AI Agent Risk Audit — Lethal Trifecta

**Assessment date:** 19 October 2026  
**Scope:** AI-assisted month-end incident and log triage  
**Decision:** Accept a constrained design that removes autonomous side-effect capability.

### 1. Current state versus proposed operating scenario

The repository describes a future production scenario involving a database, message topic, PayEx integration and 24x7 on-call support. The README explicitly states that these components are not yet implemented in the application. This assessment therefore distinguishes existing evidence packs from the proposed future environment; it does not claim that a production AI agent or its permissions already exist.

### 2. Lethal-trifecta assessment

| Risk element | Assessment | Evidence and reasoning |
|---|---|---|
| Access to sensitive data | Potentially present | Incident logs, metrics and deployment diffs are available in the evidence packs. Future invoice records and provider data may contain sensitive information. The actual sensitivity and agent access permissions must be verified before rollout. |
| Access to untrusted content | Present in the proposed workflow | Alerts, application logs, publisher/worker logs and deployment diffs may contain malformed input or attacker-controlled text. The agent must treat all retrieved content as data, never as instructions. |
| Ability to perform consequential actions | Not evidenced in the current repository; possible in a future integrated setup | The README does not establish that an AI agent can call production tools. Future integrations with deployment, database, messaging or PayEx operations could create consequential side effects if write permissions are granted. |

**Conclusion:** The complete trifecta is not proven to exist in the current repository. However, a future agent that can read sensitive operational data, consume untrusted logs and execute privileged tools would create a high-risk combination.

### 3. Risk decision and mitigation

**Decision: Redesign the initial workflow to remove the side-effect leg.**

The month-end triage agent will operate in read-only recommendation mode:

- It may summarize approved alerts, logs, metrics and deployment history.
- It may propose diagnostic queries and remediation steps, but must not execute them.
- It must not deploy code, restart services, mutate database records, replay messages, change invoice approval states or submit/re-submit transactions to PayEx.
- Production changes and financially consequential actions remain under explicit human control.
- Retrieved content is treated as untrusted. The agent must not follow instructions found inside logs, alerts, tickets or documents.
- Use least-privilege access, secret redaction, bounded context, evidence-linked findings and audit logging.
- Do not expose production credentials or grant the agent write-capable credentials for this workflow.

This design accepts that sensitive data and untrusted content may coexist, but prevents the agent from directly combining them with autonomous production actions. Read-only access still carries confidentiality and prompt-injection risks; it is not risk-free.

### 4. Validation and ownership

Before enabling the workflow, the engineering lead and security owner must verify:

1. The agent's actual data sources and permissions.
2. That its identity cannot write to production databases, deploy applications, publish messages or invoke consequential PayEx operations.
3. That logs containing malicious instructions cannot trigger tool execution.
4. That secrets and sensitive customer information are redacted where feasible.
5. That each reported finding cites its supporting evidence and is traceable to the relevant run.

**Owners:** Engineering lead owns workflow approval; security owner approves access boundaries; the on-call engineer remains accountable for incident decisions.

### 5. Revisit trigger

Reassess this decision before introducing write-capable tools, production credentials, autonomous remediation, or access to additional sensitive data. Also reassess after a security incident, a material change in agent capabilities, or evidence that the read-only boundary can be bypassed.

Any proposal to allow production actions requires a new documented risk decision, least-privilege design, tested safeguards and explicit approval. It must not be enabled merely because the agent performs well on evaluation cases.
