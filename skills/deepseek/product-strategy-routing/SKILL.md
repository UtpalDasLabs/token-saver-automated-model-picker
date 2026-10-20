---
name: product-strategy-routing
description: "Model routing for product management and founders: which tier writes PRDs, roadmaps, strategy memos, user research synthesis, prioritisation and stakeholder updates. Use when planning products, features or go-to-market. Not for writing the code itself."
license: MIT
compatibility: "Agent Skills format. Packaged for DeepSeek: DeepSeek Harness, Claude Code or Codex on the DeepSeek API, DeepSeek API. Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "deepseek"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
  modeled-token-saving: "43%"
  modeled-cost-saving: "65%"
  pricing-checked: "2026-10-20"
---

# Product strategy routing (DeepSeek)

Keep DeepSeek V4 Pro on the decisions that move the business and push the formatting, summarising and template work down.

- **For:** Product managers, product leads and founders writing PRDs, roadmaps, strategy memos and decision documents.
- **Win condition:** Better decisions per hour, with documents that stakeholders read and trust, at a fraction of the token cost.
- **Modeled saving on DeepSeek:** about 65% lower cost and 43% fewer tokens than running everything on DeepSeek V4 Pro (pessimistic case: 51% / 10%). [Method](https://github.com/UtpalDasLabs/token-saver-automated-model-picker/blob/main/METHODOLOGY.md)

## Core rules

Apply `base-model-routing` if it is installed. If not, these are the rules that matter:

1. Use a tool or script (T0) whenever a deterministic command can do the job.
2. Otherwise pick the lowest tier in the routing table below, at the lowest listed effort.
3. Run the listed check before accepting any output.
4. On failure, retry once with the exact error, then move up one tier. Never skip to the top.
5. Judging, choosing the best option and anything public or irreversible start at T3.
6. Brief workers with only the context they need, and cap the output length.

Tiers on DeepSeek: **T0** tool · **T1** DeepSeek V4.1 Flash (non-thinking) · **T2** DeepSeek V4.1 Flash (thinking) · **T3** DeepSeek V4 Pro · **T4** DeepSeek V4 Pro (max effort) (rare).

## Routing table

| Task | Tier | Effort | Context in | Check before accepting | Escalate when |
|---|---|---|---|---|---|
| Summarise each interview transcript | **T1** DeepSeek V4.1 Flash (non-thinking) | low | ≤15k | Fixed template: pains, jobs, quotes | Never |
| Meeting notes to action items | **T1** DeepSeek V4.1 Flash (non-thinking) | low | ≤6k | Owner + date per item | Never |
| PRD first draft from a brief | **T2** DeepSeek V4.1 Flash (thinking) | medium | ≤10k | Template sections all filled, metrics defined | Problem statement unclear -> T3 |
| Synthesise user interviews | **T2** DeepSeek V4.1 Flash (thinking) | medium | ≤25k | Themes with quote evidence and counts | Conflicting signals -> T3 to interpret |
| Prioritise backlog with RICE or similar | **T2** DeepSeek V4.1 Flash (thinking) | low | ≤8k | Scores computed by formula | Final ranking call -> T3 |
| Write user stories and acceptance criteria | **T2** DeepSeek V4.1 Flash (thinking) | low | ≤5k | Given/When/Then format | Never |
| Weekly stakeholder update | **T2** DeepSeek V4.1 Flash (thinking) | low | ≤6k | Under 250 words, RAG status | Bad news or escalation -> T3 tone review |
| Competitor feature table | **T2** DeepSeek V4.1 Flash (thinking) | medium | ≤15k | Every cell has a source | Positioning implications -> T3 |
| Metrics definitions and dashboard specs | **T2** DeepSeek V4.1 Flash (thinking) | medium | ≤8k | Formula + source table per metric | North-star choice -> T3 |
| Strategy, positioning, trade-off decisions | **T3** DeepSeek V4 Pro | high | ≤25k | Options, criteria, recommendation, risks | Bet-the-company decision -> T4 second opinion |
| PRD review and gap finding | **T3** DeepSeek V4 Pro | medium | ≤15k | Lists risks, edge cases, open questions | Never above T3 |
| Pitch or exec narrative | **T3** DeepSeek V4 Pro | medium | ≤15k | Story arc, ask, numbers sourced | Never above T3 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Pricing, layoffs, partnerships, fundraising or anything an executive will decide on.
- Conflicting user research signals.
- A roadmap trade-off between two strategic goals.

## Context diet

- Summarise every interview on T1 into a fixed template before synthesis.
- Give the PRD writer the brief, the template and the 3 key research themes, not every transcript.
- Keep a stable product context card (vision, ICP, metrics, constraints) as the first block.
- Use off-peak hours (half price) for big batch jobs that can wait.

## Do it without a model (T0)

- RICE/ICE scores with a spreadsheet formula.
- Ticket formatting and bulk label changes with the tracker's own bulk edit or API script.
- Date maths for roadmaps in a sheet, not a model.

## Briefing workers

Brief T2 with the product context card, the template, the decided direction and 'no new strategy, flag gaps only'.

In Claude Code or Codex on the DeepSeek API, send T1 work to the `micro-worker` agent, T2 to `standard-worker` and T3 reviews to `strong-reviewer`; each one is pinned to the right DeepSeek model. Anywhere else, print the routing plan and tell the user which model to use at each step.

## Anti-patterns

- DeepSeek V4 Pro formatting Jira tickets.
- DeepSeek V4.1 Flash (non-thinking) deciding the roadmap.
- Feeding 20 raw transcripts into one strategy prompt.

## Example

Request: "I've got 8 user interviews. Turn them into a PRD for a subscription pause feature."

```text
ROUTING PLAN
1. [T1] flash/low              Summarise each interview into the template (batch of 8)
2. [T2] flash-think/medium     Synthesise themes with quote evidence and counts
3. [T3] v4-pro/high            Decide problem framing, scope and success metrics
4. [T2] flash-think/medium     Draft the PRD from the decided framing
5. [T3] v4-pro/medium          Review PRD for gaps, risks, edge cases
6. [T2] flash-think/low        Write user stories + acceptance criteria
```
