---
name: vibe-coder-routing
description: "Model routing for AI-assisted coding: decide which tier plans, implements, tests, debugs and reviews code. Use when building features, fixing bugs, refactoring, writing tests or commits, or asked to code cheaper. Not for product strategy or PRDs."
license: MIT
compatibility: "Agent Skills format. Packaged for Anthropic: Claude Code, Claude.ai, Claude API. Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "anthropic"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
  modeled-token-saving: "65%"
  modeled-cost-saving: "68%"
  pricing-checked: "2026-10-20"
---

# Vibe coder routing (Anthropic)

Ship working code fast without paying Claude Opus 5.5 prices for routine edits. Claude Opus 5.5 thinks, Claude Sonnet 5.5 types, Claude Haiku 5.5 and scripts do the chores.

- **For:** Indie hackers, prototypers and AI-assisted builders shipping web apps with AI coding agents, Vercel and Supabase.
- **Win condition:** Feature merged, tests green, lowest spend per merged change.
- **Modeled saving on Anthropic:** about 68% lower cost and 65% fewer tokens than running everything on Claude Opus 5.5 (pessimistic case: 50% / 21%). [Method](https://github.com/UtpalDasLabs/token-saver-automated-model-picker/blob/main/METHODOLOGY.md)

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
| Rename files, format, auto-fix lint | **T0** script / tool | - | ≤1.5k | Formatter/linter exit code 0 | Linter rule needs a code decision -> T2 |
| Check routes, links, env vars, dead code | **T0** script / tool | - | ≤1.5k | Script report | Report shows unexpected failures -> T1 summary |
| Summarise a log or stack trace | **T1** Claude Haiku 5.5 | low | ≤5k | Names the failing file and line | Trace spans several services |
| Explain an error or answer a small API question | **T1** Claude Haiku 5.5 | medium | ≤3k | Answer cites the doc or line | Answer contradicts observed behaviour |
| Commit message or PR description from a diff | **T1** Claude Haiku 5.5 | low | ≤3k | Conventional-commit format | Never |
| Implement a feature from a clear spec | **T2** Claude Sonnet 5.5 | medium | ≤18k | Tests + typecheck + lint pass | Fails checks twice or spec gap found |
| UI tweak, copy or style change | **T2** Claude Sonnet 5.5 | low | ≤6k | Build passes, screenshot matches | Layout breaks across breakpoints twice |
| Write tests for existing code | **T2** Claude Sonnet 5.5 | medium | ≤12k | Tests run and fail when code is broken | Tests need design decisions about behaviour |
| Refactor to a known pattern | **T2** Claude Sonnet 5.5 | medium | ≤20k | Same tests pass, diff is behaviour-neutral | Touches more than 5 files or public APIs |
| Docs, README, code comments | **T2** Claude Sonnet 5.5 | low | ≤8k | Commands in docs actually run | Never; docs stay on T2 |
| Plan a feature or choose an architecture | **T3** Claude Opus 5.5 | high | ≤25k | Plan names files, data model and test strategy | Two plausible designs remain and stakes are high |
| Debug an unclear or multi-file bug | **T3** Claude Opus 5.5 | medium | ≤35k | Repro test fails before, passes after | Root cause still unknown after one T3 pass at high |
| Review a risky change before deploy (auth, payments, migrations) | **T3** Claude Opus 5.5 | high | ≤20k | Reviewer verdict SHIP | Reviewer unsure on security or data loss -> T4 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Auth, payments, row-level security, database migrations or anything that can lose user data.
- The bug only reproduces in production or is intermittent.
- The user cannot describe the expected behaviour; clarify on T3 before any code is written.
- Two cheap attempts produced different wrong fixes for the same failing test.

## Context diet

- Send the failing test output, the stack trace's top frames and the touched files, never the whole repo.
- Give T2 workers file paths plus a 10-line spec; let them open files themselves.
- Summarise long CI logs on T1 down to the first error and its cause.
- Keep the project conventions (stack, lint rules, folder layout) in one stable AGENTS.md or CLAUDE.md-style project file so it is cached.
- Claude Haiku 5.5 costs 5x more per token once a prompt passes 100k tokens. Split or compact before that line.

## Do it without a model (T0)

- Formatting, import sorting and lint autofix (`prettier --write`, `eslint --fix`, `ruff --fix`).
- Renames and moves with `git mv` and editor refactors, not a model rewrite.
- Dead links, env var presence, route lists, TODO extraction with `grep`/`rg` scripts.
- Type errors: run `tsc` first and pass only the errors to the worker.

## Briefing workers

Brief T2 with: goal, files to touch, files not to touch, the exact test command, and 'diff only'.

In Claude Code, send T1 work to the `micro-worker` agent, T2 to `standard-worker` and T3 reviews to `strong-reviewer`; each one is pinned to the right Anthropic model. Anywhere else, print the routing plan and tell the user which model to use at each step.

## Anti-patterns

- Asking Claude Opus 5.5 to "make the button blue".
- Pasting the full repo into a commit-message request.
- Letting a T2 worker loop five times on the same failing test instead of escalating after two.
- Refactoring and adding features in the same step, which makes validation impossible.

## Example

Request: "Add Google sign-in to my Next.js + Supabase app, write tests, and open a PR."

```text
ROUTING PLAN
1. [T3] opus/high              Design auth flow: callback route, session handling, RLS impact
2. [T2] sonnet/medium          Implement provider config + callback route from the design
3. [T2] sonnet/medium          Write tests for sign-in, sign-out, expired session
4. [T0] script                 Run lint --fix, typecheck, test suite
5. [T1] haiku/low              Summarise any failing test output
6. [T3] opus/high              Review diff (auth = high stakes) -> SHIP / FIX
7. [T1] haiku/low              Write PR description from the final diff
Escalate: a step failing its check twice moves up one tier.
```
