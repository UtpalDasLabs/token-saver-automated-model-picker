# Token Saver: Automating the Model Picker — Qwen

The full pack, tuned for **Qwen (Alibaba Cloud Model Studio)**. Every skill names Qwen models and prices. Average modeled saving across the 13 personas: **78% lower cost, 55% fewer tokens** vs. running everything on Qwen3.8-Max (pessimistic: 68% / 17%).

## Tiers on this platform

| Tier | Runs on | Use for | Price vs. T3 |
|---|---|---|---|
| T0 Tool | No model: shell, script, formula, regex, linter | Rename, dedupe, link check, format, count, convert, validate | ~0 |
| T1 Micro | Qwen3.7-Flash (`qwen3.7-flash`) | Classify, extract, tag, short rewrite, summarise logs, check one rule | ~1/55 |
| T2 Standard | Qwen3.7-Plus (`qwen3.7-plus`) | Routine production from a clear spec: code to spec, drafts, variants, tables | ~1/4 |
| T3 Strong | Qwen3.8-Max (`qwen3.8-max`) | Ambiguity, judgement, architecture, strategy, final review, choosing the winner | 1x |
| T4 Frontier | Qwen3.8-Max (thinking) (`qwen3.8-max`) | Rare. High stakes and T3 at `high` already failed, or very long-horizon work | 1x (same model) |

- International deployment list prices. Qwen3.7-Flash costs about 3x more per token above 32k input tokens; keep T1 prompts under 32k.
- Limited-time discounts (for example 20% off Qwen3.7-Plus) are not counted.

Prices checked 2026-10-20: https://www.alibabacloud.com/help/en/model-studio/model-pricing

## Install

### Qwen Code

Skills go in `~/.qwen/skills/`, the three worker subagents in `~/.qwen/agents/`. Each subagent pins its own `model`, so delegated work runs on Qwen3.7-Flash or Qwen3.7-Plus.

```bash
git clone https://github.com/UtpalDasLabs/token-saver-automated-model-picker.git
cd token-saver-automated-model-picker
./install.sh qwen                      # everything
./install.sh qwen social-creator-routing   # base + overlays + one persona
```

[Docs](https://qwenlm.github.io/qwen-code-docs/en/users/features/sub-agents/)

### Model Studio API

Load `routing.json` and call the tier's model; turn thinking on only for T3 judgement and T4.

[Docs](https://www.alibabacloud.com/help/en/model-studio/model-pricing)

## Downloads

- All skills: [`qwen-all-skills.zip`](../../dist/qwen/qwen-all-skills.zip)
- Worker agents: [`qwen-worker-agents.zip`](../../dist/qwen/qwen-worker-agents.zip)

## Pick your persona

| Persona | Who it's for | Cost saved | Tokens saved | Skill | Zip |
|---|---|---:|---:|---|---|
| Data analyst | Data and BI analysts | **88%** | 79% | [SKILL.md](../../skills/qwen/data-analyst-routing/SKILL.md) | [zip](../../dist/qwen/data-analyst-routing.zip) |
| Designer | UX and UI designers | **69%** | 55% | [SKILL.md](../../skills/qwen/designer-routing/SKILL.md) | [zip](../../dist/qwen/designer-routing.zip) |
| Educator and course creator | Teachers and course creators | **77%** | 56% | [SKILL.md](../../skills/qwen/educator-creator-routing/SKILL.md) | [zip](../../dist/qwen/educator-creator-routing.zip) |
| Growth marketer | Marketers, SEO and growth | **75%** | 55% | [SKILL.md](../../skills/qwen/growth-marketer-routing/SKILL.md) | [zip](../../dist/qwen/growth-marketer-routing.zip) |
| Job seeker | Job seekers and career changers | **74%** | 54% | [SKILL.md](../../skills/qwen/job-seeker-routing/SKILL.md) | [zip](../../dist/qwen/job-seeker-routing.zip) |
| Ops assistant | VAs, ops and chiefs of staff | **88%** | 63% | [SKILL.md](../../skills/qwen/ops-assistant-routing/SKILL.md) | [zip](../../dist/qwen/ops-assistant-routing.zip) |
| Product strategy | Product managers and founders | **69%** | 43% | [SKILL.md](../../skills/qwen/product-strategy-routing/SKILL.md) | [zip](../../dist/qwen/product-strategy-routing.zip) |
| Research analyst | Analysts, consultants, researchers | **85%** | 33% | [SKILL.md](../../skills/qwen/research-analyst-routing/SKILL.md) | [zip](../../dist/qwen/research-analyst-routing.zip) |
| Sales and BD | Sales and business development | **82%** | 51% | [SKILL.md](../../skills/qwen/sales-bd-routing/SKILL.md) | [zip](../../dist/qwen/sales-bd-routing.zip) |
| Social creator | Video and social media creators | **81%** | 59% | [SKILL.md](../../skills/qwen/social-creator-routing/SKILL.md) | [zip](../../dist/qwen/social-creator-routing.zip) |
| Support and success | Support and customer success | **81%** | 54% | [SKILL.md](../../skills/qwen/support-success-routing/SKILL.md) | [zip](../../dist/qwen/support-success-routing.zip) |
| Vibe coder | Indie hackers and AI-assisted builders | **79%** | 65% | [SKILL.md](../../skills/qwen/vibe-coder-routing/SKILL.md) | [zip](../../dist/qwen/vibe-coder-routing.zip) |
| Writer and editor | Writers, newsletter authors, editors | **67%** | 45% | [SKILL.md](../../skills/qwen/writer-editor-routing/SKILL.md) | [zip](../../dist/qwen/writer-editor-routing.zip) |

Always install `base-model-routing` with a persona skill; the overlays (`cheap-batch-mode`, `judge-best-output`, `high-stakes-review`, `context-diet`) are optional but recommended.
