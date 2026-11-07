# Held-out batch 2 — results and priorities

November 7, 2026. 20 new cases, expectations frozen before running. Calendar availability is simulated; no real calendar or application records were changed. No recipe fixes were applied during this batch.

**13 complete plans. 17/20 expected-outcome matches.** All feasible outputs passed the independent schedule validator. These are code-based evaluations, not LLM-judge or real cooking validation.

| Case | Gathering | Expected | Actual | Assessment |
|---|---|---|---|---|
| heldout-01 | Winter supper for four | complete | complete | Matches expectation |
| heldout-02 | Vegetarian weekday dinner | complete | complete | Matches expectation |
| heldout-03 | Family Sunday roast | complete | complete | Matches expectation |
| heldout-04 | Goan birthday lunch | complete | complete | Matches expectation |
| heldout-05 | Vegetarian friends evening | complete | complete | Matches expectation |
| heldout-06 | Winter holiday buffet | complete | complete | Matches expectation |
| heldout-07 | Spring daylight-saving supper | complete | complete | Matches expectation |
| heldout-08 | Fall daylight-saving supper | complete | complete | Matches expectation |
| heldout-09 | Dinner with adult helper | complete | complete | Matches expectation |
| heldout-10 | Same dinner without helper | complete | complete | Matches expectation |
| heldout-11 | Dinner with thirty-minute helper | complete | unsupported | Real helper fallback defect |
| heldout-12 | Supervised helper weekend | complete | complete | Matches expectation |
| heldout-13 | No nuts listed holiday meal | complete | complete | Matches expectation |
| heldout-14 | Gluten-screened curry dinner | complete | needs_input | Recipe metadata gap; optimistic test assumption |
| heldout-15 | Potluck dessert contribution | complete | complete | Matches expectation |
| heldout-16 | Nut conflict in paneer meal | needs_input | needs_input | Matches expectation |
| heldout-17 | Gluten conflict in holiday starter | needs_input | needs_input | Matches expectation |
| heldout-18 | Vegetarian coverage missing | needs_input | needs_input | Matches expectation |
| heldout-19 | Zero prep allowance | no_fit_found | no_fit_found | Matches expectation |
| heldout-20 | Allergies not confirmed | needs_input | validation_failed | Wrong status for missing dietary confirmation |

## Fix first: optional helpers must not disable solo scheduling

Case 11 returns unsupported because the constraint-solver fallback rejects every configuration containing helpers. A controlled repeat removing only the 30-minute helper produces a complete plan. Implement a host-only fallback without changing the input preference or dropping the helper record; validate against original inputs. Then extend solver support for genuine helper allocation. Do not add time or change recipes for this case.

## Fix next: reconcile dietary-review metadata

Case 14 has reviewed recipe ingredients but null allergen metadata for butter chicken and chana masala. The app blocks rather than declaring them gluten-free; this is appropriate caution. Review ingredient lists, ambiguous packaged ingredients and declarations, then save explicit screening results in the app and Notion. Do not remove the user’s gluten restriction to get a passing result. A diagnostic removing the restriction proved that scheduling itself fits, but is not an acceptable dietary solution.

## Fix next: missing allergy confirmation should be needs_input

Case 20 enters solver validation with allergies unset and is labeled validation_failed. Move missing gathering-data checks before scheduling or classify the dietary violation as needs_input. A controlled test confirming no known allergies produces a complete plan.

## Expected blocked cases

- Case 16: known nut ingredients. Choose genuinely suitable recipes or reviewed substitutions; do not simply erase the restriction.
- Case 17: gluten-containing starter. Choose another starter or validate a suitable variation.
- Case 18: five vegetarian guests but no vegetarian main coverage. Add or swap a main that serves at least five vegetarians.
- Case 19: zero prep budget. Increase allowed prep time or use an appropriately specified prepared-food menu.

## Coverage limitations

- Cases 9, 11 and 12 include helpers, but successful plans assigned zero tasks to helpers. This does not establish useful helper delegation. The supervised helper only has fetch/measure capabilities, while these imported cooking tasks generally require cook capability.
- Cases 7 and 8 cross spring/fall daylight-saving dates and passed; they use daytime windows, not ambiguous 1–2 am transitions.
- One confirmed no-warming guest contribution passed. Warming/late arrivals remain separate coverage gaps.
- No calendar integration calls, Notion writes, model judge, real cooking tests, or UI clicks were performed in this batch.

## Inputs

Readable inputs: `docs/demo/20-heldout-gathering-test-inputs.md`. Frozen fixtures: `evals/heldout-gatherings-v1.json`. Results: `docs/reviews/2026-11-07-heldout-results.json`. Controlled diagnoses: `docs/reviews/2026-11-07-heldout-diagnostics.json`.
