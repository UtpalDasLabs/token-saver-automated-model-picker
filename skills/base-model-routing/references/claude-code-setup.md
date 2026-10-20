# Claude Code setup

Claude Code can switch models per task, which turns a routing plan into real savings.

1. Copy the skills: `cp -R skills/* ~/.claude/skills/` (personal) or into `.claude/skills/` (one project).
2. Copy the subagents: `cp agents/*.md ~/.claude/agents/`.
3. Restart Claude Code and run `/skills` and `/agents` to confirm they are listed.

The bundled subagents:

| Subagent | `model` | `effort` | Tier |
|---|---|---|---|
| `micro-worker` | `haiku` | `low` | T1 |
| `standard-worker` | `sonnet` | `medium` | T2 |
| `strong-reviewer` | `opus` | `high` | T3 review |

Optional: set `CLAUDE_CODE_SUBAGENT_MODEL=sonnet` so any subagent without its own `model` defaults to T2 instead of inheriting the main session's model.

Keep the main session on Opus 5.5 at `medium` for planning and judgement; it delegates bulk work down.

Reference: [Claude Code subagents](https://code.claude.com/docs/en/sub-agents), [Claude Code skills](https://code.claude.com/docs/en/skills).
