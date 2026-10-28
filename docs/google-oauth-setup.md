# Google sign-in and Calendar setup

Use a separate **Simmer and Gather** project. No paid services or billing linkage needed for this setup. Project creation is awaiting explicit user approval after automatic approval review blocked it; no project was created by the agent.

1. In Google Cloud Console, create/select the app project. Enable **Google Calendar API**.
2. Open Google Auth Platform → Branding. App name: Simmer and Gather. Use your own support/contact email. Review the Google API User Data Policy yourself before accepting it.
3. Audience: **External**, testing mode. Add your own Google account as a test user. This keeps the demo private. Testing refresh tokens for Calendar scopes can expire after seven days; reconnect near demo day.
4. Data Access: `openid`, `email`, `calendar.calendarlist.readonly`, `calendar.events.readonly`, `calendar.app.created` (Calendar scopes use prefix `https://www.googleapis.com/auth/`). This permits reading selected calendars in application code and creating/managing secondary app calendars; it does not request editing all primary-calendar events. Google grants read scope broadly, so the app's selected-calendar allowlist still matters.
5. Clients → Create client → **Web application**, named Simmer and Gather web. Register `http://localhost:8000/api/google/callback` for local testing. Once hosting is selected, add exactly `https://YOUR_APP_HOST/api/google/callback`. Do not use a Desktop client for this hosted web app.
6. Download client JSON into a private local directory or paste fields directly into the host's secrets manager. Never paste client secrets in chat, Notion, GitHub or browser URLs. Configure the names in `.env.example`. Generate SESSION_SECRET and a Fernet CREDENTIAL_ENCRYPTION_KEY locally; keep them stable across restarts.
7. Start production entrypoint with `uv run uvicorn simmer.server:build_app --factory --host 127.0.0.1 --port 8000` after migration/frontend build. Sign in yourself, review permissions, and grant consent. Verify calendar listing/read first. Only then review/approve a real prep plan and Apply.

The callback uses single-use browser-bound state, PKCE, verified Google ID token email and a one-owner allowlist. Refresh tokens stay encrypted server-side. Production startup fails closed without required configuration. The separate `simmer.dev` entrypoint is synthetic loopback demo only.

Sources: https://developers.google.com/identity/protocols/oauth2/web-server ; https://developers.google.com/workspace/calendar/api/auth . Live OAuth exchange and booking remain unverified until setup and user consent.
