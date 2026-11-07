# Current evaluation evidence

Updated November 7, 2026. Latest recorded result per distinct suite only. These are recorded runs, not a new rerun caused by this documentation update. Test fixtures remain reproducible; superseded result reports are removed from the working tree.

| Suite | Latest result | Scope |
| --- | --- | --- |
| Realistic gatherings | 19/20 original menus complete; a separately tested starter swap completes the remaining scenario | Free synthetic calendar; original limits preserved. Alternative result is not the baseline score. |
| Corrected second batch | 15 complete; 20/20 expected outcomes matched; all 15 complete schedules validate | Varied guests, helpers and dietary constraints. Expected blocks remain blocks. |
| Randomized UX batch | 14 complete, 3 needs_input, 3 no_fit_found; all complete schedules validate | Actual PlanningService/LangGraph with isolated owner and simulated free calendar. 18/20 original desired labels matched; random-menu feasibility labels are hypotheses. |
| Randomized recovery options | Separate bought-turkey and dietary/vegetarian swaps can complete four blocked cases | Preview results, not applied user-menu changes. Zero prep budget and unconfirmed allergies require a decision. |

Latest randomized experiment: https://smith.langchain.com/o/8ea48a8e-b636-497e-a9eb-ecd377951afe/datasets/1f7f374d-2553-4f71-bf5c-a821dff6b0ab/compare?selectedSessions=c11e89ee-b866-4639-93a0-34f2128cb82b

## Final traced randomized batch

20 fresh scenarios (seed 20261108), generated and run November 7, 2026 against the current merge-fix working tree. Guest counts 4–16; 2–4 prep days; 0/90/120/180/240 minute allowances; 30/60 minute buffers; varied helpers and dietary needs. Three cases include simulated midday calendar conflicts. All writes used a dedicated test database; the real owner's before/after fingerprint was unchanged.

**20/20 expected outcomes matched.** Fifteen complete schedules passed independent validation. Four correctly need input (nut conflict, gluten conflict, vegetarian coverage, unconfirmed allergies); one correctly has no fit with zero prep budget. Checked alternatives were returned for the nut, gluten and vegetarian cases (3, 2 and 3 options). No changes were approved on the user's behalf.

LangSmith readback verified **20 experiment runs and 60 application trace records**: 20 hosting-plan parents, 20 build_prep_schedule stages and 20 validate_hosting_plan stages. Individual reads were rate-limited; a batch query verified every recorded trace ID. Traces contain allowlisted summaries, not raw calendar or recipe payloads. Evaluation is code-based, not LLM-as-judge.

[Open final traced experiment](https://smith.langchain.com/o/8ea48a8e-b636-497e-a9eb-ecd377951afe/datasets/0508a433-17bf-4fe3-b2b7-b8d822cc9111/compare?selectedSessions=c860c3b5-ebc3-4402-8fd2-a9964995d359).

Inputs: [20 reproducible cases](../demo/20-final-traced-test-inputs.md). Frozen JSON: `evals/final-traced-2026-11-07.json`. Detailed results/readback: `2026-11-07-final-traced-results.json` and `2026-11-07-final-traced-run.json`. Runner: `scripts/evaluate_final_traced_batch.py`.

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

## Final merge checks — November 7, 2026

- 171 backend tests passed against a dedicated test database.
- 54 frontend tests and the production build passed.
- 25/25 fixture evaluations passed.
- All 20 randomized scenarios passed at 1440px and 390px (40 browser case checks); no unexpected dialogs, JavaScript errors or page-width overflow. The separate desktop/phone architecture audit also passed. API responses were mocked throughout browser runs.
- Regression coverage verifies overlapping hosting reservations, retry exclusions, stale unchanged dishes, stale bought-food previews/acceptance, and a recipe change between scheduling and final commit.
- Independent code review found no remaining merge blockers in these fixes. Nonblocking follow-up: a stale recipe may still be offered in a swap preview; acceptance correctly rejects it.

These are local results for the merge-fix working tree. Remote CI must run on its eventual commit; earlier green CI does not cover uncommitted changes. No saved user records or actual calendar events were modified. Production deployment and controlled real-calendar booking acceptance remain separate release gates.
