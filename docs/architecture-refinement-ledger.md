# Architecture refinement ledger — October 28
Spec: PRD.md. Plan: docs/superpowers/plans/2026-10-27-hosting-demo.md.
Existing branch/workspace retained with all prior uncommitted work.
Ruling: retain legacy reviewed and unknown-storage behavior for old snapshots; explicit new policies opt into same-day behavior, avoiding silent reinterpretation of saved approved data.
Pre-flight: preparation consumes source evidence, scheduler consumes typed tasks, UI consumes generated plan; tests must cover their shared contract.

Tasks 1–4 local implementation: backward-compatible preparation policy/attention/storage fields, source/schema/preference/model cache versioning, granular readiness service, bounded priority retry, menu advisories, timestamped plans and separate previous proposals, stale local recipe approval guard, linked sanitized stage traces and output tables.
Regression evidence: 87 backend tests, 5 frontend tests, TypeScript/Vite build passed. Cases in evals/architecture-cases.json. No paid model calls for regeneration. LangSmith credentials absent, so live delivery is not verified.
Live read-only calendar acceptance: primary calendar fresh; current saved menu yields 22 assignments, no validator violations, daily presence 45/90/105 minutes Fri/Sat/Sun; 60-minute buffer. No calendar events created. Existing recipe timing estimates retained, not claimed as measured cooking evidence.
Ruling: no user input or external-service purchase needed for deterministic implementation; live LangSmith delivery and hosted cost acceptance remain explicit release gates because credentials/topology are not configured.

Final independent review: four important findings fixed with failing-then-passing regressions: imported return attention, stale Notion plan export, seed fallback overriding edited methods, and calculated shopping quantities hidden by UI. No critical findings or deferred minor findings.
Ruling: legacy mixed work/wait steps without attention placement now reserve the whole interval conservatively; explicit attention estimates were added to the four selected Diwali snapshots, preserving the menu, portions, daily limits and buffer. Cost if wrong: more conservative planning for other recipes until their attention is refined; estimates remain adjustable.
Ruling: no universal intraday holding limit is invented. Serving/next-step storage constraints and recipe guidance remain explicit; no food-safety certification is claimed. Semantic evidence support and live model quality require separate labeled experiments.
Final live regeneration after attention refinement: 22 assignments, no constraint violations; Friday45/Saturday90/Sunday115 minutes including cleanup; primary calendar fresh; one-hour buffer; no model calls or Calendar writes.

Additional lifecycle regression: opening a saved plan with newly busy calendar time now displays conflict without rewriting its immutable saved snapshot. Test observed failing then passing.
Final verification: 92 backend tests and 6 frontend tests plus production build passed. Phone-width375 browser rendering verified. Existing build branch retained; no merge or calendar booking.

User refinement: daily default changed to120 minutes on weekdays and weekends, preserving explicit daily overrides and60-minute arrival buffer. Applied to saved default profile and current Diwali gathering; regenerated proposal with primary calendar.

UX correction requested by user: remove the previous-proposal/revision section from the product screen. Retain stored history internally for recovery only. Broader visual redesign is being reviewed, not yet applied.
