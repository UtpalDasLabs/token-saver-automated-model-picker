# Setup on DeepSeek

## DeepSeek Harness

Skills go in `~/.agents/skills/` (or `.dsh/skills/` in a project). The skill writes a routing plan and keeps cheap steps on Flash with small context.

```bash
./install.sh deepseek                      # all skills
./install.sh deepseek vibe-coder-routing   # base + overlays + one persona
```

Skills: `~/.agents/skills`

Docs: https://deepseek-harness.github.io/deepseek-harness/en/reference/subsystems/skills

## Claude Code or Codex on the DeepSeek API

DeepSeek's API supports the Anthropic and OpenAI interfaces, so Claude Code and Codex can run on it. Install with `--tool claude-code`: the worker subagents pin `deepseek-flash` and `deepseek-v4-pro`.

```bash
./install.sh deepseek --tool claude-code                      # all skills + worker agents
./install.sh deepseek --tool claude-code vibe-coder-routing   # base + overlays + one persona
```

Skills: `~/.claude/skills` · Workers: `~/.claude/agents`

Docs: https://api-docs.deepseek.com/updates/

## DeepSeek API

Load `routing.json` and call `deepseek-flash` (thinking off for T1, on for T2) or `deepseek-v4-pro`.

Docs: https://api-docs.deepseek.com/quick_start/pricing
