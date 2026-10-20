# Qwen pricing reference (checked 2026-10-20)

USD per million tokens. Source: https://www.alibabacloud.com/help/en/model-studio/model-pricing

| Tier | Model | Input | Output | Applies to |
|---|---|---:|---:|---|
| T1 | Qwen3.7-Flash (`qwen3.7-flash`) | $0.03 | $0.13 | prompt ≤ 32k |
| T1 | Qwen3.7-Flash (`qwen3.7-flash`) | $0.10 | $0.40 | prompt ≤ 256k |
| T2 | Qwen3.7-Plus (`qwen3.7-plus`) | $0.40 | $1.60 | all prompt sizes |
| T3 | Qwen3.8-Max (`qwen3.8-max`) | $2.00 | $6.00 | all prompt sizes |
| T4 | Qwen3.8-Max (thinking) (`qwen3.8-max`) | $2.00 | $6.00 | all prompt sizes |

- International deployment list prices. Qwen3.7-Flash costs about 3x more per token above 32k input tokens; keep T1 prompts under 32k.
- Limited-time discounts (for example 20% off Qwen3.7-Plus) are not counted.

Prices change. Re-check the source page before quoting numbers.