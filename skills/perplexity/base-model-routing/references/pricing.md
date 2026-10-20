# Perplexity pricing reference (checked 2026-10-20)

USD per million tokens. Source: https://docs.perplexity.ai/docs/agent-api/models

| Tier | Model | Input | Output | Applies to |
|---|---|---:|---:|---|
| T1 | GPT-6 Luna (`openai/gpt-6-luna`) | $0.10 | $0.50 | all prompt sizes |
| T2 | Gemini 3.8 Flash (`google/gemini-3.8-flash`) | $0.75 | $3.75 | all prompt sizes |
| T3 | Claude Opus 5.5 (`anthropic/claude-opus-5-5`) | $4.00 | $20.00 | all prompt sizes |
| T4 | Claude Fable 5.1 (`anthropic/claude-fable-5-1`) | $10.00 | $50.00 | all prompt sizes |

- Agent API model prices, which match each provider's direct pricing. Web search and fetch tools are billed separately and not counted.
- For quick web-grounded lookups, `perplexity/sonar` is a good T1 alternative because it searches and cites in one call.

Prices change. Re-check the source page before quoting numbers.