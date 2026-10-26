---
name: base-model-routing
description: "Route every AI task to the cheapest Kimi K3.1 Pro model tier that can finish it: script, Kimi K3.1 Pro (low effort), Kimi K3.1 Pro, Kimi K3.1 Pro or Kimi K3.1 Pro (max effort). Use when planning multi-step work, delegating to subagents, batching jobs, or when the user asks to cut token cost or pick a model. Not for comparing AI vendors or plans."
license: MIT
compatibility: "Agent Skills format. Packaged for Kimi: Kimi Code, Kimi API. Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "kimi"
  repo: "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
  pricing-checked: "2026-10-26"
---

# Base model routing (Kimi)

The shared policy every persona skill in this pack extends. Goal: lowest cost per **completed** task, not lowest price per token. A cheap attempt that fails and gets redone is not cheap.

## The tier ladder

| Tier | Runs on | Use for | Price vs. T3 |
|---|---|---|---|
| T0 Tool | No model: shell, script, formula, regex, linter | Rename, dedupe, link check, format, count, convert, validate | ~0 |
| T1 Micro | Kimi K3.1 Pro (low effort) (`kimi-k3.1-pro`) | Classify, extract, tag, short rewrite, summarise logs, check one rule | 1x (same model) |
| T2 Standard | Kimi K3.1 Pro (`kimi-k3.1-pro`) | Routine production from a clear spec: code to spec, drafts, variants, tables | 1x (same model) |
| T3 Strong | Kimi K3.1 Pro (`kimi-k3.1-pro`) | Ambiguity, judgement, architecture, strategy, final review, choosing the winner | 1x |
| T4 Frontier | Kimi K3.1 Pro (max effort) (`kimi-k3.1-pro`) | Rare. High stakes and T3 at `high` already failed, or very long-horizon work | 1x (same model) |

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
- Total 0–2 → **T1**. Total 3–4 → **T2**. Total 5–6 → **T3** (`high`). Total 7–8 → **T3** (`max`); offer **T4** only if the user accepts the cost.
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
- Kimi has no supported cheaper micro model. Use T0 scripts, low effort and tight context for savings; do not use retired K2 models.
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
2. [T1] Kimi K3.1 Pro (low effort)/low          tag each clip by topic, batch of 40
3. [T2] Kimi K3.1 Pro/high         write 3 caption variants per clip
4. [T3] Kimi K3.1 Pro/high         pick the strongest hook, explain why
Escalate: any step failing its check twice moves up one tier.
```

## Running it on Kimi

- **Kimi Code**: Skills go in `~/.kimi-code/skills/` (or `.kimi-code/skills/` in a project). Run `/reload`, then invoke `/skill:base-model-routing` and your persona, or let Kimi load them automatically. The skill prints a routing plan; use `/model` to choose K3.1 Pro and its effort for each step. Subagents share `/secondary-model`, so per-tier model switching is not automatic. [Docs](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html)
- **Kimi API**: Load `routing.json`, call `kimi-k3.1-pro`, and set `reasoning_effort` to `low`, `high` or `max` by tier. K3.1 Pro requires thinking. [Docs](https://platform.moonshot.ai/docs/guide/kimi-k3-1-pro-quickstart)

Read `references/setup.md` when installing or when the user asks how model switching works here.

## Anti-patterns

- Running every step on the strongest model "to be safe".
- Escalating before running the validator.
- Pasting a whole repo, inbox or transcript into a micro-task.
- Asking a cheap model to judge which of several outputs is best; judging belongs on T3.
- Rewriting the system prompt mid-session, which breaks the prompt cache.
