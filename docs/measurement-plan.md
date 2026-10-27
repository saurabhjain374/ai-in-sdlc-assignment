# Measurement Plan: AI in the SDLC

**Date:** 2026-10-21

## 1. Purpose

The goal is to check whether AI helps us deliver software faster without increasing defects or risks.

We will measure:
- Lead time for changes
- Production change failure rate
- Code review turnaround time
- CI pipeline results

We must use actual evidence and clearly mention when data is missing.

## 2. Metrics

### 2.1 Lead Time for Changes

**What it means:** The time taken from the first commit of a change until it is deployed to production.

**How to measure:** Compare the first commit timestamp with the production deployment timestamp.

**Current status:** We have commit history, but a verified production deployment timestamp is not available. Therefore, actual production lead time cannot be calculated yet.

### 2.2 Change Failure Rate

**What it means:** The percentage of production changes that cause a failure requiring a rollback, fix, or hotfix.

**Formula:**

`Change Failure Rate = Failed Production Changes / Total Production Changes × 100`

**How to measure:** Use production deployment records, incidents, rollbacks, and hotfix records.

**Current status:** Verified production change and failure records are not available. Pipeline failures must not be counted as production failures.

### 2.3 Review Turnaround Time

**What it means:** The time between a pull request becoming ready for review and receiving its first meaningful human review.

**How to measure:** Compare GitHub's pull request timestamps and calculate the median review time.

**Current status:** We have not collected a verified set of review timestamps yet.

## 3. Measurements Collected

### Evidence A — Repository Activity

**Source:** Git commit history on the `master` branch.

**Command:**

`git log --all --format="%h | %ad | %s" --date=iso-strict`

- First commit: `abe109b` — 19 October 2026, 17:04:55 (+05:30)
- Latest commit at the time of review: `5d4ed40` — 21 October 2026, 21:03:42 (+05:30)
- Total elapsed time: **51 hours, 58 minutes, 47 seconds**

This shows how long the repository activity window lasted. It is **not production lead time**.

### Evidence B — Evaluation File History

**Source:** Git history for `ops/evals`.

**Commands:**

`git log --all --format="%h | %ad | %s" --date=iso-strict -- ops/evals`

`git log --all --reverse --format="%ad" --date=iso-strict -- ops/evals`

- Commits affecting evaluation files: 5
- Time span: 19 October 2026, 17:04:55 to 21 October 2026, 17:47:17 (+05:30)

This shows when the evaluation files were updated. It does not tell us the actual engineering effort or code review time.

### Evidence C — Sample Pipeline Data

**Source:** `ops/pipeline/run-timings.csv`

The assignment provides sample pipeline data with these results:

- Total sample runs: 20
- Successful runs: 18
- Failed runs: 2
- Success rate: **90%**
- Average sum of step durations per run: 1,880.5 seconds
- Median sum of step durations: 1,875.5 seconds
- Minimum: 1,702 seconds
- Maximum: 2,108 seconds

These numbers come from the assignment's sample data. They are **not live CI results or production failure measurements**.

The summed step durations may include parallel steps, so they should not automatically be treated as total pipeline elapsed time.

### Evidence D — GitHub Actions Results

**Source:** `.github/workflows/ci.yml`

- Branch: `master`
- Completed workflow runs observed: 4
- Successful runs: 4
- Failed runs: 0
- Sample success rate: **100% (4 out of 4)**
- Approximate elapsed time per run: 23–40 seconds
- Median elapsed time: approximately 30 seconds

All four observed runs completed the Release build and test steps successfully.

This is a small sample from the assignment repository. It does not prove long-term CI reliability or improved production performance. The timings are estimates based on workflow creation and last-update timestamps.

## 4. How We Will Report Results

For every measurement, we will record:

- The source of the data
- The measurement period
- The command or calculation used
- The number of records measured
- The result and its limitations

We will keep sample data separate from live system data.

If data is unavailable, we will report it as unavailable rather than zero. We will also avoid assuming that a commit means a change was deployed to production.

## 5. Next Steps

1. Collect a baseline for production lead time, change failure rate, and review turnaround using verified records.
2. Continue collecting CI results over a larger period.
3. Repeat the measurements after introducing AI-assisted workflow changes.
4. Compare similar periods and sample sizes.
5. Check whether faster delivery is achieved without reducing quality.

## 6. Conclusion

We have measured the repository activity window, reviewed the sample pipeline data, and observed four successful GitHub Actions runs.

However, verified production deployment timestamps, production change failure records, and pull request review timestamps are still missing.

**Therefore, we cannot yet prove that AI has improved delivery performance.** More reliable data and measurements over a longer period are needed to reach that conclusion.
