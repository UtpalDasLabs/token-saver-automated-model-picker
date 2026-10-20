# Token Saver: Automating the Model Picker — Perplexity

The full pack, tuned for **Perplexity Computer and Agent API**. Every skill names Perplexity models and prices. Average modeled saving across the 13 personas: **76% lower cost, 55% fewer tokens** vs. running everything on Claude Opus 5.5 (pessimistic: 66% / 17%).

## Tiers on this platform

| Tier | Runs on | Use for | Price vs. T3 |
|---|---|---|---|
| T0 Tool | No model: shell, script, formula, regex, linter | Rename, dedupe, link check, format, count, convert, validate | ~0 |
| T1 Micro | GPT-6 Luna (`openai/gpt-6-luna`) | Classify, extract, tag, short rewrite, summarise logs, check one rule | ~1/40 |
| T2 Standard | Gemini 3.8 Flash (`google/gemini-3.8-flash`) | Routine production from a clear spec: code to spec, drafts, variants, tables | ~1/5 |
| T3 Strong | Claude Opus 5.5 (`anthropic/claude-opus-5-5`) | Ambiguity, judgement, architecture, strategy, final review, choosing the winner | 1x |
| T4 Frontier | Claude Fable 5.1 (`anthropic/claude-fable-5-1`) | Rare. High stakes and T3 at `high` already failed, or very long-horizon work | ~2.5x |

- Agent API model prices, which match each provider's direct pricing. Web search and fetch tools are billed separately and not counted.
- For quick web-grounded lookups, `perplexity/sonar` is a good T1 alternative because it searches and cites in one call.

Prices checked 2026-10-20: https://docs.perplexity.ai/docs/agent-api/models

## Install

### Perplexity Computer

Import the whole pack as a plugin: Plugins → Add custom → Import plugin from GitHub, and paste the URL of `dist/perplexity/plugin`. Or upload a single skill zip under Plugins → Add custom → Skill. The skill makes Computer plan by tier and keep cheap steps cheap.

[Docs](https://www.perplexity.ai/help-center/en/articles/2026100802-create-or-upload-a-custom-plugin)

### Perplexity Agent API

Upload skills with the Skills API, then set `model` per request from `routing.json`. One API key covers all four tiers across providers.

[Docs](https://docs.perplexity.ai/docs/agent-api/skills)

## Downloads

- All skills: [`perplexity-all-skills.zip`](../../dist/perplexity/perplexity-all-skills.zip)
- Perplexity plugin (all 18 skills): import from GitHub with the folder URL `https://github.com/UtpalDasLabs/token-saver-automated-model-picker/tree/main/dist/perplexity/plugin`, or upload [`token-saver-perplexity-plugin.zip`](../../dist/perplexity/token-saver-perplexity-plugin.zip)

## Pick your persona

| Persona | Who it's for | Cost saved | Tokens saved | Skill | Zip |
|---|---|---:|---:|---|---|
| Data analyst | Data and BI analysts | **87%** | 79% | [SKILL.md](../../skills/perplexity/data-analyst-routing/SKILL.md) | [zip](../../dist/perplexity/data-analyst-routing.zip) |
| Designer | UX and UI designers | **66%** | 55% | [SKILL.md](../../skills/perplexity/designer-routing/SKILL.md) | [zip](../../dist/perplexity/designer-routing.zip) |
| Educator and course creator | Teachers and course creators | **77%** | 56% | [SKILL.md](../../skills/perplexity/educator-creator-routing/SKILL.md) | [zip](../../dist/perplexity/educator-creator-routing.zip) |
| Growth marketer | Marketers, SEO and growth | **73%** | 55% | [SKILL.md](../../skills/perplexity/growth-marketer-routing/SKILL.md) | [zip](../../dist/perplexity/growth-marketer-routing.zip) |
| Job seeker | Job seekers and career changers | **71%** | 54% | [SKILL.md](../../skills/perplexity/job-seeker-routing/SKILL.md) | [zip](../../dist/perplexity/job-seeker-routing.zip) |
| Ops assistant | VAs, ops and chiefs of staff | **86%** | 63% | [SKILL.md](../../skills/perplexity/ops-assistant-routing/SKILL.md) | [zip](../../dist/perplexity/ops-assistant-routing.zip) |
| Product strategy | Product managers and founders | **65%** | 43% | [SKILL.md](../../skills/perplexity/product-strategy-routing/SKILL.md) | [zip](../../dist/perplexity/product-strategy-routing.zip) |
| Research analyst | Analysts, consultants, researchers | **83%** | 33% | [SKILL.md](../../skills/perplexity/research-analyst-routing/SKILL.md) | [zip](../../dist/perplexity/research-analyst-routing.zip) |
| Sales and BD | Sales and business development | **81%** | 51% | [SKILL.md](../../skills/perplexity/sales-bd-routing/SKILL.md) | [zip](../../dist/perplexity/sales-bd-routing.zip) |
| Social creator | Video and social media creators | **80%** | 59% | [SKILL.md](../../skills/perplexity/social-creator-routing/SKILL.md) | [zip](../../dist/perplexity/social-creator-routing.zip) |
| Support and success | Support and customer success | **79%** | 54% | [SKILL.md](../../skills/perplexity/support-success-routing/SKILL.md) | [zip](../../dist/perplexity/support-success-routing.zip) |
| Vibe coder | Indie hackers and AI-assisted builders | **77%** | 65% | [SKILL.md](../../skills/perplexity/vibe-coder-routing/SKILL.md) | [zip](../../dist/perplexity/vibe-coder-routing.zip) |
| Writer and editor | Writers, newsletter authors, editors | **65%** | 45% | [SKILL.md](../../skills/perplexity/writer-editor-routing/SKILL.md) | [zip](../../dist/perplexity/writer-editor-routing.zip) |

Always install `base-model-routing` with a persona skill; the overlays (`cheap-batch-mode`, `judge-best-output`, `high-stakes-review`, `context-diet`) are optional but recommended.
