---
name: educator-creator-routing
description: "Model routing for teaching and course creation: which tier designs curricula, writes lessons, generates quizzes and flashcards, translates material, checks answers and creates video scripts for education. Use for lessons, courses, exam prep or study apps. Not for marketing the course."
license: MIT
compatibility: "Agent Skills format. Packaged for Google: Gemini CLI, Gemini API and Managed Agents. Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "google"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
  modeled-token-saving: "56%"
  modeled-cost-saving: "71%"
  pricing-checked: "2026-10-20"
---

# Educator and course creator routing (Google)

Curriculum design and fact accuracy deserve Gemini 4 Argon. Generating hundreds of questions, flashcards and translations is volume work for cheaper tiers, with a strong check on correctness.

- **For:** Teachers, tutors, course creators and education YouTubers building lessons, quizzes, flashcards and study apps.
- **Win condition:** Accurate learning material at scale, produced at a fraction of the cost, with zero factual errors shipped.
- **Modeled saving on Google:** about 71% lower cost and 56% fewer tokens than running everything on Gemini 4 Argon (pessimistic case: 58% / 18%). [Method](https://github.com/UtpalDasLabs/token-saver-automated-model-picker/blob/main/METHODOLOGY.md)

## Core rules

Apply `base-model-routing` if it is installed. If not, these are the rules that matter:

1. Use a tool or script (T0) whenever a deterministic command can do the job.
2. Otherwise pick the lowest tier in the routing table below, at the lowest listed effort.
3. Run the listed check before accepting any output.
4. On failure, retry once with the exact error, then move up one tier. Never skip to the top.
5. Judging, choosing the best option and anything public or irreversible start at T3.
6. Brief workers with only the context they need, and cap the output length.

Tiers on Google: **T0** tool · **T1** Gemini 3.1 Flash-Lite · **T2** Gemini 3.8 Flash · **T3** Gemini 4 Argon · **T4** Gemini 4 Argon (high thinking) (rare).

## Routing table

| Task | Tier | Effort | Context in | Check before accepting | Escalate when |
|---|---|---|---|---|---|
| Dedupe, format, export question bank | **T0** script / tool | - | ≤1.5k | Schema + duplicate check | Never |
| Flashcards from a word or fact list | **T1** Gemini 3.1 Flash-Lite | low | ≤5k | Front/back schema, no duplicates | Never |
| Lesson draft from objectives | **T2** Gemini 3.8 Flash | medium | ≤8k | Covers each objective, level-appropriate | Never |
| Generate quiz questions and distractors | **T2** Gemini 3.8 Flash | low | ≤5k | One correct answer, schema valid | Never |
| Translate learning material | **T2** Gemini 3.8 Flash | low | ≤8k | Terms glossary respected | Legal or exam wording -> T3 |
| Plain-language explanations | **T2** Gemini 3.8 Flash | low | ≤3k | Reading level check | Never |
| Grade or give feedback on student writing | **T2** Gemini 3.8 Flash | medium | ≤4k | Rubric criteria scored | Disputed grade -> T3 |
| Educational video script | **T2** Gemini 3.8 Flash | medium | ≤6k | Timed, one concept per segment | Never |
| Curriculum and learning objectives | **T3** Gemini 4 Argon | medium | ≤12k | Objectives map to official syllabus | Never above T3 |
| Verify answers against the official source | **T3** Gemini 4 Argon | medium | ≤10k | Each answer has source reference | Source unclear -> flag to the user |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Exam content where a wrong answer costs a learner a pass (citizenship, licence, certification).
- Legal, medical or safety facts.
- Disputed grades or complaints from learners.

## Context diet

- Generate questions per topic from the objective list and a short source excerpt, not the whole textbook.
- Keep a stable glossary and level card as the first block for translations.
- Verification step reads question + answer + source excerpt only.
- Keep T1 prompts small; Flash-Lite is for short, bounded inputs.

## Do it without a model (T0)

- Deduplication and schema checks on question banks with a script.
- Export to CSV, Anki or JSON with a converter.
- Text-to-speech and reading-level scores with tools.

## Briefing workers

Brief T2 with the objective, level, source excerpt, schema and 'exactly one correct option'.

In Gemini CLI, send T1 work to the `micro-worker` agent, T2 to `standard-worker` and T3 reviews to `strong-reviewer`; each one is pinned to the right Google model. Anywhere else, print the routing plan and tell the user which model to use at each step.

## Anti-patterns

- Generating 500 questions on Gemini 4 Argon.
- Publishing generated exam answers without a T3 source check.
- Translating without a glossary, so terms drift.

## Example

Request: "Create 200 B1 German grammar drills with explanations, checked and exported for my app."

```text
ROUTING PLAN
1. [T3] argon/medium           Map grammar topics to B1 syllabus, set difficulty mix
2. [T2] flash/low              Generate drills per topic (batches of 20)
3. [T0] script                 Schema check, dedupe
4. [T3] argon/medium           Verify a sample of 40 + all flagged items against grammar rules
5. [T2] flash/low              Fix flagged items
6. [T0] script                 Export JSON for the app
```
