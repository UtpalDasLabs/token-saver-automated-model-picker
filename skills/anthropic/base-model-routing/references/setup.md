# Setup on Anthropic

## Claude Code

Skills go in `~/.claude/skills/`, the three worker subagents in `~/.claude/agents/`. Each subagent pins its own `model` and `effort`, so delegated work really runs on the cheaper model. Check with `/skills` and `/agents`.

```bash
./install.sh anthropic                      # all skills + worker agents
./install.sh anthropic vibe-coder-routing   # base + overlays + one persona
```

Skills: `~/.claude/skills` · Workers: `~/.claude/agents`

Docs: https://code.claude.com/docs/en/sub-agents

## Claude.ai

Upload a skill zip under Customize → Skills → + → Upload a skill. The skill prints a routing plan and tells you which model to switch to at each step.

Docs: https://code.claude.com/docs/en/skills

## Claude API

Load `routing.json`, look up the task's tier and call that model ID.

Docs: https://platform.claude.com/docs/en/about-claude/pricing
