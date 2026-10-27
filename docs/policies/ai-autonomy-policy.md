# AI Autonomy Policy — Month-End Invoice Incidents

**Status:** Proposed  
**Date:** 19 October 2026  
**Owner:** Invoice Application Engineering Team

## 1. Why do we need this policy?

During month-end invoice processing, problems may occur that require quick investigation.

An AI agent can help the team by:
- Summarising alerts and error messages.
- Checking logs and monitoring data to find possible causes.
- Suggesting what to investigate next.
- Preparing incident reports and possible solutions.

However, AI must not independently change live systems or make decisions that could affect payments.

**Our rule: AI can help investigate and recommend. A responsible person must verify the findings and decide what to do.**

## 2. What is AI allowed to do?

We use five levels to describe how much freedom the AI has.

| Level | What it means | Example |
|---|---|---|
| **L0 — Observe** | AI can read approved information but cannot change anything. | Read error logs and alerts. |
| **L1 — Recommend** | AI can explain what might be wrong and suggest next steps. | Suggest checking a database connection after an error. |
| **L2 — Prepare** | AI can prepare work for a person to review. | Draft a report, query or code change. |
| **L3 — Execute approved actions** | AI can perform specific, pre-approved actions under strict controls. | Run an approved diagnostic check after a named person authorises it. |
| **L4 — Act independently in production** | AI makes production changes without approval for each action. | Restart a production service on its own. |

L2 and L3 require additional controls and approval before they can be introduced. **L4 is not allowed under this policy.**

## 3. What can AI do on day one?

**Day-one limit: L1 — Recommend.**

Our engineering team has six members, including two who are new to the codebase. Therefore, we will start with limited AI permissions.

Initially, AI can read approved information, investigate possible causes and recommend next steps.

AI must not:
- Deploy code to production.
- Restart production services.
- Change database records.
- Replay messages or resubmit payments.
- Change an invoice's approval status.

AI may prepare an incident summary and an investigation plan. A responsible engineer must check the evidence and decide what action to take.

## 4. What safety rules must AI follow?

The following rules apply whenever AI assists with an incident.

- **Limit access:** Give AI access only to the information and tools it needs. Initially, access must be read-only.
- **Protect sensitive information:** Do not expose passwords, access tokens, customer personal information or payment details in prompts or reports.
- **Do not blindly trust input:** Logs, tickets and documents may contain incorrect information or misleading instructions. AI must treat them as information to examine, not instructions to follow.
- **Show evidence:** AI must point to the relevant logs, timestamps or other evidence supporting its findings. If something is only a guess, it must say so.
- **Handle PayEx timeouts carefully:** A timeout does not prove that PayEx failed to process a submission. Check the submission status before attempting a potentially duplicate submission.
- **Keep records:** Record what information AI used, what it recommended, which model and prompt version were used, and what decision the human made.
- **Escalate risky situations:** Send unclear, security-related, customer-impacting or payment-related incidents to the on-call engineer.

## 5. What must be proven before AI gets more freedom?

We must not increase AI's permissions simply because it appears to work well.

Before allowing L2 or L3, we must:

1. Test AI against real or representative incidents, including cases where no action is needed.
2. Measure how often AI misses problems, raises false alarms, uses incorrect evidence or recommends unsafe actions.
3. Confirm that AI cannot access information or perform actions outside its permissions.
4. Ensure that its recommendations and actions can be traced through an audit record.
5. Document how to reverse an action if something goes wrong.
6. Assign a responsible human owner.

The engineering lead and production/service owner must approve any increase in autonomy. Security approval is also required if permissions or access to sensitive information change.

We will increase autonomy one level at a time. L4 remains prohibited under this policy.

## 6. When should we review or stop AI access?

We will review this policy:
- After a major incident.
- When the AI model, tools or permissions change.
- At least once every three months.

We must immediately suspend AI access if it exposes sensitive information, performs an unauthorised action, goes beyond its approved permissions or cannot provide evidence for its findings.

AI access can resume only after the issue has been investigated and the responsible owners approve it.

**Final rule:** Start with AI as an assistant, not an independent operator. Give it more responsibility only after testing, evidence and formal approval show that it can be done safely.