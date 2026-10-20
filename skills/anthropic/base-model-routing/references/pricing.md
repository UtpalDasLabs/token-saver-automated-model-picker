# Anthropic pricing reference (checked 2026-10-20)

USD per million tokens. Source: https://platform.claude.com/docs/en/about-claude/pricing

| Tier | Model | Input | Output | Applies to |
|---|---|---:|---:|---|
| T1 | Claude Haiku 5.5 (`claude-haiku-5-5`) | $0.10 | $0.50 | prompt ≤ 100k |
| T1 | Claude Haiku 5.5 (`claude-haiku-5-5`) | $0.50 | $2.50 | longer prompts |
| T2 | Claude Sonnet 5.5 (`claude-sonnet-5-5`) | $2.00 | $10.00 | all prompt sizes |
| T3 | Claude Opus 5.5 (`claude-opus-5-5`) | $4.00 | $20.00 | all prompt sizes |
| T4 | Claude Fable 5.1 (`claude-fable-5-1`) | $10.00 | $50.00 | all prompt sizes |

- Haiku 5.5 costs 5x more per token once a prompt passes 100k tokens. Split or compact before that line.
- Batch API: 50% off input and output. Cache hits cost 5% of input price on Opus 5.5 and Sonnet 5.5.

Prices change. Re-check the source page before quoting numbers.