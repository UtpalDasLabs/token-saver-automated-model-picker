# OpenAI pricing reference (checked 2026-10-20)

USD per million tokens. Source: https://developers.openai.com/api/docs/pricing

| Tier | Model | Input | Output | Applies to |
|---|---|---:|---:|---|
| T1 | GPT-6 Luna (`gpt-6-luna`) | $0.10 | $0.50 | all prompt sizes |
| T2 | GPT-6.1 Sol (low effort) (`gpt-6.1-sol`) | $2.00 | $10.00 | all prompt sizes |
| T3 | GPT-6.1 Sol (`gpt-6.1-sol`) | $2.00 | $10.00 | all prompt sizes |
| T4 | GPT-6 Astra (`gpt-6-astra`) | $10.00 | $50.00 | all prompt sizes |

- T2 and T3 use the same model, GPT-6.1 Sol. The saving between them comes from reasoning effort: run routine work at `low`, judgement at `medium` or `high`.
- Long prompts cost more on GPT-6.1 Sol and GPT-6 Luna above 272k tokens. Batch and Flex processing are cheaper for work that can wait.

Prices change. Re-check the source page before quoting numbers.