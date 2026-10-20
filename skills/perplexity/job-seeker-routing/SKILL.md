---
name: job-seeker-routing
description: "Model routing for job search: which tier positions your story, tailors CVs, writes cover letters, matches keywords, researches companies, preps interviews and drafts follow-ups. Use for applying to jobs or preparing interviews. Not for hiring or recruiting candidates."
license: MIT
compatibility: "Agent Skills format. Packaged for Perplexity: Perplexity Computer, Perplexity Agent API. Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "perplexity"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
  modeled-token-saving: "54%"
  modeled-cost-saving: "71%"
  pricing-checked: "2026-10-20"
---

# Job seeker routing (Perplexity)

Positioning and interview strategy deserve Claude Opus 5.5. Matching keywords, formatting and drafting from your own facts are cheaper-tier work.

- **For:** Professionals searching for a new role: tailoring CVs, writing cover letters, researching companies and preparing interviews.
- **Win condition:** More tailored applications and better-prepared interviews, without burning premium tokens on formatting.
- **Modeled saving on Perplexity:** about 71% lower cost and 54% fewer tokens than running everything on Claude Opus 5.5 (pessimistic case: 59% / 15%). [Method](https://github.com/UtpalDasLabs/token-saver-automated-model-picker/blob/main/METHODOLOGY.md)

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
| Application tracker updates | **T0** script / tool | - | ≤1.5k | Sheet row added | Never |
| Extract requirements from a job ad | **T1** GPT-6 Luna | low | ≤3k | Must-have vs nice-to-have list | Never |
| Follow-up and thank-you emails | **T1** GPT-6 Luna | low | ≤2k | Under 120 words | Negotiation -> T3 |
| Tailor CV bullets to the ad | **T2** Gemini 3.8 Flash | medium | ≤6k | Only facts from master CV | Gap needs reframing -> T3 |
| Cover letter draft | **T2** Gemini 3.8 Flash | medium | ≤6k | Under 300 words, names the company's need | Dream role -> T3 edit |
| Company research brief | **T2** Gemini 3.8 Flash | low | ≤8k | 5 facts with sources | Never |
| Career positioning and target-role story | **T3** Claude Opus 5.5 | high | ≤15k | Headline, 3 proof points, target roles | Never above T3 |
| Interview question prep and STAR answers | **T3** Claude Opus 5.5 | medium | ≤10k | Answers use real stories, under 2 minutes each | Never above T3 |
| Mock interview feedback | **T3** Claude Opus 5.5 | medium | ≤8k | 3 fixes per answer | Never above T3 |
| Salary negotiation prep | **T3** Claude Opus 5.5 | high | ≤10k | Range, anchors, walk-away | Never above T3 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Salary and offer negotiation.
- Final applications for roles you care most about.
- Explaining career gaps or role changes.

## Context diet

- Keep one master CV and one proof-points file; send the relevant bullets, not the whole history.
- Extract the ad's requirements on T1 first; the tailoring step reads only that list.
- Never paste the full company website; send the research brief.
- Web search and fetch tool calls are billed on top of tokens; search once, then reuse the results.

## Do it without a model (T0)

- Application tracking in a sheet with formulas for follow-up dates.
- PDF export and formatting with a template, not a model.
- Keyword overlap counts with a script.

## Briefing workers

Brief T2 with the extracted requirements, the master bullets and 'only reword facts given; no new claims'.

In Perplexity Computer, write the tier and model into each step of the plan and keep cheap steps on small context or scripts. On the Agent API, set `model` per request from the routing table.

## Anti-patterns

- Claude Opus 5.5 reformatting a CV.
- Letting any model invent achievements not in the master CV.
- Rewriting the whole CV for every application instead of swapping bullets.

## Example

Request: "Apply to this Head of Product role at a mobility company: tailor my CV, write the letter, and prep me for the interview."

```text
ROUTING PLAN
1. [T1] luna/low               Extract must-haves and nice-to-haves from the ad
2. [T2] gemini-flash/low       Company research brief
3. [T2] gemini-flash/medium    Tailor CV bullets from the master CV
4. [T2] gemini-flash/medium    Cover letter draft
5. [T3] opus/medium            Edit letter + check positioning (dream role)
6. [T3] opus/medium            Likely questions + STAR answers from real stories
7. [T0] sheet                  Log application, set follow-up date
```
