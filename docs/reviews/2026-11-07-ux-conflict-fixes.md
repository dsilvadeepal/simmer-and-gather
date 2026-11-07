# UX recovery and preview-isolation fixes

Implemented read-only alternative schedule previews, one initial option with More options, dish-level explanations for dependency failures, a dedicated unconfirmed-allergies screen, checked bought-food preview/approval, one guest contribution form, and grocery-category placement of range quantities. No CSS or color changes.

Dietary paths remain distinct: explicit guest confirmation; ingredient/product screening where metadata is missing; checked whole-recipe substitutions for known conflicts; vegetarian-main portions sized to coverage. No automatic removal of allergies or ingredient substitution. Unsupported dietary screening stays unresolved. Real saved plans and calendar unchanged; scripts verify original-owner record fingerprints. Tests use isolated owners or mocked APIs.

Re-ran identical 20 planning scenarios through LangGraph/LangSmith: 14 complete, three needs_input, three no_fit_found. No planning outcomes changed. All complete plans validate. Experiment: https://smith.langchain.com/o/8ea48a8e-b636-497e-a9eb-ecd377951afe/datasets/1f7f374d-2553-4f71-bf5c-a821dff6b0ab/compare?selectedSessions=c11e89ee-b866-4639-93a0-34f2128cb82b

The UI harness covers all 20 outputs. Preview checkboxes no longer exist and preview interaction cannot write the shared shopping checklist. Bought-prepared API tests verify read-only preview, explicit acceptance saves a new plan, historical plan preservation and stale-revision rejection. Browser visual acceptance remains limited by the previously observed Chrome remote-debugging policy; DOM tests and production build are not a substitute for full responsive browser review.
