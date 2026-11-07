# Checked alternatives: implementation and validation

Implemented a bounded, deterministic search in `backend/src/simmer/alternatives.py`. Dietary conflicts trigger replacements from the owner's reviewed saved recipes. Vegetarian coverage can replace a nonvegetarian dish with a main for the shortfall. Must-haves and contributions are preserved. Full-menu screening, scheduling and independent validation gate every result. The app uses its synced library, not a live Notion database fetch per request.

The alternatives endpoint returns transient previews. Approval checks owner scope, revision, recipe versions, fresh calendar availability and feasibility, then updates the menu only. It never writes plans or calendar events. Users expand the checked schedule before approval and generate a new proposal afterward. Optional traces contain aggregate counts, not recipe or calendar content. No model calls are required.

Live-library checks found three complete options for each of the nut, gluten and vegetarian cases. Detailed results: `2026-11-07-automatic-alternatives.json`. Same fixture prep limits, buffers and simulated free calendar. Search is bounded to 12 schedule attempts and is not exhaustive.

Wings and mashed-potato screening saved in the app and existing Notion pages, including Dietary Notes and structured data, then read back verified. Existing curry wording normalized. Non-recipe record fingerprints remained unchanged.

Validation: 165 backend tests, 29 frontend tests, production build. API tests cover read-only preview, changed-calendar rejection, explicit approval and stale-approval rejection. Tests use isolated owners; no real plans or calendar events were changed. Ingredient screening requires product-label and cross-contact checks before serving.
