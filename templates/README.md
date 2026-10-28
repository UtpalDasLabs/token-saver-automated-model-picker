# {{NAME}}

**Stop paying top-model prices for bottom-model work.** An open-source pack of [Agent Skills](https://agentskills.io) that picks the model for you: each AI task goes to the cheapest model that can actually finish it — a script, a small model, a mid model or the flagship — and moves up only when a check fails.

Packaged for **Anthropic, OpenAI, Google, DeepSeek, Qwen, Perplexity and Kimi**, with one skill for each of 13 ways of working: vibe coding, social video, product, research, ops, marketing, writing, data, design, sales, support, teaching and job search.

| Modeled across 7 platforms × 13 personas | Average | Pessimistic case |
|---|---:|---:|
| **Cost saved** | **{{AVG_COST}}%** | {{CONS_COST}}% |
| **Tokens saved** | **{{AVG_TOKENS}}%** | {{CONS_TOKENS}}% |

Cost savings range from {{RANGE_LO}}% to {{RANGE_HI}}% depending on persona and platform. Compared with running every task on each platform's strong everyday model with full context, including failed attempts, escalations and the routing overhead itself. [How it's calculated](METHODOLOGY.md) · [Every persona on every platform](benchmarks/RESULTS.md) · [Website]({{SITE}})

## Watch the product demo

[![Token Saver product demo](docs/token-saver-poster.jpg)](docs/Token-Saver-Product-Demo.mp4)

[Watch the 38-second demo](docs/Token-Saver-Product-Demo.mp4): the cost problem, smart model routing, platform and workflow selection, and the modeled savings.

![Modeled cost savings by persona and platform](docs/savings.svg)

---

## Find your package in 3 steps

1. **Pick your platform** — the AI you already pay for.
2. **Pick your persona** — the row that sounds like your week.
3. **Install** `base-model-routing` + your persona skill (zip link in the cell, or `./install.sh <platform> <persona>`).

Each cell shows the modeled **cost saving** for that persona on that platform. Click the percentage for the skill file, or **zip** to download it.

{{FINDER}}

Not sure which persona? Pick the one whose most frequent task matches yours; you can install several. The four overlays (`cheap-batch-mode`, `judge-best-output`, `high-stakes-review`, `context-diet`) work with any persona.

## Platforms

{{PLATFORM_TABLE}}

Each platform guide lists its model tiers, verified prices, install steps for every tool, and downloads.

## How it works

Every skill uses the same five-step ladder, mapped to each platform's models:

| Tier | Role | Anthropic | OpenAI | Google | DeepSeek | Qwen | Perplexity | Kimi |
|---|---|---|---|---|---|---|---|---|
| **T0** | Scripts and tools, no model | — | — | — | — | — | — | — |
| **T1** | Micro: tag, extract, summarise | Haiku 5.5 | GPT-6 Luna | Gemini 3.1 Flash-Lite | V4.1 Flash | Qwen3.7-Flash | GPT-6 Luna | K3.1 Pro (low) |
| **T2** | Standard: production from a clear spec | Sonnet 5.5 | GPT-6.1 Sol (low effort) | Gemini 3.8 Flash | V4.1 Flash (thinking) | Qwen3.7-Plus | Gemini 3.8 Flash | K3.1 Pro |
| **T3** | Strong: judgement, strategy, review | Opus 5.5 | GPT-6.1 Sol | Gemini 4 Argon | V4 Pro | Qwen3.8-Max | Claude Opus 5.5 | K3.1 Pro |
| **T4** | Frontier: rare, high stakes | Fable 5.1 | GPT-6 Astra | Argon (high thinking) | V4 Pro (max effort) | Qwen3.8-Max (thinking) | Claude Fable 5.1 | K3.1 Pro (max) |

The strong model thinks; the mid model produces; the small model and scripts do the chores. Escalate one tier at a time, only after a check fails. Anything public, irreversible or "which option is best" starts at T3.

**What a skill does in practice.** Ask: "Turn my 25-minute video into 5 Reels with captions and hashtags, and tell me which to post first." With `social-creator-routing` loaded, the agent plans before it spends:

```text
ROUTING PLAN
1. [T1] haiku/low       Clean transcript, keep timestamps
2. [T1] haiku/low       Summarise into 12 key moments with timestamps
3. [T2] sonnet/medium   Draft 5 Reels: in/out times, hook, on-screen text
4. [T2] sonnet/low      3 caption variants per Reel
5. [T1] haiku/low       Hashtags + alt text per Reel (batch of 5)
6. [T3] opus/medium     Rank the 5 Reels and pick the first to post, with reason
7. [T0] script          Rename clip files, build upload CSV
```

On OpenAI the same plan reads `luna/low`, `sol/medium`; on Qwen `flash/low`, `plus/medium`, `max/medium`; and so on.

## Install

```bash
git clone {{REPO}}.git
cd token-saver-automated-model-picker
./install.sh <platform> [--tool <tool>] [persona-skill ...]
```

| You use | Command | Where it installs | Model switching |
|---|---|---|---|
| Claude Code | `./install.sh anthropic` | `~/.claude/skills`, `~/.claude/agents` | Automatic (subagents pin `haiku`/`sonnet`/`opus`) |
| Claude.ai | Upload a zip from `dist/anthropic/` | Customize → Skills | Skill tells you which model to pick |
| Codex | `./install.sh openai` | `~/.agents/skills`, `~/.codex/agents` | Automatic (custom agents pin model + reasoning effort) |
| ChatGPT | Add a zip from `dist/openai/` | Skills | Skill tells you which model to pick |
| Gemini CLI | `./install.sh google` | `~/.gemini/skills`, `~/.gemini/agents` | Automatic (subagents pin `model`) |
| Qwen Code | `./install.sh qwen` | `~/.qwen/skills`, `~/.qwen/agents` | Automatic (subagents pin `model`) |
| DeepSeek Harness | `./install.sh deepseek` | `~/.agents/skills` | Routing plan |
| Claude Code on the DeepSeek API | `./install.sh deepseek --tool claude-code` | `~/.claude/skills`, `~/.claude/agents` | Automatic (`deepseek-flash` / `deepseek-v4-pro`) |
| Perplexity Computer | Plugins → Add custom → Import plugin from GitHub → paste `{{REPO}}/tree/main/dist/perplexity/plugin` | Your plugins | Routing plan |
| Kimi Code | `./install.sh kimi` | `~/.kimi-code/skills` (`PREFIX=.` for project skills) | Routing plan; choose model/effort with `/model` |
| Any API / agent framework | Read [`routing.json`](routing.json) | — | Your code picks the model per task |

Always install `base-model-routing` with a persona; the installer does this for you.

## Where the savings come from

1. **Routing** — most weekly tasks are routine. Moving them to a model that costs a fraction of the flagship is where the cost saving comes from. It holds up in the pessimistic case.
2. **Context diet** — sending a worker 5k tokens of relevant context instead of 40k of conversation is where the token saving comes from. It depends on discipline, which is why the pessimistic number is much lower.
3. **No model at all** — renames, link checks, CSV cleanup and arithmetic run as scripts.

The size of the saving depends on the price gap inside each platform. Qwen and Perplexity save the most because their small models are very cheap relative to their strong ones. Kimi has no supported cheaper micro model, so its savings come from tools, lower effort and smaller context. Prompt caching, batch and off-peak discounts are not counted and stack on top.

## Measure your own

The numbers come from modeled weekly workloads in [`data/personas/`](data/personas) and verified list prices in [`data/platforms/`](data/platforms). Edit them to match your week:

```bash
pip install pyyaml
python3 benchmarks/calculate.py   # recompute savings
python3 tools/build.py            # regenerate every skill, package, guide and this README
python3 tools/chart.py            # redraw the chart
```

For real numbers, run the same week with and without the skill and compare your provider's usage dashboard. PRs with measured before/after results are very welcome.

## Repo layout

```text
skills/<platform>/<skill>/SKILL.md   126 generated skills (18 per platform)
agents/<platform>/<tool>/            worker agents: Claude Code, Codex, Gemini CLI, Qwen Code
platforms/<platform>/README.md       install guide + savings per persona
dist/<platform>/*.zip                ready-to-upload zips (+ Perplexity plugin)
data/personas/*.yaml                 13 persona workloads and routing tables
data/platforms/*.yaml                7 platforms: tiers, models, prices, tools
templates/                           base skill, overlays, workers, this README
benchmarks/                          assumptions, calculator, results
routing.json                         machine-readable tiers + routing tables
```

## Contributing

Add a persona (copy a file in `data/personas/`) or a platform (copy a file in `data/platforms/`), run the three commands above, and open a PR. Keep task counts realistic, cite official price pages, and explain any change to the assumptions.

## Licence

MIT © Utpal Das. Built in [Labs]({{SITE}}). Prices change; every platform file links its official pricing page — re-check before quoting numbers.
