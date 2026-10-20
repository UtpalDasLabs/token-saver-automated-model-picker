# Setup on OpenAI

## Codex (CLI, IDE, app)

Skills go in `~/.agents/skills/`, the three worker agents (TOML) in `~/.codex/agents/`. Each agent pins `model` and `model_reasoning_effort`, so delegated work runs on GPT-6 Luna or Sol at low effort.

```bash
./install.sh openai                      # all skills + worker agents
./install.sh openai vibe-coder-routing   # base + overlays + one persona
```

Skills: `~/.agents/skills` · Workers: `~/.codex/agents`

Docs: https://learn.chatgpt.com/docs/agent-configuration/subagents

## ChatGPT

Add a skill zip where your ChatGPT plan supports skills. The skill prints a routing plan and tells you when to switch between GPT-6 Luna, GPT-6 and GPT-6 Pro.

Docs: https://learn.chatgpt.com/docs/build-skills

## OpenAI API

Load `routing.json`, look up the task's tier and call that model with the listed `reasoning.effort`.

Docs: https://developers.openai.com/api/docs/pricing
