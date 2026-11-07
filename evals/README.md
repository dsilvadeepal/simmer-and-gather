# Evaluations

Current recorded results: [evaluation summary](../docs/reviews/current-evaluation-results.md). Only the latest result per suite is retained in review documents. Frozen inputs and regression fixtures are retained to reproduce failures and prevent regressions.

## Run offline
```sh
uv run python evals/run.py --mode fixtures --split all
uv run python scripts/evaluate_architecture.py
uv run python scripts/evaluate_heldout_gatherings.py --corrected
```
The service regression runner exercises hard constraints and authorization against local PostgreSQL with external fakes. Architecture cases use frozen recipe fixtures. Corrected heldout cases preserve their input constraints. Review each runner before use: library/integration scripts are separate from offline evaluations.

For current random inputs see `random-ux-2026-11-07.json` and [human-readable inputs](../docs/demo/20-random-ux-test-inputs.md). `scripts/evaluate_random_ux_batch.py` runs the actual PlanningService/LangGraph under an isolated owner with simulated availability and publishes sanitized results to configured LangSmith.

## Interpretation
Independent code evaluators check valid complete schedules, expected blocks and constraints. Completion is not correctness: allergies, missing information or impossible budgets should block. No LLM-as-judge is used. Paid semantic/model-quality evaluation and physical cooking validation remain separate work. `run.py --mode live` is not configured and fails rather than claiming fixture success.

Vision benchmarks use synthetic labeled images and paid-provider inference; see [benchmark](../docs/vision-benchmark.md). They do not establish real pantry-photo accuracy. Jev is not a selected dependency.

## Privacy
No live calendar writes in these suites. Never publish credentials, private calendar text or real household data. Keep tracing and evaluation credentials in ignored environment files. See [LangSmith setup](../docs/setup/langsmith-evaluations.md).
