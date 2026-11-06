# Alternative Christmas recipe split review

Scope: read-only dry run of five different library recipes, using the saved Christmas test settings (15 people; Dec 25 at 6 pm; Dec 22–25 prep; 120 minutes on earlier days, 180 on Christmas Day; 30-minute buffer; avoid nuts). The current Goan gathering and recipe records were not changed. Calendar availability is the existing snapshot, not newly fetched; no events were created. This is a recipe readiness test, not a completed alternative menu proposal.

## Actual dry-run result

The scheduler returned incomplete with zero assignments and 20 preparation-window evidence issues. Every task in this set has preparation_policy=unknown and max_ahead_hours unset. These gaps must be addressed before drawing conclusions about fit. The audit also found 12 mixed active/passive tasks without attention placement, two oven tasks without structured temperatures, three unknown allergen lists, and three ingredient lists containing non-food import commentary. Machine-readable findings: christmas-alternative-audit.json.

## Proposed logical groups and gaps

| Recipe | Proposed logical groups | Corrections needed |
|---|---|---|
| Mince meat cutlets | Cook potato and mince; sauté aromatics → cool → combine and shape → coat and fry near serving | Potato and mince are unnecessarily serial today. Aromatics need their own action. Choose chicken or beef explicitly because the source gives different handling. Egg coating must appear in ingredients/allergens. The source's freeze-ahead variant excludes potato until thawed; do not generalize it to fully shaped cutlets. Pan-frying requires attention throughout; 25 elapsed/15 active is not justified by a check-in model. |
| Pork bafat | Chop pork and aromatics → simmer, add onions/garlic late, finish tender → chill if cooked ahead → reheat | Current ahead-of-time note says reheat, but no reheat task exists. Keep the two simmer phases together with a later-add instruction, avoiding an arbitrary gap mid-cook. The stored 110-minute cooking allowance exceeds the source's 40-minute headline; preserve it as an explicit estimate pending chosen cut/quantity, not a claimed source time. |
| Black chana sukka | Rinse → overnight soak note → pressure-cook and release → sauté aromatics while chana cooks → combine and finish | A 725-minute combined rinse/soak step should become 5 minutes work plus 12 hours waiting. Onion preparation does not depend on pressure cooking finishing. Keep the coconut/spice stage and final simmer together. Whistles are not an Instant Pot timing conversion; require an appliance-appropriate method or retain uncertainty. Cooked make-ahead storage is not established by this source. |
| Brussels sprouts | Trim and prepare glaze → coat, roast and turn → season | The glaze-mixing and oven-preheating actions are not explicit. Store 400°F in structured data. Keep coating and roasting together; the planned half-hour buffer means crispness at serving is a tradeoff, not a guarantee. Source supports refrigerated leftovers and reheating, but that is different from claiming freshly roasted texture. |
| Coffee fruit cake | Chop fruit and simmer with coffee → cool mixture → mix batter and bake → cool in tin, unmold and cool fully → wrap | Cooling before egg addition is an essential dependency. Combine batter mixing with baking or bound their gap. Include the 45-minute browning check, 350°F oven, 10-minute tin cooling, and final wrapping. Source explicitly gives 3–4 days airtight at room temperature, so the current generic 'verify storage' note can be replaced with attributed guidance. Inspect malformed ingredient names/amounts; preserve gluten, milk and egg information. |

## Tool/validator changes indicated by this review

1. Separate method review, ingredient review, and schedule readiness; reviewed=true alone is insufficient.
2. Reject non-food ingredient placeholders and flag quantities embedded in names before producing shopping amounts.
3. Validate that ahead-cooked dishes include necessary cooling/storage and reheating/finishing actions.
4. Separate passive waiting from active work; require evidence for sparse check-ins, especially pan-frying.
5. Distinguish minimum waits (soak) from maximum gaps (mixed cake batter, cooked components awaiting combination).
6. Keep independent prep parallelizable; add dependencies only where the cooking method requires them.
7. Store doneness/temperature cues with the correct task, and preserve unresolved appliance conversions.
8. Test the real serving deadline plus buffer: fresh/crisp dishes cannot simply be shifted earlier without a quality tradeoff.

Suggested eval cases: no overnight soak as an active block; no non-food shopping rows; cooked-ahead pork has reheating; egg added only after fruit mixture cools; cutlet frying never modeled as unattended; sprouts oven temperature present; primary recipe dependency graph remains valid; unknown storage is not silently treated as approved.

## Sources checked October 29, 2026

- https://www.ruchikrandhap.com/mince-meat-cutlets/
- https://www.ruchikrandhap.com/pork-bafa/
- https://www.ruchikrandhap.com/sonay-sukhe-black-chana-fugadsukka/
- https://www.ruchikrandhap.com/coffee-fruit-cake-no-alcohol-las/
- https://www.wellplated.com/caramelized-brussels-sprouts/

No complete alternative hosting menu is claimed: this diagnostic sample omits a bread/rice accompaniment and does not establish buffet portion adequacy or packaged-product nut cross-contact safety.

## Implemented follow-up

The five recipes were corrected and saved to the local library, with gathering-specific snapshots saved in `alternative-christmas-reviewed-recipes.json`. Coffee ingredient amounts were normalized and non-food rows removed. Chicken is explicitly selected for mince cutlets; pan-frying reserves the whole 35-minute step. Source-based methods and estimated timing/storage allowances remain distinct. No verified Instant Pot conversion is claimed for black chana.

Separate app gathering: `31f9651b-6c4c-48ea-9352-2edfd0673fca`. Live Personal-calendar read, no calendar writes. Result: feasible, 25 assignments, no validator violations; Dec 23 120 minutes, Dec 24 110 minutes, Dec 25 130 minutes; final cleanup ends 5:25 pm. Dec 22 requires no work. The existing Christmas gathering and menu were compared before/after and are identical. A title matching error briefly selected an unrelated mushroom recipe; it was removed from this alternative and its library contents restored from the prior snapshot.

Tool v3 adds deterministic review signals and validates attention segments. A cache-version change prevents reuse of v2 outputs. The test suite verifies missing reheating/non-food notes, pan-frying supervision and invalid check-ins. Backend: 96 tests passed. These are local regression checks, not a live LangSmith experiment or a cooked trial.
