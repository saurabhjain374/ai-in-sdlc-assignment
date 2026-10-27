## AI Agent Risk Audit — Lethal Trifecta

**Assessment date:** 19 October 2026  
**Scope:** Using AI to help investigate month-end incidents and application logs.

### 1. What Are We Assessing?

We are assessing how AI could help engineers investigate production issues in the planned production environment.

The main question is: **Can AI analyse operational data safely without putting production systems or financial transactions at risk?**

This is a risk assessment of the proposed workflow. It does not mean an AI agent already has production access.

### 2. What Are the Main Risks?

The Lethal Trifecta looks at three risk areas:

| Risk | Assessment |
|---|---|
| Sensitive information | Logs and future invoice or payment data may contain sensitive information. We must check what data the AI can access. |
| Untrusted content | Logs, alerts, and deployment details may contain incorrect or malicious text. AI must treat this content as data, not as instructions. |
| Ability to take actions | The current repository does not show an AI agent with production action permissions. Future integrations could create this risk if write access is granted. |

**Conclusion:** The repository does not prove that all three risks exist together today. However, combining sensitive data, untrusted content, and the ability to change production systems could create a serious security risk.

### 3. Our Decision: Keep AI Read-Only

The initial AI workflow will be limited to analysis and recommendations.

AI can:

- Summarise approved logs, alerts, metrics, and deployment history.
- Suggest diagnostic queries and possible solutions.
- Provide findings with supporting evidence.

AI must not independently:

- Deploy code or restart services.
- Change database records or invoice approval states.
- Replay messages.
- Submit or resubmit transactions to PayEx.

**Humans remain responsible for production changes and financial decisions.**

We will also apply these safeguards:

- Give AI only the minimum access it needs.
- Remove secrets and sensitive information where possible.
- Limit the information provided to the AI.
- Record AI activity and link findings to supporting evidence.
- Never give this workflow credentials that allow it to make production changes.
- Ensure AI does not follow instructions hidden inside logs, alerts, or documents.

Read-only access reduces the risk of harmful actions, but it does not remove every risk. Sensitive information could still be exposed, and malicious content could still influence AI responses.

### 4. Checks and Responsibilities

Before enabling the workflow, we must verify:

1. Which data sources the AI can access and what permissions it has.
2. That the AI cannot change production databases, deploy code, publish messages, or perform PayEx operations.
3. That malicious instructions inside logs cannot cause the AI to execute tools.
4. That secrets and sensitive customer information are protected where possible.
5. That each finding includes supporting evidence and can be traced to the relevant run.

**Responsibilities**

- **Engineering lead:** Approves the workflow.
- **Security owner:** Reviews and approves access permissions.
- **On-call engineer:** Remains responsible for incident decisions.

### 5. When Should We Review This Decision?

We must reassess the risks before:

- Giving AI access to tools that can change production.
- Providing production credentials.
- Allowing AI to fix incidents automatically.
- Giving AI access to more sensitive information.

We must also review the decision after a security incident, a significant change in AI capabilities, or evidence that the read-only restrictions can be bypassed.

Any proposal to allow AI to take production actions requires a new risk assessment, tested safeguards, least-privilege access, and explicit approval.

**Good evaluation results alone are not enough to allow AI to make production changes.**