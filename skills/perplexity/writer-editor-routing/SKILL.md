---
name: writer-editor-routing
description: "Model routing for writing and editing: which tier ideates, outlines, drafts, edits, proofreads, fact-checks and formats newsletters, blogs, essays, ghostwritten posts and books. Use for long-form writing or editing. Not for short social captions or ad copy."
license: MIT
compatibility: "Agent Skills format. Packaged for Perplexity: Perplexity Computer, Perplexity Agent API. Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "perplexity"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
  modeled-token-saving: "45%"
  modeled-cost-saving: "65%"
  pricing-checked: "2026-10-20"
---

# Writer and editor routing (Perplexity)

The idea, the argument and the final edit deserve Claude Opus 5.5. Outlines, drafts from approved outlines, proofreading and formatting do not.

- **For:** Newsletter writers, bloggers, ghostwriters, copywriters and editors producing long-form text.
- **Win condition:** Finished pieces with a strong point of view, produced at a fraction of the token cost.
- **Modeled saving on Perplexity:** about 65% lower cost and 45% fewer tokens than running everything on Claude Opus 5.5 (pessimistic case: 52% / 11%). [Method](https://github.com/UtpalDasLabs/token-saver-automated-model-picker/blob/main/METHODOLOGY.md)

## Core rules

Apply `base-model-routing` if it is installed. If not, these are the rules that matter:

1. Use a tool or script (T0) whenever a deterministic command can do the job.
2. Otherwise pick the lowest tier in the routing table below, at the lowest listed effort.
3. Run the listed check before accepting any output.
4. On failure, retry once with the exact error, then move up one tier. Never skip to the top.
5. Judging, choosing the best option and anything public or irreversible start at T3.
6. Brief workers with only the context they need, and cap the output length.

Tiers on Perplexity: **T0** tool · **T1** GPT-6 Luna · **T2** Gemini 3.8 Flash · **T3** Claude Opus 5.5 · **T4** Claude Fable 5.1 (rare).

## Routing table

| Task | Tier | Effort | Context in | Check before accepting | Escalate when |
|---|---|---|---|---|---|
| Formatting, links, image alt text | **T0** script / tool | - | ≤1.5k | Markdown lint + link check | Never |
| Proofread: spelling, grammar, consistency | **T1** GPT-6 Luna | low | ≤8k | Changes listed as diffs | Never |
| Outline from the thesis | **T2** Gemini 3.8 Flash | low | ≤5k | Sections map to thesis points | Never |
| First draft from an approved outline | **T2** Gemini 3.8 Flash | medium | ≤8k | Word count, follows outline | Voice is off twice -> T3 |
| Apply edit list | **T2** Gemini 3.8 Flash | low | ≤10k | Each edit applied | Never |
| Headline and subject-line variants | **T2** Gemini 3.8 Flash | low | ≤2k | Length limits | Pick on T3 |
| Repurpose into thread, LinkedIn post, summary | **T2** Gemini 3.8 Flash | low | ≤5k | Platform length | Never |
| Find the angle and thesis | **T3** Claude Opus 5.5 | medium | ≤8k | One-sentence thesis + 3 supporting points | Never above T3 |
| Structural and line edit | **T3** Claude Opus 5.5 | medium | ≤10k | Edit list, not a rewrite | Never above T3 |
| Fact-check claims and quotes | **T3** Claude Opus 5.5 | medium | ≤8k | Verdict + source per claim | Never above T3 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Ghostwriting in a named person's voice for public posting.
- Anything with legal exposure: named people, health, money claims.
- When two drafts both miss the thesis.

## Context diet

- Keep a stable voice sample (300 words) and style rules at the top of every brief.
- Editors return edit lists, not full rewrites; T2 applies them.
- Send only the section being drafted plus the outline, not the whole manuscript.
- Web search and fetch tool calls are billed on top of tokens; search once, then reuse the results.

## Do it without a model (T0)

- Word counts, reading level and link checks with tools.
- Markdown formatting and lint with a formatter.
- Find-and-replace consistency fixes (spelling of names, units) with search.

## Briefing workers

Brief T2 with the voice sample, the outline section, the word target and 'no new arguments'.

In Perplexity Computer, write the tier and model into each step of the plan and keep cheap steps on small context or scripts. On the Agent API, set `model` per request from the routing table.

## Anti-patterns

- Claude Opus 5.5 proofreading for commas.
- Asking for a "better version" instead of a specific edit list.
- Drafting before the thesis is agreed.

## Example

Request: "Write my weekly 1,200-word newsletter on why AI agents need accountability."

```text
ROUTING PLAN
1. [T3] opus/medium            Thesis + 3 points + the one story to open with
2. [T2] gemini-flash/low       Outline
3. [T2] gemini-flash/medium    Draft from outline (voice sample in brief)
4. [T3] opus/medium            Edit list: structure, argument, lines
5. [T2] gemini-flash/low       Apply edits
6. [T1] luna/low               Proofread, list diffs
7. [T2] gemini-flash/low       5 subject lines -> [T3] pick one
```
