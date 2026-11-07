# Second batch: controlled correction rerun

Same 20 gatherings, menus, guest counts, helper availability, dietary requirements, prep limits, buffers and free simulated calendar. Original fixtures/results retained. No calendar API calls or saved-plan edits.

## Results

| Measure | Before | After |
|---|---:|---:|
| Complete plans | 13 | 15 |
| Expected outcome matches | 17/20 | 20/20 |
| Complete plans passing independent schedule checks | 13/13 | 15/15 |

- **11: short helper** — now complete. Optional helper availability no longer disables the host-only constraint fallback. Original helper preferences remain intact and the result is validated against original inputs. This fix does not claim improved delegation; the fallback assigns work to the host.
- **14: gluten-screened curries** — now complete. Butter chicken and chana masala reviewed against their original Ministry of Curry ingredient lists. Explicit milk flag retained for ghee. No gluten or nuts detected in these curry lists; packaged-product labels and cross-contact remain checks before serving. These are ingredient screening results, not allergen-free certification. Saved in the app and existing Notion pages, read back verified.
- **20: unconfirmed allergies** — now needs input, before scheduling, with a direct request to confirm allergies or select none. No misleading solver-failure message.

Expected blocks unchanged: 16 nut conflict, 17 gluten conflict, 18 vegetarian coverage, 19 zero prep budget, 20 missing allergy confirmation. Passing an evaluation means producing the correct outcome, including these blocks.

## Evidence and repeatability

- Frozen original: `evals/heldout-gatherings-v1.json`
- Corrected recipe snapshots: `evals/heldout-gatherings-corrected.json`
- Results: `docs/reviews/2026-11-07-heldout-corrected-results.json`
- Re-run: `uv run python scripts/evaluate_heldout_gatherings.py --corrected`
- LangSmith: `uv run python scripts/run_langsmith_heldout.py --corrected`
- Recipe sync: `scripts/apply_heldout_recipe_corrections.py`; verifies non-recipe records unchanged.

Source checks: https://ministryofcurry.com/instant-pot-butter-chicken/ and https://ministryofcurry.com/instant-pot-chana-masala-recipe/ . Recipe changes are metadata-only; tasks, quantities and timing remain unchanged. Evaluation expectations remain unchanged. Code-based evaluation, not an LLM judge or real cooking trial.
