# Simmer and Gather — current architecture

Updated November 7, 2026. Product behavior: [PRD](../../../PRD.md). Work status: [build plan](../plans/2026-10-27-hosting-demo.md).

## Data and responsibilities
React/TypeScript calls authenticated FastAPI services. One bounded LangGraph workflow coordinates recipe retrieval, scheduling and validation. PostgreSQL stores owner-scoped input snapshots, recipe versions, plans, approvals, credentials and the operation ledger. Notion is the editable recipe library and readable plan projection. Google Calendar supplies selected availability and receives separately approved hosting blocks.

## Preparation
`prepare_recipe_for_hosting` v5 creates typed task graphs, source evidence, active/presence/elapsed durations, attention segments and advance-preparation/storage constraints. It never approves its own output. Quantity metadata distinguishes exact, range, to-taste and unknown amounts and preserves original text. Cache keys include source/content, schema, prompt, model and preferences; calendar-only replanning does not re-extract recipes.

## Scheduling and recovery
Validate recipe graphs before scheduling. Scale ingredients independently of the standard single-batch kitchen assumption. Use bounded heuristic/search and a supported host-only OR-Tools fallback, then independently validate completeness, dependencies, storage, attention, resources, daily allowances, helper availability and buffer. Search failure is not proof of impossibility.

Outcomes distinguish complete, needs_input, no_fit_found, search_exhausted, unsupported search and final validation failure. Menu requirements can block an otherwise time-feasible schedule. Guest allergies must be explicit; missing screening is not absence of allergens.

Checked alternatives use reviewed owner-library recipes, preserve must-haves and limits, and validate the entire menu and schedule. Search is bounded to 12 schedule attempts, 256 combinations, five candidates per dish and three results. Bought-prepared options use the same read-only preview/explicit acceptance pattern. Accepting a choice refreshes availability and recipe versions, validates again, and atomically saves the menu plus a new plan. Existing plan snapshots remain unchanged.

## UI and write boundaries
Gathering → Menu → Prep plan, with Schedule first and Menu/Shopping/Finishing secondary views. Previews contain read-only schedules, never shared shopping controls. Have checks use per-gathering browser storage with amount-change reconfirmation; they do not modify recipe quantities or server plans.

Calendar approval and application remain separate from planning and menu acceptance. Exact revision/hash, fresh availability, recipe-version checks and idempotent operations guard booking. No background calendar polling or alerts. No automatic personal-event movement.

## Evidence and deployment
Sanitized LangSmith traces and code-based experiments record bounded summaries. See [current evidence](../../reviews/current-evaluation-results.md). LLM judges are not used. Local fixture success is not hosted acceptance. Replit is paused; $5/month remains a deployment target requiring verification. Upload retention, additional accounts and cross-device checklist sync are deferred.
