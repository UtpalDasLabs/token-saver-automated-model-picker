---
name: sales-bd-routing
description: "Model routing for sales and business development: which tier researches accounts, enriches leads, personalises outreach, writes sequences, preps calls, summarises calls and updates CRM. Use for prospecting, outreach or deal work. Not for marketing campaigns or ads."
license: MIT
compatibility: "Any Agent Skills host. Automatic model switching in Claude Code with the bundled subagents; elsewhere it outputs a routing plan to apply."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "1.0.0"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-skills"
  modeled-token-saving: "51%"
  modeled-cost-saving: "75%"
  pricing-checked: "2026-10-20"
---

# Sales and BD routing

Account strategy and the high-value deal deserve Opus. List enrichment, first-line personalisation and CRM hygiene do not.

- **For:** Account executives, SDRs, founders doing sales and business developers researching accounts and writing outreach.
- **Win condition:** More qualified meetings per week at a lower AI cost per meeting booked.
- **Modeled saving:** about 51% fewer tokens and 75% lower cost than running everything on Opus 5.5 (pessimistic case: 14% / 61%). [Method](https://github.com/UtpalDasLabs/token-saver-skills/blob/main/METHODOLOGY.md)

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
| CRM field updates and dedupe | **T0** script / tool | - | ≤1.5k | API write log | Never |
| Lead qualification against ICP | **T1** haiku | low | ≤5k | Fit score + reason per lead | Borderline enterprise leads -> T2 |
| Personalised first lines | **T1** haiku | medium | ≤4k | References one real fact | Top-20 accounts -> T2 |
| Call summary and next steps | **T1** haiku | low | ≤15k | MEDDICC-style fields filled | Never |
| Account research summary | **T2** sonnet | low | ≤8k | 5 facts with sources | Never |
| Outreach sequence templates | **T2** sonnet | medium | ≤6k | Under 90 words, one ask | Never |
| Call prep brief | **T2** sonnet | medium | ≤8k | Agenda, questions, objections | Strategic deal -> T3 |
| Proposal draft | **T2** sonnet | medium | ≤10k | Pricing from the price sheet only | Custom pricing or terms -> T3 review |
| Account strategy for a key deal | **T3** opus | high | ≤15k | Stakeholders, pains, plan, risks | Never above T3 |
| Objection handling and negotiation prep | **T3** opus | medium | ≤8k | Response per objection + walk-away | Never above T3 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Pricing, discounts, contract terms or legal language.
- Replies to an angry or churning customer.
- Enterprise deals above your team's normal deal size.

## Context diet

- Enrich leads from structured fields (company, role, size, one recent signal), not full web pages.
- Summarise call transcripts on T1 into a fixed template; later steps use only the summary.
- Keep a stable ICP and value-prop card as the first block of every batch.

## Do it without a model (T0)

- Dedupe, normalise and update CRM fields via import or API scripts.
- Email verification and bounce checks with a verification tool.
- Sequencing and scheduling in the sales tool, not via a model.

## Briefing workers

Brief T1 with the ICP card, the lead's 4 fields and 'one sentence, must reference one fact from input'.

In Claude Code, send T1 work to the `micro-worker` subagent, T2 to `standard-worker` and T3 reviews to `strong-reviewer`. In chat apps, print the plan and tell the user which model to switch to at each step.

## Anti-patterns

- Opus writing 200 first lines.
- Pasting whole LinkedIn profiles into every personalisation call.
- Model-generated pricing without the price sheet.

## Example

Request: "Find and prioritise 100 Berlin mobility startups, then draft outreach for the top 20."

```text
ROUTING PLAN
1. [T0] script         Pull list, dedupe, verify emails
2. [T1] haiku/low      ICP fit score per company (batch of 50)
3. [T2] sonnet/low     Research summary for top 20
4. [T2] sonnet/medium  Personalised first line + 3-step sequence for top 20
5. [T3] opus/medium    Review the 5 biggest accounts' messages
6. [T0] script         Push to CRM
```
