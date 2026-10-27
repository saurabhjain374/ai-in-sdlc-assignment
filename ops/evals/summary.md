# AI Code Review Evaluation Summary

## 1. What Was Tested

- **Baseline:** Prompt v1 was tested three times on the same 10 cases.
- **Revised version:** Prompt v2 was tested in Run 4.
- **Model:** GPT-5.6 Luna.
- **Tool:** GitHub Copilot Chat Ask.
- **Run 4:** Tested the original 10 cases plus two new cases: Case 11 (lifecycle regression) and Case 12 (clean control).

The prompt was the only planned change. Findings were scored against specific expected defects, rather than counting a case as successful just because the review reported an issue.

## 2. Important Limitation: Case 03

Case 03 contains a code patch for a static `DiscountCalculator.Apply` method. However, the current repository has an instance method called `ApplyDiscount`, with a different discount-rate convention.

Because the patch does not match the current code, Case 03 is excluded from the primary defect-detection metrics. Its raw results are retained for transparency. Identifying this API mismatch does not count as detecting the intended rounding defect.

## 3. Run 4: Initial Results

Run 4 covered 12 cases:

- 10 cases produced findings.
- 2 cases reported no findings.
- Case 12, the clean control, was correctly reported as having no findings.

These are case-level results, not the final accuracy metrics. Final scores are based on individual defects.

## 4. How Results Are Scored

- **True positive (TP):** A real, expected defect was correctly identified.
- **False negative (FN):** An expected defect was missed.
- **False positive (FP):** An incorrect, unsupported, speculative, or pre-existing issue was reported as a defect introduced by the change.
- **True negative (TN):** A clean case was correctly treated as having no defect.

Metrics:

- **Recall:** TP / (TP + FN). How many expected defects were detected.
- **Precision:** TP / (TP + FP). How many reported defects were correct.
- **False-alarm share:** FP / (TP + FP). How many reported defects were false alarms.
- **False-positive rate:** FP / (FP + TN). How often clean outcomes were incorrectly flagged, using the adjudicated counts.

A single underlying defect is counted once, even if it causes multiple symptoms, unless the symptoms represent separate actionable defects.

## 5. Expected Defects and Review Rules

| Case | What the review should check |
|---|---|
| Case 01 | Undefined `CurrentUser`, null request IDs, exception handling, partial batch approval, and authorization issues supported by the existing contract. |
| Case 02 | Missing query-service dependency or registration, and SQL injection through customer/status parameters. |
| Case 03 | Monetary calculation and rounding changes. Excluded from primary scoring because the patch does not match the current API. |
| Case 04 | No expected defect. A field or constructor-parameter rename is not a defect without evidence of a broken caller. |
| Case 05 | Repository method mismatch (`Delete` vs. `Remove`), undefined `_logger` or `CurrentUser`, and supported authorization or not-found response defects. |
| Case 06 | Undefined `Pending(...)` helper calls in tests. |
| Case 07 | Undefined `_logger` or `CurrentUser`, and sensitive invoice data added to logs. |
| Case 08 | Replacing thread-safe `ConcurrentDictionary` with `Dictionary`, and non-atomic duplicate detection. Related symptoms count as one root defect unless independently actionable. |
| Case 09 | No expected defect from the logging-level change unless the change introduces another concrete defect. Unchanged README issues are not defects introduced by the patch. |
| Case 10 | A catch-all exception handler returning HTTP 200 with a success-like response. |
| Case 11 | Removing the Draft-status check from `ApprovalService.Submit`, allowing non-draft invoices to be resubmitted. |
| Case 12 | No expected defect. Replacing `string.Empty` with `""` is the clean control. |

The original outputs in `results.csv` remain unchanged. Adjudicated scores are stored separately in `adjudication.csv` so the results can be reviewed and audited.

Case 03 is excluded from the primary metrics, and authorization findings without supporting evidence are not counted.

## 6. Final Results

### Results by run

| Run | TP | FN | FP | TN | Recall | Precision | False-alarm share | False-positive rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Run 1 | 11 | 2 | 2 | 1 | 84.6% | 84.6% | 15.4% | 66.7% |
| Run 2 | 11 | 2 | 1 | 1 | 84.6% | 91.7% | 8.3% | 50.0% |
| Run 3 | 13 | 0 | 2 | 0 | 100.0% | 86.7% | 13.3% | 100.0% |
| Run 4 — all scored cases | 13 | 1 | 1 | 2 | 92.9% | 92.9% | 7.1% | 33.3% |

### Baseline vs. revised prompt

For a fair comparison, Run 4 must use only the original comparable cases. Cases 11 and 12 are reported separately as additional tests.

| Metric | Baseline (Runs 1–3 combined) | Revised prompt (Run 4 comparable cases) |
|---|---:|---:|
| TP | 35 | 12 |
| FN | 4 | 1 |
| FP | 5 | 1 |
| TN | 2 | 1 |
| Recall | 89.7% | 92.3% |
| Precision | 87.5% | 92.3% |
| False-alarm share | 12.5% | 7.7% |
| False-positive rate | 71.4% | 50.0% |

### What the results suggest

Compared with the combined baseline, the revised prompt showed:

- **Recall increased by 2.6 percentage points.**
- **Precision increased by 4.8 percentage points.**
- **False-alarm share decreased by 4.8 percentage points.**
- **False-positive rate decreased by 21.4 percentage points.**

These results suggest that prompt v2 may provide a better balance between finding defects and avoiding incorrect findings.

## 7. Limitations and Next Steps

The results should be treated as preliminary:

- The evaluation set is small.
- Defects within the same case may be related and are not independent observations.
- The test cases may not represent real production changes.
- Case 03 has a known fixture mismatch and is excluded from the primary metrics.

The experiment kept the model and review mode fixed while changing the prompt. Cases 11 and 12 provide additional coverage but are excluded from the original-set comparison.

**Conclusion:** Prompt v2 shows promising results in this evaluation, but the evidence is not sufficient to prove a general improvement in AI code review. Further testing on a larger, representative, fixed test set is needed.