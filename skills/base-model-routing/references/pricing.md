# Pricing reference (checked 2026-10-20)

Standard Claude API list prices, USD per million tokens. Source: [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing).

| Tier | Model | Input | Output | Cache hit | Batch (in / out) |
|---|---|---:|---:|---:|---:|
| T1 | Claude Haiku 5.5 (prompt ≤ 100k) | $0.10 | $0.50 | $0.01 | $0.05 / $0.25 |
| T1 | Claude Haiku 5.5 (prompt > 100k) | $0.50 | $2.50 | $0.05 | $0.25 / $1.25 |
| T2 | Claude Sonnet 5.5 | $2 | $10 | $0.10 | $1 / $5 |
| T3 | Claude Opus 5.5 | $4 | $20 | $0.20 | $2 / $10 |
| T4 | Claude Fable 5.1 | $10 | $50 | $0.25 | $5 / $25 |

Ratios used by this pack: Haiku ≈ 1/40 of Opus, Sonnet = 1/2 of Opus, Fable = 2.5x Opus.

## Effort and output tokens

From [Anthropic's cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence):

- On long coding tasks, `medium` cost about 30–52% less than `high`, and `low` about two thirds less.
- Running all tasks at `low` and rerunning only failures at `high` solved about 97% of tasks at about $0.17 per task, versus 95.3% at $0.29 for everything at `high` (Opus 5.5, SWE-bench Pro subset).
- Compare models by cost per completed task, not cost per token.

## Discounts that stack on top of routing

- Batch API: 50% off input and output for work that can wait up to 24 hours.
- Prompt caching: cache hits cost 5% of input price on Opus 5.5 and Sonnet 5.5. Production agent loops read a median 84.2% of input from cache.

Prices change. Re-check the source page before quoting numbers to anyone.
