# LangSmith configuration and evaluations

Updated November 7, 2026. Local runtime traces and code-based experiments have been recorded. See [current evidence and experiment link](../reviews/current-evaluation-results.md).

## Credentials
Keep the app tracing key in ignored `.env.services` with `LANGSMITH_API_KEY`, `LANGSMITH_TRACING` and `LANGSMITH_PROJECT` as configured by the runtime. Load it privately into the server environment; files are not automatically loaded by the production factory.

Evaluation runners use ignored `.env.langsmith-evals` containing `LANGSMITH_EVAL_API_KEY`, with dataset/experiment permissions. The evaluation token was created with a 30-day expiry; rotate when required. Never print or commit either key. A tracing-only key may not allow experiment/read operations.

## Reproduce experiments
```sh
uv run python scripts/run_langsmith_regression.py
uv run python scripts/run_langsmith_heldout.py --corrected
uv run python scripts/run_langsmith_realistic.py
uv run python scripts/evaluate_random_ux_batch.py
```
Read each script's frozen inputs and database requirements first. Regression scenarios use synthetic availability; randomized service runs isolate their records and check the real owner's records remain unchanged. No calendar integration writes. Uploads send redacted metrics/case labels, not personal event text.

## What to inspect
Open Datasets & Experiments, select the suite, then inspect expected outcome, actual outcome, validator violations and linked trace. A blocked case can pass. Compare against the frozen inputs instead of changing constraints just to improve the completion percentage.

No model judge is used and these evaluators do not invoke paid judging models. LangSmith usage allowances still apply. Exact current results and scope live in the single evidence summary rather than duplicated counts here.
