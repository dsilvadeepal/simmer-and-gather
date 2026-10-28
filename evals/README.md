# Evaluation evidence

Two separate evaluation tracks:

- `vision_benchmark.py`: actual paid-provider inference on four synthetic labeled image cases. Reports exact ingredient fields, unsupported quantities, latency and estimated token cost. See `docs/vision-benchmark.md`. No real pantry-photo accuracy claim.
- `run.py --mode fixtures --split all`: 25 versioned executable hard-constraint/authorization scenarios, split 18 development / 7 heldout. Runs real application services against local PostgreSQL with external-service fakes. These are code regression evaluations, not 25 AI-generated menus or hosted acceptance tests. The heldout label reserves cases for future prompt/model comparisons; current deterministic code has been tested against them.

Human rubric for real plan review: acceptable / needs changes / unusable; record the recipe evidence, workload concern and proposed correction. No human scores are filled in yet. Real recipe/source adequacy, cooking effort and menu practicality remain unvalidated. Live planning semantic evaluation is not yet configured; runner refuses `--mode live` rather than substituting fixture success.

LangSmith: sanitized synthetic trace submitted using the configured tracing key. Readback returned 403: `runs:read` is not permitted for tracing keys. Submission is not verified dashboard persistence. No raw image, private calendar text, secrets or helper names sent. Trace `6204d85c-fb70-439c-a39e-bb684ba89311`, project `simmer-and-gather-dev`. Check dashboard with the user account; do not broaden key permissions just to read it. Runtime traces are opt-in and allowlisted, not automatic full LangGraph state capture. Paid judges remain disabled. Jev not selected without access and a labeled comparison.

Failure/fix example: scheduler initially allowed active work with zero presence to evade daily/calendar constraints. A failing regression reproduced it; source-duration validation now rejects that inconsistent task. Calendar retry tests similarly caught resurrection of deleted reservations. These are local code correctness improvements, not proof of real hosting success.
