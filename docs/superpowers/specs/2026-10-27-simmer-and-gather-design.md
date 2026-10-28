# Simmer and Gather — product and technical design

Date: October 27, 2026. Status: **Approved by Deepal on October 27, 2026; implementation planning authorized.**
Companion: ../../../PRD.md. Implementation plan: ../plans/2026-10-27-hosting-demo.md. App implementation has not started.

## Intent and selected approach
Help a host enjoy guests without exhausting work evenings or cooking at the last minute. First user is Deepal; first demonstration is a Diwali gathering for approximately fifteen friends and family, with vegetarian and nonvegetarian dishes, drinks and dessert. Thanksgiving, Christmas and a three-year-old's birthday are subsequent scenarios, not separate products.

Approaches considered in conversation:
1. Notion-led planner: smaller interface, but awkward phone execution and change approval.
2. Focused hosting app with Notion recipe knowledge: coherent mobile planning, cooking and review experience. **Selected by Deepal.**
3. Broader household food planner: adds ongoing pantry, weekly meals and family accounts; excessive initial scope.

## Confirmed demo scope — October 27 clarification
The demo ends with the final hosting prep/cook plan and approved calendar booking, after an explicit customization stage:
1. Generate an initial menu and indicative preparation workload from the gathering brief, recipes, schedule and saved preferences.
2. Let Deepal swap recipes, retain must-haves, choose cook versus bought/prepared alternatives, and select helpers with availability windows (including no helper). Existing defaults are starting values, not fixed assignments.
3. On Generate final prep plan, rebuild affected ingredients, quantities, tasks, dependencies, equipment allocations and helper assignments. Remove obsolete work; include real air-fryer/oven work for semi-prepared purchases. Validate against current calendar availability, protected times, preparation limits and source-supported storage windows.
4. Display final menu, shopping/bought items, dated sessions with who/what/when, equipment needs, make-ahead evidence, cleanup and final minor-task checklist. Clearly expose unresolved inputs or infeasibility; request a tradeoff rather than inventing a feasible result.

5. Review and approve the exact prep-block proposal, recheck availability, then create Busy events in a dedicated “Simmer and Gather” calendar within the user’s Google Calendar account, visible alongside the primary calendar. Persist and reuse the calendar ID across gatherings. Show confirmed bookings and any partial failures honestly. This booking result is the demo endpoint. Phone task completion, percentage progress and running-behind recovery below are retained as post-demo design, not implementation requirements for this demo. Calendar reads, manual recheck and approved Busy-block booking are in demo scope. No background monitoring or alerts. A material customization invalidates an older generated plan until regenerated; generation itself does not authorize external writes.

Weekly meal prep is a future extension of the same recipes, inventory, resource scheduling and time preferences. It needs multiple meal deadlines, portions/leftovers across days, variety preferences and appropriate storage windows rather than the single hosting arrival deadline. Keep shared planning concepts reusable without building a second mode now.

## Confirmed behavior
### Reusable profile and gathering overrides
Save kitchen equipment/capacities, helper capabilities, preparation limits, protected time rules and calendar selection. Initial equipment includes oven, stovetop, air fryer and Instant Pot. Capacity and oven temperature conflicts and air-fryer batches are important. Unknown capacities remain unknown until clarified. Defaults are copied into each gathering; overrides do not silently change the reusable profile.

Default preparation limits: one hour on a work evening and two hours on a weekend, including cleanup. These are maximum desired effort windows, not a requirement to consume all free time. Deepal chooses the earliest preparation date. Protect work, family and sleep even when calendars show free. Default major-cooking/cleanup cutoff is one hour before arrival; allow only 15–20 minutes of hands-on finishing during that hour, adjustable per gathering. Proposed implementation default: 20 minutes, leaving forty minutes genuinely unallocated. Confirmed October 27: these limits are daily totals covering the whole preparation session, including cleanup and required supervision/presence. Default one hour per work evening and two hours per weekend day. Passive overnight chilling does not consume a session. The user can adjust limits for each gathering, including individual-day exceptions, and split the daily allowance into shorter sessions. Count the union of host-required session intervals so concurrent compatible tasks do not double-count time; helper work does not erase host supervision requirements. Store timezone explicitly and convert calendar timestamps consistently, including daylight-saving transitions.

### Menu and guest requirements
Suggest a complete menu first. User can swap dishes, mark must-haves and choose bought prepared or semi-prepared starters/desserts. No spending budget or cost optimization in demo. Record vegetarian count, other dietary restrictions, allergies and preferences per gathering; unknown is not confirmed none. Shared vegetarian dishes may serve everyone; vegetarian guests must have a complete meal. Use editable target servings per dish, accounting for courses and contributions, not a naive equal split or universal portion guarantee.

Preserve must-haves. If they make the plan infeasible, explicitly request a tradeoff; do not replace them silently. Prefer rearranging unfinished work and assigning available helpers, then simpler recipes or optional-dish removal, then prepared components as appropriate, always presenting meaningful changes for approval.

Each menu item has source: host-cooked, bought prepared/semi-prepared, or guest contribution. Deepal manually records contributor, dish, servings, confirmation, expected arrival and warming/equipment needs. Confirmed contributions count toward coverage; tentative items stay visibly uncertain. Guest cooking does not enter host progress. Bought food can still require real preparation, batch cooking and equipment reservations. Final small hosting tasks are a separate checklist.

### When available preparation time is insufficient
Attempt rearrangement within current limits first. If no feasible candidate is found, surface a specific bottleneck before replacing optional dishes: affected tasks/day, current allowance, proposed extra session minutes and contiguous window, equipment/helper constraints, and the reason this adjustment could help. Label duration estimates and avoid claiming a globally minimal shortfall from a heuristic scheduler. Show a validated alternative when available; otherwise clearly label conditional or unresolved suggestions. Extra aggregate hours do not solve all dependency, storage or resource conflicts.

The host can accept a per-day allowance increase, add/move availability, choose an earlier start consistent with recipe windows, change helpers or select simpler/bought dishes. Preserve saved defaults unless explicitly changed. Protected times and the pre-arrival buffer remain hard constraints until explicitly edited by the host. Do not move personal/work calendar events: explain that the host can rearrange those externally, then use Recheck my plan. Recompute the schedule against fresh inputs and require approval of the resulting booking revision. Never auto-relax constraints or book conditional/infeasible plans. Show these choices in the active planning flow; no notifications are introduced.

Evaluation must cover daily-total enforcement across split sessions, concurrent task time counting, required supervision, quantified time-change proposals, rejected and accepted adjustments, unchanged protected time, fresh calendar conflicts and approval invalidation. A proposed 30-minute extension is illustrative until validated for that scenario, not a general promise.

### Recipe collection and ingestion
Notion recipes first; discover online if no suitable fit. Candidates display source links, why suggested and missing information. Deepal reviews candidates and saves chosen recipes. Do not auto-approve a discovered dish or claim it was personally tested.

Import is a bounded workflow, not a second agent: fetch accessible URL -> extract -> normalize -> source-check -> preview -> save through Notion MCP. Support pasted text when fetch fails. Support manual Process recipe inbox for Notion URLs; background inbox monitoring is deferred. User need not rewrite every recipe: automate curation and escalate consequential gaps.

Recipe provenance includes source URL/author, fetched time, structured ingredients/units/servings, original stated durations, step evidence, review stage and version. Task graph includes prerequisites, active duration, elapsed duration, equipment/capacity/temperature, presence/supervision needs, make-ahead window, storage conditions, finishing and quality constraints. Label source-stated, estimated, unknown and personally measured separately. No invented make-ahead/storage limits. Use explicit recipe guidance or separately cited applicable authoritative guidance; if unsupported, flag, clarify or choose another recipe. More calendar time does not justify earlier preparation that harms the dish. Imported publisher text/images require appropriate reuse rights; preserve links and attribution. No bulk copying assumed.

### Inventory and shopping
Per-gathering inventory snapshot only. Upload receipts/photos, inspect extraction, correct, add manually and confirm. Receipt proves purchase, not remaining stock. Deduplicate or ask about overlap; don't sum photo and receipt blindly. Subtract only confirmed compatible quantities/units. Unknown units/amounts block precise deductions rather than being converted arbitrarily. Shopping list consolidates host needs and bought components, excluding guest-supplied quantities. Do not infer shelf life from a photo. Reconfirm stale inventory when relevant.

### Helpers
Profiles store parent/user-approved capabilities and supervision rules. Son independently handles measuring, fetching, peeling eggs, stirring, air-fryer loading/unloading/batches and plating/transferring; cutting excluded per user. Never infer additional capabilities. Availability is specific to session/gathering and can be zero, thirty minutes or an hour. Adults have their own editable capabilities. Respect full task duration, supervision costs, equipment contention and handoff dependencies; never count a child as a fractional adult or assume all tasks speed up with help. Deepal reviews assignments.

### Calendar and notifications
User chooses read calendars. Dedicated Simmer and Gather calendar receives Busy preparation blocks after review. Every creation/update/deletion requires approval of exact revision and recheck immediately before execution. Busy is a reservation, not prevention of external invitations. Only app-created events are mutable; persist calendar/event IDs and idempotency keys. Do not copy unrelated event descriptions into plans or logs.

Check selected calendars when the authenticated user opens the app and through Recheck my plan. Also fetch fresh availability immediately before calendar writes. No background calendar checks, scheduled monitoring jobs, alerts, emails or quiet-hour settings. Coalesce duplicate page-load requests; check active gatherings within their preparation horizons. Show last successful check and ordinary plan status; failed/disconnected checks must show stale or unavailable state, never imply availability.

Compare intervals deterministically without model calls. Exclude the same plan's owned prep blocks from external conflicts but include other gatherings' reservations. Manual edits to owned blocks become discrepancies for review, not silent restoration. Request AI replanning only when the user asks to resolve a conflict. Existing events remain unchanged until exact revision approval. Upload-retention housekeeping remains necessary but is independent of calendar monitoring; use storage expiry or bounded cleanup, not an always-running calendar worker.

### Phone execution and progress — post-demo
Mobile checklist per session and cross-menu overview before/after sessions. Break recipes into meaningful preparation/cooking stages. Progress measures prep/cooking completion, not readiness to serve. Warming, table transfer, utensils and final small tasks are separate and do not reduce completion. Garnish counts in cooking only when part of that dish's chosen preparation stages. A dish can be 100% cooked while warming remains.

Proposed formula: completed prep/cooking stage effort divided by all prep/cooking stage effort, using reviewed active-minute estimates; display approximately, not false precision. If durations unknown, show completed stages instead of a percentage. Lock weights to recipe-plan revision, preserve completed stage IDs on replans, and explain any new work. Overview total is weighted host cooking work, not average dish percentages; excludes guest contributions and already-ready purchases. Include helper-performed stages because they advance the same work. Track elapsed/presence dependencies independently: a cooking step does not complete until user confirms it, even if predicted time elapsed.

Running behind accepts delay and current completion. Rearrange unfinished work across available capable helpers and equipment first. If infeasible, suggest simplifying/dropping optional items while protecting must-haves. Approval required for changed plan/calendar. Unchecked does not prove late. Completed work stays completed. Final checklist groups warming, drinks, serving dishes, table transfer and spoons; it still has an aggregate time/equipment allowance, not obsessive microtracking.

## Proposed technical architecture — builder recommendations, not previous user commitments
Responsive React/TypeScript frontend; Python FastAPI backend with one LangGraph planning agent. PostgreSQL for durable business state and checkpoints; managed object storage for uploads. Hosting must fit the confirmed $5/month total operating ceiling after course credits. Replit remains a candidate only if its actual account entitlement and all operating costs fit; otherwise compare free-tier hosting before choosing a runtime. The Python/PostgreSQL recommendation is provisional pending this feasibility check. Authentication restricts launch to Deepal's account; ownership keys on all entities preserve a later multi-account path without building invitations or family onboarding now.

Agent tools: retrieve_recipes, discover_recipe_candidates, import_recipe_preview, inspect_inventory, read_availability, propose_menu, validate_schedule, propose_revision and request_approval. Pure calculation/scheduling tools own arithmetic and constraints. External writes run through application services after verified approval, not unrestricted model calls. Bounded retries, tool/time budgets and structured outputs. A model call for image extraction or evaluation is not another autonomous agent.

### Data ownership
- Notion: editable recipe knowledge and readable gathering/session projections.
- Application DB: user profiles, per-gathering overrides, ingredient snapshot, typed recipe/task versions, menu quantities, dependencies, schedule, completion, approvals, integration IDs, sync jobs and calendar-check results.
- LangGraph checkpoints: unfinished conversational work, not source of truth for approval.
- Google Calendar: actual reservations/appointments.
- LangSmith: redacted traces and evaluation results.

Normalized recipe snapshots reference Notion page and last-edited version. Refresh before a new plan; if edited after approval, mark affected plans for review and preserve their prior snapshot. Gatherings/session fields edited in Notion enter as proposed changes, not authorization. Show sync state (pending/synced/failed) and retain retries; remote save failure must not claim success. Database status alone cannot authorize a write.

### Existing Notion area
Reuse the three databases and root recorded in local host-ready-notion-setup.json; never recreate or mix with existing workspace planners. Recipe Library, Gatherings and Prep Sessions exist with internal relations and views. Existing budget fields are unused, not silently deleted. Detailed task/ingredient tables need normalization during import; Notion's current fields alone cannot prove scheduling readiness. Technical allowlist of data-source/database IDs and per-page membership enforcement wraps MCP. No unrestricted workspace search or access to unrelated pages. Broad OAuth permission must not be represented as page-scoped security. Check connector limitations before relying on full enumeration. If hosted MCP cannot provide required bounded retrieval, propose a scoped API-backed MCP adapter rather than silently swapping integrations.

### Schedule validation
Use explicit task dependencies, eligibility windows, release/finish times, non-preemptible cooking and batch constraints, person availability/attention, shared equipment and temperature compatibility. Cleanup consumes host capacity. Unattended work consumes equipment and any required presence; it does not disappear when active minutes end. Recipe storage limits constrain completion-to-serving interval. Serialize resource conflicts and account for transitions/buffers. A bounded heuristic scheduler is sufficient initially: return a feasible candidate or specific conflicts, not a claim of global optimality. Unknown critical timing yields conditional/incomplete status, never verified feasibility. Run validation after every meaningful change.

### Revision transaction and recovery
Maintain monotonic revision plus content hash and input versions. Approval binds to exact proposed menu/tasks/calendar diff and expires on material edits. Apply with durable outbox and stable operation IDs. Recheck calendars, fail closed on stale approval, record each write result. Partial calendar success is visible; retry only missing operations after reconciling remote IDs. No all-or-nothing claim across providers. Prevent concurrent applies with revision locks. Cancellation of gathering proposes removal only of its owned events and removes it from active-gathering checks after approval.

## Tools and credits — tracker read October 27; balances not checked live
Source: parent folder Course-Credits-and-Tools-Tracker.md.
| Tool | Decision and rationale | Recorded entitlement / caveat |
| --- | --- | --- |
| Replit | Preferred host, database/object-storage capabilities to validate | Active month; cancel-by Nov 6; confirmed $5/month total cap; paid renewal is not assumed affordable |
| Nebius | First model-provider candidate; exact tool-calling and vision models selected by small tests | $25 received, recorded non-expiring; remaining balance unverified |
| Fireworks | Alternative candidate, no automatic paid fallback | $15 redeemed; expiry and remainder unverified; Oct 21 was redemption deadline |
| LangGraph | One-agent workflow, checkpoint and approval pause | Open source; not paid with LangSmith credits |
| Notion MCP | Required knowledge integration | Existing account; app OAuth/access test still needed |
| Google Calendar API | Availability, dedicated calendar and owned events | OAuth credentials/scopes and deployment consent setup needed; chat connection is not app credentials |
| Tavily | Online discovery/accessibly extracted source content | $25/3,125 add-on plus 1,000 monthly recorded; expiry/balance unverified |
| LangSmith | User-selected tracing, datasets, experiments and human review | $100 received, expiry Nov 20 2027; billing setup unclear |
| Langfuse | Not integrated in demo; LangSmith selected | Active discounted Core; final renewal needs verification |
| Mem0 | Defer; structured preferences belong in app DB | Starter three-month offer believed; renewal unconfirmed |
| Pinecone | Defer; bounded Notion retrieval initially | Starter; Builder $40 promotion requires paid upgrade, do not upgrade |
| LlamaIndex | Defer unless document ingestion requires it | 50,000 credits recorded |
| Keenable | Search alternative if needed; no duplicate search stack | 100,000 monthly free requests recorded; $500 promotion not visible |
| ElevenLabs | Defer with voice | Offer unclaimed |
| Toloka / Tendem / Granola | No demonstrated initial need | Available/offered per tracker; do not add merely to use credits |
| ChatGPT Pro | Development assistance, not app inference budget | Subscription does not establish API credit |

Email integration is removed from the initial scope following the user's latest preference. No sender service, domain purchase, email OAuth scopes, alert deduplication pipeline or quiet-hour policy is needed. Verify balances before live tests; no paid fallback or automatic recharge without agreement.

## Security and operational scope
OAuth tokens server-side encrypted; no browser secrets. Validate URL imports against private-network/redirect abuse; treat retrieved pages as data, not instructions. Scope uploads by owner and limit type/size; confirmed raw-upload retention seven days after successful extraction, with explicit delete control; retain the confirmed ingredient list. Failed extraction retention still needs a bounded implementation policy. Redact receipts, calendar metadata and child identifiers from traces; use generic helper labels for public demo. Private personal mode and synthetic demo dataset are separate; no public route exposing real accounts. Pin owner approval actions to authenticated session, prevent CSRF and replay. Maintain disconnect/delete controls. No external messages in initial scope.

## Evaluation and demo evidence
LangSmith is confirmed as the sole tracing/evaluation platform for this demo. Its recorded credit does not establish remaining balance or enabled features; verify account setup before paid runs. No Langfuse integration is planned.

### Dataset and offline experiments
Create approximately 25 versioned scenarios with gathering brief, recipe/source snapshots, calendar availability, equipment, helpers, inventory and user customizations. Reference outcomes describe invariants and acceptable behavior, not an exact menu or phrasing. Include: faithful extraction; unknown timings; unsupported make-ahead; inventory duplicates; unit conversion; dietary coverage; oven/air-fryer constraints; protected time; partial/zero helpers; final-hour limits; must-haves; tentative potluck and warming; recipe swaps; cook-to-bought conversions; stale-plan invalidation; changed availability; stale approvals; duplicate retries; partial provider failures.

Use deterministic calendar fixtures and fake external-write adapters for repeatable experiments; model calls may be live under a bounded evaluation budget. No offline experiment writes to personal calendars. Conduct a separate controlled end-to-end test of approved booking in the dedicated calendar and verify remote event IDs/state. Fixtures, simulations and live checks must be labeled separately.

Run baseline and candidate prompt/model versions against identical data. Keep development examples separate from held-out evaluation cases; repeat selected cases to assess variability. Retain the dataset version, application revision, prompt/model configuration and recipe versions. Add sanitized real failures as regression cases rather than silently changing expected answers to match the model.

### Evaluator responsibilities
- Code: validate overlap, dependencies, equipment capacity, preparation limits, serving coverage under explicit assumptions, helper capabilities/availability, preservation of must-haves and host edits, removal of obsolete work, exact approval binding, destination calendar, retry idempotency and partial-write reporting. Evaluate final plans and relevant intermediate tool outputs.
- Human: Deepal reviews a small representative set for practical workload, clarity and willingness to follow the plan; record acceptable / needs changes / unusable with specific reasons. Review ambiguous source claims against their evidence. Ratings assess practicality, not a claim of verified food safety or timing.
- Optional AI judge: assess recipe-source support or explanation quality with a defined rubric and source excerpts. Validate judge agreement/errors against human labels. Jev may be compared with an economical LLM for supported / contradicted / insufficient-evidence judgments; neither is ground truth. Do not use an AI judge for exact arithmetic or calendar authorization.

### Traces and actual-use feedback
Trace the initial proposal, host customization, task rebuilding, schedule validation and final plan, then link the later approval/booking execution through plan ID and revision. Do not treat human waiting time as model latency. Capture bounded/redacted inputs and outputs, source IDs/versions, tool results, model/prompt version, validation failures, latency, usage, estimated cost and provider outcomes. Explicitly instrument non-LLM tools and Jev if used; custom-provider costs may need explicit accounting. Trace metadata does not itself authorize a write.

Exclude secrets, raw uploaded receipts/photos, unrelated calendar titles/descriptions and identifying helper details. Use synthetic data for public demonstrations. Add code scores automatically, route selected failures/ambiguous outputs to human review, and attach feedback to the corresponding run. Online evaluation means evaluating actual app runs, not periodically checking calendars. Keep paid online judges off by default or tightly sampled under a separate budget; offline experiments and manual review are the initial priority.

### Evidence and release criteria
Proposed release gate: all defined hard-constraint and authorization cases pass; representative human-reviewed plans have no unresolved blocking practicality issue. Report passed/total counts separately from source-support errors, review/abstention rates, human ratings, latency and cost per accepted plan (including repairs). Do not claim general reliability from a small test set. A real cooking trial remains necessary to validate actual effort estimates; it is not part of the demo endpoint. No evaluation results exist yet.

Show a failing example, trace-localized cause, correction and rerun in the course evidence. Execution-progress and running-behind recovery tests remain deferred. References: [LangSmith evaluation workflows](https://docs.langchain.com/langsmith/evaluation-types) and [evaluation capabilities](https://www.langchain.com/langsmith/evaluation).

Demo sequence: source-linked import -> review/save to Notion -> Diwali brief and calendar availability -> initial menu/workload proposal -> host swaps recipes, selects available helpers and chooses buy/cook alternatives -> optional inventory confirmation -> Generate final prep plan -> final menu, shopping and validated prep/cooking schedule -> review and approve blocks -> fresh availability check -> Busy blocks in the dedicated hosting calendar -> confirmed booking results. Stop here. Evaluation evidence can accompany the submission without extending the product journey into cooking execution. Explicitly label fixtures/simulated inputs. Demo evals prioritize recipe swaps, changed helper windows, buy/cook conversions, stale-plan invalidation and scheduling constraints, approval enforcement, duplicate-write prevention and partial booking failures; execution/progress/recovery cases are deferred.

## Scope, risks and approval
The user explicitly narrowed the demo to initial proposal, customization and final hosting prep/cook plan. Imports/discovery, inventory uploads, scheduling, helper and potluck support and on-open/manual calendar reads remain planning capabilities. Phone progress and execution recovery are post-demo; approved booking in the dedicated hosting calendar is included. Further reductions require an explicit decision. Course submission Nov 6 11:59 PM Pacific, shortlist Nov 8, live demo Nov 10 per earlier handout/email review. Hosted account setup and scheduling-engine validation may be critical path. Design approval received October 27; Superpowers writing-plans is the current step.

Confirmed operating decisions: $5/month total after course credits, calendar checks on app open, manual request and before calendar writes, no alerts, and seven-day raw-upload deletion after extraction while retaining confirmed ingredients. Preparation-limit semantics are confirmed: whole-session daily totals, adjustable per gathering. First actual gathering date/time, sources and precise capacities are onboarding inputs, not reasons to invent values in this design. Exact provider models, scheduling library and UI styling are builder decisions after documented capability checks. Screen mockups and typography were approved October 28.

## Technical references checked October 27
- Notion MCP and OAuth: https://developers.notion.com/guides/mcp/overview
- Google Calendar change notifications: https://developers.google.com/workspace/calendar/api/guides/push
- Replit deployment choices: https://docs.replit.com/features/publishing/deployment-types
These establish available platform concepts, not account entitlement or working integration.

## Builder review
A separate reviewer checked this draft against the conversation. Agreed requirements were preserved. The reviewer flagged daily versus per-session capacity and hands-on versus required-presence duration; Deepal has now confirmed whole-session daily totals including cleanup and supervision, with per-gathering overrides. Subsequent user answers confirmed the $5/month cap, on-open/manual checking without background monitoring or alerts, and seven-day raw-upload retention. Additional-time negotiation is now explicitly in scope before final-plan generation and booking.

## Budget feasibility update
A $5/month ceiling is a design constraint, not an achieved cost estimate. Do not assume a paid Replit subscription fits. Compare free-tier hosting/database/storage and account for model/search costs after promotional balances run out. On-open/manual conflict detection should use deterministic calendar comparisons; invoke the planning model only on a meaningful change or user request. Cache approved recipe extraction; bound model tokens and discovery calls; stop paid operations before budget exhaustion while preserving read/checklist/manual use. Provider caps and conservative local accounting are needed; do not promise a universal exact hard cap from delayed billing telemetry. Cloudflare Workers free tier and free-tier storage are candidates, not verified replacements for the proposed Python agent runtime. Sources checked: https://developers.cloudflare.com/workers/platform/pricing/ ; https://resend.com/pricing ; https://replit.com/pricing . Final all-in deployment estimate remains required before stack approval.

## Operating cost priorities — October 27 scope revision
Largest likely fixed expense: paid hosting/deployment and managed database subscriptions. Largest variable expense: planning/replanning model calls, vision imports and model-graded eval runs; actual mix requires measurement. Search/extraction should fit existing credits/free allowances at modest use, but enforce limits. Prefer saved recipe/task snapshots, bounded candidates, compact model context and deterministic calculation/validation. Calendar reads/checklist updates must not trigger LLM calls. Cap paid AI usage with conservative reservation accounting; pause paid actions before budget exhaustion and preserve saved/manual functions. Email removed. Suggested $5 envelope is a target, not provider pricing: $0 infrastructure if compatible free tiers work, at most $3 model/search spend, $2 headroom. If fixed infrastructure cannot fit, compare architectures before implementation rather than conceal costs or reduce agreed behavior silently. Development/evaluation usage is separate from recurring operation and must also be budgeted explicitly.

## Model routing proposal — October 27
One agent can call different model types without creating multiple autonomous agents. Correction following the user-provided TypeSafe reference: System One here refers to TypeSafe’s class of models returning typed, probabilistic decisions from predefined answer spaces, rather than generated text. Jev is its model, not shorthand for a small or low-deliberation LLM. Evaluate Jev as a bounded decision tool; adoption and account access remain unconfirmed.

| Work | Proposed execution |
| --- | --- |
| Calendar overlap, portions/unit arithmetic, progress, permissions, deduplication and resource validation | Deterministic code; no LLM |
| Parse available structured recipe metadata | Ordinary parser first |
| Categorize course/cuisine or already-extracted steps using fixed labels | Evaluate Jev Choice, including an unknown/needs-review option, against an economical LLM baseline |
| Normalize text ingredients and extract explicit steps/equipment | Parser or economical generative model with schema validation and source references; Jev does not generate arbitrary strings |
| Receipt/pantry images | Tested vision model, then user confirmation; never infer hidden quantities |
| Break recipe into dependency tasks and extract explicit make-ahead instructions | Start with economical model; validate source coverage and dependencies; escalate ambiguous cases or request clarification |
| Propose complete menu, reconcile competing preferences and explain complex replans | Lowest-cost model that passes planning evals; stronger reasoning model only where tests justify it |
| Storage limits, allergy suitability or absent evidence | Verify applicable source or ask; a stronger model cannot manufacture missing evidence |

Use a static task-to-model map initially, not another AI router. Bounded repair (proposed one attempt), then evidence-based escalation for persistent schema failure, missing source coverage, unresolved dependency contradictions or repeated infeasible proposals. Do not use an LLM’s self-reported confidence as the trigger. Jev’s trained decision probabilities are distinct, but any probability-based routing requires task-specific calibration tests and validated thresholds. Escalation remains inside the approved provider/budget envelope; otherwise surface the issue for review. Measure end-to-end cost per accepted result, including retries, latency and grounding quality. Benchmark economical versus stronger configurations on the same saved scenarios before deciding which is cheaper in practice. Cache extraction by source/version; invalidate when source or reviewed record changes. No flagship API subscription is assumed required.

Provider references: https://github.com/nebius/token-factory-cookbook/blob/main/models/README.md and https://docs.fireworks.ai/ . Catalog availability, tool/vision support and remaining balances require account-level checks before implementation.


### Jev candidate and evaluation — researched October 27
Official documentation lists Jev 1.14 (`jev-1.14.0`, released October 14) as newest, with text-only inputs and Choice, Score and Noul decision primitives. Proposed first experiment: classify existing recipe stages and assess whether a source explicitly supports a proposed make-ahead instruction (supported / contradicted / insufficient evidence). This is evidence triage, not food-safety certification. Keep source excerpts attached through extraction; Jev cannot generate explanations or missing preparation steps. Vision remains a separate model. Scheduling, equipment capacity, permissions and calendar writes remain deterministic and approval-gated.

Test labeled source/claim pairs, ambiguous steps, missing storage guidance and conflicting evidence. Compare Jev with an economical LLM on classification errors, unsupported claims incorrectly accepted, abstention/review rate, latency and cost per accepted result. Tune routing thresholds on development examples and report results on held-out examples; do not assume 0.5 is suitable or treat model-as-judge output as ground truth. Pin the tested model version. Retain a manual-review path if unavailable or inconclusive. No app-specific results exist yet.

Official price: $0.042 per million input tokens; output free. Illustratively, 1,000 requests averaging 2,000 total billed input tokens cost $0.084, excluding generative/vision calls, search and hosting. Jev is not recorded in the course credits tracker; verify access and billing terms before adoption. It is optional, not a new paid dependency already selected.

Sources: [announcement](https://typesafe.ai/blog/introducing-system-one-models-and-jev), [current models/pricing](https://docs.typesafe.ai/models), [decision primitives and limitations](https://docs.typesafe.ai/concepts/system-one). A September 29 [independent preprint](https://arxiv.org/abs/2609.37647) evaluates 1.13, not 1.14: promising Choice calibration, but binary thresholds and rubric judgments require care. Typed valid outputs do not guarantee semantic correctness.


## UI/UX discovery — October 28
Confirmed: laptop-first planning with phone consultation and quick changes; guided Gathering → Menu → Prep plan, editable cards and preserved choices when going back. Visual preference is warm/inviting plus clean/practical, uncluttered with readable kitchen phone views. Superpowers interactive mockups were approved October 28. They use illustrative dishes/timings, make no external writes and do not demonstrate scheduler feasibility. Phone consultation does not add live completion tracking.


## UI refinement — October 28
Show prep start date, individually selectable prep days and editable daily allowances in Gathering; distinguish total allowance from actual calendar availability. Default to a manageable menu recommendation with a More generous option and editable counts for starters, mains, sides, desserts and drinks. Counts include bought and guest-contributed items. Recommend based on occasion, guest/dietary mix, prep horizon, helpers and resources; do not hard-code two mains or fixed category counts. Count changes propose additions/removals for review, preserve must-haves and invalidate affected plans; re-evaluate quantities, dietary coverage and workload. Prototype values are illustrative, not validated recommendations.


## Recipe imagery and actionable session details — October 28
Use small source-permitted recipe photos in menu/picker cards and recipe details, with attribution and an accessible fallback. Do not imply an illustrative photo belongs to an imported recipe. Use restrained SVG icons alongside text for calendar, time, helpers, equipment, buying, guest contributions and must-haves. Session views must name the selected recipe and actionable step, estimated time window, assigned person, equipment, scaled quantities and dependencies; show source-supported storage/make-ahead guidance where applicable. Keep ingredient quantities directly visible beside each task on phones; only extra recipe notes and source detail remain expandable. Generic session headings are summaries only, never substitutes for recipe-specific tasks. Recipe edits regenerate affected steps. No live progress tracking is added.


Phone task presentation confirmed: show task-specific ingredient names and scaled quantities directly below the action, with amounts aligned for easy scanning. Extra recipe notes, provenance and additional instructions can expand. Critical safety/storage instructions needed to perform the task stay visible. Unknown quantities are explicitly marked for review, never fabricated. Mockup quantities are illustrative and not validated for cooking.


UI refinement: obvious tasks such as cleanup appear as a concise title and duration, without supply lists or instructional prose. Reserve visible ingredients and detailed actions for recipe-specific work. Phone typography uses a restrained sans-serif hierarchy: 18px task titles, 16px action/ingredient text, 13–14px metadata; keep quantities bold, maintain comfortable spacing and support text zoom. This visual direction is approved.


Typography direction approved: cleaner task hierarchy and concise obvious tasks. Apply the same task/ingredient type scale on laptop and phone; retain larger editorial page headings and wider layouts on laptop. Both views keep ingredient quantities visible, extra recipe detail expandable, and cleanup as a compact title/duration row.

## Approved implementation decisions — October 28

Native execution is approved: one implementer uses Superpowers executing-plans with test-first development, targeted independent reviews of the scheduler and calendar authorization/recovery, and a final whole-branch review. Reuse the private `dsilvadeepal/simmer-and-gather` GitHub repository.

UI/UX is approved: guided Gathering → Menu → Prep plan, editable cards, backward navigation preserving choices, selected prep days and per-day totals, Manageable/More generous menus with editable category counts, compact attributed recipe photos and labeled icons. Laptop and phone share readable task typography; task ingredient quantities remain visible and extra notes expand. Cleanup is a short title/duration. Phone consultation/quick edits are included; cooking progress remains deferred.

Benchmark available Nebius and Fireworks vision endpoints using existing credits. Begin with a bounded development experiment capped at $1 total, no automatic recharge; verify each model ID and published rates before calls. Compare identical labeled images, extraction precision/recall, quantities/units, unsupported claims, latency and normal-rate cost per usable extraction. Distinguish synthetic receipts, public licensed images and any later user-provided samples. A small test yields a provisional selection, not general accuracy. Prefer the cheapest model meeting the accuracy/abstention gate; keep manual correction and unknown amounts. No personal uploads are required to continue building, and no live winner is claimed before results. Jev remains an optional text decision experiment, not the vision extractor.
