---
name: research-analyst-routing
description: "Model routing for research and analysis: which tier searches, reads, extracts, compares, fact-checks and synthesises sources into briefs or reports. Use for market research, literature reviews, due diligence or competitive analysis. Not for numeric data analysis in SQL or spreadsheets."
license: MIT
compatibility: "Agent Skills format. Packaged for Qwen: Qwen Code, Model Studio API. Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "qwen"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
  modeled-token-saving: "33%"
  modeled-cost-saving: "85%"
  pricing-checked: "2026-10-20"
---

# Research analyst routing (Qwen)

Read wide on cheap tiers, think deep on strong ones. Qwen3.7-Flash extracts, Qwen3.7-Plus compiles, Qwen3.8-Max concludes.

- **For:** Analysts, consultants, journalists, students and operators who search, read, compare and synthesise many sources.
- **Win condition:** Sourced, trustworthy conclusions at a fraction of the cost of reading everything with the top model.
- **Modeled saving on Qwen:** about 85% lower cost and 33% fewer tokens than running everything on Qwen3.8-Max (pessimistic case: 77% / 5%). [Method](https://github.com/UtpalDasLabs/token-saver-automated-model-picker/blob/main/METHODOLOGY.md)

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
| Citation formatting and link checks | **T0** script / tool | - | ≤1.5k | All URLs return 200 | Never |
| Extract facts from each source | **T1** Qwen3.7-Flash | low | ≤12k | Each fact has quote + URL | Paywalled, scanned or contradictory source -> T2 |
| Relevance triage of search results | **T1** Qwen3.7-Flash | low | ≤6k | Keep/drop with one reason | Never |
| Summarise long reports or papers | **T1** Qwen3.7-Flash | medium | ≤50k | 300 words, section anchors | Technical depth needed -> T2 |
| Compile comparison table | **T2** Qwen3.7-Plus | medium | ≤15k | Every cell sourced, gaps marked | Sources conflict -> T3 |
| Write the final brief from the synthesis | **T2** Qwen3.7-Plus | medium | ≤10k | Matches outline, citations intact | Never |
| Translate a foreign-language source | **T2** Qwen3.7-Plus | low | ≤10k | Names, numbers unchanged | Legal text -> T3 |
| Frame the research question and plan | **T3** Qwen3.8-Max | medium | ≤5k | Sub-questions + source types | Never above T3 |
| Synthesis and conclusions | **T3** Qwen3.8-Max | high | ≤20k | Claims trace to extracted facts | High-stakes decision -> T4 second read |
| Fact-check key claims | **T3** Qwen3.8-Max | medium | ≤10k | Verdict + source per claim | Never above T3 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Claims that will be published, given to investors or used for legal, medical or financial decisions.
- Sources that directly contradict each other on a key number.
- The research question itself is fuzzy.

## Context diet

- Extract facts from each source on T1 into a fixed schema (claim, quote, URL, date); synthesis reads only the fact table.
- Never paste whole PDFs into the synthesis step.
- Keep summaries anchored to sections so T3 can pull a raw passage only when needed.
- Qwen3.7-Flash 5.5 reading long PDFs: split above 100k tokens to stay on the cheaper price band.
- Qwen3.7-Flash costs about 3x more per token above 32k input tokens. Keep T1 prompts under 32k.

## Do it without a model (T0)

- De-duplicate URLs and sources with a script.
- Link checks and citation formatting with a reference manager or script.
- PDF to text with a converter before any model reads it.

## Briefing workers

Brief T1 extractors with the schema, 'quote verbatim', 'URL required', and 'NONE if not stated'.

In Qwen Code, send T1 work to the `micro-worker` agent, T2 to `standard-worker` and T3 reviews to `strong-reviewer`; each one is pinned to the right Qwen model. Anywhere else, print the routing plan and tell the user which model to use at each step.

## Anti-patterns

- Qwen3.8-Max reading 40 sources one by one.
- Qwen3.7-Flash writing the conclusion.
- Synthesis without a fact table, which makes claims untraceable.

## Example

Request: "Compare the top 6 EV charging networks in Germany on price, coverage and reliability."

```text
ROUTING PLAN
1. [T3] max/medium             Define criteria, sub-questions, source list
2. [T1] flash/low              Triage 60 search results to ~20 sources
3. [T1] flash/low              Extract facts per source into schema (batch)
4. [T2] plus/medium            Build comparison table, mark gaps and conflicts
5. [T3] max/high               Resolve conflicts, write conclusions
6. [T2] plus/medium            Write the brief from conclusions
7. [T0] script                 Link check all citations
```
