# Goan Christmas recipe and schedule review

User-approved test: December 25, 2026 at 6 pm; 15 people; prep December 22–25; 120 minutes daily, 180 on Christmas Day; 30-minute buffer; avoid nuts. Personal calendar read only. No calendar events created.

Menu: pork vindaloo, chicken cafreal, fish caldin, yeast sannas, doce and fruit cake adapted without almonds/walnuts. Coconut remains. Ingredient review does not establish packaged-product cross-contact safety; use non-nut oil and check labels. Vegetarian guest count is not confirmed; this is not a vegetarian-balanced menu.

## Refinements

- Task-specific directions replace repeated source commentary.
- Whole cooking phases stay together when separating them would permit a long gap mid-method.
- Sannas use the complete Xantilicious yeast recipe, including ingredients, rather than mixing yeast with the incomplete toddy-based source. Source yield 18–20 pieces; serving basis is an estimate of two pieces.
- Soaking, fermenting and cooling are separate dependencies displayed as notes. Completion depends on actual texture/doneness, not only clock time.
- Caldin is cooked on the day. Vindaloo is cooked ahead and reheated. Sannas are chilled after steaming and re-steamed before serving. Hot-holding instructions accompany food finished before arrival.
- Fruit-cake almonds and walnuts are omitted only in the gathering snapshot; source recipe remains available. No claim of certified allergen-free food.
- The exact six gathering snapshots are in `christmas-reviewed-recipes.json`; they include test-specific eligible windows. `scripts/christmas_recipe_refinements.py` holds reusable initial proposals. Do not overwrite final snapshots by reapplying the initial proposals.

## Result and limits

30 assignments, including waits and cleanup; independent schedule validation and menu validation report no violations. Personal-calendar availability fetched live. All work ends December 25 at 5:25 pm.

| Date | Counted work and cleanup | Daily limit |
| --- | --- | --- |
| Dec 22 | 80 min | 120 min |
| Dec 23 | 115 min | 120 min |
| Dec 24 | 125 min | 120 min + flexible cleanup |
| Dec 25 | 175 min | 180 min |

These are modeled hands-on/presence totals, not elapsed span. Baking and simmering require being nearby for check-ins; the cake block is 3.5 hours elapsed. Check-in placement and cooking times are estimates. The solver checks scheduled presence against the calendar, not every minute of passive baking. Daily limits should not be represented as a promise that the host can leave during those blocks.

No actual cooking or package-label verification performed. The demo retains the user-approved single-batch kitchen assumption; this is not proof that a specific pot or steamer accommodates scaled quantities. Serving and ingredient quantities still need host review.

## UI verification

The Christmas gathering opens directly in Schedule with all four dates and task groups. Fixed recipe-note lookup to use menu-selection IDs, restoring source links and storage notes. Browser verification confirmed 5:30 pm deadline, 30-minute buffer, cleanup overrun, and all six recipe task groups. Frontend build and tests run after the lookup fix.

Sources: https://aromaticessence.co/chicken-cafreal/ ; https://theaspiringhomecook.com/2019/10/goan-pork-vindaloo.html ; https://withwendyandshannon.com/blog/the-ultimate-goan-caldin-curry/ ; https://xantilicious.com/recipe/sanna/ ; https://withwendyandshannon.com/blog/the-best-doce/ ; https://www.ruchikrandhap.com/christmas-fruit-cake-without-alcohol/ ; https://www.fda.gov/food/buy-store-serve-safe-food/serving-safe-buffets

## Time-label clarification

The day now labels 175 minutes as hands-on work, supervision and cleanup, and separately displays 4 hours across Christmas Day's cooking blocks. The 65-minute difference is cooking/waiting within those blocks; the 3-hour batter fermentation between blocks remains a separate wait note. Each block shows elapsed duration, and mixed active/passive tasks show hands-on versus cooking/waiting time. No recipe timings, plan assignments or calendar events changed in this UI pass. Frontend: 21 tests passed; production build passed.
