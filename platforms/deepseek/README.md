# Token Saver: Automating the Model Picker — DeepSeek

The full pack, tuned for **DeepSeek V4**. Every skill names DeepSeek models and prices. Average modeled saving across the 13 personas: **74% lower cost, 55% fewer tokens** vs. running everything on DeepSeek V4 Pro (pessimistic: 61% / 17%).

## Tiers on this platform

| Tier | Runs on | Use for | Price vs. T3 |
|---|---|---|---|
| T0 Tool | No model: shell, script, formula, regex, linter | Rename, dedupe, link check, format, count, convert, validate | ~0 |
| T1 Micro | DeepSeek V4.1 Flash (non-thinking) (`deepseek-flash`) | Classify, extract, tag, short rewrite, summarise logs, check one rule | ~1/4 |
| T2 Standard | DeepSeek V4.1 Flash (thinking) (`deepseek-flash`) | Routine production from a clear spec: code to spec, drafts, variants, tables | ~1/4 |
| T3 Strong | DeepSeek V4 Pro (`deepseek-v4-pro`) | Ambiguity, judgement, architecture, strategy, final review, choosing the winner | 1x |
| T4 Frontier | DeepSeek V4 Pro (max effort) (`deepseek-v4-pro`) | Rare. High stakes and T3 at `high` already failed, or very long-horizon work | 1x (same model) |

- Calculated at peak-hour prices. Off-peak prices are half, which lowers both sides equally and does not change the percentages.
- DeepSeek has no model above V4 Pro, so T4 means V4 Pro at maximum reasoning effort. For the rarest, highest-stakes calls, a second opinion from another provider is a reasonable T4.

Prices checked 2026-10-20: https://api-docs.deepseek.com/quick_start/pricing

## Install

### DeepSeek Harness

Skills go in `~/.agents/skills/` (or `.dsh/skills/` in a project). The skill writes a routing plan and keeps cheap steps on Flash with small context.

```bash
git clone https://github.com/UtpalDasLabs/token-saver-automated-model-picker.git
cd token-saver-automated-model-picker
./install.sh deepseek                      # everything
./install.sh deepseek social-creator-routing   # base + overlays + one persona
```

[Docs](https://deepseek-harness.github.io/deepseek-harness/en/reference/subsystems/skills)

### Claude Code or Codex on the DeepSeek API

DeepSeek's API supports the Anthropic and OpenAI interfaces, so Claude Code and Codex can run on it. Install with `--tool claude-code`: the worker subagents pin `deepseek-flash` and `deepseek-v4-pro`.

```bash
git clone https://github.com/UtpalDasLabs/token-saver-automated-model-picker.git
cd token-saver-automated-model-picker
./install.sh deepseek --tool claude-code                      # everything
./install.sh deepseek --tool claude-code social-creator-routing   # base + overlays + one persona
```

[Docs](https://api-docs.deepseek.com/updates/)

### DeepSeek API

Load `routing.json` and call `deepseek-flash` (thinking off for T1, on for T2) or `deepseek-v4-pro`.

[Docs](https://api-docs.deepseek.com/quick_start/pricing)

## Downloads

- All skills: [`deepseek-all-skills.zip`](../../dist/deepseek/deepseek-all-skills.zip)
- Worker agents: [`deepseek-worker-agents.zip`](../../dist/deepseek/deepseek-worker-agents.zip)

## Pick your persona

| Persona | Who it's for | Cost saved | Tokens saved | Skill | Zip |
|---|---|---:|---:|---|---|
| Data analyst | Data and BI analysts | **87%** | 79% | [SKILL.md](../../skills/deepseek/data-analyst-routing/SKILL.md) | [zip](../../dist/deepseek/data-analyst-routing.zip) |
| Designer | UX and UI designers | **67%** | 55% | [SKILL.md](../../skills/deepseek/designer-routing/SKILL.md) | [zip](../../dist/deepseek/designer-routing.zip) |
| Educator and course creator | Teachers and course creators | **75%** | 56% | [SKILL.md](../../skills/deepseek/educator-creator-routing/SKILL.md) | [zip](../../dist/deepseek/educator-creator-routing.zip) |
| Growth marketer | Marketers, SEO and growth | **72%** | 55% | [SKILL.md](../../skills/deepseek/growth-marketer-routing/SKILL.md) | [zip](../../dist/deepseek/growth-marketer-routing.zip) |
| Job seeker | Job seekers and career changers | **71%** | 54% | [SKILL.md](../../skills/deepseek/job-seeker-routing/SKILL.md) | [zip](../../dist/deepseek/job-seeker-routing.zip) |
| Ops assistant | VAs, ops and chiefs of staff | **82%** | 63% | [SKILL.md](../../skills/deepseek/ops-assistant-routing/SKILL.md) | [zip](../../dist/deepseek/ops-assistant-routing.zip) |
| Product strategy | Product managers and founders | **65%** | 43% | [SKILL.md](../../skills/deepseek/product-strategy-routing/SKILL.md) | [zip](../../dist/deepseek/product-strategy-routing.zip) |
| Research analyst | Analysts, consultants, researchers | **75%** | 33% | [SKILL.md](../../skills/deepseek/research-analyst-routing/SKILL.md) | [zip](../../dist/deepseek/research-analyst-routing.zip) |
| Sales and BD | Sales and business development | **77%** | 51% | [SKILL.md](../../skills/deepseek/sales-bd-routing/SKILL.md) | [zip](../../dist/deepseek/sales-bd-routing.zip) |
| Social creator | Video and social media creators | **77%** | 59% | [SKILL.md](../../skills/deepseek/social-creator-routing/SKILL.md) | [zip](../../dist/deepseek/social-creator-routing.zip) |
| Support and success | Support and customer success | **77%** | 54% | [SKILL.md](../../skills/deepseek/support-success-routing/SKILL.md) | [zip](../../dist/deepseek/support-success-routing.zip) |
| Vibe coder | Indie hackers and AI-assisted builders | **77%** | 65% | [SKILL.md](../../skills/deepseek/vibe-coder-routing/SKILL.md) | [zip](../../dist/deepseek/vibe-coder-routing.zip) |
| Writer and editor | Writers, newsletter authors, editors | **64%** | 45% | [SKILL.md](../../skills/deepseek/writer-editor-routing/SKILL.md) | [zip](../../dist/deepseek/writer-editor-routing.zip) |

Always install `base-model-routing` with a persona skill; the overlays (`cheap-batch-mode`, `judge-best-output`, `high-stakes-review`, `context-diet`) are optional but recommended.
