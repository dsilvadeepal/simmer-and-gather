# Alternatives for three dietary-conflict cases

Read-only review of the live Notion recipe database on November 7, 2026: 42 pages, 37 reviewed app recipes matched by original-source URL. Candidate Notion page contents were read; scheduling used their reviewed app snapshots. This does not establish that all 42 pages are fully synchronized or planning-ready.

All tests retained the original guests, dates, three prep days, 180 minutes per day, free simulated calendar, buffers and 15-minute cleanup-overrun allowance. No app records, Notion pages, saved plans or calendars were changed. Full proposed inputs and schedule outputs are in `2026-11-07-alternative-menu-tests.json`.

| Conflict | Proposed changes | Result | Daily attention including cleanup |
|---|---|---|---|
| Nuts, 8 vegetarian guests, April 24, 6pm, 60-minute buffer | Palak paneer → chana masala; pulao → Brussels sprouts; rice pudding → doce. Eight portions each. | Complete | Apr 22: 115; Apr 23: 40; Apr 24: 65 minutes |
| Gluten, 8 guests, May 1, 6pm, 30-minute buffer | Brie en croûte → tandoori wings. Keep cafreal and garlic mashed potatoes, eight portions each. | Complete with test-only ingredient metadata review | Apr 29: 70; Apr 30: 0; May 1: 185 minutes |
| Vegetarian coverage, 10 guests including 5 vegetarian, May 8, 6pm, 60-minute buffer | Wings → butter paneer for five. Keep butter chicken and Brussels sprouts at their original ten portions. | Complete | May 6: 75; May 7: 35; May 8: 85 minutes |
| Same vegetarian case, alternative | Wings → chana masala for five; rest unchanged. | Complete | May 6: 75; May 7: 40; May 8: 75 minutes |

The nut case requires all three swaps: the saved palak paneer, pulao and rice pudding all declare nuts. This alternative is less traditional than a curry-and-rice menu. A reviewed plain-rice recipe would preserve that role better, but was not invented or imported for this test. Doce contains coconut and ghee; this test's `nuts` family means peanuts/tree nuts and does not cover a separate coconut allergy.

The gluten case initially remained needs_input because wings and mashed potatoes have null allergen metadata. Their saved ingredient lists matched the original source lists checked in this review. Temporary test copies record milk and retain label/cross-contact reminders; no gluten ingredient was detected. These corrections have NOT been saved to Notion or the app. It needs 170 minutes cooking attention plus 15 cleanup on party day, so five cleanup minutes use the existing overrun allowance. No prep limit or buffer was increased.

A second gluten option replacing mashed potatoes with Brussels sprouts also completes, but requires 190 minutes including cleanup on party day (175 cooking plus 15 cleanup). It is not an improvement, so it is not recommended over the potato option.

All five complete candidates passed the independent schedule validator and finished by their original buffer deadline. The sixth run is the unchanged-metadata gluten control and correctly remains needs_input. Times describe host attention/presence, not total elapsed cooking and waiting.

## What this shows

The collection has workable alternatives for these cases. The remaining product gap is discovering and proposing these swaps automatically, screening the entire resulting menu, and rechecking scheduling before approval. Missing metadata can still hide suitable candidates. Vegetarian coverage needed an actual vegetarian main, not more meat or side portions. These tests retain generous original meat quantities; portion optimization is separate.

Ingredient screening is not allergen-free certification. Check purchased product labels and cross-contact. Source checks: https://ministryofcurry.com/tandoori-chicken-wings/ and https://www.wellplated.com/garlic-mashed-potatoes/ .
