---
name: ops-assistant-routing
description: "Model routing for operations and admin work: which tier handles spreadsheets, CSV cleanup, file renaming, inbox triage, scheduling, data entry, uploads and recurring reports. Use for bulk admin, VA or chief-of-staff tasks. Not for financial analysis or strategy."
license: MIT
compatibility: "Agent Skills format. Packaged for Kimi: Kimi Code, Kimi API. Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "kimi"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
  modeled-token-saving: "64%"
  modeled-cost-saving: "56%"
  pricing-checked: "2026-10-26"
---

# Ops assistant routing (Kimi)

Most ops work is rules, not judgement. Push it to scripts and Kimi K3.1 Pro (low effort), keep Kimi K3.1 Pro for drafting and Kimi K3.1 Pro for the rare exception.

- **For:** Virtual assistants, operations managers, chiefs of staff and admins running sheets, inboxes, files, uploads and recurring admin.
- **Win condition:** Admin done on time with near-zero AI spend and no silent data errors.
- **Modeled saving on Kimi:** about 56% lower cost and 64% fewer tokens than running everything on Kimi K3.1 Pro (pessimistic case: 19% / 22%). [Method](https://github.com/UtpalDasLabs/token-saver-automated-model-picker/blob/main/METHODOLOGY.md)

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
| Clean and normalise a CSV or sheet | **T0** script / tool | - | ≤2k | Row count unchanged, schema valid | Messy free text -> T1 per column |
| Rename and sort files | **T0** script / tool | - | ≤1.5k | Dry-run list approved | Never |
| Check links and uploads | **T0** script / tool | - | ≤1.5k | Status code report | Never |
| Categorise or tag rows | **T1** Kimi K3.1 Pro (low effort) | low | ≤8k | Only allowed labels used | More than 10% UNSURE -> T2 |
| Inbox triage and labelling | **T1** Kimi K3.1 Pro (low effort) | low | ≤6k | Label + priority per email | Legal, HR or money emails -> T3 |
| Extract fields from invoices or forms | **T1** Kimi K3.1 Pro (low effort) | low | ≤4k | JSON schema + totals add up | Handwritten or unclear scan -> T2 |
| Meeting scheduling and agenda | **T1** Kimi K3.1 Pro (low effort) | low | ≤2k | Time zones correct | Never |
| Draft routine email replies | **T2** Kimi K3.1 Pro | low | ≤3k | Under 120 words, facts from thread | Sensitive or angry thread -> T3 |
| Weekly ops report from data | **T2** Kimi K3.1 Pro | low | ≤6k | Numbers match sheet | Anomaly needs explaining -> T3 |
| Write an SOP or process doc | **T2** Kimi K3.1 Pro | high | ≤8k | Numbered steps, owner, done condition | Process redesign -> T3 |
| Resolve an unusual exception | **T3** Kimi K3.1 Pro | high | ≤8k | Decision + rationale | Never above T3 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Anything involving payments, contracts, HR, legal or personal data deletion.
- Emails to executives, investors or upset customers.
- A rule that conflicts with what the data shows.

## Context diet

- Send only the columns the task needs plus 3 example rows, not the whole sheet.
- For inbox triage, send sender, subject and the first 300 characters, not full threads.
- Keep a stable labels-and-rules card as the first block of every batch.
- Kimi has no supported cheaper micro model. Use T0 scripts, low effort and tight context for savings; do not use retired K2 models.

## Do it without a model (T0)

- CSV cleanup: trim, dedupe, case, date formats with a script or sheet formulas.
- File renames with a dry-run script the user approves.
- Link and upload checks with `curl` or the platform's API.
- Totals and reconciliation with formulas; the model only explains differences.

## Briefing workers

Brief T1 with the label list, 3 labelled examples, 'one line per row, ID first', and 'UNSURE if unclear'.

In Kimi Code, print the routing plan and use `/model` to select K3.1 Pro with the listed effort before each step. `/secondary-model` sets one default for subagents, but custom agents cannot pin different models; do not claim automatic per-tier switching. On the Kimi API, set `model` and `reasoning_effort` per request from the routing table.

## Anti-patterns

- Asking any model to "clean up this spreadsheet" when a formula would do it exactly.
- Kimi K3.1 Pro drafting "thanks, received" replies.
- Bulk-sending model-drafted emails without a T3 check on sensitive ones.

## Example

Request: "Clean this 2,000-row supplier sheet, tag each by category, and draft a reminder to the 40 overdue ones."

```text
ROUTING PLAN
1. [T0] script                 Trim, dedupe, normalise dates and country codes
2. [T1] k3.1-pro/low           Tag category per row, chunks of 50 (UNSURE allowed)
3. [T2] k3.1-pro/low           Tag the UNSURE rows
4. [T0] formula                Filter overdue suppliers
5. [T2] k3.1-pro/low           One reminder template + merge fields
6. [T3] k3.1-pro/high          Review tone for the 5 largest suppliers before sending
```
