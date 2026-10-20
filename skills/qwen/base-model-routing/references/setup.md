# Setup on Qwen

## Qwen Code

Skills go in `~/.qwen/skills/`, the three worker subagents in `~/.qwen/agents/`. Each subagent pins its own `model`, so delegated work runs on Qwen3.7-Flash or Qwen3.7-Plus.

```bash
./install.sh qwen                      # all skills + worker agents
./install.sh qwen vibe-coder-routing   # base + overlays + one persona
```

Skills: `~/.qwen/skills` · Workers: `~/.qwen/agents`

Docs: https://qwenlm.github.io/qwen-code-docs/en/users/features/sub-agents/

## Model Studio API

Load `routing.json` and call the tier's model; turn thinking on only for T3 judgement and T4.

Docs: https://www.alibabacloud.com/help/en/model-studio/model-pricing
