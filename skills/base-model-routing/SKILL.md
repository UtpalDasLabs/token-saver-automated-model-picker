---
name: base-model-routing
description: "Route every AI task to the cheapest model tier that can finish it: script, Haiku, Sonnet, Opus or Fable. Use when planning multi-step work, delegating to subagents, batching jobs, or when the user asks to cut token cost or pick a model. Not for comparing AI vendors or plans."
license: MIT
compatibility: "Any Agent Skills host. Model switching is automatic in Claude Code with the bundled subagents; elsewhere the skill outputs a routing plan to apply manually or via API."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "1.0.0"
  repo: "https://github.com/UtpalDasLabs/token-saver-skills"
  pricing-checked: "2026-10-20"
---

# Base model routing

The shared policy every persona skill in this pack extends. Goal: lowest cost per **completed** task, not lowest price per token. A cheap attempt that fails and gets redone is not cheap.

## The tier ladder

| Tier | Runs on | Use for | Price vs. Opus 5.5 |
|---|---|---|---|
| T0 Tool | No model: shell, script, formula, regex, linter | Rename, dedupe, link check, format, count, convert, validate | ~0 |
| T1 Micro | Haiku 5.5, effort `low`/`medium` | Classify, extract, tag, short rewrite, summarise logs, check one rule | ~1/40 |
| T2 Standard | Sonnet 5.5, effort `medium` | Routine production from a clear spec: code to spec, drafts, variants, tables | ~1/2 |
| T3 Strong | Opus 5.5, effort `low`/`medium`/`high` | Ambiguity, judgement, architecture, strategy, final review, choosing the winner | 1x |
| T4 Frontier | Fable 5.1 | Rare. High stakes and Opus at `high` already failed, or very long-horizon work | ~2.5x |

Prices and sources: read `references/pricing.md` when the user asks why a tier is cheaper, or when estimating cost.

## Decide the tier

Score the task 0–2 on each axis, then add the scores.

| Axis | 0 | 1 | 2 |
|---|---|---|---|
| Ambiguity | Spec is exact | Some gaps, sensible defaults exist | Goal itself is unclear |
| Blast radius | Easy to undo, private | Visible to others, undoable | Public, legal, money, production data |
| Checkability | A script/test verifies it | A quick human glance verifies it | Only expert judgement verifies it |
| Novelty | Done this exact thing before | Variation of a known pattern | New problem |

- Before scoring: if a deterministic tool can do it, use **T0** and stop.
- Total 0–2 → **T1**. Total 3–4 → **T2**. Total 5–6 → **T3** (`medium`). Total 7–8 → **T3** (`high`); offer **T4** only if the user accepts the cost.
- Hard overrides: anything irreversible and public, any legal/financial/medical claim, and any "which option is best" judgement go to at least T3.

## Escalation ladder

1. Run at the chosen tier with the lowest sensible effort.
2. Check the output with the validator named in the persona skill (test, lint, schema, word count, link check, rubric).
3. On failure, retry **once** at the same tier, passing the exact error.
4. Still failing: move **one** tier up with the original brief plus the failure notes. Never skip tiers, except straight to T3 when the failure reveals real ambiguity.
5. For checkable bulk work, run everything at `low` effort and rerun only the failures at `high`. Anthropic measured this at about 97% solved for roughly half the cost of running everything at `high`.

## Context diet

- Send the worker only what the task needs: the brief, the relevant files or rows, and the acceptance check. Never the whole conversation.
- Budgets: T1 ≤ 8k tokens in, T2 ≤ 30k, T3 as needed but summarised first.
- Haiku 5.5 costs 5x more per token once a prompt passes 100k tokens. Split or compact before that line.
- Summarise long material once (T1), then pass the summary up, not the raw text.
- Keep reusable prefixes (system prompt, tool list, style guide) byte-identical so prompt caching works.
- Cap output length in the brief: "max 120 words", "diff only", "JSON only".

## When not to delegate

- Do not split one tightly dependent chain of reasoning that fits in one context. Lower the effort instead.
- Do not delegate a task smaller than its own brief. Do it in place.
- Batch micro-tasks: one brief for 20 items beats 20 briefs.

## Worker brief template

```text
TASK: <one sentence, imperative>
INPUT: <only the needed material, or file paths>
RULES: <3-5 hard constraints>
OUTPUT: <exact format + length cap>
DONE WHEN: <the check that will be run>
IF STUCK: return "ESCALATE: <reason>" instead of guessing.
```

## Output a routing plan

Before multi-step work, show the plan in this shape, then execute it:

```text
ROUTING PLAN
1. [T0] rename 40 files to slug format            -> script
2. [T1] tag each clip by topic                     -> haiku/low, batch of 40
3. [T2] write 3 caption variants per clip          -> sonnet/medium
4. [T3] pick the strongest hook, explain why       -> opus/medium
Escalate: any step failing its check twice moves up one tier.
```

## Running it in each host

- **Claude Code:** delegate T1 to the `micro-worker` subagent, T2 to `standard-worker`, T3 review to `strong-reviewer` (files in this repo's `agents/`). Read `references/claude-code-setup.md` when setting this up.
- **Claude.ai or other chat apps:** print the routing plan and tell the user which model to switch to for each step.
- **API or agent frameworks:** load `routing.json` from the repo and map tiers to model IDs in code.

## Anti-patterns

- Running every step on the strongest model "to be safe".
- Escalating before running the validator.
- Pasting a whole repo, inbox or transcript into a micro-task.
- Asking a cheap model to judge which of several outputs is best; judging belongs on T3.
- Rewriting the system prompt mid-session, which breaks the prompt cache.
