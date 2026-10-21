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

### Scoring scope

The primary comparison uses the original nine comparable cases (case-01, case-02, and case-04 through case-10). Case-03 is excluded because its diff targets an API that does not match the current baseline. Cases 11 and 12 were added only for Run 4 and are reported separately. Unverified authorization findings are excluded from the metrics.

### Results

| Metric | Baseline (Runs 1–3 combined) | Run 4 (prompt v2) |
|---|---:|---:|
| True positives (TP) | 35 | 12 |
| False negatives (FN) | 4 | 1 |
| False positives (FP) | 5 | 1 |
| True negatives (TN) | 2 | 1 |
| Recall / catch rate | 89.7% | 92.3% |
| Precision | 87.5% | 92.3% |
| False-alarm share of reported findings | 12.5% | 7.7% |

Definitions:
- Recall = TP / (TP + FN)
- Precision = TP / (TP + FP)
- False-alarm share = FP / (TP + FP)

### Interpretation and limitations

On the comparable cases, prompt v2 improved observed recall by 2.6 percentage points, precision by 4.8 percentage points, and reduced the false-alarm share by 4.8 percentage points.

These results are preliminary, not proof of a general improvement. The baseline has three repeated runs, while prompt v2 has one run on the comparable cases. The evaluation set is small, defects vary in difficulty, and some findings required adjudication. The classical false-positive rate is unstable because there are very few clean cases.

Only the prompt changed; the model and Ask mode remained the same. Case 11 was correctly caught, and Case 12 was correctly classified as clean, but these added cases are not included in the baseline comparison.

The adjudication CSV is the scoring audit trail. Revisit the results if further source inspection changes an expected-defect classification.
