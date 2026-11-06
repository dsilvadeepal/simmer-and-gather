# Five-menu rerun: make-ahead work and logical task sequences

All five menus now have complete schedules under the original test limits. No bought dishes or extra cooking time were introduced. The tests remain separate from saved plans and use simulated availability, not a live calendar check.

**Settings unchanged:** 15 people, including five vegetarians; prep December 22–25; 120 minutes daily and 180 minutes on serving day; 6 pm arrival; 30-minute buffer; no helpers. The existing 15-minute flexible cleanup allowance remains available.

## Before and after

| Test | Before | Now | Main correction |
|---|---|---|---|
| Indian supper | Incomplete | Complete | Cook butter chicken and halwa ahead; prepare chaat filling and pulao vegetables separately from fresh finishing. |
| Indian vegetarian | Incomplete | Complete | Prepare spinach sauce ahead; separate salad tempering from tossing; reserve paneer cooking near serving. |
| Thanksgiving | Incomplete | Complete | Keep potatoes boiling-to-mashing together; explicitly cool and pack cornbread; coordinate the shared oven. |
| Goan Christmas | Incomplete | Complete | Start soaking immediately after setup; drain and refrigerate rice before later grinding; preserve fermentation and steaming order. |
| Christmas mixed table | Incomplete | Complete | Keep cutlet filling, cooling and shaping connected; cook chana and pork ahead with reheating included. |

## What changed

- Updated 18 library recipes. Verified source-supported windows were restored; conservative culinary estimates remain identified separately.
- Added maximum gaps between steps that must continue promptly, and a minimum storage interval for the selected cook-ahead/reheat path. These prevent overnight pauses after cooking and pointless immediate cooling/reheating.
- Replaced the unsuccessful backward-only trial with a bounded OR-Tools constraint-search fallback. It considers whole task chains together, then passes the result through the independent existing validator. No model/API spending is required.
- A solver timeout or failure to find a candidate is not proof that more host time is necessary. Unsupported helper/finishing configurations continue through the existing scheduling path.
- Corrected ingredient-based vegetarian/allergen metadata for selected recipes. Package labels and cross-contact are still outside this ingredient review.

**Thanksgiving draft adaptation:** white beans replace sausage and vegetable broth replaces chicken broth in the stuffing. It is treated as the substantial vegetarian option, with portions reserved for five vegetarian guests. This is a test-only culinary variation; the original library stuffing and saved Thanksgiving plan are unchanged.

## Time comparison

| Menu | Dec 22 | Dec 23 | Dec 24 | Dec 25 |
|---|---:|---:|---:|---:|
| Indian supper | 0 + 0 cleanup | 115 + 15 cleanup | 110 + 15 cleanup | 125 + 15 cleanup |
| Indian vegetarian | 0 + 0 cleanup | 115 + 15 cleanup | 60 + 15 cleanup | 95 + 15 cleanup |
| Thanksgiving | 20 + 15 cleanup | 105 + 15 cleanup | 115 + 15 cleanup | 105 + 15 cleanup |
| Goan Christmas | 0 + 0 cleanup | 105 + 15 cleanup | 100 + 15 cleanup | 135 + 15 cleanup |
| Christmas mixed table | 0 + 0 cleanup | 100 + 15 cleanup | 115 + 15 cleanup | 140 + 15 cleanup |

Numbers are hands-on work/supervision plus cleanup, in minutes. Elapsed oven, pressure-cooking, soaking and fermentation time can be longer. Some days use part of the approved cleanup overrun; cooking remains within the unchanged daily limits.

## Indian supper

**Menu:** Aloo Chaat in Phyllo Shells; Instant Pot Butter Chicken; Instant Pot Palak Paneer; Vegetable Pulao Recipe | Veg Pulav; Instant Pot Carrot Halwa Recipe.

| Day | Prep block | Tasks |
|---|---|---|
| Dec 23 | 05:40 PM–08:00 PM | Instant Pot Butter Chicken · Cut chicken and chop aromatics; Instant Pot Butter Chicken · Sauté aromatics; add tomato and chicken; Instant Pot Butter Chicken · Pressure-cook and release safely; Instant Pot Carrot Halwa Recipe · Peel and grate carrots; Instant Pot Butter Chicken · Stir in coconut cream and finish sauce; Instant Pot Carrot Halwa Recipe · Sauté carrots and pressure-cook with almond milk; Instant Pot Butter Chicken · Portion, cool promptly and refrigerate; Instant Pot Carrot Halwa Recipe · Add sugar and almond meal; stir until thick; Instant Pot Carrot Halwa Recipe · Portion, cool promptly and refrigerate; Cleanup |
| Dec 24 | 09:00 AM–11:05 AM | Instant Pot Carrot Halwa Recipe · Portion chilled halwa and refrigerate; Aloo Chaat in Phyllo Shells · Steam potatoes; Vegetable Pulao Recipe / Veg Pulav · Chop the pulao vegetables; Vegetable Pulao Recipe / Veg Pulav · Fry cashews and sauté vegetables in stages; Aloo Chaat in Phyllo Shells · Cool briefly, dice potatoes and sauté the filling; Vegetable Pulao Recipe / Veg Pulav · Portion, cool promptly and refrigerate; Aloo Chaat in Phyllo Shells · Portion, cool promptly and refrigerate; Cleanup |
| Dec 25 | 09:00 AM–10:00 AM | Instant Pot Palak Paneer · Wash spinach, chop aromatics and blend cashew paste; Instant Pot Palak Paneer · Sauté aromatics and pressure-cook spinach; Aloo Chaat in Phyllo Shells · Prepare yogurt and chutneys; refrigerate separately; Instant Pot Palak Paneer · Blend spinach sauce and stir in cashew paste; Instant Pot Palak Paneer · Portion, cool promptly and refrigerate |
| Dec 25 | 03:55 PM–05:30 PM | Instant Pot Butter Chicken · Reheat gently and keep hot; Vegetable Pulao Recipe / Veg Pulav · Cook rice with whole spices; Instant Pot Palak Paneer · Reheat spinach sauce; add paneer and season; Aloo Chaat in Phyllo Shells · Fill phyllo shells and bake; Vegetable Pulao Recipe / Veg Pulav · Reheat vegetables and fold into fresh rice; Aloo Chaat in Phyllo Shells · Add chilled sauces and garnish the chaat cups; Cleanup |

**New-host review:** All selected cooking tasks, storage transitions and cleanup are present. The final block ends by 5:30 pm. Read the temperature/doneness notes as well as the clock; estimates do not replace checking the food.

## Indian vegetarian

**Menu:** Air Fryer Paneer Tikka; Instant Pot Palak Paneer; Vegetable Pulao Recipe | Veg Pulav; Indian Cucumber Salad (Kakdi Koshimbir); Instant Pot Carrot Halwa Recipe.

| Day | Prep block | Tasks |
|---|---|---|
| Dec 23 | 05:35 PM–08:00 PM | Vegetable Pulao Recipe / Veg Pulav · Chop the pulao vegetables; Vegetable Pulao Recipe / Veg Pulav · Fry cashews and sauté vegetables in stages; Vegetable Pulao Recipe / Veg Pulav · Portion, cool promptly and refrigerate; Instant Pot Carrot Halwa Recipe · Peel and grate carrots; Instant Pot Carrot Halwa Recipe · Sauté carrots and pressure-cook with almond milk; Instant Pot Carrot Halwa Recipe · Add sugar and almond meal; stir until thick; Instant Pot Carrot Halwa Recipe · Portion, cool promptly and refrigerate; Cleanup |
| Dec 24 | 05:40 PM–06:55 PM | Instant Pot Palak Paneer · Wash spinach, chop aromatics and blend cashew paste; Instant Pot Palak Paneer · Sauté aromatics and pressure-cook spinach; Instant Pot Carrot Halwa Recipe · Portion chilled halwa and refrigerate; Instant Pot Palak Paneer · Blend spinach sauce and stir in cashew paste; Instant Pot Palak Paneer · Portion, cool promptly and refrigerate; Cleanup |
| Dec 25 | 03:35 PM–05:30 PM | Indian Cucumber Salad (Kakdi Koshimbir) · Dice cucumber and chop cilantro; refrigerate; Air Fryer Paneer Tikka · Cut paneer and vegetables; coat in marinade; Vegetable Pulao Recipe / Veg Pulav · Cook rice with whole spices; Instant Pot Palak Paneer · Reheat spinach sauce; add paneer and season; Air Fryer Paneer Tikka · Thread skewers, preheat and air-fry paneer tikka; Indian Cucumber Salad (Kakdi Koshimbir) · Sizzle spices for the cucumber salad; Vegetable Pulao Recipe / Veg Pulav · Reheat vegetables and fold into fresh rice; Indian Cucumber Salad (Kakdi Koshimbir) · Toss cucumber salad with tempering and seasoning; Cleanup |

**Waiting notes:**
- Air Fryer Paneer Tikka · Refrigerate to marinate — 30 min waiting; At least 30 minutes; the publisher permits up to 24 hours refrigerated.

**New-host review:** All selected cooking tasks, storage transitions and cleanup are present. The final block ends by 5:30 pm. Read the temperature/doneness notes as well as the clock; estimates do not replace checking the food.

## Thanksgiving

**Menu:** Thanksgiving Turkey; Garlic Mashed Potatoes Recipe; Vegetarian Cornbread and White Bean Stuffing; Cranberry Orange Sauce; Gluten Free Apple Crisp.

| Day | Prep block | Tasks |
|---|---|---|
| Dec 22 | 06:15 PM–06:50 PM | Thanksgiving Turkey · Season thawed turkey for dry brining; Cleanup |
| Dec 23 | 05:35 PM–07:45 PM | Vegetarian Cornbread and White Bean Stuffing · Mix and bake cornbread; Cranberry Orange Sauce · Wash cranberries and zest orange; Garlic Mashed Potatoes Recipe · Peel and cut potatoes; prepare garlic; Garlic Mashed Potatoes Recipe · Boil potatoes and garlic until tender; Cranberry Orange Sauce · Simmer cranberry sauce; Cranberry Orange Sauce · Transfer sauce to a container and refrigerate; Garlic Mashed Potatoes Recipe · Drain and mash with butter and warm milk; Vegetarian Cornbread and White Bean Stuffing · Pack cooled cornbread airtight; Garlic Mashed Potatoes Recipe · Portion, cool promptly and refrigerate; Cleanup |
| Dec 24 | 03:15 PM–04:50 PM | Gluten Free Apple Crisp · Slice apples, mix topping and assemble crisp; Gluten Free Apple Crisp · Bake apple crisp until tender and golden |
| Dec 24 | 05:05 PM–07:45 PM | Vegetarian Cornbread and White Bean Stuffing · Cube and toast the cornbread; Gluten Free Apple Crisp · Cover and refrigerate the crisp; Vegetarian Cornbread and White Bean Stuffing · Cook white beans, vegetables and apple; Vegetarian Cornbread and White Bean Stuffing · Mix and bake stuffing; Thanksgiving Turkey · Uncover turkey to dry the skin; Vegetarian Cornbread and White Bean Stuffing · Portion, cool promptly and refrigerate; Cleanup |
| Dec 25 | 11:25 AM–05:30 PM | Thanksgiving Turkey · Prepare turkey and roasting pan; preheat oven; Thanksgiving Turkey · Roast turkey, reduce heat and check doneness; Gluten Free Apple Crisp · Rewarm the apple crisp; Vegetarian Cornbread and White Bean Stuffing · Reheat stuffing and crisp the top; Garlic Mashed Potatoes Recipe · Reheat mashed potatoes gently; Thanksgiving Turkey · Carve turkey into serving portions; Cleanup |

**Waiting notes:**
- Thanksgiving Turkey · Leave turkey dry-brining in refrigerator — 2160 min waiting; Keep refrigerated throughout the brining period.
- Vegetarian Cornbread and White Bean Stuffing · Cool cornbread on a rack — 60 min waiting; Let cool fully before packing.
- Gluten Free Apple Crisp · Cool the apple crisp — 60 min waiting; Let cool before covering; refrigerate within two hours.
- Thanksgiving Turkey · Rest turkey before carving — 30 min waiting; Tent loosely and rest for 20–30 minutes.

**New-host review:** All selected cooking tasks, storage transitions and cleanup are present. The final block ends by 5:30 pm. Read the temperature/doneness notes as well as the clock; estimates do not replace checking the food.

## Goan Christmas

**Menu:** Easy Tuna Croquettes; Chicken Cafreal; Goan Sannas (yeast method); Sonay Sukhe (Black Chana Sukka); The Best Doce.

| Day | Prep block | Tasks |
|---|---|---|
| Dec 23 | 12:05 PM–12:10 PM | The Best Doce · Rinse chana dal and cover with water |
| Dec 23 | 06:10 PM–09:00 PM | The Best Doce · Cook dal until soft; cool and blend with coconut; The Best Doce · Stir the doce until thick, then shape and cut; Sonay Sukhe (Black Chana Sukka) · Rinse chana and cover with water; Cleanup |
| Dec 24 | 09:00 AM–10:50 AM | Sonay Sukhe (Black Chana Sukka) · Pressure-cook chana until tender; Sonay Sukhe (Black Chana Sukka) · Temper aromatics and finish chana sukka; Sonay Sukhe (Black Chana Sukka) · Portion, cool promptly and refrigerate |
| Dec 24 | 05:45 PM–06:20 PM | Easy Tuna Croquettes · Mix tuna filling; Easy Tuna Croquettes · Shape, coat and refrigerate croquettes |
| Dec 24 | 08:40 PM–09:00 PM | Goan Sannas (yeast method) · Rinse rice and cover with water; Cleanup |
| Dec 25 | 09:45 AM–09:50 AM | Goan Sannas (yeast method) · Drain soaked rice and refrigerate until grinding |
| Dec 25 | 12:25 PM–01:25 PM | Goan Sannas (yeast method) · Grind rice and coconut; mix in yeast and sugar; Chicken Cafreal · Prepare chicken and blend cafreal paste |
| Dec 25 | 03:45 PM–05:30 PM | Sonay Sukhe (Black Chana Sukka) · Reheat gently and keep hot; Goan Sannas (yeast method) · Fill molds, steam and unmold sannas; Chicken Cafreal · Sear chicken, then cook in cafreal paste; Easy Tuna Croquettes · Air-fry croquettes, turning halfway; Cleanup |

**Waiting notes:**
- The Best Doce · Soak chana dal — 360 min waiting; Soak for 5–6 hours or overnight, then drain. Keep refrigerated during the soak; continue with cooking or grinding when it finishes.
- The Best Doce · Let doce cool fully — 120 min waiting; Leave pieces to cool before separating and packing. For this ahead-of-time plan, refrigerate in a covered container once cool. Once cool, pack covered and refrigerate; remove portions shortly before serving.
- Sonay Sukhe (Black Chana Sukka) · Soak chana overnight — 720 min waiting; Soak for 10–12 hours in the refrigerator, then drain. Keep refrigerated during the soak; continue with cooking or grinding when it finishes.
- Goan Sannas (yeast method) · Soak rice overnight — 720 min waiting; Leave the rice soaking overnight; drain before grinding. Keep refrigerated during the soak; continue with cooking or grinding when it finishes.
- Goan Sannas (yeast method) · Let batter rise until bubbly — 180 min waiting; Allow about 3 hours in a warm spot. Continue when visibly risen and bubbly; use the batter once ready.
- Chicken Cafreal · Refrigerate chicken in its marinade — 180 min waiting; Leave covered in the fridge for at least 2–3 hours, or overnight. Keep reserved paste separate from raw chicken.

**New-host review:** All selected cooking tasks, storage transitions and cleanup are present. The final block ends by 5:30 pm. Read the temperature/doneness notes as well as the clock; estimates do not replace checking the food.

## Christmas mixed table

**Menu:** Mushroom Cutlets; Pork Bafat | Dukra Maas; Sonay Sukhe (Black Chana Sukka); Caramelized Brussels Sprouts; The Best Doce.

| Day | Prep block | Tasks |
|---|---|---|
| Dec 23 | 10:30 AM–10:35 AM | The Best Doce · Rinse chana dal and cover with water |
| Dec 23 | 04:35 PM–07:20 PM | The Best Doce · Cook dal until soft; cool and blend with coconut; The Best Doce · Stir the doce until thick, then shape and cut; Cleanup |
| Dec 24 | 05:30 PM–08:20 PM | Mushroom Cutlets · Boil and mash potato; Mushroom Cutlets · Cook mushrooms dry and sauté aromatics; Pork Bafat / Dukra Maas · Cut pork, onions and aromatics; Pork Bafat / Dukra Maas · Simmer pork; add onions and garlic toward the end; Mushroom Cutlets · Mix, shape cutlets and refrigerate |
| Dec 24 | 08:40 PM–09:00 PM | Sonay Sukhe (Black Chana Sukka) · Rinse chana and cover with water; Cleanup |
| Dec 25 | 09:00 AM–10:50 AM | Sonay Sukhe (Black Chana Sukka) · Pressure-cook chana until tender; Caramelized Brussels Sprouts · Trim sprouts and mix the glaze; Sonay Sukhe (Black Chana Sukka) · Temper aromatics and finish chana sukka; Sonay Sukhe (Black Chana Sukka) · Portion, cool promptly and refrigerate |
| Dec 25 | 03:45 PM–05:15 PM | Caramelized Brussels Sprouts · Coat sprouts and roast, turning halfway; Pork Bafat / Dukra Maas · Reheat pork bafat; Sonay Sukhe (Black Chana Sukka) · Reheat gently and keep hot; Mushroom Cutlets · Coat and pan-fry cutlets; Cleanup |

**Waiting notes:**
- The Best Doce · Soak chana dal — 360 min waiting; Soak for 5–6 hours or overnight, then drain. Keep refrigerated during the soak; continue with cooking or grinding when it finishes.
- The Best Doce · Let doce cool fully — 120 min waiting; Leave pieces to cool before separating and packing. For this ahead-of-time plan, refrigerate in a covered container once cool. Once cool, pack covered and refrigerate; remove portions shortly before serving.
- Mushroom Cutlets · Let filling cool enough to handle — 20 min waiting; Cool briefly before shaping.
- Sonay Sukhe (Black Chana Sukka) · Soak chana overnight — 720 min waiting; Soak for 10–12 hours in the refrigerator, then drain. Keep refrigerated during the soak; continue with cooking or grinding when it finishes.

**New-host review:** All selected cooking tasks, storage transitions and cleanup are present. The final block ends by 5:30 pm. Read the temperature/doneness notes as well as the clock; estimates do not replace checking the food.

## Verification and limits

- 107 backend tests passed, including regression tests for all five complete menus, busy-calendar exclusions, impossible daily limits and bounded step transitions.
- All 45 non-recipe records were hashed before and after library updates and remained identical. No saved plan was regenerated or replaced. No calendar write was made.
- These are isolated feasibility and readability tests with an empty availability fixture. They do not establish fit against real calendar events.
- Quantities retain the earlier stress-test serving setup and the agreed one-batch kitchen assumption. This pass is about task order and scheduling, not a physical cooking trial or final buffet shopping quantities.
- Timing checks and source review were local. No live LangSmith experiment was run.

## Source support

- [Aloo chaat: advance filling and sauces](https://ministryofcurry.com/aloo-chaat-in-phyllo-cups/)
- [Pulao: vegetables may be sautéed ahead](https://ministryofcurry.com/moms-veg-pulao/)
- [Butter chicken: method and refrigerated storage](https://ministryofcurry.com/instant-pot-butter-chicken/)
- [Cornbread stuffing: advance preparation and reheating](https://www.wellplated.com/cornbread-sausage-stuffing/)
- [Apple crisp: baked storage and reheating](https://www.wellplated.com/gluten-free-apple-crisp/)
- [OR-Tools: precedence and shared-resource scheduling](https://developers.google.com/optimization/scheduling/job_shop)
