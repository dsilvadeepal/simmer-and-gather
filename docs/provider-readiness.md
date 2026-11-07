# Integration and provider readiness

Updated November 7, 2026. Status reflects recorded local implementation/evidence, not a fresh external-account audit.

| Component | Current state | Still to verify |
| --- | --- | --- |
| Google OAuth/Calendar | App-owned OAuth and read integration implemented and locally exercised; dedicated-calendar approval path exists | Approved booking acceptance, refresh/reconnect and hosted callback lifecycle |
| Notion | Scoped app integration, recipe reads/corrections and plan projection implemented; no chat-credential reuse | Hosted lifecycle and ongoing source/version synchronization |
| LangSmith | Local tracing and dataset experiments recorded; separate evaluation credential | Credential expiry/rotation and ongoing allowance |
| Nebius / Fireworks | Optional bounded inference and completed synthetic vision experiment | Current balances, pricing and task-specific quality before paid use |
| Tavily | Optional bounded source discovery/extraction | Current allowance before new searches |
| PostgreSQL | Durable local application storage | Hosted backups, restore and resource footprint |
| Hosting | Local app; Replit deployment paused | Explicitly approved topology and all-in $5/month budget |
| GitHub | Public project repository; active build branch `build/hosting-demo` | Branch review/merge is separate from deployment |

Keys stay in ignored local files or secret stores. Models/search are disabled unless configured; no automatic recharge. Uploads remain gated on independent retention cleanup. See [runbook](runbook.md), [budget](budget.md) and [latest evaluations](reviews/current-evaluation-results.md). Catalog access and course credit grants do not prove current balance or entitlement.
