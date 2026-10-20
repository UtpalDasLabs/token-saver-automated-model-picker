# Setup on Perplexity

## Perplexity Computer

Import the whole pack as a plugin: Plugins → Add custom → Import plugin from GitHub, and paste the URL of `dist/perplexity/plugin`. Or upload a single skill zip under Plugins → Add custom → Skill. The skill makes Computer plan by tier and keep cheap steps cheap.

Docs: https://www.perplexity.ai/help-center/en/articles/2026100802-create-or-upload-a-custom-plugin

## Perplexity Agent API

Upload skills with the Skills API, then set `model` per request from `routing.json`. One API key covers all four tiers across providers.

Docs: https://docs.perplexity.ai/docs/agent-api/skills
