---
name: writer-editor-routing
description: "Model routing for writing and editing: which tier ideates, outlines, drafts, edits, proofreads, fact-checks and formats newsletters, blogs, essays, ghostwritten posts and books. Use for long-form writing or editing. Not for short social captions or ad copy."
license: MIT
compatibility: "Any Agent Skills host. Automatic model switching in Claude Code with the bundled subagents; elsewhere it outputs a routing plan to apply."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "1.0.0"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-skills"
  modeled-token-saving: "45%"
  modeled-cost-saving: "56%"
  pricing-checked: "2026-10-20"
---

# Writer and editor routing

The idea, the argument and the final edit deserve Opus. Outlines, drafts from approved outlines, proofreading and formatting do not.

- **For:** Newsletter writers, bloggers, ghostwriters, copywriters and editors producing long-form text.
- **Win condition:** Finished pieces with a strong point of view, produced at a fraction of the token cost.
- **Modeled saving:** about 45% fewer tokens and 56% lower cost than running everything on Opus 5.5 (pessimistic case: 11% / 39%). [Method](https://github.com/UtpalDasLabs/token-saver-skills/blob/main/METHODOLOGY.md)

## Core rules

Apply `base-model-routing` if it is installed. If not, these are the rules that matter:

1. Use a tool or script (T0) whenever a deterministic command can do the job.
2. Otherwise pick the lowest tier in the routing table below, at the lowest listed effort.
3. Run the listed check before accepting any output.
4. On failure, retry once with the exact error, then move up one tier. Never skip to the top.
5. Judging, choosing the best option and anything public or irreversible start at T3.
6. Brief workers with only the context they need, and cap the output length.

Tiers: **T0** tool · **T1** Haiku 5.5 · **T2** Sonnet 5.5 · **T3** Opus 5.5 · **T4** Fable 5.1 (rare).

## Routing table

| Task | Tier | Effort | Context in | Check before accepting | Escalate when |
|---|---|---|---|---|---|
| Formatting, links, image alt text | **T0** script / tool | - | ≤1.5k | Markdown lint + link check | Never |
| Proofread: spelling, grammar, consistency | **T1** haiku | low | ≤8k | Changes listed as diffs | Never |
| Outline from the thesis | **T2** sonnet | low | ≤5k | Sections map to thesis points | Never |
| First draft from an approved outline | **T2** sonnet | medium | ≤8k | Word count, follows outline | Voice is off twice -> T3 |
| Apply edit list | **T2** sonnet | low | ≤10k | Each edit applied | Never |
| Headline and subject-line variants | **T2** sonnet | low | ≤2k | Length limits | Pick on T3 |
| Repurpose into thread, LinkedIn post, summary | **T2** sonnet | low | ≤5k | Platform length | Never |
| Find the angle and thesis | **T3** opus | medium | ≤8k | One-sentence thesis + 3 supporting points | Never above T3 |
| Structural and line edit | **T3** opus | medium | ≤10k | Edit list, not a rewrite | Never above T3 |
| Fact-check claims and quotes | **T3** opus | medium | ≤8k | Verdict + source per claim | Never above T3 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Ghostwriting in a named person's voice for public posting.
- Anything with legal exposure: named people, health, money claims.
- When two drafts both miss the thesis.

## Context diet

- Keep a stable voice sample (300 words) and style rules at the top of every brief.
- Editors return edit lists, not full rewrites; T2 applies them.
- Send only the section being drafted plus the outline, not the whole manuscript.

## Do it without a model (T0)

- Word counts, reading level and link checks with tools.
- Markdown formatting and lint with a formatter.
- Find-and-replace consistency fixes (spelling of names, units) with search.

## Briefing workers

Brief T2 with the voice sample, the outline section, the word target and 'no new arguments'.

In Claude Code, send T1 work to the `micro-worker` subagent, T2 to `standard-worker` and T3 reviews to `strong-reviewer`. In chat apps, print the plan and tell the user which model to switch to at each step.

## Anti-patterns

- Opus proofreading for commas.
- Asking for a "better version" instead of a specific edit list.
- Drafting before the thesis is agreed.

## Example

Request: "Write my weekly 1,200-word newsletter on why AI agents need accountability."

```text
ROUTING PLAN
1. [T3] opus/medium    Thesis + 3 points + the one story to open with
2. [T2] sonnet/low     Outline
3. [T2] sonnet/medium  Draft from outline (voice sample in brief)
4. [T3] opus/medium    Edit list: structure, argument, lines
5. [T2] sonnet/low     Apply edits
6. [T1] haiku/low      Proofread, list diffs
7. [T2] sonnet/low     5 subject lines -> [T3] pick one
```
