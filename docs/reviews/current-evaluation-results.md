# Current evaluation evidence

Updated November 7, 2026. Latest recorded result per distinct suite only. These are recorded runs, not a new rerun caused by this documentation update. Test fixtures remain reproducible; superseded result reports are removed from the working tree.

| Suite | Latest result | Scope |
| --- | --- | --- |
| Realistic gatherings | 19/20 original menus complete; a separately tested starter swap completes the remaining scenario | Free synthetic calendar; original limits preserved. Alternative result is not the baseline score. |
| Corrected second batch | 15 complete; 20/20 expected outcomes matched; all 15 complete schedules validate | Varied guests, helpers and dietary constraints. Expected blocks remain blocks. |
| Randomized UX batch | 14 complete, 3 needs_input, 3 no_fit_found; all complete schedules validate | Actual PlanningService/LangGraph with isolated owner and simulated free calendar. 18/20 original desired labels matched; random-menu feasibility labels are hypotheses. |
| Randomized recovery options | Separate bought-turkey and dietary/vegetarian swaps can complete four blocked cases | Preview results, not applied user-menu changes. Zero prep budget and unconfirmed allergies require a decision. |

Latest randomized experiment: https://smith.langchain.com/o/8ea48a8e-b636-497e-a9eb-ecd377951afe/datasets/1f7f374d-2553-4f71-bf5c-a821dff6b0ab/compare?selectedSessions=c11e89ee-b866-4639-93a0-34f2128cb82b

## Correctness versus completion
A pass means the expected valid outcome, not necessarily a complete plan. Unknown allergies, known dietary conflicts and zero prep budgets must not silently become feasible. Code checks cover independent validation and expected outcomes. No LLM judge or paid inference quality claim.

## Current artifacts
- `2026-11-07-random-ux-results.json` and `2026-11-07-random-ux-run.json`: latest randomized results and experiment metadata.
- `2026-11-07-random-ux-turkey-option.json`: separately checked bought-food option.
- `2026-11-07-heldout-corrected-results.json`: latest corrected second batch.
- `2026-11-07-realistic-after.json`: latest original-menu realistic batch; starter alternative is separate.
- `2026-11-07-architecture-evals-after.json`: latest controlled architecture regression output.
- `../demo/20-random-ux-test-inputs.md`, `../demo/20-heldout-gathering-test-inputs.md`, `../demo/20-gathering-test-inputs.md`: reproducible inputs.

## UX and release limits
All 20 randomized outcomes were exercised in a React DOM interaction harness. Read-only previews, explicit allergy recovery, inline contributions and atomic bought/swap acceptance have regression coverage. Latest isolated desktop/phone screenshots and captioned walkthrough verify one sample presentation path; they do not establish comprehensive browser coverage.

No actual-calendar writes in these evaluations. No physical cooking validation, exhaustive solver proof, live model ranking benchmark, hosted cost acceptance or production reliability claim. Recipe product-label and cross-contact checks remain distinct from ingredient screening.

## Documentation refresh verification
54 frontend tests, two targeted telemetry tests and the production frontend build passed. All five relocated regression fixtures validated against current input/plan schemas. Local Markdown links and whitespace checks passed. This documentation change did not rerun the full backend suite or live-provider experiments.
