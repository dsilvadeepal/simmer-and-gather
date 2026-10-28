# Simmer and Gather Hosting Demo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (Native, approved) to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver one private hosting workflow from a customizable menu proposal to a validated prep plan and approved Busy blocks in a dedicated Google Calendar.

**Architecture:** React UI calls a Python API containing one LangGraph planning agent and deterministic scheduling/validation services. PostgreSQL owns revisions, approval and operations; Notion MCP provides scoped recipe knowledge and readable projections. Provider adapters and fixtures allow local development without live writes; deployment is gated by a verified post-credit budget.

**Tech Stack:** React, TypeScript, Vite, Python 3.12+, FastAPI, Pydantic, SQLAlchemy/Alembic, PostgreSQL, LangGraph, LangSmith, pytest, Vitest and Playwright. Pin compatible versions at Task 1; use ordinary HTTP/SDK adapters for Google, Notion MCP, model and search calls. No vector database, second agent or queue service.

**Spec:** `docs/superpowers/specs/2026-10-27-simmer-and-gather-design.md` and `PRD.md`, approved October 27, 2026. Native execution and UI/UX are approved October 28.

## Global Constraints

- Demo: initial proposal -> host adjustments -> final prep/cook plan -> exact approval -> dedicated-calendar Busy booking confirmation.
- Daily totals: one hour per work evening and two hours per weekend day, including cleanup and required supervision; gathering/day overrides do not change defaults.
- Main cooking/cleanup ends one hour before arrival; final-hour finishing allowance is adjustable, proposed default 20 minutes. Do not consume the remaining protected time.
- Earliest prep date and source-supported storage/quality windows constrain scheduling.
- Preserve must-haves; report time shortfalls and obtain explicit availability/limit changes before regenerating.
- Helpers have explicit capabilities and per-session availability; never assume extra capabilities or universal speedups.
- Notion-first recipe discovery; review new imports, inventory extraction and all external writes.
- Calendar reads on app open, manual Recheck and immediately before booking only. No background checks, alerts or email.
- Only app-owned events in the dedicated Simmer and Gather calendar may be changed. No personal/work-event rescheduling.
- One private user initially; owner IDs on all records. No public real-account demo data.
- $5/month total operating ceiling after credits; no assumed paid subscriptions, automatic recharge or hidden free-to-paid fallback.
- LangSmith selected; no Langfuse integration. Optional Jev experiment only after access and evaluation budget checks.
- Raw uploads deleted within seven days after extraction; retain confirmed ingredients. No ongoing pantry inventory.
- Post-demo: cooking check-offs/progress, running-behind recovery, weekly meal planning, voice and additional users.

## Review Focus

- Daylight-saving/overnight windows must retain the host's local-day limits: tests in Task 6.
- A stale Notion edit or delayed browser save must not overwrite a newer plan: tests in Tasks 3 and 7.
- An ambiguous unit, duplicated receipt/photo or unresolved ingredient must not create a false shopping deduction: Task 5.
- A timed-out Google write may already have succeeded; retries and double-clicks must not duplicate events: Task 9.
- Session expiry, cold starts and disconnected providers must preserve saved work and show honest stale/failed state: Tasks 2, 4 and 11.

## File structure and shared contracts

All paths below are new unless explicitly marked Modify. Keep production code under `backend/src/simmer/` and `frontend/src/`. Mirror backend features under `backend/tests/`. Root `pyproject.toml` defines the `backend/src` package layout and pytest path; `uv.lock` pins Python dependencies. Frontend has its own package/lock files. Use local PostgreSQL through `compose.yaml`, not SQLite as an untested production substitute.

- `backend/src/simmer/domain.py`: Pydantic contracts shared by services and API; emit frontend types through FastAPI OpenAPI.
- `backend/src/simmer/db.py`, `models.py`, `migrations/`: persistence, ownership, revisions, operation ledger.
- Feature modules: `auth.py`, `profiles.py`, `recipes.py`, `inventory.py`, `availability.py`, `scheduler.py`, `menu.py`, `agent.py`, `approval.py`, `booking.py`, `budget.py`, `telemetry.py`.
- `backend/src/simmer/adapters/{notion,google,models,search,storage}.py`: external boundaries; tests inject fakes.
- `backend/src/simmer/api.py`: authenticated HTTP routes and static frontend serving; no business logic in route handlers.
- `frontend/src/features/{setup,recipes,inventory,menu,plan,booking}/`: feature screens and tests; `api.ts` handles authenticated requests and typed errors.
- `evals/{cases.jsonl,run.py,evaluators.py,README.md}`: versioned scenarios, experiment runner and scoring.
- `docs/{provider-readiness,budget,runbook,demo-evidence}.md`: verified setup, costs, recovery and actual evidence.

Define these contracts in Task 2; later tasks extend only through explicit reviewed schema migrations:
`OwnerId`, `GatheringId`, `RecipeId`, `PlanId` are UUID aliases; `Revision` is a positive integer. `Interval(start,end)` uses timezone-aware datetimes and half-open intervals. `HostProfile` stores timezone, daily limits, protected intervals, equipment and helper profiles. `Gathering` snapshots these defaults and stores arrival, earliest prep date, guests/dietary needs, contributions and per-day overrides. `RecipeSnapshot` stores servings, ingredient quantities/units, source/version, evidence and `PrepTask` records. Each task has stable ID, dependencies, active/elapsed/presence minutes, required skill/resource/capacity, eligible window, source support and uncertainty. `MenuSelection` stores recipe/version or bought/guest source, servings and must-have status. `PlanInputs` combines gathering, selections, confirmed inventory and `AvailabilitySnapshot`; `PlanCandidate` contains sessions, assignments, shopping, final checklist, input hash, revision and feasibility status. `ConstraintViolation` has code, affected IDs, explanation and evidence; `TimeAdjustment` identifies day, current/proposed minutes, window and conditional reason. `Approval` binds owner, plan revision/hash and exact event proposal. `BookingResult` lists per-operation outcomes, never a single false all-or-nothing result.

## Budget and deployment decision

Keep the approved Python/PostgreSQL architecture. Supabase is not required or selected. Google OAuth supplies owner sign-in; standard PostgreSQL holds app state. Evaluate Neon Free or the user's previously used Replit PostgreSQL alongside hosting, selecting only a verified combination within $5/month after credits. Hosting remains undecided. The current session-level advisory locks require a direct/session-mode database connection, not transaction pooling. Do not use expiring Render Free Postgres as persistent storage. Verify independent upload cleanup before enabling hosted uploads.

Earlier Render/Supabase comparisons were research candidates, not approved purchases or entitlements. Recheck current pricing and account limits before deployment; do not buy a domain or upgrade plans without authorization.

Budget target, not measured forecast: $0 fixed infrastructure, at most $3/month combined model/search/eval/trace spend, $2 headroom for remaining usage/taxes. Model planning runs per month and token/search/image usage explicitly in `docs/budget.md`; report maximum supported usage rather than inventing a universal monthly total. Price at normal rates after credits. Track credit balances separately. LangSmith included/credit entitlement and retention must be verified; disable paid judging and cap trace volume before spending the reserve. Development experiments get a separate explicit spend allowance before live calls; no paid calls in fixture tests.

## UI/UX review prerequisite — October 28

Superpowers visual brainstorming and screen approval are complete. Laptop-first planning, phone-friendly plan consultation and quick edits; guided Gathering → Menu → Prep plan with editable cards, preserved inputs and backward navigation. Visual direction: warm and inviting but clean, practical and uncluttered. Mockups are throwaway design artifacts, not app code. Task 8 implements the approved screens rather than postponing design until that task. Live cooking progress remains deferred.

## Task 1: Verify a viable deployment and provider contract

**Files:** Create `docs/provider-readiness.md`, `docs/budget.md`, `.env.example`, `backend/tests/contracts/test_provider_config.py`, `backend/src/simmer/config.py`, `pyproject.toml`, `uv.lock`.
**Interfaces:** Produces `validate_provider_config(config: dict) -> list[str]`; config selects exactly one planning provider/model, one vision model, one search provider, LangSmith, Google, scoped Notion MCP and storage. No secrets in examples.

- [ ] Benchmark Nebius and Fireworks vision using a shared labeled dataset and a $1 total development cap; report provisional winner only from observed results. Add `evals/vision_benchmark.py`, fixtures and `docs/vision-benchmark.md`. Introduce conservative call reservations before live experiments; Task 10 expands persistent runtime guards.
- [ ] Record account-level access checks from the credits tracker: Nebius first, Fireworks alternative, Tavily and LangSmith. Identify model IDs, structured/tool and vision capabilities, current rates, quotas and expirations. Verify hosted app credentials independently of chat connectors. Select compatible pinned library versions.
- [ ] Write `test_provider_config.py` asserting missing rates reject paid mode, unknown model IDs reject live mode, fixtures need no secrets, and a forecast over $5 returns a blocking error.
- [ ] Run `uv run pytest backend/tests/contracts/test_provider_config.py -q`; expect failure until config validation exists.
- [ ] Implement `validate_provider_config` and record the measured/quoted cost envelope plus OAuth callbacks, refresh-token/testing-mode limitations and Notion MCP enumeration/access findings. Choose the free deployment candidate only after its requirements pass. If blocked, stop deployment-dependent work and present the concrete issue; fixture-based domain tasks can proceed.
- [ ] Rerun the contract tests; require PASS and a readiness table labeling verified, unavailable and simulated items. No account upgrade, card entry or new billable service activation is implied by this plan.
- [ ] Commit these exact files with message `chore: define verified provider and budget contract`.

## Task 2: Persist a private gathering and its editable defaults

**Files:** Create `domain.py`, `models.py`, `db.py`, `auth.py`, `profiles.py`, `api.py` under backend package, root `compose.yaml`, `backend/migrations/001_core.py`, `backend/tests/test_profiles.py`, `backend/tests/test_auth.py`.
**Interfaces:** Produces `save_gathering(owner: OwnerId, gathering: Gathering, expected_revision: int | None) -> Gathering`; `require_owner(session_token: str) -> OwnerId`; `load_plan_inputs(owner: OwnerId, gathering_id: GatheringId) -> PlanInputs`. Partial inputs remain draft.

- [ ] Write tests asserting 60/120-minute defaults, arrival buffer 60/finishing 20, per-day override isolation, zero/30-minute helper availability, missing allergy/capacity data remain unknown, and another owner or expired session cannot access data. Assert stale revisions return conflict rather than overwrite.
- [ ] Run `uv run pytest backend/tests/test_profiles.py backend/tests/test_auth.py -q`; expect missing implementation failures.
- [ ] Implement contracts, database migration, transaction-backed revision checks and private allowlisted login. Use server-validated auth, encrypted integration credentials, CSRF protection on cookie-authenticated writes and owner predicates. Expose `/api/profile` and `/api/gatherings` with typed errors; no tokens in logs.
- [ ] Rerun tests against local PostgreSQL; require PASS including persistence across API restart.
- [ ] Commit the task files with message `feat: persist private hosting profiles and gathering overrides`.

## Task 3: Retrieve and curate recipes through scoped Notion MCP

**Files:** Create backend `recipes.py`, `adapters/notion.py`, `adapters/search.py`, `adapters/models.py`; `backend/tests/test_recipes.py`; `backend/tests/fixtures/recipes.json`.
**Interfaces:** Produces `list_recipes(owner: OwnerId) -> list[RecipeSnapshot]`; `preview_recipe(owner: OwnerId, source: str) -> RecipeSnapshot`; `save_reviewed_recipe(owner: OwnerId, recipe: RecipeSnapshot, expected_source_version: str | None) -> RecipeSnapshot`; `discover_recipes(query: str, limit: int = 3) -> list[dict]` with URL/title/evidence status.

- [ ] Write tests for allowlist rejection, paginated enumeration, source-edited conflict, blocked localhost/private-IP/redirect URLs, pasted-text fallback, missing timings, unsupported make-ahead, and malicious page instructions treated as recipe data. Assert unknown storage guidance cannot become confirmed by model output.
- [ ] Run `uv run pytest backend/tests/test_recipes.py -q`; expect failure.
- [ ] Implement parser-first previews, bounded economical-model extraction, source-linked task evidence and explicit facts/estimates/unknowns. Cache by source/version. Resolve the existing Notion IDs from ignored local setup data; never recreate databases. Wrap hosted MCP with database/page membership checks, or use the documented scoped API-backed MCP adapter if Task 1 established that need. Save only reviewed previews. Retrieve saved recipes first; request at most three discovery candidates when needed.
- [ ] Create a small source-linked starter set adequate for Diwali menu alternatives, including vegetarian/nonvegetarian mains, sides, starters, drinks and dessert. Curate accessible recipe guidance without bulk copying; no claims of personally testing dishes. Review records before live Notion save; use synthetic fixtures in tests.
- [ ] Rerun tests; require PASS. Verify one controlled read/preview/save round trip when credentials and review are available; label fake/live outcomes.
- [ ] Commit with message `feat: add scoped recipe collection and reviewed import`.

## Task 4: Read calendars and protected availability

**Files:** Create backend `availability.py`, `adapters/google.py`; `backend/tests/test_availability.py`.
**Interfaces:** Produces `read_availability(owner: OwnerId, gathering: Gathering) -> AvailabilitySnapshot` containing selected-calendar busy intervals, checked_at, freshness and errors. Google adapter also defines `ensure_hosting_calendar(owner: OwnerId) -> str` for Task 9, using persisted calendar ID and reconciliation.

- [ ] Write tests asserting selected calendars only, protected free-looking time excluded, same-plan events excluded by owned IDs, other gatherings included, timezone conversion, disconnected calendar returns unavailable (not empty), and duplicate page-open reads coalesce.
- [ ] Run `uv run pytest backend/tests/test_availability.py -q`; expect failure.
- [ ] Implement calendar selection/free-busy retrieval and event ownership mapping. On-open/manual requests read active gathering horizons. No scheduler/polling job. Retain last successful snapshot, clearly mark stale results, and minimize event metadata.
- [ ] Rerun tests; require PASS. Verify read-only OAuth access to chosen calendars separately from fixture results.
- [ ] Commit with message `feat: read calendar availability and protected windows`.

## Task 5: Confirm ingredient snapshots and compute shopping needs

**Files:** Create backend `inventory.py`, `adapters/storage.py`; `backend/tests/test_inventory.py`, `backend/tests/test_retention.py`.
**Interfaces:** Produces `extract_inventory(owner: OwnerId, upload_id: str) -> list[dict]` (unconfirmed candidates); `confirm_inventory(owner: OwnerId, gathering_id: GatheringId, items: list[dict]) -> dict`; `shopping_for(inputs: PlanInputs) -> list[dict]`.

- [ ] Write tests for duplicate receipt/photo entries, receipt purchase vs remaining quantity, ambiguous units, nonmatching ingredients, manual entries, guest quantities excluded, and bought components included. Assert unconfirmed amounts never subtract. Assert owner/type/size checks and expiration of failed as well as successful uploads.
- [ ] Run `uv run pytest backend/tests/test_inventory.py backend/tests/test_retention.py -q`; expect failure.
- [ ] Implement private uploads (builder limit: 10 MB each, JPEG/PNG/WebP), tested vision extraction and explicit confirmation. Scale known recipe quantities with compatible units only. Delete raw data no later than seven days after extraction; failed/unprocessed uploads expire seven days after upload. Use verified storage cleanup independent of app uptime; if unsupported by candidate storage, resolve before release. Delete early on user request and preserve confirmed entries.
- [ ] Rerun tests; require PASS, including cleanup when no user opens the app. Never add calendar-monitoring jobs for this purpose.
- [ ] Commit with message `feat: confirm ingredient snapshots and shopping deductions`.

## Task 6: Generate and validate a feasible prep schedule

**Files:** Create backend `scheduler.py`; `backend/tests/test_scheduler.py`; `backend/tests/fixtures/schedules.json`.
**Interfaces:** Produces `schedule(inputs: PlanInputs) -> PlanCandidate`; `validate_schedule(inputs: PlanInputs, candidate: PlanCandidate) -> list[ConstraintViolation]`; `suggest_time_adjustments(inputs: PlanInputs, violations: list[ConstraintViolation]) -> list[TimeAdjustment]`.

- [ ] Write tests asserting two 40-minute weekday sessions violate 60 minutes; a reviewed 90-minute override permits 80; concurrent compatible tasks count host presence once; cleanup/supervision count; overnight chilling does not. Assert deadline, 20-minute finishing limit, helper capability/window, oven temperature, air-fryer batches, dependency and storage constraints.
- [ ] Add daylight-saving and cross-midnight tests attributing presence to each local day; unknown critical durations produce incomplete, not feasible. Add a shortfall fixture requiring a validated 30-minute extension; reject it unless explicitly selected, and preserve protected work time and must-haves.
- [ ] Run `uv run pytest backend/tests/test_scheduler.py -q`; expect failure.
- [ ] Implement a bounded deterministic heuristic over task dependencies/resource windows, with a separate validator. Use five-minute scheduling increments, round duration estimates upward and label estimates; impose a search limit and report unresolved conflicts rather than claiming impossibility or global optimality. Separate final checklist tasks from major cooking but reserve their effort/resources. Show specific day/window/task constraints in adjustments; never move personal calendar events.
- [ ] Rerun tests; require PASS and deterministic fixture outputs. Unknown capacities or unsupported prep windows cannot be repaired by fabricated values.
- [ ] Commit with message `feat: schedule prep within daily and kitchen constraints`.

## Task 7: Orchestrate editable menu proposals and final-plan generation

**Files:** Create backend `menu.py`, `agent.py`; `backend/tests/test_menu.py`, `backend/tests/test_agent.py`.
**Interfaces:** Produces `propose_menu(inputs: PlanInputs) -> list[MenuSelection]`; `apply_menu_changes(owner: OwnerId, gathering_id: GatheringId, changes: list[dict], expected_revision: int) -> PlanInputs`; `generate_final_plan(owner: OwnerId, gathering_id: GatheringId, expected_revision: int) -> PlanCandidate`.

- [ ] Write tests for Notion-first retrieval, source-linked discovery fallback, complete vegetarian coverage, must-have preservation, bought vs semi-prepared vs guest work, removing old recipe tasks, changed helper windows, approved time extensions and stale edits invalidating prior plans/approvals. Test incomplete evidence and infeasible must-haves remain visible.
- [ ] Run `uv run pytest backend/tests/test_menu.py backend/tests/test_agent.py -q`; expect failure using fake model responses.
- [ ] Implement one bounded LangGraph workflow: retrieve -> propose -> pause for customization -> rebuild -> schedule -> validate -> return final or adjustments. Persist revisions in application DB across requests; do not leave a graph execution open awaiting human input. Models propose, code validates. Cap at eight tool calls and one schema repair per generation initially; no write tools reachable from the model. Cache source-derived task graphs and reuse unchanged recipes.
- [ ] Rerun tests; require PASS, including duplicate submission and restart after menu review. Compare economical planning models only in Task 10's bounded experiments.
- [ ] Commit with message `feat: customize menus and generate validated final plans`.

## Task 8: Build the mobile-friendly review journey

**Files:** Create frontend `package.json`, lockfile, Vite/TypeScript configuration, `src/api.ts`, `src/App.tsx`, feature folders listed above, `tests/hosting-flow.spec.ts`; modify backend `api.py`.
**Interfaces:** Uses the service functions from Tasks 2–7 through authenticated `/api/recipes`, `/api/inventory`, `/api/availability`, `/api/menu`, `/api/plans` endpoints. Plan response includes revision/hash, evidence, freshness, violations and adjustments. Expose `/api/plans/{id}/approve` and `/api/plans/{id}/apply` in Task 9.

- [x] Screen mockups approved. Implement prep-day selection, editable category counts, Manageable/More generous spread, compact photos/labeled icons and consistent desktop/phone task typography from v7.
- [ ] Write `hosting-flow.spec.ts` asserting edits survive reload, bought dessert removes baking, helper changes update assignments after Generate, extra time needs explicit selection, stale plan disables approval, missing evidence is visible, and no cooking-progress screen appears. Assert 375px viewport keyboard-accessible controls and understandable loading/error states.
- [ ] Run `npm --prefix frontend test -- --run`; run `npm --prefix frontend run test:e2e`; expect missing journey failures.
- [ ] Implement screens using generated API types, editable cards/forms and session timeline. Avoid compulsory chat for structured edits. Phone tasks display ingredient names and scaled amounts without expanding details; test that amounts remain visible at 375px and unknown amounts show needs-review. Extra notes/source detail remain expandable. Final screen includes shopping, who/what/when, equipment, sources, cleanup and finishing checklist; show current plan status, not false percentages. Keep Approve separate from Apply and make recheck available.
- [ ] Rerun unit/browser tests; require PASS and manually inspect mobile layout and keyboard navigation.
- [ ] Commit with message `feat: add hosting proposal and final-plan review interface`.

## Task 9: Approve and safely book the dedicated hosting calendar

**Files:** Create backend `approval.py`, `booking.py`, `backend/migrations/002_operations.py`, `backend/tests/test_booking.py`; modify `adapters/google.py`, `api.py`, frontend booking feature.
**Interfaces:** Produces `approve_plan(owner: OwnerId, plan_id: PlanId, revision: int, content_hash: str) -> Approval`; `apply_booking(owner: OwnerId, approval_id: str) -> BookingResult`; `sync_plan_to_notion(owner: OwnerId, plan_id: PlanId) -> dict` in `adapters/notion.py`.

- [ ] Write tests for no approval/no writes, wrong owner, stale hash/revision, fresh calendar conflict, repeated Apply, timeout-after-success, missing vs already-applied operations, changed remote event and partial failure. Assert Busy events only in persisted hosting calendar, no invitations and no modification of external events. Test Notion sync failure does not erase successful calendar results.
- [ ] Run `uv run pytest backend/tests/test_booking.py -q`; expect failure.
- [ ] Implement transactional approval/operation ledger and concurrency lock. Persist proposal before action; obtain fresh availability and reject material changes. Create/reconcile the hosting calendar once; persist returned ID. Use stable Google-compatible event identifiers and operation keys; reconcile ambiguous responses before retrying. Resume pending operations on explicit Apply/retry, not a monitoring worker. Render per-event status and exact retry action.
- [ ] Sync reviewed gathering/session projections to the existing Notion databases with membership enforcement and recorded success/failure. Notion edits propose changes; a checkbox never authorizes bookings.
- [ ] Rerun tests; require PASS. Run a separately approved live booking check, confirm remote IDs/Busy state and demonstrate safe retry. Do not claim this passed from mocks. Remove test events only with explicit approval.
- [ ] Commit with message `feat: book approved prep blocks with recoverable operations`.

## Task 10: Add cost controls, LangSmith traces and evaluation evidence

**Files:** Create backend `budget.py`, `telemetry.py`, `backend/tests/test_budget.py`, `backend/tests/test_telemetry.py`, all `evals/` files; modify provider adapters and agent entry points.
**Interfaces:** Produces `reserve_spend(owner: OwnerId, request_id: str, estimated_usd: Decimal) -> bool`; `settle_spend(request_id: str, actual_usd: Decimal | None) -> None`; `record_run(metadata: dict, redacted_payload: dict) -> str`; `evaluate_case(case: dict, result: PlanCandidate) -> dict`.

- [ ] Write tests for simultaneous reservations, duplicate request IDs, unknown rates denying paid mode, budget exhaustion preserving saved/manual use, and unpaid calendar/checklist arithmetic. Assert no secrets/raw images/private event text in traces and human waiting time excluded from inference latency.
- [ ] Run `uv run pytest backend/tests/test_budget.py backend/tests/test_telemetry.py -q`; expect failure.
- [ ] Implement conservative reservations before paid calls, bounded output tokens, spend settlement and provider-side caps where available. Include trace/judge/search costs; retain reservation on unknown bill until reconciled. Never promise an exact provider hard cap based only on delayed telemetry. Add LangSmith parent/child traces linked by plan revision, custom tool spans, token/cost estimates and actual booking results. Configure trace volume/retention against verified entitlement.
- [ ] Create 25 cases with stable IDs and explicit expectations covering Tasks 2–9. Use 18 development and 7 held-out scenarios; no exact-menu string matching. Implement code scorers and manual acceptable/needs-changes/unusable labels. Keep model judge disabled by default; optional Jev source-support experiment compares human labels with an economical model using a separately approved spend allowance.
- [ ] Run `uv run python evals/run.py --mode fixtures --split all`; require all hard-constraint/authorization assertions pass and label fixture results. Run `--mode live --split heldout --max-usd <approved-allowance>` only after budget/access verification. Record passed/total, errors, manual ratings, retries, latency and cost per accepted plan; do not fabricate results or substitute judge scores for human reference labels.
- [ ] Commit with message `feat: add budget guards and LangSmith hosting evaluations`.

## Task 11: Deploy the scoped demo and verify the complete journey

**Files:** Create `Dockerfile`, `render.yaml` (only if Task 1 selected Render), `.github/workflows/check.yml`, `docs/runbook.md`, `docs/demo-evidence.md`; modify `README.md` and `docs/budget.md`; create `backend/tests/test_restart.py` and frontend `tests/recovery.spec.ts`.
**Interfaces:** Release uses the same authenticated API/service contracts; no new product features. `/health` reveals readiness only, never credentials or personal data.

- [ ] Write restart/session-expiry tests preserving reviewed menu and operation ledger, provider-disconnect errors, unauthorized access denial and pending booking recovery without duplicates.
- [ ] Run `uv run pytest backend/tests/test_restart.py -q` and `npm --prefix frontend run test:e2e`; expect failure until deployment/recovery handling is configured.
- [ ] Build/deploy only the verified free topology. Persist everything outside ephemeral host disk. Configure TLS, exact OAuth redirects, secret storage, owner allowlist and independent upload cleanup. Document cold start/inactivity/quota limits and recovery; do not add keepalive jobs to conceal them. Use synthetic demo data separate from private account records.
- [ ] Run full backend tests, frontend tests/build, fixture evals and `git diff --check`. Perform hosted browser acceptance: source-linked recipe -> customized Diwali menu -> helper/buy-cook edits -> shortfall adjustment -> final plan -> approval -> Busy blocks verified remotely. Document any unverified stage as a release blocker, not success.
- [ ] Record actual operating-cost forecast at measured usage, balances, hosting limitations, deployment URL, evaluation counts and one failure/fix/retest story. Verify seven-day deletion policy independently of daily app use. Recheck the course deadline from the handout before scheduling submission work; dates in earlier notes are context, not live verification.
- [ ] Commit with message `chore: verify hosted hosting demo and document evidence`. Push/deploy according to the user's execution authorization; do not include secrets or ignored personal setup data.

## Dependency order, coverage and self-review

Execute 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 -> 10 -> 11. Provider configuration precedes live use; fixture-based work can continue if account setup is blocked. Budget reservations and trace wrappers from Task 10 must be integrated before any paid end-to-end run; earlier live smoke checks require a separately bounded, explicit allowance. No background job is needed for calendar monitoring; storage cleanup is independent infrastructure.

PRD coverage: R1–R4 Tasks 2/4/6; R5–R9 Tasks 3/7; R10 Task 5; R11–R13 Tasks 2/6/7; R14–R16 Tasks 4/9; R17–R19 explicitly deferred; R20 Tasks 6/8; R21 Tasks 2/3/9; R22 Tasks 2/4/9/11. Time negotiation Tasks 6–8; budget Tasks 1/10/11; LangSmith/evals Task 10. The five Review Focus items have named tests in owning tasks.

Self-review completed: checked scope through booking, daily-total semantics, source-grounded preparation, helper/equipment dependencies, approval and retry boundaries, provider costs, no hidden monitoring, and deferred execution features. Shared interfaces are defined above; task-specific dictionaries must be promoted to named domain schemas as each feature is implemented and reflected in OpenAPI. No production results, cost guarantees or working integrations are claimed by this plan.

## Execution handoff

Native execution is selected. Implement in this session, with targeted independent reviews after Task 6 and Task 9 and a final whole-branch review. This development choice is separate from the app's one-agent architecture and its $5/month operating budget.

## Approved implementation decisions — October 28

Native execution is approved: one implementer uses Superpowers executing-plans with test-first development, targeted independent reviews of the scheduler and calendar authorization/recovery, and a final whole-branch review. Reuse the private `dsilvadeepal/simmer-and-gather` GitHub repository.

UI/UX is approved: guided Gathering → Menu → Prep plan, editable cards, backward navigation preserving choices, selected prep days and per-day totals, Manageable/More generous menus with editable category counts, compact attributed recipe photos and labeled icons. Laptop and phone share readable task typography; task ingredient quantities remain visible and extra notes expand. Cleanup is a short title/duration. Phone consultation/quick edits are included; cooking progress remains deferred.

Benchmark available Nebius and Fireworks vision endpoints using existing credits. Begin with a bounded development experiment capped at $1 total, no automatic recharge; verify each model ID and published rates before calls. Compare identical labeled images, extraction precision/recall, quantities/units, unsupported claims, latency and normal-rate cost per usable extraction. Distinguish synthetic receipts, public licensed images and any later user-provided samples. A small test yields a provisional selection, not general accuracy. Prefer the cheapest model meeting the accuracy/abstention gate; keep manual correction and unknown amounts. No personal uploads are required to continue building, and no live winner is claimed before results. Jev remains an optional text decision experiment, not the vision extractor.

## Build status and Google setup — October 28, 2026

The implementation plan is ready and execution has started; this is not a declaration that the app is finished. Tasks 1–9 have local implementation slices and tests, with remaining integration and acceptance work. Task 10 (cost controls/evals/tracing) is in progress; hosted release and final whole-branch review are outstanding. Unchecked task steps remain acceptance requirements, even where local code already exists.

- [x] Create dedicated Google Cloud project `keen-autumn-513015-c5`, without billing linkage.
- [x] Enable Google Calendar API with approved terms.
- [x] Create OAuth app configuration in External / Testing mode with approved User Data Policy.
- [x] Create Web application client with callback `http://localhost:8000/api/google/callback`; keep credentials local, Git-ignored and owner-readable only.
- [x] Add the owner as sole test user and prepare the real local OAuth server.
- [ ] Owner completes Google sign-in and consent (account chooser opened; consent pending).
- [ ] Verify token exchange, encrypted storage, calendar listing and selected-calendar availability reads.
- [ ] Verify reviewed plan approval and Busy booking in the dedicated app calendar, without changing unrelated events.
- [ ] Add the exact hosted callback only after the deployment host is selected.

Detailed connection steps and current evidence: `docs/google-oauth-setup.md`. Vision comparison: `docs/vision-benchmark.md`. Remaining app work includes runtime Notion/model/vision wiring, UI refinements, broader live evaluation, final review and deployment.

GitHub: https://github.com/dsilvadeepal/simmer-and-gather (private, verified October 28). Local implementation branch: `build/hosting-demo`. Implementation branch was pushed on October 28. Subsequent work is committed and pushed in verified increments; the main branch is not merged automatically. Never include `.env.google` or other credentials.

October 28 continuation: runtime text-model budget wiring, calendar checkbox picker, recipe review form, Google refresh-race recovery, CI workflow, Docker packaging and operating runbook added. Backend 54 tests, frontend 3 tests, production build and 25 fixture eval checks pass; Docker image builds locally. Live integrations and final acceptance remain incomplete.

Recipe preview now uses the explicitly enabled, budgeted text model for candidate steps; original source survives failures and candidates never become automatically reviewed. Latest local backend run: 55 passed. Existing Deepal Old project databases will be reused; app-owned Notion connection is awaiting browser sign-in.

### Live connections verified — October 28, 2026

The app-owned Notion connection is authorized only for the existing HR Recipe Library, Gatherings and Prep Sessions databases in Deepal Old. All three data sources returned successful read responses; all are empty. Recipe browsing now runs through the scoped app MCP server and opens candidates for source import/review. A Notion Planning Ready flag never bypasses application recipe validation. Reviewed recipe publication and gathering/session projections back to Notion remain to be implemented. No unrelated pages were granted access. Credentials are local, ignored by Git, owner-readable only.

Google OAuth and listing of 11 accessible calendars verified. The user chooses calendars in the app before availability checks. No real calendar events have been created. Local production server now loads both integrations; this is not a hosted deployment.

### Reviewed Notion saves and recipe collection — October 28, 2026

Explicit Save to Notion actions now export the locally saved reviewed recipe revision or the current validated plan and its prep-task pages. The owner and revision/hash are checked server-side. Saving to Notion does not approve Calendar writes. Immutable pages preserve manual Notion edits. A local export ledger serializes attempts; uncertain POST outcomes reconcile by a deterministic page title rather than creating again. Preflight/definitive rejection is retryable. Missing, moved or archived saved pages are reported without silent recreation. A live synthetic recipe/plan/session save and repeat-save check succeeded; all four QA pages were archived afterward.

The existing Recipe Library now contains 35 curated candidates: 15 Indian/Diwali plus 20 Thanksgiving/Christmas (12 Well Plated, eight With Wendy and Shannon/previously Platin It With Wendy). Source links, publisher ratings and vote counts are retained where verified. 27 have structured ingredient/timing metadata; eight Wendy pages are source-link only because the importer received HTTP 403. All 35 are Needs details and Planning Ready=false. See docs/recipe-collection.md. Recipe-level total time is not task-level active time or storage evidence.

Added user-triggered online link discovery with daily query caching, three-result limit and $0.008 basic-search reservation against the shared $3 monthly AI/search envelope. Runtime key comes from the existing authorized tool setup, stored privately. One live search verified; no background searches or automatic imports. Current rates checked at https://docs.tavily.com/documentation/api-credits . Added reviewed-collection menu suggestions with explicit preview/add action. Fixed HTTPS redirects with destination revalidation and nested HowToSection extraction; live Paneer Tikka import verified without automatically reviewing the recipe.

Remaining release work: runtime vision/upload retention, broader real-recipe planning/evals, full LangSmith runtime integration, hosted topology/entitlement verification and final branch review. No hosted deployment or real Calendar booking acceptance is claimed.
