# Simmer and Gather — current build plan

Updated November 7, 2026. Branch: `build/hosting-demo`. Requirements: [PRD](../../../PRD.md). Native implementation; retain existing integrations and data.

## Implemented
- [x] Versioned recipe preparation v5; typed quantities, source text, dependencies, storage policies, attention segments and granular readiness; cached results invalidate on relevant recipe/schema/prompt/preference changes.
- [x] Bounded scheduling and host-only constraint fallback with independent validation; explicit missing-input, no-fit, search-limit, unsupported and validation-failure outcomes.
- [x] Immutable plan snapshots, stale-version checks, exact approval and idempotent calendar operations.
- [x] Current food-led responsive UI, schedule-first day/session groups, expandable practical instructions, active versus elapsed time, readable portions and photos.
- [x] Explicit allergy confirmation; one Save and continue action and one Build my prep plan action.
- [x] Checked dietary/vegetarian alternatives and bought-prepared previews; fresh recheck and atomic menu/new-plan acceptance; previous snapshots preserved.
- [x] Read-only alternative previews, grouped conflict explanations, one option first, inline guest contributions.
- [x] Device-local Have checklist, crossed-out items, reversible filtering and changed-amount reconfirmation. No hosting import/pantry-entry panel.
- [x] Include existing hosting reservations in conflict checks; recheck all selected recipe versions under the shared recipe-save/acceptance lock.
- [x] Scoped Notion persistence and Google OAuth integration; local runtime tracing and LangSmith experiment runners.
- [x] Refreshed README screenshots and silent generic-data walkthrough.

## Latest verification
Use [current evaluation results](../../reviews/current-evaluation-results.md) as the single result summary. Keep executable fixtures and automated regressions. Synthetic-calendar tests, DOM interaction tests and isolated browser captures have different scopes; none establishes production or physical-cooking reliability.

## Remaining release work
- [ ] Full responsive browser journeys for conflict recovery, checked swaps, bought-food approval, long content and error/retry states. The 20-case mocked desktop/phone suite passes; live integration and all recovery/error journeys are not covered.
- [ ] Controlled Google calendar-write acceptance with explicit authorization, including retry/partial failure and stale approval. Generation alone never authorizes booking.
- [ ] Verify deployed OAuth refresh/reconnect, Notion lifecycle, backups/restores, monitoring and account isolation if hosting resumes. Replit deployment is paused; no hosted app claimed.
- [ ] Verify an all-in deployment topology within the $5/month target before any deployment.
- [ ] Further practical recipe review, quantity ambiguity and helper/multiple-window/finishing coverage. Never relax constraints or source steps merely to increase completion rate.

## Deferred
Additional accounts, cross-device shopping sync, cooking progress, voice, live recovery and weekly meal prep. Live receipt/pantry upload remains gated on verified independent retention cleanup. Jev and paid semantic judges are optional experiments, not required runtime components.

## Invariants
Two-hour daily defaults, flexible cleanup allowance and editable arrival buffer. No standalone measuring tasks. No silent buy/swap or larger time allowance. Preserve saved plans. Book only exact approved versions in the dedicated hosting calendar. No personal-event changes.
