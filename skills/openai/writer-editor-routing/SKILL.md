---
name: writer-editor-routing
description: "Model routing for writing and editing: which tier ideates, outlines, drafts, edits, proofreads, fact-checks and formats newsletters, blogs, essays, ghostwritten posts and books. Use for long-form writing or editing. Not for short social captions or ad copy."
license: MIT
compatibility: "Agent Skills format. Packaged for OpenAI: Codex (CLI, IDE, app), ChatGPT, OpenAI API. Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "openai"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
  modeled-token-saving: "46%"
  modeled-cost-saving: "44%"
  pricing-checked: "2026-10-20"
---

# Writer and editor routing (OpenAI)

The idea, the argument and the final edit deserve GPT-6.1 Sol. Outlines, drafts from approved outlines, proofreading and formatting do not.

- **For:** Newsletter writers, bloggers, ghostwriters, copywriters and editors producing long-form text.
- **Win condition:** Finished pieces with a strong point of view, produced at a fraction of the token cost.
- **Modeled saving on OpenAI:** about 44% lower cost and 46% fewer tokens than running everything on GPT-6.1 Sol (pessimistic case: 18% / 13%). [Method](https://github.com/UtpalDasLabs/token-saver-automated-model-picker/blob/main/METHODOLOGY.md)

## Core rules

Apply `base-model-routing` if it is installed. If not, these are the rules that matter:

1. Use a tool or script (T0) whenever a deterministic command can do the job.
2. Otherwise pick the lowest tier in the routing table below, at the lowest listed effort.
3. Run the listed check before accepting any output.
4. On failure, retry once with the exact error, then move up one tier. Never skip to the top.
5. Judging, choosing the best option and anything public or irreversible start at T3.
6. Brief workers with only the context they need, and cap the output length.

Tiers on OpenAI: **T0** tool · **T1** GPT-6 Luna · **T2** GPT-6.1 Sol (low effort) · **T3** GPT-6.1 Sol · **T4** GPT-6 Astra (rare).

## Routing table

| Task | Tier | Effort | Context in | Check before accepting | Escalate when |
|---|---|---|---|---|---|
| Formatting, links, image alt text | **T0** script / tool | - | ≤1.5k | Markdown lint + link check | Never |
| Proofread: spelling, grammar, consistency | **T1** GPT-6 Luna | low | ≤8k | Changes listed as diffs | Never |
| Outline from the thesis | **T2** GPT-6.1 Sol (low effort) | low | ≤5k | Sections map to thesis points | Never |
| First draft from an approved outline | **T2** GPT-6.1 Sol (low effort) | low | ≤8k | Word count, follows outline | Voice is off twice -> T3 |
| Apply edit list | **T2** GPT-6.1 Sol (low effort) | low | ≤10k | Each edit applied | Never |
| Headline and subject-line variants | **T2** GPT-6.1 Sol (low effort) | low | ≤2k | Length limits | Pick on T3 |
| Repurpose into thread, LinkedIn post, summary | **T2** GPT-6.1 Sol (low effort) | low | ≤5k | Platform length | Never |
| Find the angle and thesis | **T3** GPT-6.1 Sol | medium | ≤8k | One-sentence thesis + 3 supporting points | Never above T3 |
| Structural and line edit | **T3** GPT-6.1 Sol | medium | ≤10k | Edit list, not a rewrite | Never above T3 |
| Fact-check claims and quotes | **T3** GPT-6.1 Sol | medium | ≤8k | Verdict + source per claim | Never above T3 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Ghostwriting in a named person's voice for public posting.
- Anything with legal exposure: named people, health, money claims.
- When two drafts both miss the thesis.

## Context diet

- Keep a stable voice sample (300 words) and style rules at the top of every brief.
- Editors return edit lists, not full rewrites; T2 applies them.
- Send only the section being drafted plus the outline, not the whole manuscript.
- GPT-6.1 Sol and GPT-6 Luna cost more per token above 272k input tokens. Compact long sessions before that.

## Do it without a model (T0)

- Word counts, reading level and link checks with tools.
- Markdown formatting and lint with a formatter.
- Find-and-replace consistency fixes (spelling of names, units) with search.

## Briefing workers

Brief T2 with the voice sample, the outline section, the word target and 'no new arguments'.

In Codex (CLI, IDE, app), send T1 work to the `micro-worker` agent, T2 to `standard-worker` and T3 reviews to `strong-reviewer`; each one is pinned to the right OpenAI model. Anywhere else, print the routing plan and tell the user which model to use at each step.

## Anti-patterns

- GPT-6.1 Sol proofreading for commas.
- Asking for a "better version" instead of a specific edit list.
- Drafting before the thesis is agreed.

## Example

Request: "Write my weekly 1,200-word newsletter on why AI agents need accountability."

```text
ROUTING PLAN
1. [T3] sol/medium             Thesis + 3 points + the one story to open with
2. [T2] sol/low                Outline
3. [T2] sol/medium             Draft from outline (voice sample in brief)
4. [T3] sol/medium             Edit list: structure, argument, lines
5. [T2] sol/low                Apply edits
6. [T1] luna/low               Proofread, list diffs
7. [T2] sol/low                5 subject lines -> [T3] pick one
```
