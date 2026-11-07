# Vision comparison — October 28, 2026

Live calls, synthetic images. Four hand-labeled cases (11 food entries) tested identically with GLM-5.3-Flash on Nebius and Fireworks, and DeepSeek V4.1 Flash on Fireworks. Cases: clear receipt, decimal quantities, pantry labels with unknown quantities, receipt with nonfood/payment details. Exact labels existed before inference. No actual household images tested yet; the pantry-label case is OCR, not object recognition. This is an initial endpoint comparison, not a comprehensive model leaderboard.

| Endpoint | Exact item quantity/unit fields | Unsupported claims | Median seconds | Estimated total USD |
|---|---:|---:|---:|---:|
| Nebius GLM-5.3-Flash | 11/11 | 0 | 6.383 | 0.0005634 |
| Fireworks GLM-5.3-Flash | 11/11 | 0 | 3.308 | 0.0005354 |
| Fireworks DeepSeek V4.1 Flash | 11/11 | 0 | 1.566 | 0.0012156 |

Provisional default: Fireworks GLM-5.3-Flash; tied accuracy here and the lowest observed token-cost estimate. DeepSeek was also accurate on these cases; this small sample does not establish broader superiority. GLM published rates are $0.15/M input and $0.50/M output; DeepSeek rates are $0.30/M and $1.20/M; total twelve-call estimate $0.0023144, not a provider invoice. No statistical significance claim from four cases. Do not automatically switch providers on errors; preserve manual entry and explicit retry.

Raw sanitized results and image fixtures: `evals/vision/`. Rerun with environment keys: `uv run python evals/vision_benchmark.py --max-usd 1`. $0.05 reserved per request, $0.60 cumulative reservation for twelve calls. No retries. Each 850×360 image and 2,000-token output cap bounds this experiment; the runtime requires its own persisted budget accounting.

Still needed: real produce/package photos, blurry/rotated receipts, obscured labels, duplicate photos, aliases and larger held-out corpus; expand beyond these synthetic OCR cases before claiming the most accurate affordable model generally. Human confirmation is mandatory in the app. Never infer remaining pantry stock from a receipt.

Official sources: https://fireworks.ai/models/fireworks/glm-5p3-flash ; https://nebius.com/services/token-factory/models/glm-models-inference . Models also verified through each authenticated inference catalog. No secrets or personal data included.

DeepSeek source: https://fireworks.ai/models?featured=true&serverless=true ; model ID also verified through the authenticated catalog.
