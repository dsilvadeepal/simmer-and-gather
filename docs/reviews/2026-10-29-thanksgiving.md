# Thanksgiving recipe review

Separate test gathering: `2157897c-206e-491c-80bd-8ac654cd09df`. Provisional November 26, 2026 at 6 pm, 15 guests, November 23–26 prep, 120 minutes per day, 60-minute buffer, Personal calendar only. No calendar writes.

Six source-checked recipes: turkey, garlic mashed potatoes, cornbread stuffing, cranberry orange sauce, green bean casserole, chocolate pecan pie. Source URLs and proposed task guidance are retained in `scripts/thanksgiving_recipe_refinements.py`.

Changes: separate passive brining/chilling from work; explicit source-supported advance windows; add missing potato/stuffing reheating; use task-specific guidance rather than repeated recipe-wide notes. Timing and attention placement remain estimates. Turkey assumes a fully thawed bird at the start and allows four hours roasting for the larger gathering; this is not a weight-independent promise. Diet settings are provisional, not confirmed guest requirements.

Scheduler now excludes necessarily invalid candidate starts before running full validation (same-day policy, dependencies, serving-based storage bounds and eligible windows). Full validation remains authoritative. Backend suite: 93 tests passed.

Outstanding: inspect generated schedule, confirm calendar fit and distinguish elapsed oven time from hands-on work. Do not mark this complete solely because recipe review flags are set. No Notion publication performed in this pass.

First generated candidate: 32 assignments, missing the final casserole step. Manual review caught early reheating and an overnight gap before baking filled pie. Test selection refinements now constrain reheating/finishing to 3–5 pm and combine pie filling with baking; these gathering-specific constraints are not generic library dates. Preserve these checks in future evaluations. Do not use the earlier +30-minute suggestion as proof for the refined plan.

Final saved candidate remains incomplete: 28 assignments; missing pie baking/cooling and casserole finish. In-memory alternative with bought pie plus 150 minutes on November 26 passed schedule validation against fresh Personal calendar availability. Bought pie alone remains incomplete. Neither alternative has been applied. This is modeled feasibility, not measured cooking performance; turkey weight/thawed state and unattended-versus-supervised oven assumptions remain important review points.
