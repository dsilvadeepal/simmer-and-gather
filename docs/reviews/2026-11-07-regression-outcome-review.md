# Review of the 20 LangSmith scheduler cases

November 7, 2026. Same historical menus, time limits, allergy settings and simulated calendars. No live calendar or saved plan writes.

## Why only six were complete

Ten cases intentionally prevent completion: five block all prep days and five inject a nonexistent dependency. Of the remaining ten, four Christmas cases had feasible schedules but were blocked by blanket allergy-unknown warnings. Two busy-calendar Christmas cases were also mislabeled as needing menu input because menu validation overwrote the scheduling failure.

## Changes

- Reviewed, populated ingredient lists without a detected requested allergen produce visible ingredient-label and cross-contact reminders. This is not allergen-free certification. Known ingredients/declarations, missing or unreviewed lists, bought dishes and unsupported allergy types still block as appropriate.
- Menu validation preserves existing scheduling failures and solver diagnostics while retaining menu violations.
- Generation, approval and Notion export use the same blocker classification. No approval or export was performed.
- Expected-outcome evaluation requires complete normal cases, no-fit busy cases, and needs-input broken-dependency cases. The old checks could pass an app that simply refused every plan.

## Case-by-case result

| Menu | Condition | Before | After | Assessment |
|---|---|---|---|---|
| Indian supper | baseline | complete | complete | Already complete; unchanged. |
| Indian supper | more_time | complete | complete | Already complete; unchanged. |
| Indian supper | busy_calendar | no_fit_found | no_fit_found | Expected no fit: every prep day deliberately blocked. |
| Indian supper | missing_dependency | needs_input | needs_input | Expected rejection: prerequisite deliberately removed. |
| Indian vegetarian | baseline | complete | complete | Already complete; unchanged. |
| Indian vegetarian | more_time | complete | complete | Already complete; unchanged. |
| Indian vegetarian | busy_calendar | no_fit_found | no_fit_found | Expected no fit: every prep day deliberately blocked. |
| Indian vegetarian | missing_dependency | needs_input | needs_input | Expected rejection: prerequisite deliberately removed. |
| Thanksgiving | baseline | complete | complete | Already complete; unchanged. |
| Thanksgiving | more_time | complete | complete | Already complete; unchanged. |
| Thanksgiving | busy_calendar | no_fit_found | no_fit_found | Expected no fit: every prep day deliberately blocked. |
| Thanksgiving | missing_dependency | needs_input | needs_input | Expected rejection: prerequisite deliberately removed. |
| Goan Christmas | baseline | needs_input | complete | Fixed blanket allergy blocker; original schedule fits. |
| Goan Christmas | more_time | needs_input | complete | Fixed blanket allergy blocker; original schedule fits. |
| Goan Christmas | busy_calendar | needs_input | no_fit_found | Expected no fit: every prep day deliberately blocked. Fixed misleading outcome. |
| Goan Christmas | missing_dependency | needs_input | needs_input | Expected rejection: prerequisite deliberately removed. |
| Christmas mixed table | baseline | needs_input | complete | Fixed blanket allergy blocker; original schedule fits. |
| Christmas mixed table | more_time | needs_input | complete | Fixed blanket allergy blocker; original schedule fits. |
| Christmas mixed table | busy_calendar | needs_input | no_fit_found | Expected no fit: every prep day deliberately blocked. Fixed misleading outcome. |
| Christmas mixed table | missing_dependency | needs_input | needs_input | Expected rejection: prerequisite deliberately removed. |

Result: 10/10 normal or expanded-time cases complete; 5/5 busy-calendar cases reject; 5/5 broken-dependency cases require input. All 20 match their expected outcome.

These are scheduler regression tests on historical fixtures, not evidence that every current-library recipe or live integration is correct. Ingredient screening cannot establish product-label or cross-contact safety. FDA reference: https://www.fda.gov/consumers/consumer-updates/have-food-allergies-read-label
