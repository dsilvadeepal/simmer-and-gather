# Provider readiness — October 28, 2026

| Component | Evidence | Status |
|---|---|---|
| Nebius | Authenticated `/v1/models` returned 30 models | Catalog access verified; balance/expiry not exposed by inference API |
| Fireworks | Authenticated `/inference/v1/models` returned 29 models | Catalog access verified; balance/expiry not verified |
| Vision | GLM-5.3-Flash listed on both accounts, image input documented | Live experiment in `vision-benchmark.md` |
| Planning | Nebius Qwen3-30B-A3B-Instruct-2507 available; $0.10/$0.30 per million input/output per official cookbook | Candidate; planning evals pending |
| Tavily | Tracker records $25/3,125 credits plus monthly allowance | App access/remaining balance unverified |
| LangSmith | Key configured locally; tracker $100 through Nov 20, 2027 | Trace smoke/entitlement pending; no card activation |
| Google Calendar | Chat connection is not hosted-app OAuth | Client/refresh-token provisioning pending |
| Notion | Existing scoped databases recorded in ignored setup JSON | Hosted-app integration token/MCP OAuth pending |
| Render + Supabase | Candidate free web service + durable Postgres/auth/private storage | Account provisioning, independent upload expiry and full costs unverified; no deployment claim |
| GitHub | Existing private dsilvadeepal/simmer-and-gather repo | Verified; build branch used |

Secrets are read only into process environments, never printed or committed. No new paid service, recharge or card entry. Missing app credentials must produce disconnected/unavailable state, never empty calendars or simulated success. Local Docker PostgreSQL is available for real persistence tests.

Google needs exact registered redirects and offline access. Testing-mode refresh tokens may expire after seven days for external apps with calendar scopes; verify consent configuration before release. Store refresh credentials encrypted, never in browser storage. Notion hosted MCP OAuth and enumeration still require app-level verification; no connector credential reuse. A scoped API-backed adapter can be developed/tested but must be identified clearly as an alternative requiring integration setup.

Sources: https://developers.google.com/identity/protocols/oauth2 ; https://developers.notion.com/guides/mcp/overview ; https://nebius.com/services/token-factory/models/glm-models-inference ; https://fireworks.ai/models/fireworks/glm-5p3-flash ; https://dev.nebius.com/cookbook/openhands-agent-canvas . Account catalog results are separate from vendor descriptions.

MCP implementation decision: app-owned scoped Notion MCP server (`adapters/notion_mcp.py`) exposes only recipe listing/read tools, backed by the official API and an explicit collection allowlist. This avoids depending on unrestricted hosted workspace search. It still requires the user's app integration token/shared pages; no live Notion round trip is claimed. Reviewed writes remain in application code, not agent tools. Existing database IDs are retained in ignored local setup, never recreated.
