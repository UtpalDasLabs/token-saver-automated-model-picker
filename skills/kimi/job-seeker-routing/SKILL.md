---
name: job-seeker-routing
description: "Model routing for job search: which tier positions your story, tailors CVs, writes cover letters, matches keywords, researches companies, preps interviews and drafts follow-ups. Use for applying to jobs or preparing interviews. Not for hiring or recruiting candidates."
license: MIT
compatibility: "Agent Skills format. Packaged for Kimi: Kimi Code, Kimi API. Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "kimi"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
  modeled-token-saving: "55%"
  modeled-cost-saving: "42%"
  pricing-checked: "2026-10-26"
---

# Job seeker routing (Kimi)

Positioning and interview strategy deserve Kimi K3.1 Pro. Matching keywords, formatting and drafting from your own facts are cheaper-tier work.

- **For:** Professionals searching for a new role: tailoring CVs, writing cover letters, researching companies and preparing interviews.
- **Win condition:** More tailored applications and better-prepared interviews, without burning premium tokens on formatting.
- **Modeled saving on Kimi:** about 42% lower cost and 55% fewer tokens than running everything on Kimi K3.1 Pro (pessimistic case: 9% / 15%). [Method](https://github.com/UtpalDasLabs/token-saver-automated-model-picker/blob/main/METHODOLOGY.md)

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
| Application tracker updates | **T0** script / tool | - | ≤1.5k | Sheet row added | Never |
| Extract requirements from a job ad | **T1** Kimi K3.1 Pro (low effort) | low | ≤3k | Must-have vs nice-to-have list | Never |
| Follow-up and thank-you emails | **T1** Kimi K3.1 Pro (low effort) | low | ≤2k | Under 120 words | Negotiation -> T3 |
| Tailor CV bullets to the ad | **T2** Kimi K3.1 Pro | high | ≤6k | Only facts from master CV | Gap needs reframing -> T3 |
| Cover letter draft | **T2** Kimi K3.1 Pro | high | ≤6k | Under 300 words, names the company's need | Dream role -> T3 edit |
| Company research brief | **T2** Kimi K3.1 Pro | low | ≤8k | 5 facts with sources | Never |
| Career positioning and target-role story | **T3** Kimi K3.1 Pro | max | ≤15k | Headline, 3 proof points, target roles | Never above T3 |
| Interview question prep and STAR answers | **T3** Kimi K3.1 Pro | high | ≤10k | Answers use real stories, under 2 minutes each | Never above T3 |
| Mock interview feedback | **T3** Kimi K3.1 Pro | high | ≤8k | 3 fixes per answer | Never above T3 |
| Salary negotiation prep | **T3** Kimi K3.1 Pro | max | ≤10k | Range, anchors, walk-away | Never above T3 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Salary and offer negotiation.
- Final applications for roles you care most about.
- Explaining career gaps or role changes.

## Context diet

- Keep one master CV and one proof-points file; send the relevant bullets, not the whole history.
- Extract the ad's requirements on T1 first; the tailoring step reads only that list.
- Never paste the full company website; send the research brief.
- Kimi has no supported cheaper micro model. Use T0 scripts, low effort and tight context for savings; do not use retired K2 models.

## Do it without a model (T0)

- Application tracking in a sheet with formulas for follow-up dates.
- PDF export and formatting with a template, not a model.
- Keyword overlap counts with a script.

## Briefing workers

Brief T2 with the extracted requirements, the master bullets and 'only reword facts given; no new claims'.

In Kimi Code, print the routing plan and use `/model` to select K3.1 Pro with the listed effort before each step. `/secondary-model` sets one default for subagents, but custom agents cannot pin different models; do not claim automatic per-tier switching. On the Kimi API, set `model` and `reasoning_effort` per request from the routing table.

## Anti-patterns

- Kimi K3.1 Pro reformatting a CV.
- Letting any model invent achievements not in the master CV.
- Rewriting the whole CV for every application instead of swapping bullets.

## Example

Request: "Apply to this Head of Product role at a mobility company: tailor my CV, write the letter, and prep me for the interview."

```text
ROUTING PLAN
1. [T1] k3.1-pro/low           Extract must-haves and nice-to-haves from the ad
2. [T2] k3.1-pro/low           Company research brief
3. [T2] k3.1-pro/high          Tailor CV bullets from the master CV
4. [T2] k3.1-pro/high          Cover letter draft
5. [T3] k3.1-pro/high          Edit letter + check positioning (dream role)
6. [T3] k3.1-pro/high          Likely questions + STAR answers from real stories
7. [T0] sheet                  Log application, set follow-up date
```
