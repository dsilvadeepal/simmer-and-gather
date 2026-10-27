# Simmer and Gather — PRD

Date: October 27, 2026. Status: **Draft for review, not approved to build.**
Detailed behavior, architecture and proposed implementation decisions: [Design](docs/superpowers/specs/2026-10-27-simmer-and-gather-design.md).

## Problem and audience
Hosting combines menu decisions, ingredient shopping, kitchen bottlenecks and preparation around work. Deepal wants most cooking finished before guests arrive, without exhausting evenings. Initial product is private and single-user. Friends/family using their own accounts are future work.

## Outcome
A feasible, source-grounded plan that respects personal preparation limits, adapts to disruptions with approval, and clearly shows cooking progress. Diwali for about fifteen people anchors the demo, with vegetarian/nonvegetarian dishes, drinks and dessert. Thanksgiving, Christmas and a young child's birthday are additional use cases.

## Priorities and boundaries
Time and manageable effort matter more than spending. No budget optimization. No voice, guest login, ongoing detailed pantry upkeep, automated purchases, unsolicited guest messages, multiple planning agents or required vector database. No unsupported make-ahead/storage claims. No automatic calendar changes. No dashboard metric presented as proof of cooking quality.

## Requirements and acceptance
| ID | Requirement | Acceptance example |
| --- | --- | --- |
| R1 | Reusable profile with per-gathering overrides | Changing this gathering's available oven or prep limit leaves default profile unchanged |
| R2 | Calendar selection and protected time | Free calendar slot overlapping protected family time is not scheduled |
| R3 | Preparation capacity and horizon | One-hour work evenings/two-hour weekends include cleanup; only schedule after chosen start date |
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
| R15 | Automatic and manual recheck | Background checker runs with app closed; manual button also works; no silent rescheduling |
| R16 | Actionable email | Conflict email links to authenticated review; unchanged conflict does not repeatedly email |
| R17 | Mobile cooking | Check meaningful stages, see all dishes before/after session, persist progress across reloads |
| R18 | Progress meaning | Completed cooking can show 100% despite pending warming/table tasks; estimates labeled and unknown weights shown as stage counts |
| R19 | Late recovery | Rearrange remaining tasks/helper work first; optional simplification next; must-haves/completed stages preserved; approve changes |
| R20 | Final checklist | Small warming, drinks and serving tasks grouped separately while equipment and aggregate effort still count |
| R21 | Notion separation | Only designated app databases/pages accessible through app tools; unrelated workspace remains unchanged |
| R22 | Failure recovery | Stale approval blocked; retried writes don't duplicate; partial calendar sync and disconnected services shown honestly |

## Product experience
Onboarding: account connections, chosen calendars, kitchen profile, helpers and protected times. A gathering collects date/time, earliest prep date, guests/dietary needs, overrides and contributions. Menu proposal leads to optional inventory confirmation, shopping and preparation sessions. Review screen shows constraints, assumptions and exact calendar changes. Cooking mode emphasizes this session plus cross-menu progress; final checklist stays separate. Conflict review shows old/new plan and user choices. Recipe collection supports import, review and Notion editing.

## Data and integrations
One LangGraph planning agent is the chosen orchestration pattern. Notion MCP manages recipe knowledge and human-readable records. App database owns typed snapshots, versions, progress, authorization and calendar operation IDs. Google Calendar owns reservations. Replit is preferred hosting. Nebius, Tavily and LangSmith are proposed initial providers based on recorded credits; model capabilities/balances remain unverified. Fireworks and Langfuse are alternatives, not duplicate default services. Email sender and paid cap require user input. Detailed credits and caveats are in the design.

## Success and evaluation
Evaluate recipe fidelity, scheduling constraints, preservation of must-haves/completed work, quantity handling and approval boundaries. Use about twenty-five scenario cases, deterministic checks where possible, human practicality review and optional model-based explanation checks. Proposed release gate: all defined hard-constraint and authorization tests pass; report exact scope and failures. Track cost/latency after baseline, and conduct a real preparation trial if feasible. No results exist yet.

## Delivery and current state
Existing private GitHub repository and local folder are established. Dedicated Notion root and three empty databases exist; reuse rather than rebuild. No app, importer, calendar booking or monitoring is implemented. Design approval precedes implementation planning. Full requested experience is broader than a trivial demo; capability checks and delivery slices will expose deadline risk early without silently dropping requested functionality.

## Decisions pending review
- Preparation caps: proposed total daily session time, including cleanup and required presence, with shorter sessions allowed; confirm versus a per-session or active-time-only limit.
- Monthly paid hosting/services ceiling and what it includes.
- Conflict-check delay and email quiet-hour preference.
- Transactional sender versus personal Gmail; upload retention policy.

Concrete gathering date/time, recipe-source preferences, actual equipment capacities and calendar choices will be captured during onboarding. They need not block architectural review.
