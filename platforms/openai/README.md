# Token Saver: Automating the Model Picker — OpenAI

The full pack, tuned for **GPT, ChatGPT and Codex**. Every skill names OpenAI models and prices. Average modeled saving across the 13 personas: **61% lower cost, 56% fewer tokens** vs. running everything on GPT-6.1 Sol (pessimistic: 37% / 18%).

## Tiers on this platform

| Tier | Runs on | Use for | Price vs. T3 |
|---|---|---|---|
| T0 Tool | No model: shell, script, formula, regex, linter | Rename, dedupe, link check, format, count, convert, validate | ~0 |
| T1 Micro | GPT-6 Luna (`gpt-6-luna`) | Classify, extract, tag, short rewrite, summarise logs, check one rule | ~1/20 |
| T2 Standard | GPT-6.1 Sol (low effort) (`gpt-6.1-sol`) | Routine production from a clear spec: code to spec, drafts, variants, tables | 1x (same model) |
| T3 Strong | GPT-6.1 Sol (`gpt-6.1-sol`) | Ambiguity, judgement, architecture, strategy, final review, choosing the winner | 1x |
| T4 Frontier | GPT-6 Astra (`gpt-6-astra`) | Rare. High stakes and T3 at `high` already failed, or very long-horizon work | ~5.0x |

- T2 and T3 use the same model, GPT-6.1 Sol. The saving between them comes from reasoning effort: run routine work at `low`, judgement at `medium` or `high`.
- Long prompts cost more on GPT-6.1 Sol and GPT-6 Luna above 272k tokens. Batch and Flex processing are cheaper for work that can wait.

Prices checked 2026-10-20: https://developers.openai.com/api/docs/pricing

## Install

### Codex (CLI, IDE, app)

Skills go in `~/.agents/skills/`, the three worker agents (TOML) in `~/.codex/agents/`. Each agent pins `model` and `model_reasoning_effort`, so delegated work runs on GPT-6 Luna or Sol at low effort.

```bash
git clone https://github.com/UtpalDasLabs/token-saver-automated-model-picker.git
cd token-saver-automated-model-picker
./install.sh openai                      # everything
./install.sh openai social-creator-routing   # base + overlays + one persona
```

[Docs](https://learn.chatgpt.com/docs/agent-configuration/subagents)

### ChatGPT

Add a skill zip where your ChatGPT plan supports skills. The skill prints a routing plan and tells you when to switch between GPT-6 Luna, GPT-6 and GPT-6 Pro.

[Docs](https://learn.chatgpt.com/docs/build-skills)

### OpenAI API

Load `routing.json`, look up the task's tier and call that model with the listed `reasoning.effort`.

[Docs](https://developers.openai.com/api/docs/pricing)

## Downloads

- All skills: [`openai-all-skills.zip`](../../dist/openai/openai-all-skills.zip)
- Worker agents: [`openai-worker-agents.zip`](../../dist/openai/openai-worker-agents.zip)

## Pick your persona

| Persona | Who it's for | Cost saved | Tokens saved | Skill | Zip |
|---|---|---:|---:|---|---|
| Data analyst | Data and BI analysts | **78%** | 80% | [SKILL.md](../../skills/openai/data-analyst-routing/SKILL.md) | [zip](../../dist/openai/data-analyst-routing.zip) |
| Designer | UX and UI designers | **51%** | 55% | [SKILL.md](../../skills/openai/designer-routing/SKILL.md) | [zip](../../dist/openai/designer-routing.zip) |
| Educator and course creator | Teachers and course creators | **55%** | 57% | [SKILL.md](../../skills/openai/educator-creator-routing/SKILL.md) | [zip](../../dist/openai/educator-creator-routing.zip) |
| Growth marketer | Marketers, SEO and growth | **56%** | 57% | [SKILL.md](../../skills/openai/growth-marketer-routing/SKILL.md) | [zip](../../dist/openai/growth-marketer-routing.zip) |
| Job seeker | Job seekers and career changers | **53%** | 56% | [SKILL.md](../../skills/openai/job-seeker-routing/SKILL.md) | [zip](../../dist/openai/job-seeker-routing.zip) |
| Ops assistant | VAs, ops and chiefs of staff | **79%** | 64% | [SKILL.md](../../skills/openai/ops-assistant-routing/SKILL.md) | [zip](../../dist/openai/ops-assistant-routing.zip) |
| Product strategy | Product managers and founders | **47%** | 44% | [SKILL.md](../../skills/openai/product-strategy-routing/SKILL.md) | [zip](../../dist/openai/product-strategy-routing.zip) |
| Research analyst | Analysts, consultants, researchers | **73%** | 34% | [SKILL.md](../../skills/openai/research-analyst-routing/SKILL.md) | [zip](../../dist/openai/research-analyst-routing.zip) |
| Sales and BD | Sales and business development | **67%** | 52% | [SKILL.md](../../skills/openai/sales-bd-routing/SKILL.md) | [zip](../../dist/openai/sales-bd-routing.zip) |
| Social creator | Video and social media creators | **65%** | 61% | [SKILL.md](../../skills/openai/social-creator-routing/SKILL.md) | [zip](../../dist/openai/social-creator-routing.zip) |
| Support and success | Support and customer success | **64%** | 54% | [SKILL.md](../../skills/openai/support-success-routing/SKILL.md) | [zip](../../dist/openai/support-success-routing.zip) |
| Vibe coder | Indie hackers and AI-assisted builders | **60%** | 67% | [SKILL.md](../../skills/openai/vibe-coder-routing/SKILL.md) | [zip](../../dist/openai/vibe-coder-routing.zip) |
| Writer and editor | Writers, newsletter authors, editors | **44%** | 46% | [SKILL.md](../../skills/openai/writer-editor-routing/SKILL.md) | [zip](../../dist/openai/writer-editor-routing.zip) |

Always install `base-model-routing` with a persona skill; the overlays (`cheap-batch-mode`, `judge-best-output`, `high-stakes-review`, `context-diet`) are optional but recommended.
