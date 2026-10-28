# Local operation and release gates

The app is under implementation. A passing local suite does not mean hosted or live-provider acceptance.

## Local sample app

1. `docker compose up -d` starts local PostgreSQL.
2. `uv sync --locked` and `npm ci --prefix frontend` install pinned dependencies.
3. `uv run uvicorn simmer.dev:app --host 127.0.0.1 --port 8000` runs synthetic demo mode.
4. `npm --prefix frontend run dev` opens the Vite app on port 5173.

Sample recipes are illustrative and not cooking guidance. Never deploy `simmer.dev` or seed its sample owner as the real authenticated owner.

## Real local Google connection

Load the ignored `.env.google` into process environment without printing its contents. Run `uv run uvicorn simmer.server:build_app --factory --host 127.0.0.1 --port 8000 --no-access-log` after building the frontend. The configuration file is not loaded automatically. Keep session/encryption keys stable; losing the encryption key requires reconnecting Google. Visit http://localhost:8000/api/google/start. Use localhost consistently, matching the registered redirect. OAuth state expires after ten minutes; restart sign-in if necessary. No access logs are enabled because callback URLs contain authorization codes.

## Safety and recovery

- Store migrations must run before serving traffic; the initial schema is in `backend/migrations/`. Use direct/session PostgreSQL connections: transaction pooling is incompatible with session advisory locks.
- Approval and Apply remain separate. Review the exact plan revision before booking. Retry uses stored operation IDs; changed/deleted remote events need review, not automatic replacement.
- Back up PostgreSQL and preserve encryption/session secrets before changing hosts. Never store user records in ephemeral app files.
- Paid models are disabled by default. Set `ENABLE_PAID_MODELS=true` only with the approved Fireworks model contract and credentials. Text requests reserve $0.05 against the persisted $3/month AI envelope; remaining $2 is budget headroom. This is an application guard, not a provider invoice guarantee. No automatic recharge or hidden provider fallback.
- Uploaded images remain disabled in real mode until independent expiry cleanup is installed and verified. Manual ingredients work without uploads.
- LangSmith runtime activation, Notion integration credentials, hosted database/hosting entitlement and live end-to-end checks are still release gates. Do not treat chat connector access as app credentials.

## Validation

`uv run pytest -q`, `npm --prefix frontend test -- --run`, `npm --prefix frontend run build`, and `uv run python evals/run.py --mode fixtures --split all`.

GitHub Actions runs these checks with temporary PostgreSQL. Browser journeys require the sample backend and Playwright browsers. No production provider credentials belong in CI. Dockerfile is packaging only; no host has been provisioned or deployment verified.

When the paid text model is enabled, recipe previews also propose source-quoted preparation steps. The result remains unreviewed; extraction failures retain the original source for manual editing. Make-ahead/storage limits remain unknown until reviewed.
