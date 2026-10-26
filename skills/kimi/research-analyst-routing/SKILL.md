---
name: research-analyst-routing
description: "Model routing for research and analysis: which tier searches, reads, extracts, compares, fact-checks and synthesises sources into briefs or reports. Use for market research, literature reviews, due diligence or competitive analysis. Not for numeric data analysis in SQL or spreadsheets."
license: MIT
compatibility: "Agent Skills format. Packaged for Kimi: Kimi Code, Kimi API. Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "kimi"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
  modeled-token-saving: "33%"
  modeled-cost-saving: "28%"
  pricing-checked: "2026-10-26"
---

# Research analyst routing (Kimi)

Read wide on cheap tiers, think deep on strong ones. Kimi K3.1 Pro (low effort) extracts, Kimi K3.1 Pro compiles, Kimi K3.1 Pro concludes.

- **For:** Analysts, consultants, journalists, students and operators who search, read, compare and synthesise many sources.
- **Win condition:** Sourced, trustworthy conclusions at a fraction of the cost of reading everything with the top model.
- **Modeled saving on Kimi:** about 28% lower cost and 33% fewer tokens than running everything on Kimi K3.1 Pro (pessimistic case: 3% / 6%). [Method](https://github.com/UtpalDasLabs/token-saver-automated-model-picker/blob/main/METHODOLOGY.md)

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
| Citation formatting and link checks | **T0** script / tool | - | ≤1.5k | All URLs return 200 | Never |
| Extract facts from each source | **T1** Kimi K3.1 Pro (low effort) | low | ≤12k | Each fact has quote + URL | Paywalled, scanned or contradictory source -> T2 |
| Relevance triage of search results | **T1** Kimi K3.1 Pro (low effort) | low | ≤6k | Keep/drop with one reason | Never |
| Summarise long reports or papers | **T1** Kimi K3.1 Pro (low effort) | high | ≤50k | 300 words, section anchors | Technical depth needed -> T2 |
| Compile comparison table | **T2** Kimi K3.1 Pro | high | ≤15k | Every cell sourced, gaps marked | Sources conflict -> T3 |
| Write the final brief from the synthesis | **T2** Kimi K3.1 Pro | high | ≤10k | Matches outline, citations intact | Never |
| Translate a foreign-language source | **T2** Kimi K3.1 Pro | low | ≤10k | Names, numbers unchanged | Legal text -> T3 |
| Frame the research question and plan | **T3** Kimi K3.1 Pro | high | ≤5k | Sub-questions + source types | Never above T3 |
| Synthesis and conclusions | **T3** Kimi K3.1 Pro | max | ≤20k | Claims trace to extracted facts | High-stakes decision -> T4 second read |
| Fact-check key claims | **T3** Kimi K3.1 Pro | high | ≤10k | Verdict + source per claim | Never above T3 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Claims that will be published, given to investors or used for legal, medical or financial decisions.
- Sources that directly contradict each other on a key number.
- The research question itself is fuzzy.

## Context diet

- Extract facts from each source on T1 into a fixed schema (claim, quote, URL, date); synthesis reads only the fact table.
- Never paste whole PDFs into the synthesis step.
- Keep summaries anchored to sections so T3 can pull a raw passage only when needed.
- Kimi K3.1 Pro (low effort) 5.5 reading long PDFs: split above 100k tokens to stay on the cheaper price band.
- Kimi has no supported cheaper micro model. Use T0 scripts, low effort and tight context for savings; do not use retired K2 models.

## Do it without a model (T0)

- De-duplicate URLs and sources with a script.
- Link checks and citation formatting with a reference manager or script.
- PDF to text with a converter before any model reads it.

## Briefing workers

Brief T1 extractors with the schema, 'quote verbatim', 'URL required', and 'NONE if not stated'.

In Kimi Code, print the routing plan and use `/model` to select K3.1 Pro with the listed effort before each step. `/secondary-model` sets one default for subagents, but custom agents cannot pin different models; do not claim automatic per-tier switching. On the Kimi API, set `model` and `reasoning_effort` per request from the routing table.

## Anti-patterns

- Kimi K3.1 Pro reading 40 sources one by one.
- Kimi K3.1 Pro (low effort) writing the conclusion.
- Synthesis without a fact table, which makes claims untraceable.

## Example

Request: "Compare the top 6 EV charging networks in Germany on price, coverage and reliability."

```text
ROUTING PLAN
1. [T3] k3.1-pro/high          Define criteria, sub-questions, source list
2. [T1] k3.1-pro/low           Triage 60 search results to ~20 sources
3. [T1] k3.1-pro/low           Extract facts per source into schema (batch)
4. [T2] k3.1-pro/high          Build comparison table, mark gaps and conflicts
5. [T3] k3.1-pro/max           Resolve conflicts, write conclusions
6. [T2] k3.1-pro/high          Write the brief from conclusions
7. [T0] script                 Link check all citations
```
