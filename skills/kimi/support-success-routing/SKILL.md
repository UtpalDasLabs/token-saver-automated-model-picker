---
name: support-success-routing
description: "Model routing for customer support and success: which tier triages tickets, drafts replies from help docs, summarises threads, writes macros and help articles, flags churn risk and handles escalations. Use for support queues or account management. Not for sales outreach."
license: MIT
compatibility: "Agent Skills format. Packaged for Kimi: Kimi Code, Kimi API. Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "kimi"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
  modeled-token-saving: "54%"
  modeled-cost-saving: "47%"
  pricing-checked: "2026-10-26"
---

# Support and success routing (Kimi)

Most tickets are routine and answerable from docs. Let Kimi K3.1 Pro (low effort) triage and Kimi K3.1 Pro draft; keep Kimi K3.1 Pro for escalations, churn risks and policy calls.

- **For:** Customer support agents, support leads and customer success managers handling tickets, help docs and account health.
- **Win condition:** Faster, accurate replies at lower cost per resolved ticket, with no risky answers sent unchecked.
- **Modeled saving on Kimi:** about 47% lower cost and 54% fewer tokens than running everything on Kimi K3.1 Pro (pessimistic case: 12% / 16%). [Method](https://github.com/UtpalDasLabs/token-saver-automated-model-picker/blob/main/METHODOLOGY.md)

## Core rules

Apply `base-model-routing` if it is installed. If not, these are the rules that matter:

1. Use a tool or script (T0) whenever a deterministic command can do the job.
2. Otherwise pick the lowest tier in the routing table below, at the lowest listed effort.
3. Run the listed check before accepting any output.
4. On failure, retry once with the exact error, then move up one tier. Never skip to the top.
5. Judging, choosing the best option and anything public or irreversible start at T3.
6. Brief workers with only the context they need, and cap the output length.

Tiers on Kimi: **T0** tool · **T1** Kimi K3.1 Pro (low effort) · **T2** Kimi K3.1 Pro · **T3** Kimi K3.1 Pro · **T4** Kimi K3.1 Pro (max effort) (rare).

## Routing table

| Task | Tier | Effort | Context in | Check before accepting | Escalate when |
|---|---|---|---|---|---|
| Tagging cleanup, SLA checks, merges | **T0** script / tool | - | ≤1.5k | Helpdesk automation log | Never |
| Ticket triage: category, urgency, sentiment | **T1** Kimi K3.1 Pro (low effort) | low | ≤2k | Allowed labels only | Legal threat or safety -> T3 |
| Thread summary for handover | **T1** Kimi K3.1 Pro (low effort) | low | ≤8k | Issue, tried, next step | Never |
| Translate a reply | **T1** Kimi K3.1 Pro (low effort) | high | ≤2k | Product names unchanged | Legal or refund wording -> T2 |
| Draft reply from help docs | **T2** Kimi K3.1 Pro | low | ≤6k | Cites the doc used, no new promises | No doc covers it -> T3 |
| Write or update a help article | **T2** Kimi K3.1 Pro | high | ≤8k | Steps tested against product | Never |
| Macro and canned-response updates | **T2** Kimi K3.1 Pro | low | ≤4k | Placeholders valid | Never |
| Weekly ticket trend report | **T2** Kimi K3.1 Pro | low | ≤6k | Counts from helpdesk export | New spike -> T3 |
| Escalation or angry customer reply | **T3** Kimi K3.1 Pro | high | ≤8k | Policy-compliant, empathetic, specific | Never above T3 |
| Churn-risk review of an account | **T3** Kimi K3.1 Pro | high | ≤10k | Risk level + save plan | Never above T3 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Refunds above policy, legal threats, security or data-privacy requests.
- Public complaints on social media.
- Any reply that promises a fix date or a feature.

## Context diet

- Retrieve the 1–3 relevant help articles; don't paste the whole knowledge base.
- Send the last 3 messages plus a T1 summary of the rest of the thread.
- Keep tone guide and policy card as a stable, cached first block.
- Kimi has no supported cheaper micro model. Use T0 scripts, low effort and tight context for savings; do not use retired K2 models.

## Do it without a model (T0)

- SLA timers, tag rules and auto-merges as helpdesk automations.
- Ticket counts and trends from the helpdesk export.
- Order or account lookups via API, not by asking the model to guess.

## Briefing workers

Brief T2 with the relevant doc excerpts, the policy card, the customer's last message and 'cite the doc, max 120 words'.

In Kimi Code, print the routing plan and use `/model` to select K3.1 Pro with the listed effort before each step. `/secondary-model` sets one default for subagents, but custom agents cannot pin different models; do not claim automatic per-tier switching. On the Kimi API, set `model` and `reasoning_effort` per request from the routing table.

## Anti-patterns

- Kimi K3.1 Pro answering "how do I reset my password".
- Kimi K3.1 Pro (low effort) replying to a refund dispute.
- Sending drafted replies that cite no source doc.

## Example

Request: "Clear today's 80-ticket backlog and flag anything risky."

```text
ROUTING PLAN
1. [T1] k3.1-pro/low           Triage all 80: category, urgency, sentiment (batches of 20)
2. [T0] automation             Merge duplicates, apply tags
3. [T2] k3.1-pro/low           Draft replies for routine tickets from help docs
4. [T3] k3.1-pro/high          Handle the 6 flagged: refunds, legal, angry
5. [T1] k3.1-pro/low           Summarise the open ones for handover
```
