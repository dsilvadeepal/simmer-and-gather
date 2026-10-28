# Budget

Operating ceiling: $5/month after credits. Target $0 fixed infrastructure, at most $3 metered AI/search/evaluation/trace charges, $2 reserve. Free hosting/database/storage entitlements and cleanup must be verified before release. Paid Replit is not assumed to fit.

Development vision experiment: $1 maximum across Nebius and Fireworks, reserved $0.05/request, no retry/recharge. Model-specific published GLM-5.3-Flash rates: $0.15/M input, $0.50/M output on each provider (Oct 28). Each test image is 850×360, output capped at 2,000 tokens. Eight calls reserve $0.40; actual token cost recorded separately. This is a development allowance, not the recurring budget.

Illustrative planning envelope at Qwen3-30B rates ($0.10/M input, $0.30/M output): 10k input+2k output costs $0.0016 before repairs, search, traces or stronger fallback. This is arithmetic, not measured planning accuracy or a promise of that workload size. Gate selection on evals. Cache source/version extraction, reuse reviewed tasks, perform arithmetic/calendar/scheduling in code. Disable paid judges by default. Jev access is unverified and optional.

Credits tracker: Nebius $25 and Fireworks $15 recorded received; remaining balances cannot be inferred from those grants. No automatic paid fallback. Unknown call cost retains its reservation until reconciled; budget exhaustion must preserve saved/manual functions.

October 28 clarification: Supabase is optional, not selected. Existing projects use Replit PostgreSQL; Demo Story Studio's design targets Neon. This app uses standard PostgreSQL and can use either. Prefer evaluating Neon Free plus separately budgeted hosting; do not share unrelated project tables/credentials. Google sign-in can handle the initial owner login without buying a separate auth product. Independent upload cleanup support must be checked for the chosen database; pg_cron is not assumed available on every provider.
