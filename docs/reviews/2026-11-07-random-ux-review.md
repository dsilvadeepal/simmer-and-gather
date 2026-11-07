# Randomized planning and UX review

## Execution

20 scenarios frozen with seed 20261107 before execution. Guest counts 6–16 in this sample; 2–4 prep days, 0/120/180/240 daily minutes, 30/60-minute buffers, three helper configurations, nut/gluten restrictions and missing allergy confirmation. Menus sample Indian, Goan and holiday recipes. Real PlanningService/LangGraph generation, under an isolated synthetic owner; free simulated calendar. Original owner record fingerprint unchanged. No calendar integration calls.

LangSmith experiment: https://smith.langchain.com/o/8ea48a8e-b636-497e-a9eb-ecd377951afe/datasets/03872156-e2fe-407c-89a1-5b22116791a0/compare?selectedSessions=cce534e7-3634-4b47-8420-722c2986dd70

14 complete; 3 needs_input; 3 no_fit_found. All 14 complete plans pass independent schedule validation. 18/20 match the frozen desired-outcome labels, but these labels are hypotheses: a random menu is not guaranteed feasible. Code-based evaluators, not LLM-as-judge. No model ranking/provider reliability or real cooking validation established.

## Interpreting six incomplete cases

| Case | Result | Interpretation / next action |
|---|---|---|
| 03 | No fit | Whole turkey's 36-hour dry brine plus preparation/roasting does not fit the two-day windows. Existing buy-prepared suggestion is correct; controlled bought-turkey rerun completes. Do not shorten source steps to force a pass. |
| 16 | Needs input | Intended nut conflict. Search returns three complete replacement menus. |
| 17 | Needs input | Intended gluten conflict. Search returns two complete replacement menus. |
| 18 | No fit | Both a vegetarian-main shortage and timing conflict. Three vegetarian-main replacements complete under unchanged limits. Outcome label is not wrong, but should foreground the actionable combined remedy. |
| 19 | No fit | Deliberate zero-prep-budget case; expected block. |
| 20 | Needs input | Deliberately unconfirmed allergies; expected block. |

Separate proposed changes can therefore yield 18 complete menus; this is NOT the baseline completion score and no swaps were applied to the user's plans. Cases 19/20 still require a user decision.

## UI verification and limitations

All 20 outputs rendered through the actual React App in a component interaction harness. Each navigated from menu through Build my prep plan to the resulting plan and shopping view; no automatic approval/write occurred. A 21st diagnostic reproduced the preview checklist persistence problem below. These are DOM interaction checks, not visual/responsive checks.

Attempted full desktop 1440px and phone 390px Playwright runs did not complete. Chrome reported remote debugging disallowed by system policy and closed; one locator also encountered hidden nested preview content. One missing-allergy state was captured at both widths and visually reviewed; the remaining visual runs did not complete. No claim of full desktop/mobile acceptance or all-browser-popup coverage. Production code and styles were not changed in this review.

## Prioritized UX recommendations

1. **P1 — Make alternative previews read-only.** Each embeds full PlanViews, including shopping controls keyed to the same gathering ID. Diagnostic confirmed checking an ingredient in an unapproved alternative writes that gathering's localStorage checklist. Use a compact read-only schedule preview, or isolated draft state. It does not edit server plans/calendar, but violates user expectations that a preview changes nothing.
2. **P1 — Group failures by cause, with one next action.** Turkey produces five task failures after one brining constraint. Show “This turkey needs an earlier start” once, with “Buy prepared” and an estimated supported earlier-start option if independently checked. Collapse dependent task details. Case 18 should say “Replace a meat dish with a vegetarian main to cover 3 guests and fit the schedule,” rather than leading with a generic no-fit warning.
3. **P2 — Unify bought-food acceptance with checked swaps.** Bought-prepared fallback still updates the menu and asks for regeneration, while recipe alternatives now carry a checked plan forward. Both should use one “Use this option and plan” flow with fresh validation and atomic saving.
4. **P2 — One recommended option, then More options.** Up to three alternative cards each include a full four-tab plan workspace, boilerplate and action button. Show changed dishes, portions, time impact and one preview action; keep the original schedule clearly distinct. Do not repeat unchanged dishes as arrows.
5. **P2 — Replace guest-contribution prompt chains.** Source review confirms three native prompts for name, servings and warming. A single inline form or sheet is easier to inspect, correct and cancel. This path was not covered by these 20 generated-plan interaction tests.
6. **P2 — Simplify blocked empty states.** The captured missing-allergy screen still shows regenerate/check buttons, four plan tabs, time summary and save/calendar options despite having no schedule. Replace those with the single next action, “Confirm allergies,” linking to the field; show plan controls when a plan exists. Sticky navigation overlaps text in the full-page captures; verify in a real viewport because scroll/full-page capture can affect sticky placement.
7. **P3 — Reduce shopping taxonomy and repeated caveats.** Keep grocery categories and the have-at-home checkboxes. Place ranges beside ingredients instead of a separate Recipe ranges group. Keep genuinely missing amounts visible. Consolidate label-check reminders per menu, preserving recipe-specific exceptions.

The one-action build and explicit swap approval passed all 20 interaction cases and should remain. Keep the current colors. Next work should prioritize preview isolation and actionable conflict explanations before cosmetic changes.

## Artifacts

- `docs/demo/20-random-ux-test-inputs.md`
- `evals/random-ux-2026-11-07.json`
- `docs/reviews/2026-11-07-random-ux-results.json`
- `docs/reviews/2026-11-07-random-ux-turkey-option.json`
- `scripts/evaluate_random_ux_batch.py`
- `frontend/src/RandomGatheringAudit.test.tsx`
