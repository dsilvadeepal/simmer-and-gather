# Simmer and Gather — current PRD

Updated October 28, 2026. Approved direction: focused private hosting planner; native implementation. Historical decisions and implementation logs are retained in docs/archive, not normative requirements.

## Outcome and scope
Create an editable proposed hosting plan that explains the menu, quantities, practical preparation steps and whether the work fits the host's time. Diwali for 15 is the acceptance journey; Thanksgiving, Christmas and birthdays reuse the same contracts. One user now, owner-scoped records for future accounts. Cooking progress, live recovery, voice, meal planning and additional users are deferred.

## Experience and output contract
Guided Gathering → Menu → Prep plan with connected clickable chevron steps, an explicit current-step highlight, preserved edits and mobile readability. Generate proposed plan never means irreversible finalization. The host can swap dishes, set must-haves, select helpers and availability, choose bought/semi-prepared items, or enter potluck contributions, then regenerate.

The plan shows:
1. Menu table: role, source-linked recipe, portions/known ingredient quantities, and a factual reason for selection. Ingredient multipliers never imply appliance batch counts.
2. Does this fit? Calendar freshness, daily host presence versus allowance, cleanup allowance, main-cooking deadline and outstanding blocking issues. Separate menu recommendations from scheduling failures.
3. Compact When / What to do / Details table. Meaningful recipe-specific actions, explicit time ranges and expandable quantities, helper, source and guidance. Split separated cooking sessions instead of combining an entire day's work into one block. Soaking/chilling/waiting are notes; their dependencies remain binding. No separate measuring task; measure and add while cooking. Cleanup is a brief title and duration.
4. Recipe-specific details with source links; estimates and unsupported information distinguished. Group shopping ingredients logically with recipe details expandable.
5. Optional small finishing checklist: warming, drinks, serving dishes and spoons. No lengthy table-setting instructions in cooking blocks.

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

LangSmith sanitized linked stage traces and versioned datasets support experiments; do not equate passing fixture tests with live model quality. Keep model judges disabled by default and publish actual evidence separately. Manual practicality review remains required. Release requires a full editable Diwali journey, mobile/browser acceptance, controlled approved booking verification, and verified hosting cost. No calendar write is authorized merely by generation or this implementation request.
