---
name: base-model-routing
description: "Route every AI task to the cheapest Qwen (Alibaba Cloud Model Studio) model tier that can finish it: script, Qwen3.7-Flash, Qwen3.7-Plus, Qwen3.8-Max or Qwen3.8-Max (thinking). Use when planning multi-step work, delegating to subagents, batching jobs, or when the user asks to cut token cost or pick a model. Not for comparing AI vendors or plans."
license: MIT
compatibility: "Agent Skills format. Packaged for Qwen: Qwen Code, Model Studio API. Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "qwen"
  repo: "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
  pricing-checked: "2026-10-20"
---

# Base model routing (Qwen)

The shared policy every persona skill in this pack extends. Goal: lowest cost per **completed** task, not lowest price per token. A cheap attempt that fails and gets redone is not cheap.

## The tier ladder

| Tier | Runs on | Use for | Price vs. T3 |
|---|---|---|---|
| T0 Tool | No model: shell, script, formula, regex, linter | Rename, dedupe, link check, format, count, convert, validate | ~0 |
| T1 Micro | Qwen3.7-Flash (`qwen3.7-flash`) | Classify, extract, tag, short rewrite, summarise logs, check one rule | ~1/55 |
| T2 Standard | Qwen3.7-Plus (`qwen3.7-plus`) | Routine production from a clear spec: code to spec, drafts, variants, tables | ~1/4 |
| T3 Strong | Qwen3.8-Max (`qwen3.8-max`) | Ambiguity, judgement, architecture, strategy, final review, choosing the winner | 1x |
| T4 Frontier | Qwen3.8-Max (thinking) (`qwen3.8-max`) | Rare. High stakes and T3 at `high` already failed, or very long-horizon work | 1x (same model) |

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
5. For checkable bulk work, run everything at `low` effort and rerun only the failures at `high`. On Anthropic's published coding test this solved about 97% of tasks for roughly half the cost of running everything at `high`; the pattern applies to any model with effort or thinking controls.

## Context diet

- Send the worker only what the task needs: the brief, the relevant files or rows, and the acceptance check. Never the whole conversation.
- Budgets: T1 ≤ 8k tokens in, T2 ≤ 30k, T3 as needed but summarised first.
- Qwen3.7-Flash costs about 3x more per token above 32k input tokens. Keep T1 prompts under 32k.
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
1. [T0] script                rename 40 files to slug format
2. [T1] Qwen3.7-Flash/low             tag each clip by topic, batch of 40
3. [T2] Qwen3.7-Plus/medium           write 3 caption variants per clip
4. [T3] Qwen3.8-Max/medium            pick the strongest hook, explain why
Escalate: any step failing its check twice moves up one tier.
```

## Running it on Qwen

- **Qwen Code** (automatic model switching): Skills go in `~/.qwen/skills/`, the three worker subagents in `~/.qwen/agents/`. Each subagent pins its own `model`, so delegated work runs on Qwen3.7-Flash or Qwen3.7-Plus. [Docs](https://qwenlm.github.io/qwen-code-docs/en/users/features/sub-agents/)
- **Model Studio API**: Load `routing.json` and call the tier's model; turn thinking on only for T3 judgement and T4. [Docs](https://www.alibabacloud.com/help/en/model-studio/model-pricing)

Read `references/setup.md` when installing or when the user asks how model switching works here.

## Anti-patterns

- Running every step on the strongest model "to be safe".
- Escalating before running the validator.
- Pasting a whole repo, inbox or transcript into a micro-task.
- Asking a cheap model to judge which of several outputs is best; judging belongs on T3.
- Rewriting the system prompt mid-session, which breaks the prompt cache.
