---
name: sales-bd-routing
description: "Model routing for sales and business development: which tier researches accounts, enriches leads, personalises outreach, writes sequences, preps calls, summarises calls and updates CRM. Use for prospecting, outreach or deal work. Not for marketing campaigns or ads."
license: MIT
compatibility: "Agent Skills format. Packaged for OpenAI: Codex (CLI, IDE, app), ChatGPT, OpenAI API. Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "openai"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
  modeled-token-saving: "52%"
  modeled-cost-saving: "67%"
  pricing-checked: "2026-10-20"
---

# Sales and BD routing (OpenAI)

Account strategy and the high-value deal deserve GPT-6.1 Sol. List enrichment, first-line personalisation and CRM hygiene do not.

- **For:** Account executives, SDRs, founders doing sales and business developers researching accounts and writing outreach.
- **Win condition:** More qualified meetings per week at a lower AI cost per meeting booked.
- **Modeled saving on OpenAI:** about 67% lower cost and 52% fewer tokens than running everything on GPT-6.1 Sol (pessimistic case: 45% / 15%). [Method](https://github.com/UtpalDasLabs/token-saver-automated-model-picker/blob/main/METHODOLOGY.md)

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
| CRM field updates and dedupe | **T0** script / tool | - | ≤1.5k | API write log | Never |
| Lead qualification against ICP | **T1** GPT-6 Luna | low | ≤5k | Fit score + reason per lead | Borderline enterprise leads -> T2 |
| Personalised first lines | **T1** GPT-6 Luna | medium | ≤4k | References one real fact | Top-20 accounts -> T2 |
| Call summary and next steps | **T1** GPT-6 Luna | low | ≤15k | MEDDICC-style fields filled | Never |
| Account research summary | **T2** GPT-6.1 Sol (low effort) | low | ≤8k | 5 facts with sources | Never |
| Outreach sequence templates | **T2** GPT-6.1 Sol (low effort) | low | ≤6k | Under 90 words, one ask | Never |
| Call prep brief | **T2** GPT-6.1 Sol (low effort) | low | ≤8k | Agenda, questions, objections | Strategic deal -> T3 |
| Proposal draft | **T2** GPT-6.1 Sol (low effort) | low | ≤10k | Pricing from the price sheet only | Custom pricing or terms -> T3 review |
| Account strategy for a key deal | **T3** GPT-6.1 Sol | high | ≤15k | Stakeholders, pains, plan, risks | Never above T3 |
| Objection handling and negotiation prep | **T3** GPT-6.1 Sol | medium | ≤8k | Response per objection + walk-away | Never above T3 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Pricing, discounts, contract terms or legal language.
- Replies to an angry or churning customer.
- Enterprise deals above your team's normal deal size.

## Context diet

- Enrich leads from structured fields (company, role, size, one recent signal), not full web pages.
- Summarise call transcripts on T1 into a fixed template; later steps use only the summary.
- Keep a stable ICP and value-prop card as the first block of every batch.
- GPT-6.1 Sol and GPT-6 Luna cost more per token above 272k input tokens. Compact long sessions before that.

## Do it without a model (T0)

- Dedupe, normalise and update CRM fields via import or API scripts.
- Email verification and bounce checks with a verification tool.
- Sequencing and scheduling in the sales tool, not via a model.

## Briefing workers

Brief T1 with the ICP card, the lead's 4 fields and 'one sentence, must reference one fact from input'.

In Codex (CLI, IDE, app), send T1 work to the `micro-worker` agent, T2 to `standard-worker` and T3 reviews to `strong-reviewer`; each one is pinned to the right OpenAI model. Anywhere else, print the routing plan and tell the user which model to use at each step.

## Anti-patterns

- GPT-6.1 Sol writing 200 first lines.
- Pasting whole LinkedIn profiles into every personalisation call.
- Model-generated pricing without the price sheet.

## Example

Request: "Find and prioritise 100 Berlin mobility startups, then draft outreach for the top 20."

```text
ROUTING PLAN
1. [T0] script                 Pull list, dedupe, verify emails
2. [T1] luna/low               ICP fit score per company (batch of 50)
3. [T2] sol/low                Research summary for top 20
4. [T2] sol/medium             Personalised first line + 3-step sequence for top 20
5. [T3] sol/medium             Review the 5 biggest accounts' messages
6. [T0] script                 Push to CRM
```
