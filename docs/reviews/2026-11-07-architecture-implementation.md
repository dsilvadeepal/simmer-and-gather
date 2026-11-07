# Architecture implementation checkpoint

## Implemented
- Additive quantity contract: exact, bounded range, to taste, unknown; optional marker, original text and evidence basis. Legacy records remain readable. Explicit simple ranges scale without selecting a fictional exact amount. Ambiguous alternatives remain unresolved.
- Validate recipe task identifiers, missing dependencies, cycles, and attention segments before scheduling; apply the same checks to the hosting recipe tool.
- Distinguish complete, needs input, search exhausted, unsupported search, no fit found and final validation failure. Existing status values remain compatible with booking gates.
- Do not call a solver failure proof of insufficient host time. Menu blockers override an otherwise complete schedule.
- Preserve legacy hashes when the new optional fields are absent. New populated metadata is included in content hashing.
- Generate frontend contracts from Python schemas with optional defaults preserved.
- Remove the in-app recipe-import panel; keep existing recipe collection selection.
- Use current library image metadata to display saved menu cards without altering recipe snapshots in saved plans.

## Verification
146 backend tests passed, including the final hosting-tool and saved-plan outcome wiring.
26 frontend tests and production build passed.
20 controlled offline cases: five fixed menus, each tested at baseline, with more time, with fully busy days, and with a missing prerequisite. Ten time-feasible schedules; after menu checks, six complete plans, eleven needing input, and three with no fit found. Four time-feasible schedules are blocked by unresolved allergen review. All twenty correctness assertions passed; this is not a claim that twenty complete plans were generated. These are historical fixtures, not current-library completeness or real cooking validation.
A full API fixture flow covers gathering -> menu -> plan generation -> workspace readback.
Desktop and 390px phone browser audit passed using intercepted synthetic API responses; it cannot write to a real calendar or saved gathering.

## Course credits
Use Tavily for source evidence that direct publisher retrieval cannot obtain. It is configured locally; no unnecessary search calls were made for images already available.
LangSmith export is prepared in scripts/export_architecture_evals.py, limited to 20 redacted synthetic metric records. No live LangSmith key is configured in this checkout/session; no upload claimed.
Nebius/Fireworks remain candidates for bounded extraction comparisons after checking live balances and privately configuring credentials. No model price or remaining balance is inferred from the tracker.
No Pinecone or second tracing service is required for these improvements.

## Remaining work
- Migrate and re-review ambiguous ingredient alternatives and unresolved quantities across the current live collection; the new contract does not supply missing facts.
- Improve full-search support for helpers, multiple daily windows and finishing tasks.
- Run controlled tests on a frozen snapshot of the latest library, then human review for practical cooking instructions.
- Verify live LangSmith delivery and hosted OAuth/Notion lifecycle, credential refresh, retention, monitoring and account isolation.
- Browser acceptance on the hosted app. Local fixtures do not prove production reliability.

## Image audit
All 42 Notion covers responded with image content. Synced image metadata into all 40 app recipes, preserving non-recipe records. The Sannas cover now matches the app’s Xantilicious source. The read-only Diwali preview now receives image metadata too. Remote availability can change; this was a point-in-time check.
