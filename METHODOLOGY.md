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

## 2. Baseline

Every task runs on **Claude Opus 5.5 at medium effort** (its default) with `base_in_k` context. That reflects a common setup: one strong model for everything. Anthropic's own guidance starts most agent workloads on Opus 5.5 at medium ([cost guide](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence)).

## 3. Routed

Each task runs on its tier's model with `routed_in_k` context, and:

- **Effort** changes output tokens: low = 0.55x, high = 1.6x of medium. Based on Anthropic's measurement that on long coding tasks medium cost about 30–52% less than high, and low about two thirds less.
- **Smaller models write a bit more**: T1 and T2 output x1.1.
- **Failures are paid for**: with probability `p_fail`, the attempt is wasted and redone one tier up at medium effort with 0.5k extra tokens of error notes.
- **Routing has a cost**: every delegated task adds 0.4k input + 0.15k output on Opus for writing the brief and reading the result, and each session adds 4k input on Opus for loading the skills.
- **T0 tool tasks** are charged as a small Haiku call that writes or runs the command.

## 4. Prices

Anthropic standard list prices, USD per million tokens, checked 2026-10-20 ([source](https://platform.claude.com/docs/en/about-claude/pricing)):

| Model | Input | Output |
|---|---:|---:|
| Haiku 5.5 (prompt ≤ 100k) | 0.10 | 0.50 |
| Haiku 5.5 (prompt > 100k) | 0.50 | 2.50 |
| Sonnet 5.5 | 2 | 10 |
| Opus 5.5 | 4 | 20 |
| Fable 5.1 | 10 | 50 |

## 5. Outputs

- **Tokens saved** = 1 − routed tokens / baseline tokens (input + output, including retries and overhead).
- **Cost saved** = 1 − routed cost / baseline cost.
- **Pessimistic case**: failure rates doubled, only half of the context-diet reduction achieved, small-model output +10%.
- **vs. all-Sonnet** (in RESULTS.md): the same routed plan compared with running everything on Sonnet 5.5, to show the gain is not just "use a cheaper model".

## 6. What is not counted

- Prompt caching and Batch API discounts. Both stack on top and would increase savings.
- Quality differences beyond the failure rate. The skills keep judgement and high-stakes work on Opus for that reason.
- Human time.

## 7. Reading the results

- **Cost savings are robust** because they mostly come from routing routine work to cheaper models. They stay above 39% for every persona in the pessimistic case.
- **Token savings are fragile** because they come from context discipline. If you keep pasting whole files into every request, expect the pessimistic number.
- Research-heavy work saves the least tokens: reading sources is irreducible. It still saves a lot of money, because Haiku does the reading.

Have real usage data? Open a PR with before/after numbers from your console. Measured results beat models.
