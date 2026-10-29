# Schedule-first UI Implementation Plan
> For agentic workers: use superpowers:executing-plans (native) with final independent review.

Goal: make the proposed schedule immediately useful on phones.
Architecture: presentation components consume unchanged typed plan/input contracts; App retains mutations and approval ownership.
Tech stack: React/TypeScript, existing CSS, Vitest.
Spec: docs/superpowers/specs/2026-10-28-schedule-first-design.md.

## Global constraints
Two-hour defaults; one-hour buffer; no generation/calendar writes during visual edits. Current proposals only. Preserve dirty-input and approval guards. No invented photos/quantities.

## Task1: Day groups and secondary views
- [x] Add failing tests: a date appears once, separated times remain visible, passive notes stay small, schedule is default, keyboard navigation reaches menu/shopping, task quantities remain visible.
- [x] Implement PrepOverview day groups and PlanViews with retained panels. Expected: tests pass.

## Task2: Compact header and menu summary
- [x] Verify date/arrival/guest header in the browser and test primary-ingredient prioritization. Implement readable schedule status and Update plan label; move saving into disclosure without changing authorization.
- [x] Update PRD/current plan, run full frontend and backend tests/build, inspect375px and laptop, final independent review and targeted fixes.

Review focus: hidden panels focus, long ingredient/task text, stale/dirty proposals, waits across days, unchanged calendar approvals. No API/provider changes.

## Completion evidence — October 28
- Native implementation; no backend contracts or calendar-write behavior changed.
- RED: missing PlanViews and repeated day headings failed before implementation. GREEN: 11 frontend tests; production TypeScript/Vite build passes. Backend: 92 tests pass.
- Independent review: fixed menu fat prioritization and added full scaled ingredient disclosure; regression test observed RED then GREEN. Fixed cross-day waiting timestamps with RED/GREEN regression.
- Browser: actual saved Diwali plan; Schedule default, all secondary tabs, expanded menu quantities and task notes verified. At 375px document width is 375px, including expanded details; at 1280px document width is 1280px and schedule uses three columns. Viewport reset after checks. No calendar events written.
- PRD synchronized. No deferred review findings. Photo display remains optional; no new images fetched.

## Scheduling simplification — October 29
Approved: prep-day chips, expandable daily limits, cooking-finished time, optional windows/finishing and protected-time disclosures. Empty windows now use a visible 9 am–9 pm local search range, constrained by calendars, protected periods, daily totals and arrival buffer. Existing explicit windows are retained. Regression covers automatic availability without mutating input snapshots.

Verification: 93 backend and 12 frontend tests pass; production build passes. Independent review found the deadline input maximum exceeded the API limit; corrected to 240 minutes. Existing saved data and calendar events are unchanged.
