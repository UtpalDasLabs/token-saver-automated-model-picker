# Token Saver: Automating the Model Picker — Anthropic

The full pack, tuned for **Claude**. Every skill names Anthropic models and prices. Average modeled saving across the 13 personas: **69% lower cost, 55% fewer tokens** vs. running everything on Claude Opus 5.5 (pessimistic: 54% / 17%).

## Tiers on this platform

| Tier | Runs on | Use for | Price vs. T3 |
|---|---|---|---|
| T0 Tool | No model: shell, script, formula, regex, linter | Rename, dedupe, link check, format, count, convert, validate | ~0 |
| T1 Micro | Claude Haiku 5.5 (`claude-haiku-5-5`) | Classify, extract, tag, short rewrite, summarise logs, check one rule | ~1/40 |
| T2 Standard | Claude Sonnet 5.5 (`claude-sonnet-5-5`) | Routine production from a clear spec: code to spec, drafts, variants, tables | ~0.50x |
| T3 Strong | Claude Opus 5.5 (`claude-opus-5-5`) | Ambiguity, judgement, architecture, strategy, final review, choosing the winner | 1x |
| T4 Frontier | Claude Fable 5.1 (`claude-fable-5-1`) | Rare. High stakes and T3 at `high` already failed, or very long-horizon work | ~2.5x |

- Haiku 5.5 costs 5x more per token once a prompt passes 100k tokens. Split or compact before that line.
- Batch API: 50% off input and output. Cache hits cost 5% of input price on Opus 5.5 and Sonnet 5.5.

Prices checked 2026-10-20: https://platform.claude.com/docs/en/about-claude/pricing

## Install

### Claude Code

Skills go in `~/.claude/skills/`, the three worker subagents in `~/.claude/agents/`. Each subagent pins its own `model` and `effort`, so delegated work really runs on the cheaper model. Check with `/skills` and `/agents`.

```bash
git clone https://github.com/UtpalDasLabs/token-saver-automated-model-picker.git
cd token-saver-automated-model-picker
./install.sh anthropic                      # everything
./install.sh anthropic social-creator-routing   # base + overlays + one persona
```

[Docs](https://code.claude.com/docs/en/sub-agents)

### Claude.ai

Upload a skill zip under Customize → Skills → + → Upload a skill. The skill prints a routing plan and tells you which model to switch to at each step.

[Docs](https://code.claude.com/docs/en/skills)

### Claude API

Load `routing.json`, look up the task's tier and call that model ID.

[Docs](https://platform.claude.com/docs/en/about-claude/pricing)

## Downloads

- All skills: [`anthropic-all-skills.zip`](../../dist/anthropic/anthropic-all-skills.zip)
- Worker agents: [`anthropic-worker-agents.zip`](../../dist/anthropic/anthropic-worker-agents.zip)

## Pick your persona

| Persona | Who it's for | Cost saved | Tokens saved | Skill | Zip |
|---|---|---:|---:|---|---|
| Data analyst | Data and BI analysts | **84%** | 79% | [SKILL.md](../../skills/anthropic/data-analyst-routing/SKILL.md) | [zip](../../dist/anthropic/data-analyst-routing.zip) |
| Designer | UX and UI designers | **60%** | 55% | [SKILL.md](../../skills/anthropic/designer-routing/SKILL.md) | [zip](../../dist/anthropic/designer-routing.zip) |
| Educator and course creator | Teachers and course creators | **67%** | 56% | [SKILL.md](../../skills/anthropic/educator-creator-routing/SKILL.md) | [zip](../../dist/anthropic/educator-creator-routing.zip) |
| Growth marketer | Marketers, SEO and growth | **65%** | 55% | [SKILL.md](../../skills/anthropic/growth-marketer-routing/SKILL.md) | [zip](../../dist/anthropic/growth-marketer-routing.zip) |
| Job seeker | Job seekers and career changers | **62%** | 54% | [SKILL.md](../../skills/anthropic/job-seeker-routing/SKILL.md) | [zip](../../dist/anthropic/job-seeker-routing.zip) |
| Ops assistant | VAs, ops and chiefs of staff | **83%** | 63% | [SKILL.md](../../skills/anthropic/ops-assistant-routing/SKILL.md) | [zip](../../dist/anthropic/ops-assistant-routing.zip) |
| Product strategy | Product managers and founders | **57%** | 43% | [SKILL.md](../../skills/anthropic/product-strategy-routing/SKILL.md) | [zip](../../dist/anthropic/product-strategy-routing.zip) |
| Research analyst | Analysts, consultants, researchers | **79%** | 33% | [SKILL.md](../../skills/anthropic/research-analyst-routing/SKILL.md) | [zip](../../dist/anthropic/research-analyst-routing.zip) |
| Sales and BD | Sales and business development | **75%** | 51% | [SKILL.md](../../skills/anthropic/sales-bd-routing/SKILL.md) | [zip](../../dist/anthropic/sales-bd-routing.zip) |
| Social creator | Video and social media creators | **73%** | 59% | [SKILL.md](../../skills/anthropic/social-creator-routing/SKILL.md) | [zip](../../dist/anthropic/social-creator-routing.zip) |
| Support and success | Support and customer success | **73%** | 54% | [SKILL.md](../../skills/anthropic/support-success-routing/SKILL.md) | [zip](../../dist/anthropic/support-success-routing.zip) |
| Vibe coder | Indie hackers and AI-assisted builders | **68%** | 65% | [SKILL.md](../../skills/anthropic/vibe-coder-routing/SKILL.md) | [zip](../../dist/anthropic/vibe-coder-routing.zip) |
| Writer and editor | Writers, newsletter authors, editors | **56%** | 45% | [SKILL.md](../../skills/anthropic/writer-editor-routing/SKILL.md) | [zip](../../dist/anthropic/writer-editor-routing.zip) |

Always install `base-model-routing` with a persona skill; the overlays (`cheap-batch-mode`, `judge-best-output`, `high-stakes-review`, `context-diet`) are optional but recommended.
