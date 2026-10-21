# AI Code Review Evaluation Summary

## 1. Experiment Setup

- **Baseline:** Prompt v1, evaluated three times on the original 10 fixed cases.
- **Changed variable:** Prompt only. Prompt v2 was used for Run 4.
- **Model:** GPT-5.6 Luna.
- **Mode:** GitHub Copilot Chat Ask.
- **Run 4 scope:** All 10 original cases plus two additional cases: case-11 (lifecycle regression) and case-12 (clean control).
- **Scoring approach:** Individual findings are evaluated against concrete expected defects. A case-level `caught` verdict does not automatically count as a true positive.

## 2. Case 03 Validity Caveat

The supplied `case-03.diff` targets a static `DiscountCalculator.Apply` method, but the current repository defines an instance method named `ApplyDiscount` with a different discount-rate convention.

The patch does not match the current repository baseline. Case 03 is retained in the raw results for transparency but excluded from the primary rounding-defect detection metric. An API-mismatch finding is not counted as detection of the intended rounding defect.

## 3. Preliminary Raw Results

Run 4 evaluated 12 cases:
- 10 cases produced findings.
- 2 cases reported no findings.
- Case 12, the clean control, was correctly reported as having no findings.

These are raw case-level results, not final defect-detection rates. Final metrics will be calculated at the individual-defect level after adjudicating true positives, false negatives, and false positives.

## 4. Metrics Definitions

- **True positive (TP):** An expected defect correctly identified by the review.
- **False negative (FN):** An expected defect missed by the review.
- **False positive (FP):** A reported finding that is unsupported, incorrect, or not a defect introduced by the diff.
- **Recall / caught-defect rate:** TP / (TP + FN).
- **Precision:** TP / (TP + FP).
- **False-alarm rate:** FP / (TP + FP), using the reported-defect denominator. This is the complement of precision when TP + FP is nonzero.

The raw verdicts in `results.csv` will be preserved. The final comparison will use defect-level adjudication and disclose the small sample size.

## 5. Expected-Defect Inventory and Adjudication

The unit of scoring is an individual defect introduced by a diff, not the number of findings or the case-level verdict.

| Case | Expected defect(s) to check | Adjudication note |
|---|---|---|
| case-01 | Undefined `CurrentUser`; null request IDs; incorrect handling of approval-service exceptions; partial batch approval; Admin authorization conflict, if supported by the authorization contract | Score each distinct, supported defect separately. |
| case-02 | Missing query-service dependency or registration; SQL injection through customer/status parameters | Check compile-time and security findings independently. |
| case-03 | Monetary calculation and rounding changes | Excluded from primary scoring because the diff targets a static `Apply` API, while the baseline defines instance `ApplyDiscount`. |
| case-04 | No expected defect; field and constructor-parameter rename | A speculative compatibility concern is a false positive unless an affected caller is demonstrated. |
| case-05 | Repository method mismatch (`Delete` versus `Remove`); undefined `_logger` and `CurrentUser`; authorization defect if supported by the existing authorization contract; incorrect not-found response if introduced by the diff | Count only defects actually introduced by this diff. |
| case-06 | Undefined `Pending(...)` helper calls in tests | Compile-time defect. |
| case-07 | Undefined `_logger` and `CurrentUser`; sensitive invoice data added to logs | Count compilation and logging defects separately. |
| case-08 | Replacing thread-safe `ConcurrentDictionary` with `Dictionary`; non-atomic duplicate detection | Treat related race symptoms as one root defect unless a distinct defect is demonstrated. |
| case-09 | No expected defect from the logging-level change, unless the diff itself introduces another concrete defect | Incorrect README reset instructions or demo-account documentation are pre-existing issues if unchanged by this diff; reporting them as introduced defects is a false positive. |
| case-10 | Catch-all exception handler returns HTTP 200 with a success-like response | Runtime/logic defect. |
| case-11 | Removing the Draft-status guard from `ApprovalService.Submit` | Lifecycle regression: non-draft invoices can be resubmitted. |
| case-12 | No expected defect; `string.Empty` replaced with `""` | Clean control. |

### Scoring rules

- **True positive (TP):** A specific expected defect is correctly identified and supported by the code or contract.
- **False negative (FN):** An expected defect is not identified.
- **False positive (FP):** A reported finding is incorrect, speculative, pre-existing, or not introduced by the diff.
- **Root-cause deduplication:** Multiple symptoms of the same underlying defect count once unless they represent independently actionable defects.
- **Invalid fixture:** Case 03 is excluded from the primary metrics and disclosed separately.

The raw `results.csv` remains unchanged. The adjudicated scores will be recorded separately so the original model outputs remain auditable.

## 6. Adjudicated Results and Comparison

Metrics are calculated from defect-level adjudication rows. TP = true positive, FN = false negative, FP = false positive, and TN = true negative. Case 03 is excluded because its diff is incompatible with the current baseline. Unverified authorization findings are not counted.

### Per-run results

| Run | TP | FN | FP | TN | Recall | Precision | False-alarm share | False-positive rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 11 | 2 | 2 | 1 | 84.6% | 84.6% | 15.4% | 66.7% |
| 2 | 11 | 2 | 1 | 1 | 84.6% | 91.7% | 8.3% | 50.0% |
| 3 | 13 | 0 | 2 | 0 | 100.0% | 86.7% | 13.3% | 100.0% |
| 4, all scored cases | 13 | 1 | 1 | 2 | 92.9% | 92.9% | 7.1% | 33.3% |

### Baseline versus revised prompt

The combined baseline for Runs 1–3 is TP = 35, FN = 4, FP = 5, TN = 2. Recall is 89.7%, precision is 87.5%, false-alarm share is 12.5%, and false-positive rate is 71.4%.

For a fair comparison, Run 4 must be restricted to the original comparable cases. Excluding the newly added Case 11 and Case 12 gives TP = 12, FN = 1, FP = 1, TN = 1. Recall is 92.3%, precision is 92.3%, false-alarm share is 7.7%, and false-positive rate is 50.0%.

Compared with the combined baseline, the comparable Run 4 results show a 2.6 percentage-point increase in recall, a 4.8 percentage-point increase in precision, a 4.8 percentage-point decrease in false-alarm share, and a 21.4 percentage-point decrease in false-positive rate.

### Interpretation and confidence

The revised prompt appears to improve the balance between defect detection and false alarms on this small evaluation set. Confidence in the size and generality of the improvement is low: the cases are few, defects within a case are not independent observations, and the evaluation is not a random sample of production changes. These results are evidence of a promising direction, not proof of a general improvement. Further runs on a larger, representative, fixed test set are needed.

The experiment changed the prompt while keeping the model and review mode fixed. Cases 11 and 12 are additional coverage tests and are reported separately from the original-set comparison.
