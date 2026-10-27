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

**What it means:** The time between the first commit of a change and its production deployment.

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
- Latest verified commit: `0085761` — 27 October 2026, 22:40:58 (+05:30)
- Total elapsed time: **8 days, 5 hours, 36 minutes, 3 seconds**

This measures the repository activity window from the first commit to the latest verified commit. It is **not production lead time**.

### Evidence B — Evaluation File History

**Source:** Git history for `ops/evals`.

**Commands:**

`git log --all --format="%h | %ad | %s" --date=iso-strict -- ops/evals`

`git log --all --reverse --format="%ad" --date=iso-strict -- ops/evals`

The previous measurement recorded:

- Commits affecting evaluation files: 5
- Recorded period: 19 October 2026, 17:04:55 to 21 October 2026, 17:47:17 (+05:30)

**Note:** These are the previously recorded results, not a verified count through 27 October. Run the commands again to confirm the latest count and time span.

This history shows when evaluation files were updated. It does not measure engineering effort or code review time.

### Evidence C — Sample Pipeline Data

**Source:** `ops/pipeline/run-timings.csv`

The assignment's sample pipeline data contains:

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

**Source:** `.github/workflows/ci.yml`

The previously observed sample contained:

- Branch: `master`
- Completed workflow runs: 4
- Successful runs: 4
- Failed runs: 0
- Sample success rate: **100% (4 out of 4)**
- Approximate elapsed time per run: 23–40 seconds
- Median elapsed time: approximately 30 seconds

All four runs in that sample completed the Release build and test steps successfully.

**Note:** This is the earlier observed sample, not a verified total through 27 October. Check the latest GitHub Actions history before reporting current totals.

The sample is small and does not prove long-term CI reliability or improved production performance. The recorded timings are estimates based on workflow creation and last-update timestamps.

## 4. Reporting Rules

For every measurement, record:

- Data source and measurement period
- Command or calculation used
- Number of records measured
- Result and its limitations

Keep scenario-provided sample data separate from live system data.

Do not report missing data as zero. Do not assume a commit means a change was deployed to production.

## 5. Next Steps

1. Refresh the repository activity and evaluation-file history using the commands above.
2. Check the latest GitHub Actions runs and update the sample size, outcomes, and timings.
3. Collect verified production deployment data to measure lead time.
4. Collect production incidents, rollbacks, and hotfix records to measure change failure rate.
5. Collect pull request review timestamps to measure review turnaround.
6. Repeat the measurements over comparable periods and check whether delivery speed improves without reducing quality.

## 6. Conclusion

The repository provides evidence of development activity, sample pipeline timings, and an earlier sample of four successful GitHub Actions runs.

However, production deployment timestamps, verified production change failure records, and pull request review timestamps are still unavailable. The latest CI totals and evaluation-file history also need to be refreshed before they can be reported as current.

**Therefore, we cannot yet prove that AI has improved delivery performance.** More complete and consistently collected evidence is needed to reach that conclusion.