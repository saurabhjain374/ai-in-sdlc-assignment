# Measurement Plan: AI in the SDLC

**Last updated:** 27 October 2026

## 1. Purpose

The goal is to understand whether AI helps us deliver software faster without increasing defects or risks.

We will track:

- Lead time for changes
- Production change failure rate
- Code review turnaround time
- CI pipeline results

All measurements must be supported by evidence. Missing data must be clearly identified.

## 2. Metrics

### 2.1 Lead Time for Changes

**What it means:** The time between the first commit of a change and its verified production deployment.

**How to measure:** Compare the first commit timestamp with the verified production deployment timestamp.

**Current status:** Commit history is available, but a verified production deployment timestamp is not available. Actual production lead time cannot yet be calculated.

### 2.2 Change Failure Rate

**What it means:** The percentage of production changes that cause failures requiring a fix, rollback, or hotfix.

**Formula:**

`Change Failure Rate = Failed Production Changes / Total Production Changes × 100`

**How to measure:** Use production deployment records, incidents, rollbacks, and hotfix records.

**Current status:** Verified production change and failure records are unavailable. Pipeline failures must not be counted as production failures.

### 2.3 Review Turnaround Time

**What it means:** The time between a pull request becoming ready for review and receiving its first meaningful human review.

**How to measure:** Compare GitHub pull request timestamps and calculate the median review time.

**Current status:** A verified set of review timestamps has not yet been collected.

## 3. Measurements Collected

### Evidence A — Repository Activity

**Source:** Git commit history on the `master` branch.

**Command:**

`git log --all --format="%h | %ad | %s" --date=iso-strict`

- First commit: `abe109b` — 19 October 2026, 17:04:55 (+05:30)
- Latest verified commit before this plan update: `70ad980` — 27 October 2026, 23:20:20 (+05:30)
- Elapsed repository activity window: **8 days, 6 hours, 15 minutes, 25 seconds**

This measures the span from the first commit to the latest verified commit before this plan update. It is **not production lead time**, engineering effort, or time saved by AI.

### Evidence B — Evaluation File History

**Source:** Git history for `ops/evals`.

**Commands:**

`git log --all --format="%h | %ad | %s" --date=iso-strict -- ops/evals`

`git log --all --reverse --format="%ad" --date=iso-strict -- ops/evals`

At this update:

- Commits affecting evaluation files: **8**
- First recorded commit: 19 October 2026, 17:04:55 (+05:30)
- Latest recorded evaluation-file commit: 27 October 2026, 22:48:38 (+05:30)

This history shows when evaluation files were updated. It does not measure engineering effort or code review time.

### Evidence C — Sample Pipeline Data

**Source:** `ops/pipeline/run-timings.csv`

The assignment's scenario-provided sample data contains:

- Total sample runs: 20
- Successful runs: 18
- Failed runs: 2
- Success rate: **90%**
- Average sum of step durations per run: 1,880.5 seconds
- Median sum of step durations: 1,875.5 seconds
- Minimum: 1,702 seconds
- Maximum: 2,108 seconds

These figures come from the scenario-provided sample data. They are **not live CI results or production failure measurements**.

The sum of step durations may include parallel steps, so it should not automatically be treated as total pipeline elapsed time.

### Evidence D — GitHub Actions Results

**Source:** [GitHub Actions workflow history](https://github.com/saurabhjain374/ai-in-sdlc-assignment/actions/workflows/ci.yml) for `.github/workflows/ci.yml`, branch `master`.

**Snapshot checked:** 27 October 2026.

- Workflow runs returned: **21**
- Completed workflow runs: **21**
- Successful runs: **21**
- Failed runs: **0**
- Completed-run success rate: **100% (21 out of 21)**
- Approximate creation-to-last-update time: **23–66 seconds**
- Median approximate time: **33 seconds**

The timing values are estimates calculated from each workflow run's `created_at` and `updated_at` timestamps. They are **not guaranteed to equal actual runner execution duration**.

All 21 runs in this snapshot completed successfully. This is a small, time-bounded sample and does not prove long-term CI reliability, improved production performance, or a reduction in production failures. CI failures, if any, must not be treated as production change failures.

## 4. Reporting Rules

For every measurement, record:

- Data source and measurement period
- Command or calculation used
- Number of records measured
- Result and its limitations

Keep scenario-provided sample data separate from live system data.

Do not report missing data as zero. Do not assume a commit means a change was deployed to production. When reporting workflow timings, label timestamp-based estimates as estimates.

## 5. Next Steps

1. Refresh repository activity and evaluation-file history when new changes are made.
2. Recheck GitHub Actions history before presenting the figures in a later report or demo.
3. Collect verified production deployment data to measure lead time.
4. Collect production incidents, rollbacks, and hotfix records to measure change failure rate.
5. Collect pull request review timestamps to measure review turnaround.
6. Repeat measurements over comparable periods and assess whether delivery speed improves without reducing quality.

## 6. Conclusion

The repository provides evidence of development activity, scenario-provided pipeline timings, and **21 successful GitHub Actions runs in the checked snapshot**.

However, verified production deployment timestamps, production change failure records, and pull request review timestamps are still unavailable. The current evidence therefore does not establish production lead time, production change failure rate, review turnaround, or causal AI productivity gains.

**We cannot yet prove that AI has improved delivery performance.** More complete and consistently collected evidence is needed to reach that conclusion.
