# AI-in-SDLC Measurement Plan

## Purpose

Measure whether AI-assisted software delivery improves delivery speed without reducing quality or increasing operational risk.

## Metrics

| Metric | Definition | Data source | Measurement method |
|---|---|---|---|
| Lead time for changes | Time from a change being committed to its deployment in production | Git history and CI/CD deployment history | Calculate elapsed time between commit and successful production deployment |
| Change failure rate | Percentage of production changes that cause a failure requiring rollback, hotfix, or incident response | Deployment history and incident records | Failed production changes / total production changes × 100 |
| Review turnaround time | Elapsed time between a change being submitted for review and its first completed review | Pull request history | First review timestamp − pull request creation timestamp |

## Baseline Evidence

Record at least two actual values from available repository or CI history.

For each value, include:
- Metric and measured value
- Observation period
- Exact source, command, or query
- Evidence location or link
- Any limitations or assumptions

Do not invent missing historical data. If a metric cannot be measured from available evidence, record it as unavailable and explain why.

### Preliminary Evidence — Repository Activity

- **Source:** Local Git repository history.
- **Command:** `git log -10 --date=iso-strict --pretty=format:"%h | %ad | %s"`
- **Initial commit:** `abe109b` — 2026-10-19 17:04:55 +05:30.
- **Latest observed commit:** `3c713e5` — 2026-10-21 17:47:17 +05:30.
- **Elapsed time:** 48 hours, 42 minutes, 22 seconds.
- **Interpretation:** This measures the span between the initial commit and the latest observed commit, not the lead time of an individual change.
- **Limitation:** Production deployment timestamps are not established by this Git log, so this value must not be reported as production lead time.


## Comparison Plan

Use the same metric definitions and comparable observation periods before and after AI-assisted workflow changes. Report the sample size and limitations alongside any claimed improvement.
