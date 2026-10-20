---
name: designer-routing
description: "Model routing for UX and UI design: which tier does design critique, flows, UX research synthesis, microcopy, design tokens, component specs, accessibility checks and dev handoff notes. Use for Figma, prototyping or design-system work. Not for writing production code."
license: MIT
compatibility: "Agent Skills format. Packaged for Qwen: Qwen Code, Model Studio API. Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "qwen"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
  modeled-token-saving: "55%"
  modeled-cost-saving: "69%"
  pricing-checked: "2026-10-20"
---

# Designer routing (Qwen)

Design judgement and critique stay on Qwen3.8-Max; specs, microcopy, token tables and handoff notes go down the ladder.

- **For:** Product, UX and UI designers working in Figma, design systems and prototypes, often handing off to AI coding tools.
- **Win condition:** Clearer design decisions and cleaner handoffs, with model spend focused on critique rather than paperwork.
- **Modeled saving on Qwen:** about 69% lower cost and 55% fewer tokens than running everything on Qwen3.8-Max (pessimistic case: 57% / 16%). [Method](https://github.com/UtpalDasLabs/token-saver-automated-model-picker/blob/main/METHODOLOGY.md)

## Core rules

Apply `base-model-routing` if it is installed. If not, these are the rules that matter:

1. Use a tool or script (T0) whenever a deterministic command can do the job.
2. Otherwise pick the lowest tier in the routing table below, at the lowest listed effort.
3. Run the listed check before accepting any output.
4. On failure, retry once with the exact error, then move up one tier. Never skip to the top.
5. Judging, choosing the best option and anything public or irreversible start at T3.
6. Brief workers with only the context they need, and cap the output length.

Tiers on Qwen: **T0** tool · **T1** Qwen3.7-Flash · **T2** Qwen3.7-Plus · **T3** Qwen3.8-Max · **T4** Qwen3.8-Max (thinking) (rare).

## Routing table

| Task | Tier | Effort | Context in | Check before accepting | Escalate when |
|---|---|---|---|---|---|
| Design tokens to JSON/CSS | **T0** script / tool | - | ≤1.5k | Token build passes | Never |
| Accessibility contrast and alt text checks | **T0** script / tool | - | ≤1.5k | WCAG contrast tool report | Complex interaction a11y -> T3 |
| Alt text and image descriptions | **T1** Qwen3.7-Flash | low | ≤2k | Under 125 characters | Never |
| Image-generation prompt variants | **T1** Qwen3.7-Flash | low | ≤1.5k | Prompt template filled | Choose winners on T3 |
| Microcopy variants (buttons, errors, empty states) | **T2** Qwen3.7-Plus | low | ≤2k | Length per component | Pick on T3 for key screens |
| Component spec and props table | **T2** Qwen3.7-Plus | low | ≤5k | All variants and states covered | Never |
| Synthesise usability test notes | **T2** Qwen3.7-Plus | medium | ≤12k | Issues with severity + count | Contradictory findings -> T3 |
| Dev handoff notes | **T2** Qwen3.7-Plus | low | ≤5k | Spacing, states, breakpoints listed | Never |
| Design critique and direction | **T3** Qwen3.8-Max | medium | ≤10k | Issues ranked by user impact | Never above T3 |
| User flow and information architecture | **T3** Qwen3.8-Max | medium | ≤10k | Every state and edge case listed | Never above T3 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Changes to core navigation, onboarding or checkout flows.
- Accessibility issues beyond colour contrast (focus order, screen-reader flows).
- Brand identity decisions.

## Context diet

- Describe the screen with its component list and states, or export a single frame, not the whole Figma file.
- Keep the design-system summary (tokens, components, voice) as a stable first block.
- Usability notes: summarise per session on T1 first, then synthesise.
- Qwen3.7-Flash costs about 3x more per token above 32k input tokens. Keep T1 prompts under 32k.

## Do it without a model (T0)

- Contrast checks with a WCAG checker or plugin.
- Token export with Style Dictionary or the Figma variables export.
- Asset renaming and export presets in Figma itself.

## Briefing workers

Brief T2 with the component name, states, token names and 'table only'.

In Qwen Code, send T1 work to the `micro-worker` agent, T2 to `standard-worker` and T3 reviews to `strong-reviewer`; each one is pinned to the right Qwen model. Anywhere else, print the routing plan and tell the user which model to use at each step.

## Anti-patterns

- Qwen3.8-Max writing 30 button labels.
- Qwen3.7-Flash critiquing a flow.
- Sending screenshots of every screen when one flow diagram would do.

## Example

Request: "Review my new onboarding flow in Figma and prepare the handoff for the developers."

```text
ROUTING PLAN
1. [T3] max/medium             Critique flow: friction, missing states, a11y risks
2. [T2] plus/low               Microcopy variants for 6 key screens
3. [T3] max/medium             Pick microcopy for the 2 most important screens
4. [T0] tool                   Contrast check + token export
5. [T2] plus/low               Component specs + handoff notes
```
