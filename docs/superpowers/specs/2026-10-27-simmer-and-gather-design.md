# Simmer and Gather — current architecture design

Updated October 28, 2026. The current normative requirements are [PRD](../../../PRD.md). Historical design is preserved in docs/archive. The approved compact menu / daily-fit / When–What–Details output is the implementation target.

## Boundaries
Recipe preparation produces reusable typed task graphs; gathering planning scales quantities and schedules those graphs; publication applies exact approved versions. React calls authenticated FastAPI services. One LangGraph workflow orchestrates deterministic scheduling and validation. Models interpret recipe content and rank known menu options; external content never authorizes a write.

## Recipe contract
Retain recipe source/version, ingredients and source text, preparation provenance, dependency IDs, active/presence/elapsed minutes, optional explicit attention segments, timing basis, preparation policy and storage anchor. Unknown storage is preserved for legacy data. Explicit same-day policy permits same-day preparation without inventing advance storage. Next-step storage describes component lifetime; serving storage describes completed dish lifetime. Semantic support still requires review; substring evidence checks alone are not certification.

## State and ownership
Notion edits create new imported versions. The app stores recipe snapshots and immutable plan inputs. A changed saved recipe is surfaced and must be explicitly refreshed into selections; prior schedules remain separate. Calendar writes require exact revision/hash, current recipe checks and fresh calendar availability. Generated timestamps order plans and do not affect semantic content hashes. Old schema approvals must be revalidated rather than silently trusted.

## Scheduling
Single batch per dish is the demo default; ingredient scaling is independent. Active attention segments preserve end-of-cook work. Continuous supervision counts in presence. Passive waiting consumes elapsed time/resources where applicable but not daily effort; UI displays notes. Validator checks exact task completeness, dependencies, window anchors, helpers, resources, attention, daily totals, cleanup and one-hour buffer. Bounded search failures report unresolved work, not mathematical impossibility. Optional category-count suggestions do not block an otherwise valid schedule.

## Evaluation and cost
Versioned recipe cache keys include source content, task schema, prompt, preparation preferences and model ID. Calendar-only planning does not re-extract recipes. Sanitized linked LangSmith stage summaries retain counts, codes, versions and timings, not personal calendar text. Tests cover lifecycle and actual failure classes; live LangSmith/hosting acceptance remain separately evidenced. Keep $5/month deployment gate and no automatic purchases.
