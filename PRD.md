# Simmer and Gather — current PRD

Updated October 28, 2026. Approved direction: focused private hosting planner; native implementation. Historical decisions and implementation logs are retained in docs/archive, not normative requirements.

## Outcome and scope
Create an editable proposed hosting plan that explains the menu, quantities, practical preparation steps and whether the work fits the host's time. Diwali for 15 is the acceptance journey; Thanksgiving, Christmas and birthdays reuse the same contracts. One user now, owner-scoped records for future accounts. Cooking progress, live recovery, voice, meal planning and additional users are deferred.

## Experience and output contract
Guided Gathering → Menu → Prep plan with connected clickable chevron steps, an explicit current-step highlight, preserved edits and mobile readability. Generate proposed plan never means irreversible finalization. The host can swap dishes, set must-haves, select helpers and availability, choose bought/semi-prepared items, or enter potluck contributions, then regenerate.

The proposed-plan screen opens on **Schedule**, with **Menu**, **Shopping** and **Finishing** as compact secondary views. Switching views preserves edits and expanded details. Replace the marketing hero with the gathering title, arrival date/time and guest count. Use “Generate proposed plan” initially and “Update plan” once a proposal exists.

The schedule-first experience shows:
1. A concise fit summary: calendar freshness, main-cooking deadline and daily planned host presence versus allowance. Presence includes supervision and cleanup; it is distinct from elapsed cooking/waiting time. Keep blocking issues and outdated-input notices visible outside secondary views. Menu recommendations remain separate from scheduling failures.
2. Day groups with each date shown once and a compact When / What to do / Details layout. Preserve exact time windows, gaps and separated sessions; never imply an entire day's work is one continuous block. Show daily planned time against the editable allowance, with cleanup overrun identified separately. Empty prep days are available capacity, not scheduled work.
3. Meaningful recipe-specific tasks with known ingredient quantities directly visible beside the task. Expand only additional instructions, helper details, source links and guidance. Soaking/chilling/waiting appear as small notes while retaining their timing dependencies. No separate measuring task; measure and add while cooking. Cleanup is a brief title and duration, without obvious supplies or instructions.
4. A Menu view with role, source-linked recipe, portions, supported main-ingredient quantities and a factual selection reason. Do not present the first arbitrary ingredients as the main quantities. If no clear main ingredient is supported, show portions and expandable full ingredients. Multipliers never imply appliance batch counts. Existing recipe images may appear as small thumbnails with attribution and a fallback.
5. A Shopping view with logically grouped ingredients and readable calculated quantities, preserving confirmed inventory deductions and unknown-amount indicators. Recipe-specific details remain expandable.
6. A Finishing view with a brief checklist for warming, drinks, serving dishes and spoons. No lengthy table-setting instructions in cooking blocks.

Place Notion save and calendar actions in a compact expandable area after the plan. Keep approval separate from applying calendar changes and retain current-version, freshness and feasibility safeguards. Do not show previous proposal revision/history sections; retain recovery history internally.

Visual and accessibility requirements: warm ivory/green styling, restrained heading sizes, readable body text around 16px and metadata around 14px, reduced card/padding clutter, and touch targets at least 44px. The connected chevron navigation retains its current-step highlight and allows returning to earlier steps without starting over. Secondary views support keyboard navigation, visible focus and selected-state semantics. At 375px width, content must remain readable without page-level horizontal scrolling; adapt the schedule table into compact rows/cards as needed.

## Simple scheduling setup
The main gathering screen presents selectable prep days, a compact daily allowance with expandable per-day overrides, and a cooking-finished deadline derived from arrival minus the buffer. Keep earliest-date changes expandable. More scheduling options contains the light-finishing allowance and optional specific time windows; the calendar section shows only Personal, with no protected-time editor. Existing windows and daily overrides remain intact.

When no specific windows are set, code searches selected local dates from 9 am to 9 pm, clipped to the cooking deadline, excluding calendar conflicts and protected time. This range is shown to the host. Explicit windows replace that default; no automatic change to saved preferences or daily limits. Clearing windows returns to automatic availability. Generating a schedule still requires chosen calendars and the existing validation/approval flow.

## Time and kitchen constraints
Defaults: 120 minutes per day on both weekdays and weekends, counted across the day including required host presence/supervision. Gathering/day overrides are explicit. Cleanup may exceed the allowance by up to 15 minutes; it does not permit more cooking time. One-hour pre-arrival buffer; major cooking and cleanup end before it. At most 20 minutes of optional warming/drinks/finishing inside the buffer, editable per gathering. Never silently enlarge limits to make a plan fit.

Respect selected prep days, earliest start, protected times and chosen calendar availability. Typical home kitchen: oven, two stovetop positions, air fryer and Instant Pot. No appliance setup UI. Demo assumes one batch per dish; retain resource conflicts and ingredient scaling, do not infer capacity from source servings. No claim of verified appliance capacity.

Helpers have saved capabilities and gathering-specific availability; no automatic speedup. Guest/bought dishes remove host cooking except explicitly needed finishing. Account for vegetarian guest count and confirmed gluten/nut restrictions; do not treat unknown as none. Recommend manageable category counts, editable by host; missing recommended counts are advisories, not evidence that cooking cannot be scheduled.

## Architecture and ownership
React/TypeScript → FastAPI → one bounded LangGraph workflow plus deterministic services. PostgreSQL owns immutable input snapshots, versions, approvals and operation ledger. Notion is the editable recipe collection and readable plan projection. Google Calendar owns approved reservations. No vector database, second agent or queue is required.

Recipe preparation runs on import/edit and is cached independently of gatherings. Gathering planning reuses prepared recipes, scales ingredients, reads availability, schedules and validates. Publishing is separate and requires exact-version approval. Recipe content/schema/prompt/preference changes invalidate preparation; calendar changes do not. Record provider/model provenance. Curated JSON is a seed, not an override of newer Notion content. Saved plans retain the recipe versions they used.

Preparation readiness is granular: ingredients, logical steps, timing and advance-preparation support. A legacy reviewed flag does not prove all four. Unknown advance storage is not invented: same-day execution may be allowed only with an explicit same-day policy; unsupported overnight preparation remains blocked. Record component-to-next-step storage limits separately from final-dish-to-serving limits. Start/wait/finish stages preserve attention at the end of unattended cooking. Estimates remain estimates.

Tools/services: prepare_recipe_for_hosting; assess_menu_coverage; build_prep_schedule; validate_hosting_plan; suggest_plan_adjustments. The model interprets and explains; code calculates, validates and controls writes. Scheduling uses a bounded heuristic, an independent constraint validator and bounded adjustment search. Failure to find a schedule is not proof of impossibility. Proposed adjustments never change user constraints automatically.

Plan states distinguish complete cooking schedule, menu advisories, blocking constraints, outdated inputs and booking status. Never substitute an older schedule for a failed current attempt. Previous plans retain original inputs internally for recovery; hide revision/history sections from the hosting screen. Recipe edits mark dependent plans outdated without silently rewriting them.

## Integrations, privacy and budget
Notion access stays restricted to project databases. Calendar checks on open, manual Recheck and before writes; no background checks or alerts. Selected calendars only. Book Busy blocks only in dedicated Simmer and Gather calendar after approval, fresh recheck and revision/hash validation. Idempotent operation ledger handles retries and partial failures; never move personal events.

$5/month after credits is a deployment acceptance ceiling, not a demonstrated cost. Use code for arithmetic, cached bounded economical model calls for extraction and optional reasoning. Jev remains a measured optional classification experiment. Vision is isolated ingredient-input work, with user confirmation; uploads stay disabled until independent seven-day deletion is verified. Never use unconfirmed pantry quantities to reduce shopping.

## Evaluation and release
Code checks: missing/duplicate tasks, dependencies, start/end attention, storage, host/helper overlap, daily totals, buffer, stale recipes/plans, approval and retry boundaries. Recipe evals: source coverage, missing steps, fabricated evidence, timing plausibility, work/wait separation and cache invalidation. End-to-end scenarios use actual recipe structures and fixed calendar snapshots: swap, buy/cook, zero/partial helper, extra time, missing evidence and disconnected calendar.

LangSmith sanitized linked stage traces and versioned datasets support experiments; do not equate passing fixture tests with live model quality. Keep model judges disabled by default and publish actual evidence separately. Manual practicality review remains required. UX acceptance checks cover schedule-first default, keyboard-accessible secondary views, quantities visible without expansion, dates grouped without concealing time gaps, visible blockers, preserved approval safeguards, and a 375px phone layout without horizontal overflow. Release requires a full editable Diwali journey, mobile/browser acceptance, controlled approved booking verification, and verified hosting cost. No calendar write is authorized merely by generation or this implementation request.

Continuous cooking sessions appear as one time range with an ordered task list. Merge touching or overlapping work intervals within each day; preserve genuine breaks. Keep ingredients visible and recipe instructions expandable, without individual task time slots or hands-on-minute labels. Waiting remains a note. This presentation does not change the underlying schedule or calendar events.

Cooking copy: task-specific guidance uses expandable “How to” bullets. Keep ingredient quantities visible. Show make-ahead/storage guidance once per recipe alongside an Original recipe link, outside the task list. Omit internal provenance commentary from cooking instructions while retaining source records. Show approximate timing notice once. Never invent missing cooking settings or doneness checks.

### Recipe readiness checks (October 29 update)
`prepare_recipe_for_hosting` v3 keeps generated recipes unreviewed and returns explicit review issues for non-food ingredient rows, mixed setup/wait steps, missing cooling/soaking/packing instructions, missing reheating for cooked-ahead food, and missing oven temperatures. It validates attention segments and requires continuous presence during pan-frying. Prompt guidance keeps independent prep parallelizable and connected cooking phases together. These bounded checks do not prove culinary completeness or safe storage; source evidence and human review remain required. Cache keys include the new prompt/schema versions; traces include readiness issue counts without recipe content.

### Make-ahead sequence validation — October 29
Recipe preparation must distinguish source-supported storage from labelled culinary estimates. Cooking, cooling, packing, soaking setup and reheating are explicit linked steps; optional minimum/maximum dependency gaps prevent unsupported pauses and immediate cool/reheat cycles. The scheduler must try a bounded, local constraint search for supported solo-host cases before recommending extra time or bought dishes. Every candidate still passes the independent validator for dependencies, attention, equipment, calendar, daily limits, cleanup and the relaxation buffer. Failure to find a candidate is not a proof of infeasibility. Saved recipe snapshots in existing plans are never rewritten by a library audit.

The five-menu regression rerun is documented in `docs/reviews/2026-10-29-five-menu-rerun.md`. All five schedules fit the unchanged test limits, including the previously approved flexible cleanup allowance. This is fixture-based evidence, not live-calendar or cooking validation. The vegetarian Thanksgiving stuffing adaptation exists only in the isolated draft.

### UX clarity pass — November 6, 2026
- Shopping groups: Produce, Dairy & proteins, Pantry & spices, Frozen. Exclude plain water; clean publisher formatting and combine equivalent names with matching units. Preserve unresolved amounts rather than infer scaled quantities.
- Show practical shopping quantities with explicit “About” rounding; cooking quantities remain unchanged. Consolidate unresolved items under “Amounts to confirm,” with original recipe links available.
- Daily summaries distinguish active time (including supervision and cleanup) from start-to-finish session duration. Feasible plans with an overrun must disclose the extra time.
- Disable Save gathering when unchanged. Distinguish Check calendar conflicts from Regenerate prep plan; neither action books events. Colors and layout unchanged.

### Cooking clarity follow-up — November 6, 2026
- Use concise dish names in the schedule, remove repeated generic supervision reminders, and suppress instructions that simply repeat the task title. Preserve recipe-specific methods and existing task quantities; never invent missing cooking settings.
- Explain recipe-yield servings versus buffet portions. Replace generic review prompts with recipe review status and the servings control.
- Use plain scheduling language and readable dates; remove stale references to protected time.
- Use Ingredient, Amount and Unit fields for pantry additions, preserving existing inventory and retaining input after a failed save.
- Filter generic finishing items against the selected menu, omitting drinks when none are selected and vague unsupported warm-holding instructions. Do not rewrite saved plans.

### Architecture checkpoint · November 7, 2026
Recipe quantities must preserve original text and distinguish exact amounts, ranges, to-taste amounts and unknowns. Optional ingredients remain explicit. Scaling a range must retain both bounds. Unknowns must never become guessed numbers.
Before scheduling, validate recipe dependencies and timing consistency. Present missing inputs, an exhausted search, unsupported configurations and validation failures distinctly; none proves the host needs more time.
Remove the recipe-import panel from the hosting UI. Continue choosing from the existing recipe collection. Menu images should prefer current Notion/library image metadata without modifying saved cooking-plan snapshots.
See docs/reviews/2026-11-07-architecture-implementation.md for implementation evidence and remaining production work.

### Pantry walkthrough
Remove the separate “What you already have” input panel. Shopping rows have “Have” checkboxes and remain visible with a strikethrough until “Show only what I need” is selected. “Show all ingredients” restores them for easy undo. Checks persist per gathering on this device, not across accounts or devices. Changed quantities require reconfirmation. Checking an item does not alter a recipe, cooking plan or calendar.

### Checked menu alternatives (November 7, 2026)

When a proposed menu has nut/gluten screening conflicts or insufficient vegetarian main portions, automatically offer up to three alternatives from the owner's reviewed saved recipe library. Preserve must-haves, contributions, gathering settings, prep limits and buffer. Prefer fewer substitutions and portions covering the vegetarian shortfall. Screen the entire candidate menu and run the scheduler plus independent validator before offering it. Unknown screening remains a blocker; ingredient screening is not allergen-free certification.

Alternatives are unsaved previews with dish changes, servings and expandable prep schedules. Explicit approval rereads calendar availability and recipe versions, rejects stale or newly infeasible choices, and updates the menu only. Saved plans and calendar events are never changed by preview or approval; generating a new plan and adding events remain separate actions. Bound search to 12 schedule attempts, 256 combinations, five candidates per dish, three results. No result means the bounded search found none, not proof that no feasible alternative exists. Record aggregate search results in LangSmith when enabled; no new model calls.
