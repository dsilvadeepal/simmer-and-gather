# LangSmith regression evaluations

Run from the repository root:

```sh
uv run python scripts/run_langsmith_regression.py
```

Create a private, gitignored `.env.langsmith-evals` file containing `LANGSMITH_EVAL_API_KEY`. Use a LangSmith personal access token with dataset and experiment access. Keep the app's tracing-only key in `.env.services`; do not copy either file to GitHub. The current evaluation token expires after 30 days.

Dataset: `simmer-hosting-regression-v1`. Five historical menu fixtures are tested with baseline availability, more time, a fully busy calendar, and a missing dependency. The script runs the actual local scheduler. Only case labels and redacted outcomes are uploaded; no live calendar is accessed or changed.

Scores:
- `valid_complete_only`: a plan marked feasible has no independent-validator violations.
- `constraint_handling`: blocked days cannot produce feasible plans; missing dependencies require input.
- `complete_plan`: whether the result is complete. This is a separate outcome metric, not a correctness score; deliberately invalid inputs should not produce complete plans.

First experiment (November 7, 2026): `hosting-regression-b5695b7e`. All 20 cases passed the two correctness checks; 6 were complete, 11 needed input, and 3 had no fit found. This is a limited scheduler regression suite, not proof of recipe accuracy, food safety, usability, or full live-integration correctness. Add human review and broader representative cases before treating it as product acceptance.

No model judge is used, so the evaluation invokes no paid model. LangSmith storage/tracing allowances still apply. Results appear under simmer-and-gather-dev → Datasets & Experiments → simmer-hosting-regression-v1.

## Reviewed follow-up

The follow-up experiment adds `expected_outcome`: normal/expanded-time cases must complete; deliberately busy calendars must return `no_fit_found`; missing dependencies must return `needs_input`. The same 20 fixtures now yield 10 complete, 5 no-fit, 5 needs-input. Ingredient-label reminders remain visible, while actual missing or conflicting allergen information remains blocking. See `docs/reviews/2026-11-07-regression-outcome-review.md`.
