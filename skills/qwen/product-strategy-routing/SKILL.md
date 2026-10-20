---
name: product-strategy-routing
description: "Model routing for product management and founders: which tier writes PRDs, roadmaps, strategy memos, user research synthesis, prioritisation and stakeholder updates. Use when planning products, features or go-to-market. Not for writing the code itself."
license: MIT
compatibility: "Agent Skills format. Packaged for Qwen: Qwen Code, Model Studio API. Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "qwen"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
  modeled-token-saving: "43%"
  modeled-cost-saving: "69%"
  pricing-checked: "2026-10-20"
---

# Product strategy routing (Qwen)

Keep Qwen3.8-Max on the decisions that move the business and push the formatting, summarising and template work down.

- **For:** Product managers, product leads and founders writing PRDs, roadmaps, strategy memos and decision documents.
- **Win condition:** Better decisions per hour, with documents that stakeholders read and trust, at a fraction of the token cost.
- **Modeled saving on Qwen:** about 69% lower cost and 43% fewer tokens than running everything on Qwen3.8-Max (pessimistic case: 56% / 10%). [Method](https://github.com/UtpalDasLabs/token-saver-automated-model-picker/blob/main/METHODOLOGY.md)

## Core rules

Apply `base-model-routing` if it is installed. If not, these are the rules that matter:

1. Use a tool or script (T0) whenever a deterministic command can do the job.
2. Otherwise pick the lowest tier in the routing table below, at the lowest listed effort.
3. Run the listed check before accepting any output.
4. On failure, retry once with the exact error, then move up one tier. Never skip to the top.
5. Judging, choosing the best option and anything public or irreversible start at T3.
6. Brief workers with only the context they need, and cap the output length.

Tiers on Qwen: **T0** tool · **T1** Qwen3.7-Flash · **T2** Qwen3.7-Plus · **T3** Qwen3.8-Max · **T4** Qwen3.8-Max (thinking) (rare).

## Routing table

| Task | Tier | Effort | Context in | Check before accepting | Escalate when |
|---|---|---|---|---|---|
| Summarise each interview transcript | **T1** Qwen3.7-Flash | low | ≤15k | Fixed template: pains, jobs, quotes | Never |
| Meeting notes to action items | **T1** Qwen3.7-Flash | low | ≤6k | Owner + date per item | Never |
| PRD first draft from a brief | **T2** Qwen3.7-Plus | medium | ≤10k | Template sections all filled, metrics defined | Problem statement unclear -> T3 |
| Synthesise user interviews | **T2** Qwen3.7-Plus | medium | ≤25k | Themes with quote evidence and counts | Conflicting signals -> T3 to interpret |
| Prioritise backlog with RICE or similar | **T2** Qwen3.7-Plus | low | ≤8k | Scores computed by formula | Final ranking call -> T3 |
| Write user stories and acceptance criteria | **T2** Qwen3.7-Plus | low | ≤5k | Given/When/Then format | Never |
| Weekly stakeholder update | **T2** Qwen3.7-Plus | low | ≤6k | Under 250 words, RAG status | Bad news or escalation -> T3 tone review |
| Competitor feature table | **T2** Qwen3.7-Plus | medium | ≤15k | Every cell has a source | Positioning implications -> T3 |
| Metrics definitions and dashboard specs | **T2** Qwen3.7-Plus | medium | ≤8k | Formula + source table per metric | North-star choice -> T3 |
| Strategy, positioning, trade-off decisions | **T3** Qwen3.8-Max | high | ≤25k | Options, criteria, recommendation, risks | Bet-the-company decision -> T4 second opinion |
| PRD review and gap finding | **T3** Qwen3.8-Max | medium | ≤15k | Lists risks, edge cases, open questions | Never above T3 |
| Pitch or exec narrative | **T3** Qwen3.8-Max | medium | ≤15k | Story arc, ask, numbers sourced | Never above T3 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Pricing, layoffs, partnerships, fundraising or anything an executive will decide on.
- Conflicting user research signals.
- A roadmap trade-off between two strategic goals.

## Context diet

- Summarise every interview on T1 into a fixed template before synthesis.
- Give the PRD writer the brief, the template and the 3 key research themes, not every transcript.
- Keep a stable product context card (vision, ICP, metrics, constraints) as the first block.
- Qwen3.7-Flash costs about 3x more per token above 32k input tokens. Keep T1 prompts under 32k.

## Do it without a model (T0)

- RICE/ICE scores with a spreadsheet formula.
- Ticket formatting and bulk label changes with the tracker's own bulk edit or API script.
- Date maths for roadmaps in a sheet, not a model.

## Briefing workers

Brief T2 with the product context card, the template, the decided direction and 'no new strategy, flag gaps only'.

In Qwen Code, send T1 work to the `micro-worker` agent, T2 to `standard-worker` and T3 reviews to `strong-reviewer`; each one is pinned to the right Qwen model. Anywhere else, print the routing plan and tell the user which model to use at each step.

## Anti-patterns

- Qwen3.8-Max formatting Jira tickets.
- Qwen3.7-Flash deciding the roadmap.
- Feeding 20 raw transcripts into one strategy prompt.

## Example

Request: "I've got 8 user interviews. Turn them into a PRD for a subscription pause feature."

```text
ROUTING PLAN
1. [T1] flash/low              Summarise each interview into the template (batch of 8)
2. [T2] plus/medium            Synthesise themes with quote evidence and counts
3. [T3] max/high               Decide problem framing, scope and success metrics
4. [T2] plus/medium            Draft the PRD from the decided framing
5. [T3] max/medium             Review PRD for gaps, risks, edge cases
6. [T2] plus/low               Write user stories + acceptance criteria
```
