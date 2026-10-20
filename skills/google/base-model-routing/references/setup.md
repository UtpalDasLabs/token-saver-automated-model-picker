# Setup on Google

## Gemini CLI

Skills go in `~/.gemini/skills/`, the three worker subagents in `~/.gemini/agents/`. Each subagent pins its own `model`, so delegated work runs on Flash-Lite or Flash.

```bash
./install.sh google                      # all skills + worker agents
./install.sh google vibe-coder-routing   # base + overlays + one persona
```

Skills: `~/.gemini/skills` · Workers: `~/.gemini/agents`

Docs: https://geminicli.com/docs/core/subagents

## Gemini API and Managed Agents

Managed Agents read skills from `.agents/skills/` in the workspace. For your own code, load `routing.json` and call the tier's model.

Docs: https://ai.google.dev/gemini-api/docs/pricing
