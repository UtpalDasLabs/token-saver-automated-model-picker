---
name: designer-routing
description: "Model routing for UX and UI design: which tier does design critique, flows, UX research synthesis, microcopy, design tokens, component specs, accessibility checks and dev handoff notes. Use for Figma, prototyping or design-system work. Not for writing production code."
license: MIT
compatibility: "Any Agent Skills host. Automatic model switching in Claude Code with the bundled subagents; elsewhere it outputs a routing plan to apply."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "1.0.0"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-skills"
  modeled-token-saving: "55%"
  modeled-cost-saving: "60%"
  pricing-checked: "2026-10-20"
---

# Designer routing

Design judgement and critique stay on Opus; specs, microcopy, token tables and handoff notes go down the ladder.

- **For:** Product, UX and UI designers working in Figma, design systems and prototypes, often handing off to AI coding tools.
- **Win condition:** Clearer design decisions and cleaner handoffs, with model spend focused on critique rather than paperwork.
- **Modeled saving:** about 55% fewer tokens and 60% lower cost than running everything on Opus 5.5 (pessimistic case: 16% / 43%). [Method](https://github.com/UtpalDasLabs/token-saver-skills/blob/main/METHODOLOGY.md)

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
| Design tokens to JSON/CSS | **T0** script / tool | - | ≤1.5k | Token build passes | Never |
| Accessibility contrast and alt text checks | **T0** script / tool | - | ≤1.5k | WCAG contrast tool report | Complex interaction a11y -> T3 |
| Alt text and image descriptions | **T1** haiku | low | ≤2k | Under 125 characters | Never |
| Image-generation prompt variants | **T1** haiku | low | ≤1.5k | Prompt template filled | Choose winners on T3 |
| Microcopy variants (buttons, errors, empty states) | **T2** sonnet | low | ≤2k | Length per component | Pick on T3 for key screens |
| Component spec and props table | **T2** sonnet | low | ≤5k | All variants and states covered | Never |
| Synthesise usability test notes | **T2** sonnet | medium | ≤12k | Issues with severity + count | Contradictory findings -> T3 |
| Dev handoff notes | **T2** sonnet | low | ≤5k | Spacing, states, breakpoints listed | Never |
| Design critique and direction | **T3** opus | medium | ≤10k | Issues ranked by user impact | Never above T3 |
| User flow and information architecture | **T3** opus | medium | ≤10k | Every state and edge case listed | Never above T3 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Changes to core navigation, onboarding or checkout flows.
- Accessibility issues beyond colour contrast (focus order, screen-reader flows).
- Brand identity decisions.

## Context diet

- Describe the screen with its component list and states, or export a single frame, not the whole Figma file.
- Keep the design-system summary (tokens, components, voice) as a stable first block.
- Usability notes: summarise per session on T1 first, then synthesise.

## Do it without a model (T0)

- Contrast checks with a WCAG checker or plugin.
- Token export with Style Dictionary or the Figma variables export.
- Asset renaming and export presets in Figma itself.

## Briefing workers

Brief T2 with the component name, states, token names and 'table only'.

In Claude Code, send T1 work to the `micro-worker` subagent, T2 to `standard-worker` and T3 reviews to `strong-reviewer`. In chat apps, print the plan and tell the user which model to switch to at each step.

## Anti-patterns

- Opus writing 30 button labels.
- Haiku critiquing a flow.
- Sending screenshots of every screen when one flow diagram would do.

## Example

Request: "Review my new onboarding flow in Figma and prepare the handoff for the developers."

```text
ROUTING PLAN
1. [T3] opus/medium    Critique flow: friction, missing states, a11y risks
2. [T2] sonnet/low     Microcopy variants for 6 key screens
3. [T3] opus/medium    Pick microcopy for the 2 most important screens
4. [T0] tool           Contrast check + token export
5. [T2] sonnet/low     Component specs + handoff notes
```
