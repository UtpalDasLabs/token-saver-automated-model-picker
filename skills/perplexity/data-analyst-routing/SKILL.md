---
name: data-analyst-routing
description: "Model routing for data analysis: which tier writes SQL, pandas or spreadsheet formulas, cleans data, builds charts and dashboards, explains anomalies and writes insight summaries. Use for querying, analysing or reporting on data. Not for qualitative research synthesis."
license: MIT
compatibility: "Agent Skills format. Packaged for Perplexity: Perplexity Computer, Perplexity Agent API. Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "perplexity"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
  modeled-token-saving: "79%"
  modeled-cost-saving: "87%"
  pricing-checked: "2026-10-20"
---

# Data analyst routing (Perplexity)

Let the database and code do the maths. Models write queries, explain results and decide what matters; Claude Opus 5.5 only for the interpretation and tricky modelling.

- **For:** Data and BI analysts, analytics engineers and spreadsheet power users writing SQL, notebooks, dashboards and reports.
- **Win condition:** Correct numbers, explained clearly, with model spend that does not scale with table size.
- **Modeled saving on Perplexity:** about 87% lower cost and 79% fewer tokens than running everything on Claude Opus 5.5 (pessimistic case: 76% / 32%). [Method](https://github.com/UtpalDasLabs/token-saver-automated-model-picker/blob/main/METHODOLOGY.md)

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
| Run transforms and aggregations | **T0** script / tool | - | ≤1.5k | Code output | Never: models never do arithmetic on raw rows |
| Classify free-text fields | **T1** GPT-6 Luna | low | ≤10k | Label set only, UNSURE allowed | UNSURE above 10% -> T2 |
| Document a table or query | **T1** GPT-6 Luna | low | ≤3k | Column-by-column template | Never |
| Write SQL from a clear question | **T2** Gemini 3.8 Flash | low | ≤5k | Query runs, row counts sane | Wrong twice or complex joins -> T3 |
| Data cleaning script | **T2** Gemini 3.8 Flash | low | ≤5k | Assertions on nulls, types, counts | Never |
| Chart and dashboard code | **T2** Gemini 3.8 Flash | low | ≤5k | Renders, axes labelled | Never |
| Weekly KPI report text | **T2** Gemini 3.8 Flash | low | ≤4k | Numbers match query output | Big swing -> T3 |
| Frame the analysis and metric definitions | **T3** Claude Opus 5.5 | medium | ≤8k | Question, metric formulas, cuts | Never above T3 |
| Debug a wrong number | **T3** Claude Opus 5.5 | medium | ≤12k | Reconciles to a trusted total | Never above T3 |
| Explain results and write insights | **T3** Claude Opus 5.5 | medium | ≤6k | Each insight cites a number | Never above T3 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Numbers going to executives, investors, regulators or customers.
- A metric definition change.
- Results that contradict a trusted dashboard.

## Context diet

- Send the schema (table, column, type) and 5 sample rows, never full tables.
- Pass aggregated results to the insight step, not raw rows.
- Keep a stable metrics dictionary as the first block of every brief.
- Web search and fetch tool calls are billed on top of tokens; search once, then reuse the results.

## Do it without a model (T0)

- All arithmetic, joins, counts and aggregations in SQL, pandas or the spreadsheet.
- Profiling (nulls, distinct counts, ranges) with a profiling query.
- Chart rendering with code, not a model describing a chart.

## Briefing workers

Brief T2 with the schema, the metric definition, the expected grain and 'SQL only, then the row count'.

In Perplexity Computer, write the tier and model into each step of the plan and keep cheap steps on small context or scripts. On the Agent API, set `model` per request from the routing table.

## Anti-patterns

- Pasting 10,000 rows into a model and asking for the average.
- Claude Opus 5.5 writing a simple SELECT.
- Insights without the numbers they rest on.

## Example

Request: "Why did conversion drop last week? Give me a short explanation for the leadership channel."

```text
ROUTING PLAN
1. [T3] opus/medium            Define conversion precisely + the cuts to check
2. [T2] gemini-flash/low       SQL for funnel by day, device, channel, country
3. [T0] database               Run queries
4. [T3] opus/medium            Find the driver; reconcile to the dashboard total
5. [T2] gemini-flash/low       Chart code for the driver
6. [T3] opus/medium            150-word explanation for leadership (high-stakes-review)
```
