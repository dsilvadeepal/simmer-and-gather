# Simmer and Gather — architecture refinement implementation plan

Updated October 28, 2026. Spec: PRD.md. Native Superpowers execution. Existing implementation is retained; earlier plan is archived under docs/archive. Do not recreate integrations or databases.

## Global constraints
Preserve daily 120-minute defaults (weekdays and weekends), 15-minute flexible cleanup, one-hour arrival buffer and 20-minute finishing allowance. One batch per dish for demo. No standalone measuring tasks. No calendar writes without exact approval. No model call on ordinary calendar-only replanning. No hidden fallback to an old plan. Preserve existing recipe and gathering snapshots.

## Task 1: Versioned recipe preparation
- [x] Add explicit same-day/advance preparation policy, next-step storage anchor, start/end attention segments and granular readiness.
- [x] Test missing storage remains unknown unless same-day selected; end attention is counted; source/schema/preferences invalidate cached preparation.
- [x] Preserve source-backed guidance, provenance and recipe versions. Curated catalog is seed-only, not a permanent override of Notion edits.
- [x] Keep source interpretation separate from gathering ingredient scaling and scheduling.

## Task 2: Schedule and independent validation
- [x] Test presence at task start/end, dependency storage anchors, limits, buffer and one-batch ingredient scaling.
- [x] Validate candidate independently, including missing/duplicate work, helpers/resources and cleanup.
- [x] Keep optional menu counts advisory; retain dietary and required-work blockers.
- [x] Bounded adjustment search proposes changes only. Never claim infeasibility proven or apply a larger allowance silently.

## Task 3: Plan lifecycle and output
- [x] Store generation time; retain prior plans internally and show only the current proposal, with recipe-version staleness. Never substitute previous assignments.
- [x] Show menu/quantity/reason table; daily fit summary; compact When/What/Details rows with expanded quantities/source/helper notes.
- [x] Passive waits remain notes and dependencies; split separated work sessions. Retain small finishing checklist and grouped shopping.
- [x] Frontend tests cover output, outdated plan state and approval disabled for outdated inputs.

## Task 4: Evaluation and observability
- [x] Add real recipe-preparation regression scenarios, cache tests and scheduling scenarios reflecting observed Diwali failures.
- [x] Link sanitized preparation/schedule/validation trace stages; preserve privacy and recorded model/prompt/schema provenance.
- [x] Run backend/frontend suites and build; distinguish local fixture evidence from live LangSmith and hosted verification.

## Task 5: Acceptance and release
- [x] Verify app rendering and existing selected gathering with current recipes; preserve menu and limits. No Google writes.
- [x] Fresh-context whole-change review and targeted fixes, then record evidence and remaining external setup honestly.
- [ ] Controlled calendar-write acceptance and deployment remain separately gated by approval and verified $5/month topology.

## Review focus
Stale input/recipe versions; missing storage versus same-day; attention after waiting; source-supported component storage; preserved daily limits and buffer; old/current UI separation; cached model output and evidence; no hidden calendar writes.

## Verification evidence
92 backend tests and 6 UI tests plus production build passed; see docs/architecture-refinement-ledger.md for actual runs. Current Diwali proposal regenerated with primary calendar, 22 assignments, no scheduling violations and 45/90/115 minutes Fri/Sat/Sun. Live LangSmith delivery is unverified because credentials are absent; no hosted cost or calendar-write acceptance is claimed. Previous approvals require revalidation after the schema change.
