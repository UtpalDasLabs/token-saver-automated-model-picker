---
name: ops-assistant-routing
description: "Model routing for operations and admin work: which tier handles spreadsheets, CSV cleanup, file renaming, inbox triage, scheduling, data entry, uploads and recurring reports. Use for bulk admin, VA or chief-of-staff tasks. Not for financial analysis or strategy."
license: MIT
compatibility: "Agent Skills format. Packaged for Anthropic: Claude Code, Claude.ai, Claude API. Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "anthropic"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
  modeled-token-saving: "63%"
  modeled-cost-saving: "83%"
  pricing-checked: "2026-10-20"
---

# Ops assistant routing (Anthropic)

Most ops work is rules, not judgement. Push it to scripts and Claude Haiku 5.5, keep Claude Sonnet 5.5 for drafting and Claude Opus 5.5 for the rare exception.

- **For:** Virtual assistants, operations managers, chiefs of staff and admins running sheets, inboxes, files, uploads and recurring admin.
- **Win condition:** Admin done on time with near-zero AI spend and no silent data errors.
- **Modeled saving on Anthropic:** about 83% lower cost and 63% fewer tokens than running everything on Claude Opus 5.5 (pessimistic case: 77% / 21%). [Method](https://github.com/UtpalDasLabs/token-saver-automated-model-picker/blob/main/METHODOLOGY.md)

## Core rules

Apply `base-model-routing` if it is installed. If not, these are the rules that matter:

1. Use a tool or script (T0) whenever a deterministic command can do the job.
2. Otherwise pick the lowest tier in the routing table below, at the lowest listed effort.
3. Run the listed check before accepting any output.
4. On failure, retry once with the exact error, then move up one tier. Never skip to the top.
5. Judging, choosing the best option and anything public or irreversible start at T3.
6. Brief workers with only the context they need, and cap the output length.

Tiers on Anthropic: **T0** tool · **T1** Claude Haiku 5.5 · **T2** Claude Sonnet 5.5 · **T3** Claude Opus 5.5 · **T4** Claude Fable 5.1 (rare).

## Routing table

| Task | Tier | Effort | Context in | Check before accepting | Escalate when |
|---|---|---|---|---|---|
| Clean and normalise a CSV or sheet | **T0** script / tool | - | ≤2k | Row count unchanged, schema valid | Messy free text -> T1 per column |
| Rename and sort files | **T0** script / tool | - | ≤1.5k | Dry-run list approved | Never |
| Check links and uploads | **T0** script / tool | - | ≤1.5k | Status code report | Never |
| Categorise or tag rows | **T1** Claude Haiku 5.5 | low | ≤8k | Only allowed labels used | More than 10% UNSURE -> T2 |
| Inbox triage and labelling | **T1** Claude Haiku 5.5 | low | ≤6k | Label + priority per email | Legal, HR or money emails -> T3 |
| Extract fields from invoices or forms | **T1** Claude Haiku 5.5 | low | ≤4k | JSON schema + totals add up | Handwritten or unclear scan -> T2 |
| Meeting scheduling and agenda | **T1** Claude Haiku 5.5 | low | ≤2k | Time zones correct | Never |
| Draft routine email replies | **T2** Claude Sonnet 5.5 | low | ≤3k | Under 120 words, facts from thread | Sensitive or angry thread -> T3 |
| Weekly ops report from data | **T2** Claude Sonnet 5.5 | low | ≤6k | Numbers match sheet | Anomaly needs explaining -> T3 |
| Write an SOP or process doc | **T2** Claude Sonnet 5.5 | medium | ≤8k | Numbered steps, owner, done condition | Process redesign -> T3 |
| Resolve an unusual exception | **T3** Claude Opus 5.5 | medium | ≤8k | Decision + rationale | Never above T3 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Anything involving payments, contracts, HR, legal or personal data deletion.
- Emails to executives, investors or upset customers.
- A rule that conflicts with what the data shows.

## Context diet

- Send only the columns the task needs plus 3 example rows, not the whole sheet.
- For inbox triage, send sender, subject and the first 300 characters, not full threads.
- Keep a stable labels-and-rules card as the first block of every batch.
- Claude Haiku 5.5 costs 5x more per token once a prompt passes 100k tokens. Split or compact before that line.

## Do it without a model (T0)

- CSV cleanup: trim, dedupe, case, date formats with a script or sheet formulas.
- File renames with a dry-run script the user approves.
- Link and upload checks with `curl` or the platform's API.
- Totals and reconciliation with formulas; the model only explains differences.

## Briefing workers

Brief T1 with the label list, 3 labelled examples, 'one line per row, ID first', and 'UNSURE if unclear'.

In Claude Code, send T1 work to the `micro-worker` agent, T2 to `standard-worker` and T3 reviews to `strong-reviewer`; each one is pinned to the right Anthropic model. Anywhere else, print the routing plan and tell the user which model to use at each step.

## Anti-patterns

- Asking any model to "clean up this spreadsheet" when a formula would do it exactly.
- Claude Opus 5.5 drafting "thanks, received" replies.
- Bulk-sending model-drafted emails without a T3 check on sensitive ones.

## Example

Request: "Clean this 2,000-row supplier sheet, tag each by category, and draft a reminder to the 40 overdue ones."

```text
ROUTING PLAN
1. [T0] script                 Trim, dedupe, normalise dates and country codes
2. [T1] haiku/low              Tag category per row, chunks of 50 (UNSURE allowed)
3. [T2] sonnet/low             Tag the UNSURE rows
4. [T0] formula                Filter overdue suppliers
5. [T2] sonnet/low             One reminder template + merge fields
6. [T3] opus/medium            Review tone for the 5 largest suppliers before sending
```
