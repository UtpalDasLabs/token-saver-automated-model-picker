# Token Saver: Automating the Model Picker — Google

The full pack, tuned for **Gemini**. Every skill names Google models and prices. Average modeled saving across the 13 personas: **72% lower cost, 55% fewer tokens** vs. running everything on Gemini 4 Argon (pessimistic: 59% / 17%).

## Tiers on this platform

| Tier | Runs on | Use for | Price vs. T3 |
|---|---|---|---|
| T0 Tool | No model: shell, script, formula, regex, linter | Rename, dedupe, link check, format, count, convert, validate | ~0 |
| T1 Micro | Gemini 3.1 Flash-Lite (`gemini-3.1-flash-lite`) | Classify, extract, tag, short rewrite, summarise logs, check one rule | ~1/14 |
| T2 Standard | Gemini 3.8 Flash (`gemini-3.8-flash`) | Routine production from a clear spec: code to spec, drafts, variants, tables | ~0.38x |
| T3 Strong | Gemini 4 Argon (`gemini-4-argon`) | Ambiguity, judgement, architecture, strategy, final review, choosing the winner | 1x |
| T4 Frontier | Gemini 4 Argon (high thinking) (`gemini-4-argon`) | Rare. High stakes and T3 at `high` already failed, or very long-horizon work | 1x (same model) |

- Calculated at standard prices. Introductory prices are lower until they expire: Gemini 4 Argon $2/$10 until 30 Nov 2026, Gemini 3.8 Flash $0.75/$3.75 until 31 Dec 2026.
- Batch and Flex processing halve the price for work that can wait.

Prices checked 2026-10-20: https://ai.google.dev/gemini-api/docs/pricing

## Install

### Gemini CLI

Skills go in `~/.gemini/skills/`, the three worker subagents in `~/.gemini/agents/`. Each subagent pins its own `model`, so delegated work runs on Flash-Lite or Flash.

```bash
git clone https://github.com/UtpalDasLabs/token-saver-automated-model-picker.git
cd token-saver-automated-model-picker
./install.sh google                      # everything
./install.sh google social-creator-routing   # base + overlays + one persona
```

[Docs](https://geminicli.com/docs/core/subagents)

### Gemini API and Managed Agents

Managed Agents read skills from `.agents/skills/` in the workspace. For your own code, load `routing.json` and call the tier's model.

[Docs](https://ai.google.dev/gemini-api/docs/pricing)

## Downloads

- All skills: [`google-all-skills.zip`](../../dist/google/google-all-skills.zip)
- Worker agents: [`google-worker-agents.zip`](../../dist/google/google-worker-agents.zip)

## Pick your persona

| Persona | Who it's for | Cost saved | Tokens saved | Skill | Zip |
|---|---|---:|---:|---|---|
| Data analyst | Data and BI analysts | **85%** | 79% | [SKILL.md](../../skills/google/data-analyst-routing/SKILL.md) | [zip](../../dist/google/data-analyst-routing.zip) |
| Designer | UX and UI designers | **63%** | 55% | [SKILL.md](../../skills/google/designer-routing/SKILL.md) | [zip](../../dist/google/designer-routing.zip) |
| Educator and course creator | Teachers and course creators | **71%** | 56% | [SKILL.md](../../skills/google/educator-creator-routing/SKILL.md) | [zip](../../dist/google/educator-creator-routing.zip) |
| Growth marketer | Marketers, SEO and growth | **69%** | 55% | [SKILL.md](../../skills/google/growth-marketer-routing/SKILL.md) | [zip](../../dist/google/growth-marketer-routing.zip) |
| Job seeker | Job seekers and career changers | **66%** | 54% | [SKILL.md](../../skills/google/job-seeker-routing/SKILL.md) | [zip](../../dist/google/job-seeker-routing.zip) |
| Ops assistant | VAs, ops and chiefs of staff | **84%** | 63% | [SKILL.md](../../skills/google/ops-assistant-routing/SKILL.md) | [zip](../../dist/google/ops-assistant-routing.zip) |
| Product strategy | Product managers and founders | **61%** | 43% | [SKILL.md](../../skills/google/product-strategy-routing/SKILL.md) | [zip](../../dist/google/product-strategy-routing.zip) |
| Research analyst | Analysts, consultants, researchers | **79%** | 33% | [SKILL.md](../../skills/google/research-analyst-routing/SKILL.md) | [zip](../../dist/google/research-analyst-routing.zip) |
| Sales and BD | Sales and business development | **76%** | 51% | [SKILL.md](../../skills/google/sales-bd-routing/SKILL.md) | [zip](../../dist/google/sales-bd-routing.zip) |
| Social creator | Video and social media creators | **75%** | 59% | [SKILL.md](../../skills/google/social-creator-routing/SKILL.md) | [zip](../../dist/google/social-creator-routing.zip) |
| Support and success | Support and customer success | **75%** | 54% | [SKILL.md](../../skills/google/support-success-routing/SKILL.md) | [zip](../../dist/google/support-success-routing.zip) |
| Vibe coder | Indie hackers and AI-assisted builders | **72%** | 65% | [SKILL.md](../../skills/google/vibe-coder-routing/SKILL.md) | [zip](../../dist/google/vibe-coder-routing.zip) |
| Writer and editor | Writers, newsletter authors, editors | **60%** | 45% | [SKILL.md](../../skills/google/writer-editor-routing/SKILL.md) | [zip](../../dist/google/writer-editor-routing.zip) |

Always install `base-model-routing` with a persona skill; the overlays (`cheap-batch-mode`, `judge-best-output`, `high-stakes-review`, `context-diet`) are optional but recommended.
