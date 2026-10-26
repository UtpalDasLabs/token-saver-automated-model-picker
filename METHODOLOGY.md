# How the savings are calculated

The percentages are **modeled estimates**, not a lab benchmark. Every input is in this repo and editable, so anyone can check or change them.

## 1. Workloads

Each persona has a realistic week of AI tasks in `data/personas/<persona>.yaml`. For every task type:

- `per_week`: how often it happens
- `base_in_k`: input tokens when run the usual way, with the whole conversation or file in context
- `routed_in_k`: input tokens with the skill's context diet (scoped files, summaries, only relevant rows)
- `out_k`: output tokens at medium effort
- `tier` and `effort`: where the skill routes it
- `p_fail`: chance the routed attempt fails its check

## 2. Platforms and baseline

The same 13 workloads are priced on seven platforms. Each platform file in `data/platforms/` maps the five tiers to real models and official list prices (checked 2026-10-20; Kimi checked 2026-10-26):

| Platform | T1 | T2 | T3 (baseline) | T4 | Price source |
|---|---|---|---|---|---|
| Anthropic | Claude Haiku 5.5 | Claude Sonnet 5.5 | Claude Opus 5.5 | Claude Fable 5.1 | [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| OpenAI | GPT-6 Luna | GPT-6.1 Sol, low effort | GPT-6.1 Sol | GPT-6 Astra | [OpenAI pricing](https://developers.openai.com/api/docs/pricing) |
| Google | Gemini 3.1 Flash-Lite | Gemini 3.8 Flash | Gemini 4 Argon | Argon, high thinking | [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) |
| DeepSeek | V4.1 Flash (`deepseek-flash`), non-thinking | V4.1 Flash, thinking | V4 Pro | V4 Pro, max effort | [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing) |
| Qwen | Qwen3.7-Flash | Qwen3.7-Plus | Qwen3.8-Max | Qwen3.8-Max, thinking | [Model Studio pricing](https://www.alibabacloud.com/help/en/model-studio/model-pricing) |
| Perplexity | GPT-6 Luna | Gemini 3.8 Flash | Claude Opus 5.5 | Claude Fable 5.1 | [Agent API models](https://docs.perplexity.ai/docs/agent-api/models) |
| Kimi | K3.1 Pro, low effort | K3.1 Pro | K3.1 Pro | K3.1 Pro, max effort | [Kimi API pricing](https://platform.moonshot.ai/docs/pricing/chat) |

**Baseline:** every task runs on the platform's T3 model at medium effort with `base_in_k` context — one strong model for everything. Anthropic's own guidance starts most agent workloads on Opus 5.5 at medium ([cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)).

Pricing choices: Google at standard prices (introductory discounts excluded), DeepSeek at peak-hour prices (off-peak halves both sides and leaves percentages unchanged), Qwen at International list prices with context bands, Perplexity at Agent API model prices (search tool fees excluded). Where T2 or T4 is the same model as T3, only the effort setting differs. Kimi has no supported cheaper micro model, so all tiers use K3.1 Pro; its modeled savings come from tools, lower effort and smaller context. Kimi Code membership quota is not the same as pay-as-you-go Kimi API spending.

## 3. Routed

Each task runs on its platform's tier model with `routed_in_k` context, and:

- **Effort** changes output tokens: low = 0.55x, high = 1.6x of medium. Based on Anthropic's measurement that on long coding tasks medium cost about 30–52% less than high, and low about two thirds less.
- **Smaller models write a bit more**: T1 and T2 output x1.1 when they are a different model from T3.
- **Failures are paid for**: with probability `p_fail`, the attempt is wasted and redone one tier up at medium effort with 0.5k extra tokens of error notes.
- **Routing has a cost**: every delegated task adds 0.4k input + 0.15k output on the T3 model for writing the brief and reading the result, and each session adds 4k input on the T3 model for loading the skills.
- **T0 tool tasks** are charged as a small T1 call that writes or runs the command.

## 4. Prices

Full per-platform price tables, including context bands, are in each `data/platforms/<platform>.yaml` and in every package's `base-model-routing/references/pricing.md`.

## 5. Outputs

- **Tokens saved** = 1 − routed tokens / baseline tokens (input + output, including retries and overhead).
- **Cost saved** = 1 − routed cost / baseline cost.
- **Pessimistic case**: failure rates doubled, only half of the context-diet reduction achieved, small-model output +10%.

## 6. Why platforms differ

Token savings are almost identical across platforms, because tokens come from the context diet, not prices. Cost savings differ with the price gap inside each platform: the cheaper T1 and T2 are relative to T3, the bigger the saving. Qwen and Perplexity save most because their small models cost a few percent of the strong one. Kimi has no supported cheaper micro model, so its savings depend on lower effort and context discipline rather than model-price arbitrage.

## 7. What is not counted

- Prompt caching and Batch API discounts. Both stack on top and would increase savings.
- Quality differences beyond the failure rate. The skills keep judgement and high-stakes work on T3 for that reason.
- Human time.

## 8. Reading the results

- **Cost savings are robust** because they mostly come from routing routine work to cheaper models. They stay well above zero for every persona and platform in the pessimistic case.
- **Token savings are fragile** because they come from context discipline. If you keep pasting whole files into every request, expect the pessimistic number.
- Research-heavy work saves the least tokens: reading sources is irreducible. It still saves a lot of money, because the T1 model does the reading.

Have real usage data? Open a PR with before/after numbers from your console. Measured results beat models.
