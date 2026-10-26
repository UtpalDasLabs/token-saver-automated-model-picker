# Token Saver: Automating the Model Picker — Kimi

The full pack, tuned for **Kimi K3.1 Pro**. Every skill names Kimi models and prices. Average modeled saving across the 13 personas: **45% lower cost, 55% fewer tokens** vs. running everything on Kimi K3.1 Pro (pessimistic: 13% / 17%).

## Tiers on this platform

| Tier | Runs on | Use for | Price vs. T3 |
|---|---|---|---|
| T0 Tool | No model: shell, script, formula, regex, linter | Rename, dedupe, link check, format, count, convert, validate | ~0 |
| T1 Micro | Kimi K3.1 Pro (low effort) (`kimi-k3.1-pro`) | Classify, extract, tag, short rewrite, summarise logs, check one rule | 1x (same model) |
| T2 Standard | Kimi K3.1 Pro (`kimi-k3.1-pro`) | Routine production from a clear spec: code to spec, drafts, variants, tables | 1x (same model) |
| T3 Strong | Kimi K3.1 Pro (`kimi-k3.1-pro`) | Ambiguity, judgement, architecture, strategy, final review, choosing the winner | 1x |
| T4 Frontier | Kimi K3.1 Pro (max effort) (`kimi-k3.1-pro`) | Rare. High stakes and T3 at `high` already failed, or very long-horizon work | 1x (same model) |

- Kimi API list prices. T1-T4 use K3.1 Pro because no supported cheaper micro model is available; savings come from tools, lower effort and smaller context, not model-price arbitrage.
- Kimi Code membership uses quota rather than these per-token API prices. Model IDs in Kimi Code omit the `kimi-` prefix: use `k3.1-pro`; check `/usage` for quota.
- K3.1 Pro requires thinking. T4 means max effort; Highspeed costs twice as much and is not used in the savings model.

Prices checked 2026-10-26: https://platform.moonshot.ai/docs/pricing/chat

## Install

### Kimi Code

Skills go in `~/.kimi-code/skills/` (or `.kimi-code/skills/` in a project). Run `/reload`, then invoke `/skill:base-model-routing` and your persona, or let Kimi load them automatically. The skill prints a routing plan; use `/model` to choose K3.1 Pro and its effort for each step. Subagents share `/secondary-model`, so per-tier model switching is not automatic.

```bash
git clone https://github.com/UtpalDasLabs/token-saver-automated-model-picker.git
cd token-saver-automated-model-picker
./install.sh kimi                      # everything
./install.sh kimi social-creator-routing   # base + overlays + one persona
```

[Docs](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html)

### Kimi API

Load `routing.json`, call `kimi-k3.1-pro`, and set `reasoning_effort` to `low`, `high` or `max` by tier. K3.1 Pro requires thinking.

[Docs](https://platform.moonshot.ai/docs/guide/kimi-k3-1-pro-quickstart)

## Downloads

- All skills: [`kimi-all-skills.zip`](../../dist/kimi/kimi-all-skills.zip)

## Pick your persona

| Persona | Who it's for | Cost saved | Tokens saved | Skill | Zip |
|---|---|---:|---:|---|---|
| Data analyst | Data and BI analysts | **73%** | 80% | [SKILL.md](../../skills/kimi/data-analyst-routing/SKILL.md) | [zip](../../dist/kimi/data-analyst-routing.zip) |
| Designer | UX and UI designers | **45%** | 55% | [SKILL.md](../../skills/kimi/designer-routing/SKILL.md) | [zip](../../dist/kimi/designer-routing.zip) |
| Educator and course creator | Teachers and course creators | **45%** | 56% | [SKILL.md](../../skills/kimi/educator-creator-routing/SKILL.md) | [zip](../../dist/kimi/educator-creator-routing.zip) |
| Growth marketer | Marketers, SEO and growth | **44%** | 56% | [SKILL.md](../../skills/kimi/growth-marketer-routing/SKILL.md) | [zip](../../dist/kimi/growth-marketer-routing.zip) |
| Job seeker | Job seekers and career changers | **42%** | 55% | [SKILL.md](../../skills/kimi/job-seeker-routing/SKILL.md) | [zip](../../dist/kimi/job-seeker-routing.zip) |
| Ops assistant | VAs, ops and chiefs of staff | **56%** | 64% | [SKILL.md](../../skills/kimi/ops-assistant-routing/SKILL.md) | [zip](../../dist/kimi/ops-assistant-routing.zip) |
| Product strategy | Product managers and founders | **32%** | 43% | [SKILL.md](../../skills/kimi/product-strategy-routing/SKILL.md) | [zip](../../dist/kimi/product-strategy-routing.zip) |
| Research analyst | Analysts, consultants, researchers | **28%** | 33% | [SKILL.md](../../skills/kimi/research-analyst-routing/SKILL.md) | [zip](../../dist/kimi/research-analyst-routing.zip) |
| Sales and BD | Sales and business development | **43%** | 51% | [SKILL.md](../../skills/kimi/sales-bd-routing/SKILL.md) | [zip](../../dist/kimi/sales-bd-routing.zip) |
| Social creator | Video and social media creators | **48%** | 60% | [SKILL.md](../../skills/kimi/social-creator-routing/SKILL.md) | [zip](../../dist/kimi/social-creator-routing.zip) |
| Support and success | Support and customer success | **47%** | 54% | [SKILL.md](../../skills/kimi/support-success-routing/SKILL.md) | [zip](../../dist/kimi/support-success-routing.zip) |
| Vibe coder | Indie hackers and AI-assisted builders | **50%** | 65% | [SKILL.md](../../skills/kimi/vibe-coder-routing/SKILL.md) | [zip](../../dist/kimi/vibe-coder-routing.zip) |
| Writer and editor | Writers, newsletter authors, editors | **35%** | 45% | [SKILL.md](../../skills/kimi/writer-editor-routing/SKILL.md) | [zip](../../dist/kimi/writer-editor-routing.zip) |

Always install `base-model-routing` with a persona skill; the overlays (`cheap-batch-mode`, `judge-best-output`, `high-stakes-review`, `context-diet`) are optional but recommended.
