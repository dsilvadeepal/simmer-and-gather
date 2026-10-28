# Agentic build coverage

The course handout asks what the agent needs to **know**, what it needs to **do**, how it uses tools, how much autonomy it gets, and how we evaluate it. The demo uses one bounded LangGraph workflow rather than multiple conversational agents.

| Concept | Current implementation | Next evidence needed |
| --- | --- | --- |
| Context and memory | Saved gathering preferences, helper capabilities, reviewed recipes, plan revisions and approval state live in the app database. Notion is a scoped recipe source and a readable projection of approved records. | Exercise a full plan using several reviewed Notion recipes. |
| Tool use | The application reads Google calendar availability and scoped Notion recipe pages. Model-generated menu ranking is constrained by deterministic recipe, dietary and schedule checks. Writes are application operations outside model tool access. | Exercise real calendar availability, menu proposal and booking together. |
| Orchestration | LangGraph runs retrieve → propose and schedule → validate with recursion limits. The user edits the proposed menu before requesting the final plan. | Add trace evidence for a complete real-recipe run. |
| Autonomy and approval | The graph can propose and recalculate; it cannot save a recipe to the collection or book calendar events on its own. Save and booking require explicit user actions bound to the current revision. | Verify the UI approval path end to end. |
| Observation and evals | Allowlisted LangSmith run summaries can record status, task count, violation codes and latency when enabled. Local tests cover scheduling, revisions and approval guards. Raw household data is excluded from automatic tracing. | Configure private LangSmith credentials, run a small labeled scenario set, and record failures and corrections. |

The recipe import now reads actual Notion page details into an **unreviewed draft**. A live audit on October 28 found nonempty ingredients, task timing drafts and servings for all 40 recipes. This is a structural completeness check, not proof that every estimate or source is correct. Timing, storage limits and allergen notes remain editable before the recipe enters planning.

The course credits tracker permits development experiments with LangSmith, Nebius, Fireworks and Tavily, but these are not required for every decision. Deterministic scheduling and validation should handle arithmetic and hard constraints; a model is useful for ranking menu options or interpreting messy source material. System One/Jev remains an optional measured experiment if access and task-specific accuracy justify it.
