# Measurement Plan: AI in the SDLC

**Date:** 2026-10-21

## 1. Purpose

Measure whether AI-assisted development improves delivery speed without increasing defects or review risk. Repository activity and scenario-provided pipeline data are useful evidence, but they must not be presented as verified production performance.

## 2. Metrics and collection methods

### 2.1 Lead time for changes

- **Definition:** Elapsed time from the first commit associated with a change to that change being deployed to production.
- **Source:** Git commit history and deployment records.
- **Collection:** Link the change's first commit and production deployment timestamp; calculate the elapsed time.
- **Limitation:** Commit timestamps alone do not establish deployment time. A verified production deployment timestamp is currently unavailable.

### 2.2 Change failure rate

- **Definition:** Percentage of production changes that cause a failure requiring remediation, rollback, or a hotfix.
- **Calculation:** Failed production changes / total production changes × 100.
- **Source:** Production deployment history, incident records, rollback records, and hotfix records.
- **Limitation:** The repository does not provide a verified production-change denominator or a linked production failure history. Do not treat sample pipeline failures as production change failures.

### 2.3 Review turnaround

- **Definition:** Elapsed time from a pull request becoming ready for review to its first substantive human review.
- **Source:** GitHub pull request timeline and review events.
- **Collection:** Compare the ready-for-review timestamp with the first substantive review timestamp; report the median and sample size for the measurement period.
- **Limitation:** A verified set of review-event timestamps has not been collected for this assignment.

## 3. Available evidence

### Evidence A — Repository activity window

- **Source:** Git commit history on the `master` branch.
- **Command:** `git log --all --format="%h | %ad | %s" --date=iso-strict`
- **Observed first commit:** `abe109b` — 2026-10-19 17:04:55 (+05:30).
- **Observed latest commit at this review:** `5d4ed40` — 2026-10-21 21:03:42 (+05:30).
- **Elapsed window:** 51 hours, 58 minutes, 47 seconds.

This is the observed repository activity window, not measured lead time for a production change.

### Evidence B — Evaluation-file commit history

- **Source:** Git history for the evaluation files.
- **Commands:**
  - `git log --all --format="%h | %ad | %s" --date=iso-strict -- ops/evals`
  - `git log --all --reverse --format="%ad" --date=iso-strict -- ops/evals`
- **Observed commits affecting `ops/evals`:** 5.
- **Observed span:** From the initial commit at `2026-10-19T17:04:55+05:30` to `2026-10-21T17:47:17+05:30`.

This indicates when evaluation artifacts changed. It does not establish review turnaround, engineering effort, or production lead time.

### Evidence C — Scenario-provided pipeline timing fixture

- **Source:** `ops/pipeline/run-timings.csv`.
- **Scope:** 20 sample pipeline runs represented in the assignment fixture; 378 recorded step rows.
- **Observed outcomes:** 18 successful runs and 2 failed runs.
- **Fixture success rate:** 90%.
- **Sum of recorded step durations per run:** Mean 1,880.5 seconds; median 1,875.5 seconds; minimum 1,702 seconds; maximum 2,108 seconds.

These are calculations from the repository's scenario-provided fixture. They are **not verified live GitHub Actions results or production change-failure measurements**. Summed step durations may include parallel work and should not automatically be interpreted as wall-clock pipeline duration.

### Evidence D — GitHub Actions execution history

- **Workflow:** `.github/workflows/ci.yml`.
- **Branch:** `master`.
- **Scope:** 4 completed push-triggered workflow runs observed during this review.
- **Outcomes:** 4 successful runs, 0 failed runs.
- **Observed sample success rate:** 100% (4/4).
- **Approximate elapsed time from run creation to last update:** 23–40 seconds; median approximately 30 seconds.

All four runs completed their Release build and test steps successfully.

These results describe a small, assignment-specific CI sample. They are not production change-failure measurements, and four successful runs do not establish long-term CI reliability. Run elapsed time is estimated from GitHub's creation and last-update timestamps, not from detailed job timing measurements.

## 4. Data quality and reporting rules

- Record the measurement period, source, query or command, sample size, and calculation with each reported metric.
- Separate scenario fixtures from live system records.
- Do not report unavailable metrics as zero.
- Do not infer production deployment, review, or incident timestamps from commit history alone.
- When real data becomes available, report both the metric and its denominator; compare equivalent periods before and after introducing AI assistance.

## 5. Follow-up measurement

After verified CI and deployment records become available:

1. Capture baseline lead time, production change-failure rate, and review turnaround.
2. Repeat collection over a comparable period after AI-assisted workflow changes.
3. Record sample sizes and relevant workflow changes that may affect the comparison.
4. Review whether speed improvements coincide with stable or improved quality; do not attribute changes to AI alone without considering other factors.

**Current conclusion:** The repository provides evidence of development activity and a scenario pipeline fixture, but it does not yet provide enough verified live CI, production deployment, or review-event data to establish actual delivery-performance improvements.