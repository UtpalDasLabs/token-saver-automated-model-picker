# Setup on Kimi

## Kimi Code

Skills go in `~/.kimi-code/skills/` (or `.kimi-code/skills/` in a project). Run `/reload`, then invoke `/skill:base-model-routing` and your persona, or let Kimi load them automatically. The skill prints a routing plan; use `/model` to choose K3.1 Pro and its effort for each step. Subagents share `/secondary-model`, so per-tier model switching is not automatic.

```bash
./install.sh kimi                      # all skills
./install.sh kimi vibe-coder-routing   # base + overlays + one persona
```

Skills: `~/.kimi-code/skills`

Docs: https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html

## Kimi API

Load `routing.json`, call `kimi-k3.1-pro`, and set `reasoning_effort` to `low`, `high` or `max` by tier. K3.1 Pro requires thinking.

Docs: https://platform.moonshot.ai/docs/guide/kimi-k3-1-pro-quickstart
