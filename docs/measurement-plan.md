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

The available repository history provides two observed activity values. These are repository-activity indicators, not substitutes for the three delivery-performance metrics defined above. No production deployment, incident, or pull-request review timestamps were available during this inspection.

### Evidence 1 — Repository activity span

- **Observed value:** 48 hours, 42 minutes, 22 seconds.
- **Observation period:** 2026-10-19 17:04:55 +05:30 to 2026-10-21 17:47:17 +05:30.
- **Source:** Local Git repository history.
- **Command:** `git log -10 --date=iso-strict --pretty=format:"%h | %ad | %s"`
- **Initial commit:** `abe109b` — 2026-10-19 17:04:55 +05:30.
- **Latest observed commit:** `3c713e5` — 2026-10-21 17:47:17 +05:30.
- **Interpretation:** Elapsed time between the initial commit and the latest observed commit in the inspected history.
- **Limitation:** This does not measure the lead time of an individual change because production deployment timestamps are unavailable.

### Evidence 2 — Evaluation-file commit count

- **Observed value:** 5 commits affecting `ops/evals`.
- **Observation period:** 2026-10-19 17:04:55 +05:30 to 2026-10-21 17:47:17 +05:30.
- **Source:** Local Git repository history for evaluation files.
- **Command:** `git log --all --format="%h | %ad | %s" --date=iso-strict -- ops/evals`
- **Evidence:** Five listed commits: `abe109b`, `9e3a7d2`, `ffe6811`, `7864fe1`, and `3c713e5`.
- **Interpretation:** Number of recorded commits affecting the evaluation directory during the observed history.
- **Limitation:** Commit count measures repository activity only. It does not measure review turnaround, defect detection effectiveness, or production delivery performance.

### CI Evidence Availability

- **Workflow:** `.github/workflows/ci.yml`
- **Triggers:** Push to `main` and pull requests targeting `main`.
- **Configured checks:** Release build and test for `backend/InvoiceApp.sln`.
- **Historical run evidence:** No workflow runs were visible on the GitHub Actions page during inspection.
- **Baseline implication:** Historical CI success rate, CI duration, and deployment timing cannot be calculated from the available run history.
- **Next action:** Capture a successful run after CI executes, retaining its run URL, conclusion, timestamp, and duration.
- **Limitation:** A build/test workflow does not establish production deployment timing or production change failures.

### Unavailable baseline metrics

- **Lead time for changes:** Unavailable; production deployment timestamps are missing.
- **Change failure rate:** Unavailable; the required production-change denominator and linked incident, rollback, or hotfix records are missing.
- **Review turnaround time:** Unavailable; pull-request creation and first-review timestamps are missing.

Do not interpret unavailable values as zero. Capture the necessary source records before making a baseline or before/after improvement claim.

### CI Evidence Availability

- **Workflow:** `.github/workflows/ci.yml`
- **Triggers:** Push to `main` and pull requests targeting `main`.
- **Configured checks:** Release build and test for `backend/InvoiceApp.sln`.
- **Historical run evidence:** No workflow runs were visible in the GitHub Actions page during this inspection.
- **Baseline implication:** No historical CI success rate, CI duration, or deployment timing can be calculated from the available run history.
- **Next action:** Capture a successful run after CI executes, and retain its run URL, conclusion, timestamp, and duration.
- **Limitation:** A build/test workflow does not establish production deployment timing or production change failures.


### Preliminary Evidence — Repository Activity

- **Source:** Local Git repository history.
- **Command:** `git log -10 --date=iso-strict --pretty=format:"%h | %ad | %s"`
- **Initial commit:** `abe109b` — 2026-10-19 17:04:55 +05:30.
- **Latest observed commit:** `3c713e5` — 2026-10-21 17:47:17 +05:30.
- **Elapsed time:** 48 hours, 42 minutes, 22 seconds.
- **Interpretation:** This measures the span between the initial commit and the latest observed commit, not the lead time of an individual change.
- **Limitation:** Production deployment timestamps are not established by this Git log, so this value must not be reported as production lead time.

### Evaluation File History

- **Source:** Git history for `ops/evals`.
- **Command:** `git log --all --reverse --format="%ad" --date=iso-strict -- ops/evals`
- **Earliest recorded commit:** 2026-10-19 17:04:55 +05:30.
- **Latest recorded commit:** 2026-10-21 17:47:17 +05:30.
- **Elapsed time:** 48 hours, 42 minutes, 22 seconds.
- **Interpretation:** This is the observed span of repository history affecting evaluation files. It is not a measure of individual review turnaround or production lead time.
- **Limitation:** Git commit timestamps do not show when a reviewer first responded, when a review was completed, or when a production deployment occurred.


## Comparison Plan

Use the same metric definitions and comparable observation periods before and after AI-assisted workflow changes. Report the sample size and limitations alongside any claimed improvement.
