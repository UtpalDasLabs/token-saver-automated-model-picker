---
name: research-analyst-routing
description: "Model routing for research and analysis: which tier searches, reads, extracts, compares, fact-checks and synthesises sources into briefs or reports. Use for market research, literature reviews, due diligence or competitive analysis. Not for numeric data analysis in SQL or spreadsheets."
license: MIT
compatibility: "Any Agent Skills host. Automatic model switching in Claude Code with the bundled subagents; elsewhere it outputs a routing plan to apply."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "1.0.0"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-skills"
  modeled-token-saving: "33%"
  modeled-cost-saving: "79%"
  pricing-checked: "2026-10-20"
---

# Research analyst routing

Read wide on cheap tiers, think deep on strong ones. Haiku extracts, Sonnet compiles, Opus concludes.

- **For:** Analysts, consultants, journalists, students and operators who search, read, compare and synthesise many sources.
- **Win condition:** Sourced, trustworthy conclusions at a fraction of the cost of reading everything with the top model.
- **Modeled saving:** about 33% fewer tokens and 79% lower cost than running everything on Opus 5.5 (pessimistic case: 5% / 67%). [Method](https://github.com/UtpalDasLabs/token-saver-skills/blob/main/METHODOLOGY.md)

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
| Citation formatting and link checks | **T0** script / tool | - | ≤1.5k | All URLs return 200 | Never |
| Extract facts from each source | **T1** haiku | low | ≤12k | Each fact has quote + URL | Paywalled, scanned or contradictory source -> T2 |
| Relevance triage of search results | **T1** haiku | low | ≤6k | Keep/drop with one reason | Never |
| Summarise long reports or papers | **T1** haiku | medium | ≤50k | 300 words, section anchors | Technical depth needed -> T2 |
| Compile comparison table | **T2** sonnet | medium | ≤15k | Every cell sourced, gaps marked | Sources conflict -> T3 |
| Write the final brief from the synthesis | **T2** sonnet | medium | ≤10k | Matches outline, citations intact | Never |
| Translate a foreign-language source | **T2** sonnet | low | ≤10k | Names, numbers unchanged | Legal text -> T3 |
| Frame the research question and plan | **T3** opus | medium | ≤5k | Sub-questions + source types | Never above T3 |
| Synthesis and conclusions | **T3** opus | high | ≤20k | Claims trace to extracted facts | High-stakes decision -> T4 second read |
| Fact-check key claims | **T3** opus | medium | ≤10k | Verdict + source per claim | Never above T3 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Claims that will be published, given to investors or used for legal, medical or financial decisions.
- Sources that directly contradict each other on a key number.
- The research question itself is fuzzy.

## Context diet

- Extract facts from each source on T1 into a fixed schema (claim, quote, URL, date); synthesis reads only the fact table.
- Never paste whole PDFs into the synthesis step.
- Keep summaries anchored to sections so T3 can pull a raw passage only when needed.
- Haiku 5.5 reading long PDFs: split above 100k tokens to stay on the cheaper price band.

## Do it without a model (T0)

- De-duplicate URLs and sources with a script.
- Link checks and citation formatting with a reference manager or script.
- PDF to text with a converter before any model reads it.

## Briefing workers

Brief T1 extractors with the schema, 'quote verbatim', 'URL required', and 'NONE if not stated'.

In Claude Code, send T1 work to the `micro-worker` subagent, T2 to `standard-worker` and T3 reviews to `strong-reviewer`. In chat apps, print the plan and tell the user which model to switch to at each step.

## Anti-patterns

- Opus reading 40 sources one by one.
- Haiku writing the conclusion.
- Synthesis without a fact table, which makes claims untraceable.

## Example

Request: "Compare the top 6 EV charging networks in Germany on price, coverage and reliability."

```text
ROUTING PLAN
1. [T3] opus/medium    Define criteria, sub-questions, source list
2. [T1] haiku/low      Triage 60 search results to ~20 sources
3. [T1] haiku/low      Extract facts per source into schema (batch)
4. [T2] sonnet/medium  Build comparison table, mark gaps and conflicts
5. [T3] opus/high      Resolve conflicts, write conclusions
6. [T2] sonnet/medium  Write the brief from conclusions
7. [T0] script         Link check all citations
```
