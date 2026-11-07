# Simmer and Gather — 20 reproducible gathering inputs

Tested November 7, 2026. Use these as sample inputs; no gatherings or calendar events were created. Dates are the exact tested dates, in America/New_York. Changing dates requires a new run.

## Good starting points for a demo

- **03 — Small Indian supper:** 6 guests, 3 dishes, two prep days. Simplest complete example.
- **01 — Diwali family:** 15 guests including 5 vegetarians, 4 dishes, three prep days. Good example of advance cooking and chilled dessert.
- **09 — Thanksgiving classic:** 12 guests, turkey plus four dishes, three prep days at four hours/day.
- **12 — Thanksgiving bought turkey:** 12 guests, two prep days at four hours/day; shows buying the main while making sides and dessert.

These are complete scheduler results, not a claim that each full UI clickpath or cooking outcome has been tested.

## Shared settings

- Calendar: simulated completely free; no actual calendar reads or writes.
- Helpers: none. Standard saved home-kitchen equipment defaults; single-batch kitchen option enabled.
- Daily limits count required attendance, including supervision, plus the existing flexible cleanup allowance of up to 15 minutes beyond the daily limit. Passive cooking/cooling elapsed time can be longer than that attendance limit.
- Full buffer protected: finishing allowance is 0 minutes in these tests.
- No known allergies; no extra protected-time blocks or guest contributions.
- Every selected dish is set to the guest count in **recipe servings**, without an automatic buffet reduction. Do not interpret that as an independently validated shopping quantity recommendation.
- Menu category targets disabled (all set to 0) so the exact chosen menu is evaluated without requests for additional courses.
- Recipes use the reviewed corrections documented in the accompanying results file. No extra prep windows: default search is 9 am–9 pm on selected days, ending at the buffer on party day.

## Inputs and results

### 01 — Diwali family

- **Guests:** 15; vegetarian guests: 5.
- **Arrival:** 2026-11-15 at 18:00 Eastern.
- **Prep dates and daily limits:** 2026-11-13: 120 minutes; 2026-11-14: 120 minutes; 2026-11-15: 120 minutes.
- **Buffer:** 60 minutes; no tasks allowed in that buffer.
- **Menu:**
  - Instant Pot Butter Chicken — cook; 15 recipe servings.
  - Butter Paneer {Paneer Makhani} — cook; 15 recipe servings.
  - Vegetable Pulao Recipe | Veg Pulav — cook; 15 recipe servings.
  - Instant Pot Rice Pudding — cook; 15 recipe servings.
- **Result:** Complete; no input changes required.

### 02 — Diwali vegetarian

- **Guests:** 12; vegetarian guests: 12.
- **Arrival:** 2026-11-15 at 18:00 Eastern.
- **Prep dates and daily limits:** 2026-11-13: 120 minutes; 2026-11-14: 120 minutes; 2026-11-15: 120 minutes.
- **Buffer:** 60 minutes; no tasks allowed in that buffer.
- **Menu:**
  - Instant Pot Chana Masala (Punjabi Chole) — cook; 12 recipe servings.
  - Instant Pot Palak Paneer — cook; 12 recipe servings.
  - Vegetable Pulao Recipe | Veg Pulav — cook; 12 recipe servings.
  - Instant Pot Carrot Halwa Recipe — cook; 12 recipe servings.
- **Result:** Complete; no input changes required.

### 03 — Small Indian supper

- **Guests:** 6; vegetarian guests: 0.
- **Arrival:** 2026-11-15 at 18:00 Eastern.
- **Prep dates and daily limits:** 2026-11-14: 120 minutes; 2026-11-15: 120 minutes.
- **Buffer:** 60 minutes; no tasks allowed in that buffer.
- **Menu:**
  - Instant Pot Butter Chicken — cook; 6 recipe servings.
  - Vegetable Pulao Recipe | Veg Pulav — cook; 6 recipe servings.
  - Instant Pot Rice Pudding — cook; 6 recipe servings.
- **Result:** Complete; no input changes required.

### 04 — Paneer party

- **Guests:** 10; vegetarian guests: 10.
- **Arrival:** 2026-11-15 at 18:00 Eastern.
- **Prep dates and daily limits:** 2026-11-13: 120 minutes; 2026-11-14: 120 minutes; 2026-11-15: 120 minutes.
- **Buffer:** 60 minutes; no tasks allowed in that buffer.
- **Menu:**
  - Air Fryer Paneer Tikka — cook; 10 recipe servings.
  - Instant Pot Chana Masala (Punjabi Chole) — cook; 10 recipe servings.
  - Vegetable Pulao Recipe | Veg Pulav — cook; 10 recipe servings.
  - Instant Pot Rice Pudding — cook; 10 recipe servings.
- **Result:** Complete; no input changes required.

### 05 — Indian buffet

- **Guests:** 18; vegetarian guests: 5.
- **Arrival:** 2026-11-15 at 18:00 Eastern.
- **Prep dates and daily limits:** 2026-11-13: 180 minutes; 2026-11-14: 180 minutes; 2026-11-15: 180 minutes.
- **Buffer:** 60 minutes; no tasks allowed in that buffer.
- **Menu:**
  - Aloo Chaat in Phyllo Shells — cook; 18 recipe servings.
  - Instant Pot Butter Chicken — cook; 18 recipe servings.
  - Instant Pot Dal Makhani — cook; 18 recipe servings.
  - Vegetable Pulao Recipe | Veg Pulav — cook; 18 recipe servings.
  - Instant Pot Carrot Halwa Recipe — cook; 18 recipe servings.
- **Result:** Not complete: aloo chaat final assembly must finish within 45 minutes of serving, incompatible with a 60-minute buffer.

  **Tested alternative:** replace aloo chaat with Air Fryer Paneer Tikka, also 18 recipe servings. Keep all dates, 180-minute daily limits, and the 60-minute buffer. This separate alternative produced a complete plan.

### 06 — Curry night

- **Guests:** 8; vegetarian guests: 3.
- **Arrival:** 2026-11-15 at 18:00 Eastern.
- **Prep dates and daily limits:** 2026-11-14: 120 minutes; 2026-11-15: 120 minutes.
- **Buffer:** 60 minutes; no tasks allowed in that buffer.
- **Menu:**
  - Instant Pot Butter Chicken — cook; 8 recipe servings.
  - Butter Paneer {Paneer Makhani} — cook; 8 recipe servings.
  - Vegetable Pulao Recipe | Veg Pulav — cook; 8 recipe servings.
- **Result:** Complete; no input changes required.

### 07 — Vegetarian weekend

- **Guests:** 8; vegetarian guests: 8.
- **Arrival:** 2026-11-15 at 18:00 Eastern.
- **Prep dates and daily limits:** 2026-11-14: 120 minutes; 2026-11-15: 120 minutes.
- **Buffer:** 60 minutes; no tasks allowed in that buffer.
- **Menu:**
  - Instant Pot Chana Masala (Punjabi Chole) — cook; 8 recipe servings.
  - Butter Paneer {Paneer Makhani} — cook; 8 recipe servings.
  - Vegetable Pulao Recipe | Veg Pulav — cook; 8 recipe servings.
  - Instant Pot Rice Pudding — cook; 8 recipe servings.
- **Result:** Complete; no input changes required.

### 08 — Indian large family

- **Guests:** 20; vegetarian guests: 5.
- **Arrival:** 2026-11-15 at 18:00 Eastern.
- **Prep dates and daily limits:** 2026-11-13: 180 minutes; 2026-11-14: 180 minutes; 2026-11-15: 180 minutes.
- **Buffer:** 30 minutes; no tasks allowed in that buffer.
- **Menu:**
  - Tandoori chicken wings — cook; 20 recipe servings.
  - Instant Pot Butter Chicken — cook; 20 recipe servings.
  - Instant Pot Chana Masala (Punjabi Chole) — cook; 20 recipe servings.
  - Vegetable Pulao Recipe | Veg Pulav — cook; 20 recipe servings.
  - Instant Pot Carrot Halwa Recipe — cook; 20 recipe servings.
- **Result:** Complete; no input changes required.

### 09 — Thanksgiving classic

- **Guests:** 12; vegetarian guests: 0.
- **Arrival:** 2026-11-26 at 17:00 Eastern.
- **Prep dates and daily limits:** 2026-11-24: 240 minutes; 2026-11-25: 240 minutes; 2026-11-26: 240 minutes.
- **Buffer:** 30 minutes; no tasks allowed in that buffer.
- **Menu:**
  - Thanksgiving Turkey — cook; 12 recipe servings.
  - Garlic Mashed Potatoes Recipe — cook; 12 recipe servings.
  - Cornbread Stuffing Recipe — cook; 12 recipe servings.
  - Cranberry Orange Sauce — cook; 12 recipe servings.
  - Gluten Free Apple Crisp — cook; 12 recipe servings.
- **Result:** Complete; no input changes required.

### 10 — Thanksgiving small

- **Guests:** 8; vegetarian guests: 0.
- **Arrival:** 2026-11-26 at 17:00 Eastern.
- **Prep dates and daily limits:** 2026-11-24: 240 minutes; 2026-11-25: 240 minutes; 2026-11-26: 240 minutes.
- **Buffer:** 60 minutes; no tasks allowed in that buffer.
- **Menu:**
  - Thanksgiving Turkey — cook; 8 recipe servings.
  - Garlic Mashed Potatoes Recipe — cook; 8 recipe servings.
  - Cranberry Orange Sauce — cook; 8 recipe servings.
  - Gluten Free Apple Crisp — cook; 8 recipe servings.
- **Result:** Complete; no input changes required.

### 11 — Thanksgiving sides feast

- **Guests:** 15; vegetarian guests: 0.
- **Arrival:** 2026-11-26 at 17:00 Eastern.
- **Prep dates and daily limits:** 2026-11-24: 240 minutes; 2026-11-25: 240 minutes; 2026-11-26: 240 minutes.
- **Buffer:** 30 minutes; no tasks allowed in that buffer.
- **Menu:**
  - Thanksgiving Turkey — cook; 15 recipe servings.
  - Healthy Sweet Potato Casserole — cook; 15 recipe servings.
  - Healthy Green Bean Casserole — cook; 15 recipe servings.
  - Cranberry Orange Sauce — cook; 15 recipe servings.
  - Sweet Potato Pie — cook; 15 recipe servings.
- **Result:** Complete; no input changes required.

### 12 — Thanksgiving bought turkey

- **Guests:** 12; vegetarian guests: 0.
- **Arrival:** 2026-11-26 at 17:00 Eastern.
- **Prep dates and daily limits:** 2026-11-25: 240 minutes; 2026-11-26: 240 minutes.
- **Buffer:** 30 minutes; no tasks allowed in that buffer.
- **Menu:**
  - Thanksgiving Turkey — buy prepared; 12 recipe servings.
  - Garlic Mashed Potatoes Recipe — cook; 12 recipe servings.
  - Cornbread Stuffing Recipe — cook; 12 recipe servings.
  - Cranberry Orange Sauce — cook; 12 recipe servings.
  - Gluten Free Apple Crisp — cook; 12 recipe servings.
- **Result:** Complete; no input changes required.

### 13 — Autumn vegetarian

- **Guests:** 8; vegetarian guests: 0.
- **Arrival:** 2026-11-15 at 18:00 Eastern.
- **Prep dates and daily limits:** 2026-11-14: 180 minutes; 2026-11-15: 180 minutes.
- **Buffer:** 60 minutes; no tasks allowed in that buffer.
- **Menu:**
  - Healthy Green Bean Casserole — cook; 8 recipe servings.
  - Garlic Mashed Potatoes Recipe — cook; 8 recipe servings.
  - Caramelized Brussels Sprouts — cook; 8 recipe servings.
  - Gluten Free Apple Crisp — cook; 8 recipe servings.
- **Result:** Complete; no input changes required.

### 14 — Christmas Goan

- **Guests:** 15; vegetarian guests: 0.
- **Arrival:** 2026-12-25 at 18:00 Eastern.
- **Prep dates and daily limits:** 2026-12-22: 180 minutes; 2026-12-23: 180 minutes; 2026-12-24: 180 minutes; 2026-12-25: 180 minutes.
- **Buffer:** 30 minutes; no tasks allowed in that buffer.
- **Menu:**
  - Easy Tuna Croquettes — cook; 15 recipe servings.
  - Chicken Cafreal — cook; 15 recipe servings.
  - Goan Sannas (yeast method) — cook; 15 recipe servings.
  - Sonay Sukhe (Black Chana Sukka) — cook; 15 recipe servings.
  - The Best Doce — cook; 15 recipe servings.
- **Result:** Complete; no input changes required.

### 15 — Christmas mixed

- **Guests:** 12; vegetarian guests: 0.
- **Arrival:** 2026-12-25 at 18:00 Eastern.
- **Prep dates and daily limits:** 2026-12-23: 180 minutes; 2026-12-24: 180 minutes; 2026-12-25: 180 minutes.
- **Buffer:** 30 minutes; no tasks allowed in that buffer.
- **Menu:**
  - Mushroom Cutlets — cook; 12 recipe servings.
  - Pork Bafat | Dukra Maas — cook; 12 recipe servings.
  - Sonay Sukhe (Black Chana Sukka) — cook; 12 recipe servings.
  - Caramelized Brussels Sprouts — cook; 12 recipe servings.
  - The Best Doce — cook; 12 recipe servings.
- **Result:** Complete; no input changes required.

### 16 — Christmas curry

- **Guests:** 10; vegetarian guests: 0.
- **Arrival:** 2026-12-25 at 18:00 Eastern.
- **Prep dates and daily limits:** 2026-12-23: 180 minutes; 2026-12-24: 180 minutes; 2026-12-25: 180 minutes.
- **Buffer:** 60 minutes; no tasks allowed in that buffer.
- **Menu:**
  - Goan Pork Vindaloo — cook; 10 recipe servings.
  - Goan Sannas (yeast method) — cook; 10 recipe servings.
  - Sonay Sukhe (Black Chana Sukka) — cook; 10 recipe servings.
  - Coffee Fruit Cake — cook; 10 recipe servings.
- **Result:** Complete; no input changes required.

### 17 — Christmas roast and sides

- **Guests:** 12; vegetarian guests: 0.
- **Arrival:** 2026-12-25 at 18:00 Eastern.
- **Prep dates and daily limits:** 2026-12-23: 180 minutes; 2026-12-24: 180 minutes; 2026-12-25: 180 minutes.
- **Buffer:** 60 minutes; no tasks allowed in that buffer.
- **Menu:**
  - Tandoori chicken wings — cook; 12 recipe servings.
  - Garlic Mashed Potatoes Recipe — cook; 12 recipe servings.
  - Caramelized Brussels Sprouts — cook; 12 recipe servings.
  - Easy Christmas Fruit Cake Without Alcohol — cook; 12 recipe servings.
- **Result:** Complete; no input changes required.

### 18 — Holiday small table

- **Guests:** 6; vegetarian guests: 0.
- **Arrival:** 2026-12-25 at 18:00 Eastern.
- **Prep dates and daily limits:** 2026-12-24: 120 minutes; 2026-12-25: 120 minutes.
- **Buffer:** 60 minutes; no tasks allowed in that buffer.
- **Menu:**
  - Chicken Cafreal — cook; 6 recipe servings.
  - Goan Sannas (yeast method) — cook; 6 recipe servings.
  - Caramelized Brussels Sprouts — cook; 6 recipe servings.
  - Coffee Fruit Cake — cook; 6 recipe servings.
- **Result:** Complete; no input changes required.

### 19 — Birthday family buffet

- **Guests:** 10; vegetarian guests: 4.
- **Arrival:** 2026-11-15 at 18:00 Eastern.
- **Prep dates and daily limits:** 2026-11-13: 120 minutes; 2026-11-14: 120 minutes; 2026-11-15: 120 minutes.
- **Buffer:** 60 minutes; no tasks allowed in that buffer.
- **Menu:**
  - Chicken Mince Cutlets — cook; 10 recipe servings.
  - Butter Paneer {Paneer Makhani} — cook; 10 recipe servings.
  - Vegetable Pulao Recipe | Veg Pulav — cook; 10 recipe servings.
  - Instant Pot Rice Pudding — cook; 10 recipe servings.
- **Result:** Complete; no input changes required.

### 20 — Sunday friends

- **Guests:** 8; vegetarian guests: 0.
- **Arrival:** 2026-11-15 at 18:00 Eastern.
- **Prep dates and daily limits:** 2026-11-14: 180 minutes; 2026-11-15: 180 minutes.
- **Buffer:** 30 minutes; no tasks allowed in that buffer.
- **Menu:**
  - Easy Tuna Croquettes — cook; 8 recipe servings.
  - The Ultimate Goan Caldin Curry — cook; 8 recipe servings.
  - Vegetable Pulao Recipe | Veg Pulav — cook; 8 recipe servings.
  - The Best Doce — cook; 8 recipe servings.
- **Result:** Complete; no input changes required.

## Exact machine-readable fixtures

- Original library snapshot inputs: `evals/realistic-free-calendar.json`
- Same gathering inputs with corrected recipe records: `evals/realistic-free-calendar-corrected.json`
- Results including task assignments: `docs/reviews/2026-11-07-realistic-corrected.json`
- Tested starter alternative: `docs/reviews/2026-11-07-realistic-starter-alternative.json`

To rerun the corrected 20 cases: `uv run python scripts/evaluate_realistic_gatherings.py corrected`. This script does not call the Calendar API or write saved plans.
