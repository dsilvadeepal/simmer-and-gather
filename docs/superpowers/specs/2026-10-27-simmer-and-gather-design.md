# Simmer and Gather — product and technical design

Date: October 27, 2026. Status: **Draft for Deepal's review; not approved for implementation.**
Companion: ../../../PRD.md. No implementation plan is authorized by this document.

## Intent and selected approach
Help a host enjoy guests without exhausting work evenings or cooking at the last minute. First user is Deepal; first demonstration is a Diwali gathering for approximately fifteen friends and family, with vegetarian and nonvegetarian dishes, drinks and dessert. Thanksgiving, Christmas and a three-year-old's birthday are subsequent scenarios, not separate products.

Approaches considered in conversation:
1. Notion-led planner: smaller interface, but awkward phone execution and change approval.
2. Focused hosting app with Notion recipe knowledge: coherent mobile planning, cooking and review experience. **Selected by Deepal.**
3. Broader household food planner: adds ongoing pantry, weekly meals and family accounts; excessive initial scope.

## Confirmed behavior
### Reusable profile and gathering overrides
Save kitchen equipment/capacities, helper capabilities, preparation limits, protected time rules and calendar selection. Initial equipment includes oven, stovetop, air fryer and Instant Pot. Capacity and oven temperature conflicts and air-fryer batches are important. Unknown capacities remain unknown until clarified. Defaults are copied into each gathering; overrides do not silently change the reusable profile.

Default preparation limits: one hour on a work evening and two hours on a weekend, including cleanup. These are maximum desired effort windows, not a requirement to consume all free time. Deepal chooses the earliest preparation date. Protect work, family and sleep even when calendars show free. Default major-cooking/cleanup cutoff is one hour before arrival; allow only 15–20 minutes of hands-on finishing during that hour, adjustable per gathering. Proposed implementation default: 20 minutes, leaving forty minutes genuinely unallocated. Builder-review clarification — proposed for user approval: interpret these limits as total preparation-session time per day, including cleanup and intervals requiring the host to remain present, not merely active minutes and not an unlimited number of two-hour sessions. Passive overnight chilling does not consume a session. The user can override daily limits and split work into shorter sessions. This interpretation has not yet been explicitly confirmed. Store timezone explicitly and convert calendar timestamps consistently, including daylight-saving transitions.

### Menu and guest requirements
Suggest a complete menu first. User can swap dishes, mark must-haves and choose bought prepared or semi-prepared starters/desserts. No spending budget or cost optimization in demo. Record vegetarian count, other dietary restrictions, allergies and preferences per gathering; unknown is not confirmed none. Shared vegetarian dishes may serve everyone; vegetarian guests must have a complete meal. Use editable target servings per dish, accounting for courses and contributions, not a naive equal split or universal portion guarantee.

Preserve must-haves. If they make the plan infeasible, explicitly request a tradeoff; do not replace them silently. Prefer rearranging unfinished work and assigning available helpers, then simpler recipes or optional-dish removal, then prepared components as appropriate, always presenting meaningful changes for approval.

Each menu item has source: host-cooked, bought prepared/semi-prepared, or guest contribution. Deepal manually records contributor, dish, servings, confirmation, expected arrival and warming/equipment needs. Confirmed contributions count toward coverage; tentative items stay visibly uncertain. Guest cooking does not enter host progress. Bought food can still require real preparation, batch cooking and equipment reservations. Final small hosting tasks are a separate checklist.

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

Automatic conflict detection plus Recheck my plan button are both required. Proposed implementation: poll active gatherings every fifteen minutes, bounded to selected calendars and preparation horizon, using a real hosted scheduled job; no browser timer dependency. Interval is a user clarification. Google change notifications are an alternative if deployment economics/reliability justify them; require HTTPS callbacks, channel renewal and follow-up synchronization. Recheck stale state before writes regardless of detection mechanism.

Exclude a plan's own prep events from external-conflict detection but include other gatherings' reservations. Compare calendar edits with owned event IDs. Manual changes to a prep block become a discrepancy to review; never silently restore it. Generate a versioned proposal, leave existing events unchanged, email only actionable conflicts with a signed-in review link. No approval by GET/link click. Deduplicate by gathering, affected revision and conflict fingerprint; materially changed conflicts may notify again. No routine unchanged-state emails. Failed checks show last-successful-check/stale status; notification failures remain retryable and visible. No email functionality is being activated by writing this design.

### Phone execution and progress
Mobile checklist per session and cross-menu overview before/after sessions. Break recipes into meaningful preparation/cooking stages. Progress measures prep/cooking completion, not readiness to serve. Warming, table transfer, utensils and final small tasks are separate and do not reduce completion. Garnish counts in cooking only when part of that dish's chosen preparation stages. A dish can be 100% cooked while warming remains.

Proposed formula: completed prep/cooking stage effort divided by all prep/cooking stage effort, using reviewed active-minute estimates; display approximately, not false precision. If durations unknown, show completed stages instead of a percentage. Lock weights to recipe-plan revision, preserve completed stage IDs on replans, and explain any new work. Overview total is weighted host cooking work, not average dish percentages; excludes guest contributions and already-ready purchases. Include helper-performed stages because they advance the same work. Track elapsed/presence dependencies independently: a cooking step does not complete until user confirms it, even if predicted time elapsed.

Running behind accepts delay and current completion. Rearrange unfinished work across available capable helpers and equipment first. If infeasible, suggest simplifying/dropping optional items while protecting must-haves. Approval required for changed plan/calendar. Unchecked does not prove late. Completed work stays completed. Final checklist groups warming, drinks, serving dishes, table transfer and spoons; it still has an aggregate time/equipment allowance, not obsessive microtracking.

## Proposed technical architecture — builder recommendations, not previous user commitments
Responsive React/TypeScript frontend; Python FastAPI backend with one LangGraph planning agent. PostgreSQL for durable business state and checkpoints; managed object storage for uploads. Replit hosting preferred, actual plan/runtime/storage/scheduler costs to verify. Authentication restricts launch to Deepal's account; ownership keys on all entities preserve a later multi-account path without building invitations or family onboarding now.

Agent tools: retrieve_recipes, discover_recipe_candidates, import_recipe_preview, inspect_inventory, read_availability, propose_menu, validate_schedule, propose_revision and request_approval. Pure calculation/scheduling tools own arithmetic and constraints. External writes run through application services after verified approval, not unrestricted model calls. Bounded retries, tool/time budgets and structured outputs. A model call for image extraction or evaluation is not another autonomous agent.

### Data ownership
- Notion: editable recipe knowledge and readable gathering/session projections.
- Application DB: user profiles, per-gathering overrides, ingredient snapshot, typed recipe/task versions, menu quantities, dependencies, schedule, completion, approvals, integration IDs, sync jobs and alerts.
- LangGraph checkpoints: unfinished conversational work, not source of truth for approval.
- Google Calendar: actual reservations/appointments.
- LangSmith: redacted traces and evaluation results.

Normalized recipe snapshots reference Notion page and last-edited version. Refresh before a new plan; if edited after approval, mark affected plans for review and preserve their prior snapshot. Gatherings/session fields edited in Notion enter as proposed changes, not authorization. Show sync state (pending/synced/failed) and retain retries; remote save failure must not claim success. Database status alone cannot authorize a write.

### Existing Notion area
Reuse the three databases and root recorded in local host-ready-notion-setup.json; never recreate or mix with existing workspace planners. Recipe Library, Gatherings and Prep Sessions exist with internal relations and views. Existing budget fields are unused, not silently deleted. Detailed task/ingredient tables need normalization during import; Notion's current fields alone cannot prove scheduling readiness. Technical allowlist of data-source/database IDs and per-page membership enforcement wraps MCP. No unrestricted workspace search or access to unrelated pages. Broad OAuth permission must not be represented as page-scoped security. Check connector limitations before relying on full enumeration. If hosted MCP cannot provide required bounded retrieval, propose a scoped API-backed MCP adapter rather than silently swapping integrations.

### Schedule validation
Use explicit task dependencies, eligibility windows, release/finish times, non-preemptible cooking and batch constraints, person availability/attention, shared equipment and temperature compatibility. Cleanup consumes host capacity. Unattended work consumes equipment and any required presence; it does not disappear when active minutes end. Recipe storage limits constrain completion-to-serving interval. Serialize resource conflicts and account for transitions/buffers. A bounded heuristic scheduler is sufficient initially: return a feasible candidate or specific conflicts, not a claim of global optimality. Unknown critical timing yields conditional/incomplete status, never verified feasibility. Run validation after every meaningful change.

### Revision transaction and recovery
Maintain monotonic revision plus content hash and input versions. Approval binds to exact proposed menu/tasks/calendar diff and expires on material edits. Apply with durable outbox and stable operation IDs. Recheck calendars, fail closed on stale approval, record each write result. Partial calendar success is visible; retry only missing operations after reconciling remote IDs. No all-or-nothing claim across providers. Prevent concurrent applies with revision locks. Cancellation of gathering proposes removal only of its owned events and stops monitoring after approval.

## Tools and credits — tracker read October 27; balances not checked live
Source: parent folder Course-Credits-and-Tools-Tracker.md.
| Tool | Decision and rationale | Recorded entitlement / caveat |
| --- | --- | --- |
| Replit | Preferred host, PostgreSQL/object storage/scheduler capabilities to validate | Active month; cancel-by Nov 6; user open to modest paid hosting, cap unanswered |
| Nebius | First model-provider candidate; exact tool-calling and vision models selected by small tests | $25 received, recorded non-expiring; remaining balance unverified |
| Fireworks | Alternative candidate, no automatic paid fallback | $15 redeemed; expiry and remainder unverified; Oct 21 was redemption deadline |
| LangGraph | One-agent workflow, checkpoint and approval pause | Open source; not paid with LangSmith credits |
| Notion MCP | Required knowledge integration | Existing account; app OAuth/access test still needed |
| Google Calendar API | Availability, dedicated calendar and owned events | OAuth credentials/scopes and deployment consent setup needed; chat connection is not app credentials |
| Tavily | Online discovery/accessibly extracted source content | $25/3,125 add-on plus 1,000 monthly recorded; expiry/balance unverified |
| LangSmith | Selected tracing/eval candidate | $100 received, expiry Nov 20 2027; billing setup unclear |
| Langfuse | Alternative only; avoid duplicate observability | Active discounted Core; final renewal needs verification |
| Mem0 | Defer; structured preferences belong in app DB | Starter three-month offer believed; renewal unconfirmed |
| Pinecone | Defer; bounded Notion retrieval initially | Starter; Builder $40 promotion requires paid upgrade, do not upgrade |
| LlamaIndex | Defer unless document ingestion requires it | 50,000 credits recorded |
| Keenable | Search alternative if needed; no duplicate search stack | 100,000 monthly free requests recorded; $500 promotion not visible |
| ElevenLabs | Defer with voice | Offer unclaimed |
| Toloka / Tendem / Granola | No demonstrated initial need | Available/offered per tracker; do not add merely to use credits |
| ChatGPT Pro | Development assistance, not app inference budget | Subscription does not establish API credit |

Email provider is unresolved: recommend a small transactional-email service, sending only to Deepal, instead of requesting Gmail send access unless preferred. Verify sender setup, delivery, costs and authenticated deep links before final selection. No prices or integrations claimed verified from credit records. Verify balances before live tests; no paid fallback or automatic recharge without agreement.

## Security and operational scope
OAuth tokens server-side encrypted; no browser secrets. Validate URL imports against private-network/redirect abuse; treat retrieved pages as data, not instructions. Scope uploads by owner and limit type/size; proposed raw-upload retention seven days after successful extraction, with explicit delete control. Confirm this retention choice with user. Redact receipts, calendar metadata and child identifiers from traces; use generic helper labels for public demo. Private personal mode and synthetic demo dataset are separate; no public route exposing real accounts. Pin owner approval actions to authenticated session, prevent CSRF and replay. Maintain disconnect/delete controls. No external messages besides explicitly enabled conflict alerts.

## Evaluation and demo evidence
Proposed initial suite: twenty-five scenarios covering faithful extraction, unknown timings, unsupported make-ahead, inventory duplicates, quantity conversion, dietary coverage, oven temperature conflicts, air-fryer batches, protected time, partial helper windows, zero helpers, final-hour limits, must-haves, tentative potluck, contribution warming, changed calendars, stale approvals, duplicate retries, partial provider failure, late-session recovery and progress preservation. Use deterministic assertions for hard constraints, targeted model grading for explanation/source support, human review for practicality. Repeat a subset to detect variability; hold out some cases from prompt tuning. Release gate: all selected hard-constraint and authorization cases pass; report actual numerator/denominator, not general reliability claims. Record latency/model cost, with targets set after baseline. A real cooking trial is needed to assess estimate realism; simulated success does not establish food quality or practical timing.

Demo sequence: source-linked import -> review/save to Notion -> Diwali brief/calendar and helper limits -> full menu incl potluck/bought option -> inventory confirmation -> feasible plan and approval -> Busy block creation -> phone progress -> calendar conflict/behind schedule -> proposed revision/email -> approval -> evaluation evidence. Explicitly label fixtures/simulated triggers. Delivery of email and calendar updates require actual verification.

## Scope, risks and approval
Full agreed first-release scope includes imports/discovery, inventory uploads, scheduling, helper and potluck support, phone progress, automatic conflict detection and email; they are not silently stretch features. Implement in slices later; if course deadline threatens completion, Deepal chooses a reduced demo slice. Course submission Nov 6 11:59 PM Pacific, shortlist Nov 8, live demo Nov 10 per earlier handout/email review. Hosted account setup and scheduler may be critical path. No implementation until design approval, then Superpowers writing-plans.

Open user decisions: monthly hosting/services cap; acceptable conflict-detection delay and notification hours; sender preference; raw upload retention. First actual gathering date/time, sources and precise capacities are onboarding inputs, not reasons to invent values in this design. Exact provider models, scheduling library and UI styling are builder decisions after documented capability checks. First screen mockups remain to review before UI implementation.

## Technical references checked October 27
- Notion MCP and OAuth: https://developers.notion.com/guides/mcp/overview
- Google Calendar change notifications: https://developers.google.com/workspace/calendar/api/guides/push
- Replit deployment choices: https://docs.replit.com/features/publishing/deployment-types
These establish available platform concepts, not account entitlement or working integration.

## Builder review
A separate reviewer checked this draft against the conversation. Agreed requirements were preserved. The reviewer flagged daily versus per-session capacity and hands-on versus required-presence duration; the conservative proposed interpretation above is explicitly awaiting user review. Operating cap, notification timing/sender and upload retention remain open.
