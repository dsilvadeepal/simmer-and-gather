# Simmer and Gather — PRD

Date: October 27, 2026. Status: **Design approved by Deepal on October 27, 2026; implementation plan prepared for review.**
Detailed behavior, architecture and proposed implementation decisions: [Design](docs/superpowers/specs/2026-10-27-simmer-and-gather-design.md).

## Problem and audience
Hosting combines menu decisions, ingredient shopping, kitchen bottlenecks and preparation around work. Deepal wants most cooking finished before guests arrive, without exhausting evenings. Initial product is private and single-user. Friends/family using their own accounts are future work.

## Outcome
For the demo, a feasible, source-grounded final hosting preparation/cooking plan generated after the host customizes an initial proposal. Live cooking progress and recovery during execution are later work. Diwali for about fifteen people anchors the demo, with vegetarian/nonvegetarian dishes, drinks and dessert. Thanksgiving, Christmas and a young child's birthday are additional use cases.

## Priorities and boundaries
Time and manageable effort matter more than spending. No budget optimization. No voice, guest login, ongoing detailed pantry upkeep, automated purchases, unsolicited guest messages, multiple planning agents or required vector database. No unsupported make-ahead/storage claims. No automatic calendar changes. No dashboard metric presented as proof of cooking quality.

## Confirmed demo boundary — October 27 clarification
Initial proposal -> host review and customization -> Generate final prep plan -> final hosting plan -> review and approve calendar blocks -> confirmed booking. The initial proposal includes the menu and an indicative preparation workload so choices have context. Before final generation, the host can swap recipes, preserve must-haves, choose available helpers and their session windows, and choose cook versus bought/prepared alternatives. Recalculate ingredients, quantities, tasks, dependencies, equipment use and time feasibility from the selected options; do not retain obsolete tasks after swaps. If infeasible, show the specific conflict and request a tradeoff instead of labeling it final and feasible.

The final output includes the selected menu and sources, shopping/bought items, dated prep/cooking sessions, helper assignments, equipment/batch needs, source-supported make-ahead instructions, cleanup and the separate finishing checklist. The demo ends after review, approval and confirmed booking of the prep blocks. Cooking check-offs, live completion percentages and running-behind recovery are deferred. Calendar availability remains an input. Book approved prep sessions as Busy in a dedicated “Simmer and Gather” calendar in the user’s Google Calendar account, displayed alongside the primary calendar. Persist and reuse its calendar ID; do not create a new calendar per gathering. Recheck availability before writing and show actual booking results, including partial failures. No background checks or alerts.

Weekly meal planning/preparation is a future extension: reuse recipes, inventory, availability, helpers and scheduling, but support multiple meal/serving dates, portions across days and storage/quality windows. Do not assume it is only a change of labels or build it into this demo.

## Requirements and acceptance
The following retains the broader product requirements. R17–R19 are post-demo; calendar-write portions of R14/R22 are included in the demo. All other planning behavior remains in scope unless explicitly revised.
| ID | Requirement | Acceptance example |
| --- | --- | --- |
| R1 | Reusable profile with per-gathering overrides | Changing this gathering's available oven or prep limit leaves default profile unchanged |
| R2 | Calendar selection and protected time | Free calendar slot overlapping protected family time is not scheduled |
| R3 | Preparation capacity and horizon | Daily totals: one hour on a work evening/two hours per weekend day, including cleanup and required supervision; adjustable per gathering; only schedule after chosen start date |
| R4 | Pre-arrival buffer | Main cooking ends one hour before arrival; final-hour hands-on finishing stays within adjustable 15–20 minute allowance |
| R5 | Complete menu then adjustment | User swaps, locks must-haves and selects bought starters/desserts; affected quantities/tasks recalculate |
| R6 | Dietary/portion coverage | Vegetarian count informs complete meals; shared sides count across guests; unknown allergies remain unknown |
| R7 | Notion-first collection plus discovery | Unsuitable saved options lead to cited candidates; user selects what to save |
| R8 | Curated import | URL/text -> extracted preview -> reviewed save; facts, estimates and gaps distinct; no need to rewrite every recipe |
| R9 | Make-ahead quality | Source permits advance step under specified conditions; unsupported overnight preparation isn't silently scheduled |
| R10 | Ingredient snapshot | Review/correct receipt and photo findings; duplicates questioned; only confirmed amounts subtract from shopping |
| R11 | Helper profiles and partial availability | Thirty-minute helper receives compatible work within that interval; zero-helper plan also supported |
| R12 | Equipment constraints | Incompatible oven temperatures and excess air-fryer batches cause schedule adjustment or explicit conflict |
| R13 | Potluck | Deepal enters dish, contributor, servings and warming; confirmed food counts, guest cooking does not count as host work |
| R14 | Calendar approvals | Dedicated Busy events created/changed only after exact revision approval and fresh availability check |
| R15 | On-open and manual recheck | Check calendars when app opens, through Recheck my plan and before writes; active gatherings only; no background jobs or silent rescheduling |
| R16 | No alerts | No email or in-app notifications; normal plan screen shows check freshness and results when reviewed |
| R17 | Mobile cooking | Check meaningful stages, see all dishes before/after session, persist progress across reloads |
| R18 | Progress meaning | Completed cooking can show 100% despite pending warming/table tasks; estimates labeled and unknown weights shown as stage counts |
| R19 | Late recovery | Rearrange remaining tasks/helper work first; optional simplification next; must-haves/completed stages preserved; approve changes |
| R20 | Final checklist | Small warming, drinks and serving tasks grouped separately while equipment and aggregate effort still count |
| R21 | Notion separation | Only designated app databases/pages accessible through app tools; unrelated workspace remains unchanged |
| R22 | Failure recovery | Stale approval blocked; retried writes don't duplicate; partial calendar sync and disconnected services shown honestly |

## Product experience
Onboarding: account connections, chosen calendars, kitchen profile, helpers and protected times. A gathering collects date/time, earliest prep date, guests/dietary needs, overrides and contributions. The app proposes an initial menu and indicative workload. The host then swaps recipes, marks must-haves, sets helper availability and chooses buy/cook alternatives, optionally confirming inventory. An explicit Generate final prep plan action creates the revised shopping list and feasible preparation/cooking sessions. Final review shows assignments, constraints, evidence, assumptions and unresolved gaps. The host reviews and approves the proposed blocks; the app rechecks availability, books them in the dedicated hosting calendar and confirms the results. Confirmed booking is the demo endpoint. Recipe collection supports import, review and Notion editing. Cooking mode and disruption recovery remain later product scope.

## Data and integrations
One LangGraph planning agent is the chosen orchestration pattern. Notion MCP manages recipe knowledge and human-readable records. App database owns typed snapshots, versions, progress, authorization and calendar operation IDs. Google Calendar owns reservations. Hosting must fit a $5/month total operating ceiling after credits; Replit is conditional on affordability, and free-tier alternatives need evaluation. LangSmith is selected by Deepal for tracing, datasets, experiments and human evaluation; do not integrate Langfuse in this demo. Nebius and Tavily remain proposed providers based on recorded credits; model capabilities and all remaining balances/entitlements require verification. Fireworks remains an alternative model provider. Email integration is excluded from initial scope. Detailed credits and caveats are in the design.

## Success and evaluation
LangSmith is the selected evaluation and tracing platform. Combine deterministic checks, Deepal's manual practicality review and limited model-based evaluation. Traces explain the steps taken; evaluation scores assess their quality. A successful tool call alone is not evidence of a useful plan.

Start with approximately 25 versioned scenarios covering the demo through approved calendar booking. Inputs include recipe evidence, calendar snapshots, constraints and host edits; expected outputs specify required behavior rather than one exact menu. Include swaps, buy/cook conversions, zero or partial helper availability, infeasible must-haves, potluck, unsupported make-ahead instructions, calendar changes, stale approvals, retries and partial booking failure. Use fixed calendars and simulated writes for repeatable offline experiments; verify real writes separately in a controlled integration check.

Use code to score schedule/resource constraints, quantities, preservation of user choices, removal of obsolete tasks and authorization/idempotency. Deepal reviews representative plans for manageable effort, clarity and willingness to follow them, recording reasons for changes. Use a bounded AI judge only for source support or explanation quality, checked against human labels. Jev remains an optional judge/classification experiment, not ground truth.

Compare model/prompt versions on the same dataset; reserve held-out cases and repeat selected cases for variability. Record prompt/model/source versions, redacted tool traces, latency, token usage, estimated cost and booking outcomes. Review failed or surprising actual runs and turn sanitized examples into regression tests. Paid online judging is limited/sampled; no calendar background monitoring or user alerts are added.

Proposed release gate: every defined hard-constraint and authorization test passes, and representative plans receive human practicality review with no unresolved blocking issue. Report actual passed/total counts and quality findings separately; do not collapse them into a single reliability score. Demo evidence shows one failure, its trace, a correction and the rerun, plus measured cost/latency. No results exist yet. Cooking-progress and execution-recovery evals are deferred with those features.

## Delivery and current state
Existing private GitHub repository and local folder are established. Dedicated Notion root and three empty databases exist; reuse rather than rebuild. No app, importer, calendar booking or monitoring is implemented. Design approval precedes implementation planning. The user has explicitly narrowed the demo to customized final-plan generation and approved calendar booking. Execution/progress and late recovery are retained as future requirements, not demo delivery commitments.

## Confirmed decisions and remaining setup
- Confirmed: preparation limits are daily totals covering the whole session, including cleanup and required supervision. Default one hour per work evening and two hours per weekend day; editable per gathering, including individual-day exceptions. Shorter sessions may share the daily allowance.
- Confirmed: $5/month total hosting and app-services ceiling after credits. Feasibility is not yet demonstrated.
- Confirmed: calendar checks on app open, manual request and before writes only. No background checks, emails or alerts.
- Confirmed: deletion of raw receipts/photos seven days after extraction, retaining confirmed ingredients. No service activated yet.

Concrete gathering date/time, recipe-source preferences, actual equipment capacities and calendar choices will be captured during onboarding. They need not block architectural review.

## Economical model use
Use code for calculations, validation, approval and calendar comparisons. Use an economical model for bounded extraction/classification, a vision-capable model for images, and stronger reasoning only for planning cases where evaluations demonstrate value. These are model calls inside one agent/workflow, not extra agents. Select exact models using existing provider access and measured cost per accepted result, including retries. Missing source evidence requires verification or clarification, not confident invention by a larger model. See the design model-routing proposal.


### System One decision-model candidate
Evaluate TypeSafe Jev for fixed-label recipe-stage classification and checking source support for proposed make-ahead instructions. System One here means typed probabilistic decisions, not generic fast LLM processing. Generative models still extract/write recipe tasks and propose menus; vision handles images; code validates scheduling and enforces approvals. Jev cannot invent missing source evidence or certify food safety. Compare against a low-cost LLM using labeled, held-out cases, including uncertainty and unsupported-claim errors; adopt only if quality and total cost justify it. Jev is not listed in current course credits and no service has been activated. See design for verified references, pricing and evaluation proposal.


## When the plan needs more time — confirmed October 27
Do not silently exceed daily limits or immediately discard the desired menu. First try a feasible arrangement within existing constraints. If it still does not fit, explain the bottleneck and show a concrete proposed adjustment: extra session minutes needed on specific days, required contiguous window, affected tasks and any equipment/helper constraint. Distinguish estimated task durations from known availability; do not claim a globally minimal time increase. A total-hours surplus alone does not establish feasibility.

Let the host increase a day’s allowance, add or move availability, start earlier where recipe storage permits, change helpers, or choose simpler/bought alternatives. Explicitly review any protected-time or arrival-buffer change. The app does not move existing personal/work events; the host can rearrange those externally and recheck. Regenerate and validate the plan after edits; calendar booking still requires approval of the exact resulting blocks. If no workable option is found, display unresolved conflicts rather than a final feasible plan. This is an in-app planning conversation, not a background notification.

Evaluation includes a plan that requires extra time: explain the shortfall, obtain a user-selected adjustment, revalidate, and never book beyond the original limits without the approved change.


## UI refinement — October 28
Show prep start date, individually selectable prep days and editable daily allowances in Gathering; distinguish total allowance from actual calendar availability. Default to a manageable menu recommendation with a More generous option and editable counts for starters, mains, sides, desserts and drinks. Counts include bought and guest-contributed items. Recommend based on occasion, guest/dietary mix, prep horizon, helpers and resources; do not hard-code two mains or fixed category counts. Count changes propose additions/removals for review, preserve must-haves and invalidate affected plans; re-evaluate quantities, dietary coverage and workload. Prototype values are illustrative, not validated recommendations.


## Recipe imagery and actionable session details — October 28
Use small source-permitted recipe photos in menu/picker cards and recipe details, with attribution and an accessible fallback. Do not imply an illustrative photo belongs to an imported recipe. Use restrained SVG icons alongside text for calendar, time, helpers, equipment, buying, guest contributions and must-haves. Session views must name the selected recipe and actionable step, estimated time window, assigned person, equipment, scaled quantities and dependencies; show source-supported storage/make-ahead guidance where applicable. Keep ingredient quantities directly visible beside each task on phones; only extra recipe notes and source detail remain expandable. Generic session headings are summaries only, never substitutes for recipe-specific tasks. Recipe edits regenerate affected steps. No live progress tracking is added.


Phone task presentation confirmed: show task-specific ingredient names and scaled quantities directly below the action, with amounts aligned for easy scanning. Extra recipe notes, provenance and additional instructions can expand. Critical safety/storage instructions needed to perform the task stay visible. Unknown quantities are explicitly marked for review, never fabricated. Mockup quantities are illustrative and not validated for cooking.


UI refinement: obvious tasks such as cleanup appear as a concise title and duration, without supply lists or instructional prose. Reserve visible ingredients and detailed actions for recipe-specific work. Phone typography uses a restrained sans-serif hierarchy: 18px task titles, 16px action/ingredient text, 13–14px metadata; keep quantities bold, maintain comfortable spacing and support text zoom. This visual direction is approved.

## Approved implementation decisions — October 28

Native execution is approved: one implementer uses Superpowers executing-plans with test-first development, targeted independent reviews of the scheduler and calendar authorization/recovery, and a final whole-branch review. Reuse the private `dsilvadeepal/simmer-and-gather` GitHub repository.

UI/UX is approved: guided Gathering → Menu → Prep plan, editable cards, backward navigation preserving choices, selected prep days and per-day totals, Manageable/More generous menus with editable category counts, compact attributed recipe photos and labeled icons. Laptop and phone share readable task typography; task ingredient quantities remain visible and extra notes expand. Cleanup is a short title/duration. Phone consultation/quick edits are included; cooking progress remains deferred.

Benchmark available Nebius and Fireworks vision endpoints using existing credits. Begin with a bounded development experiment capped at $1 total, no automatic recharge; verify each model ID and published rates before calls. Compare identical labeled images, extraction precision/recall, quantities/units, unsupported claims, latency and normal-rate cost per usable extraction. Distinguish synthetic receipts, public licensed images and any later user-provided samples. A small test yields a provisional selection, not general accuracy. Prefer the cheapest model meeting the accuracy/abstention gate; keep manual correction and unknown amounts. No personal uploads are required to continue building, and no live winner is claimed before results. Jev remains an optional text decision experiment, not the vision extractor.

### Live connections verified — October 28, 2026

The app-owned Notion connection is authorized only for the existing HR Recipe Library, Gatherings and Prep Sessions databases in Deepal Old. All three data sources returned successful read responses; all are empty. Recipe browsing now runs through the scoped app MCP server and opens candidates for source import/review. A Notion Planning Ready flag never bypasses application recipe validation. Reviewed recipe publication and gathering/session projections back to Notion remain to be implemented. No unrelated pages were granted access. Credentials are local, ignored by Git, owner-readable only.

Google OAuth and listing of 11 accessible calendars verified. The user chooses calendars in the app before availability checks. No real calendar events have been created. Local production server now loads both integrations; this is not a hosted deployment.

### Reviewed Notion saves and recipe collection — October 28, 2026

Explicit Save to Notion actions now export the locally saved reviewed recipe revision or the current validated plan and its prep-task pages. The owner and revision/hash are checked server-side. Saving to Notion does not approve Calendar writes. Immutable pages preserve manual Notion edits. A local export ledger serializes attempts; uncertain POST outcomes reconcile by a deterministic page title rather than creating again. Preflight/definitive rejection is retryable. Missing, moved or archived saved pages are reported without silent recreation. A live synthetic recipe/plan/session save and repeat-save check succeeded; all four QA pages were archived afterward.

The existing Recipe Library now contains 35 curated candidates: 15 Indian/Diwali plus 20 Thanksgiving/Christmas (12 Well Plated, eight With Wendy and Shannon/previously Platin It With Wendy). Source links, publisher ratings and vote counts are retained where verified. 27 have structured ingredient/timing metadata; eight Wendy pages are source-link only because the importer received HTTP 403. All 35 are Needs details and Planning Ready=false. See docs/recipe-collection.md. Recipe-level total time is not task-level active time or storage evidence.

Added user-triggered online link discovery with daily query caching, three-result limit and $0.008 basic-search reservation against the shared $3 monthly AI/search envelope. Runtime key comes from the existing authorized tool setup, stored privately. One live search verified; no background searches or automatic imports. Current rates checked at https://docs.tavily.com/documentation/api-credits . Added reviewed-collection menu suggestions with explicit preview/add action. Fixed HTTPS redirects with destination revalidation and nested HowToSection extraction; live Paneer Tikka import verified without automatically reviewing the recipe.

Remaining release work: runtime vision/upload retention, broader real-recipe planning/evals, full LangSmith runtime integration, hosted topology/entitlement verification and final branch review. No hosted deployment or real Calendar booking acceptance is claimed.

Collection expanded at user request: five Ruchik Randhap candidates added (Mushroom Cutlets, Mince Meat Cutlets, Pork Bafat, Coconut & Roasted Chana Dal Chutney, Coffee Fruit Cake). Verified total is now 40: 15 Indian/Diwali and 25 Thanksgiving/Christmas options. Four of the five supplied structured recipe data; the chutney is an accessible source link with no structured data. All remain Needs details, not planning-ready.
