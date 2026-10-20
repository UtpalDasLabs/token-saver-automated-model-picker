---
name: job-seeker-routing
description: "Model routing for job search: which tier positions your story, tailors CVs, writes cover letters, matches keywords, researches companies, preps interviews and drafts follow-ups. Use for applying to jobs or preparing interviews. Not for hiring or recruiting candidates."
license: MIT
compatibility: "Agent Skills format. Packaged for OpenAI: Codex (CLI, IDE, app), ChatGPT, OpenAI API. Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "openai"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
  modeled-token-saving: "56%"
  modeled-cost-saving: "53%"
  pricing-checked: "2026-10-20"
---

# Job seeker routing (OpenAI)

Positioning and interview strategy deserve GPT-6.1 Sol. Matching keywords, formatting and drafting from your own facts are cheaper-tier work.

- **For:** Professionals searching for a new role: tailoring CVs, writing cover letters, researching companies and preparing interviews.
- **Win condition:** More tailored applications and better-prepared interviews, without burning premium tokens on formatting.
- **Modeled saving on OpenAI:** about 53% lower cost and 56% fewer tokens than running everything on GPT-6.1 Sol (pessimistic case: 25% / 17%). [Method](https://github.com/UtpalDasLabs/token-saver-automated-model-picker/blob/main/METHODOLOGY.md)

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
| Application tracker updates | **T0** script / tool | - | ≤1.5k | Sheet row added | Never |
| Extract requirements from a job ad | **T1** GPT-6 Luna | low | ≤3k | Must-have vs nice-to-have list | Never |
| Follow-up and thank-you emails | **T1** GPT-6 Luna | low | ≤2k | Under 120 words | Negotiation -> T3 |
| Tailor CV bullets to the ad | **T2** GPT-6.1 Sol (low effort) | low | ≤6k | Only facts from master CV | Gap needs reframing -> T3 |
| Cover letter draft | **T2** GPT-6.1 Sol (low effort) | low | ≤6k | Under 300 words, names the company's need | Dream role -> T3 edit |
| Company research brief | **T2** GPT-6.1 Sol (low effort) | low | ≤8k | 5 facts with sources | Never |
| Career positioning and target-role story | **T3** GPT-6.1 Sol | high | ≤15k | Headline, 3 proof points, target roles | Never above T3 |
| Interview question prep and STAR answers | **T3** GPT-6.1 Sol | medium | ≤10k | Answers use real stories, under 2 minutes each | Never above T3 |
| Mock interview feedback | **T3** GPT-6.1 Sol | medium | ≤8k | 3 fixes per answer | Never above T3 |
| Salary negotiation prep | **T3** GPT-6.1 Sol | high | ≤10k | Range, anchors, walk-away | Never above T3 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Salary and offer negotiation.
- Final applications for roles you care most about.
- Explaining career gaps or role changes.

## Context diet

- Keep one master CV and one proof-points file; send the relevant bullets, not the whole history.
- Extract the ad's requirements on T1 first; the tailoring step reads only that list.
- Never paste the full company website; send the research brief.
- GPT-6.1 Sol and GPT-6 Luna cost more per token above 272k input tokens. Compact long sessions before that.

## Do it without a model (T0)

- Application tracking in a sheet with formulas for follow-up dates.
- PDF export and formatting with a template, not a model.
- Keyword overlap counts with a script.

## Briefing workers

Brief T2 with the extracted requirements, the master bullets and 'only reword facts given; no new claims'.

In Codex (CLI, IDE, app), send T1 work to the `micro-worker` agent, T2 to `standard-worker` and T3 reviews to `strong-reviewer`; each one is pinned to the right OpenAI model. Anywhere else, print the routing plan and tell the user which model to use at each step.

## Anti-patterns

- GPT-6.1 Sol reformatting a CV.
- Letting any model invent achievements not in the master CV.
- Rewriting the whole CV for every application instead of swapping bullets.

## Example

Request: "Apply to this Head of Product role at a mobility company: tailor my CV, write the letter, and prep me for the interview."

```text
ROUTING PLAN
1. [T1] luna/low               Extract must-haves and nice-to-haves from the ad
2. [T2] sol/low                Company research brief
3. [T2] sol/medium             Tailor CV bullets from the master CV
4. [T2] sol/medium             Cover letter draft
5. [T3] sol/medium             Edit letter + check positioning (dream role)
6. [T3] sol/medium             Likely questions + STAR answers from real stories
7. [T0] sheet                  Log application, set follow-up date
```
