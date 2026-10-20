#!/usr/bin/env python3
"""Generate persona SKILL.md files, routing.json and the README savings table
from data/personas/*.yaml and benchmarks/results.json.

  python3 benchmarks/calculate.py && python3 tools/build.py
"""
import glob, json, os, re
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "https://github.com/UtpalDasLabs/token-saver-skills"
MODEL = {"T0": "script / tool", "T1": "haiku", "T2": "sonnet", "T3": "opus", "T4": "fable"}
AGENT = {"T1": "micro-worker", "T2": "standard-worker", "T3": "strong-reviewer"}

results = {r["id"]: r for r in json.load(open(os.path.join(ROOT, "benchmarks/results.json")))["personas"]}
summary = json.load(open(os.path.join(ROOT, "benchmarks/results.json")))["summary"]


def budget(k):
    return f"≤{k:g}k" if k >= 1 else f"≤{int(k*1000)}"


def skill_md(p):
    r = results[p["name"]]
    rows = "\n".join(
        f"| {t['task']} | **{t['tier']}** {MODEL[t['tier']]} | {t['effort']} | {budget(t['routed_in_k'])} | {t['check']} | {t['escalate']} |"
        for t in sorted(p["tasks"], key=lambda t: t["tier"]))
    bullets = lambda xs: "\n".join(f"- {x}" for x in xs)
    plan = p["example"]["plan"].rstrip()
    return f'''---
name: {p["name"]}
description: "{p["description"]}"
license: MIT
compatibility: "Any Agent Skills host. Automatic model switching in Claude Code with the bundled subagents; elsewhere it outputs a routing plan to apply."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "1.0.0"
  extends: base-model-routing
  repo: "{REPO}"
  modeled-token-saving: "{r["token_saving_pct"]}%"
  modeled-cost-saving: "{r["cost_saving_pct"]}%"
  pricing-checked: "{summary["pricing_checked"]}"
---

# {p["title"]}

{p["purpose"]}

- **For:** {p["persona"]}
- **Win condition:** {p["win"]}
- **Modeled saving:** about {r["token_saving_pct"]}% fewer tokens and {r["cost_saving_pct"]}% lower cost than running everything on Opus 5.5 (pessimistic case: {r["conservative_token_saving_pct"]}% / {r["conservative_cost_saving_pct"]}%). [Method]({REPO}/blob/main/METHODOLOGY.md)

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
{rows}

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

{bullets(p["escalate_now"])}

## Context diet

{bullets(p["context_diet"])}

## Do it without a model (T0)

{bullets(p["tool_first"])}

## Briefing workers

{p["handoff_tip"]}

In Claude Code, send T1 work to the `micro-worker` subagent, T2 to `standard-worker` and T3 reviews to `strong-reviewer`. In chat apps, print the plan and tell the user which model to switch to at each step.

## Anti-patterns

{bullets(p["anti_patterns"])}

## Example

Request: "{p["example"]["request"]}"

```text
{plan}
```
'''


def main():
    routing = {"version": "1.0.0", "pricing_checked": summary["pricing_checked"],
               "tiers": {"T0": None, "T1": "claude-haiku-5-5", "T2": "claude-sonnet-5-5", "T3": "claude-opus-5-5", "T4": "claude-fable-5-1"},
               "personas": {}}
    for f in sorted(glob.glob(os.path.join(ROOT, "data/personas/*.yaml"))):
        p = yaml.safe_load(open(f))
        d = os.path.join(ROOT, "skills", p["name"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "SKILL.md"), "w").write(skill_md(p))
        routing["personas"][p["name"]] = [
            {"task": t["task"], "tier": t["tier"], "effort": t["effort"], "context_in_k": t["routed_in_k"],
             "check": t["check"], "escalate": t["escalate"]} for t in p["tasks"]]
    json.dump(routing, open(os.path.join(ROOT, "routing.json"), "w"), indent=2)

    # README savings table
    rows = ["| Skill | Who it's for | Tokens saved | Cost saved |", "|---|---|---:|---:|"]
    for r in sorted(results.values(), key=lambda r: -r["cost_saving_pct"]):
        p = yaml.safe_load(open(os.path.join(ROOT, "data/personas", r["id"].replace("-routing", "") + ".yaml")))
        rows.append(f"| [`{r['id']}`](skills/{r['id']}/SKILL.md) | {p['who']} | **{r['token_saving_pct']}%** | **{r['cost_saving_pct']}%** |")
    rows.append(f"| **Average** | {summary['personas']} personas | **{summary['avg_token_saving_pct']}%** | **{summary['avg_cost_saving_pct']}%** |")
    readme = os.path.join(ROOT, "README.md")
    if os.path.exists(readme):
        s = open(readme).read()
        s = re.sub(r"<!-- SAVINGS:START -->.*<!-- SAVINGS:END -->",
                   "<!-- SAVINGS:START -->\n" + "\n".join(rows) + "\n<!-- SAVINGS:END -->", s, flags=re.S)
        for k, v in {"AVG_TOKENS": summary["avg_token_saving_pct"], "AVG_COST": summary["avg_cost_saving_pct"],
                     "CONS_TOKENS": summary["conservative_avg_token_saving_pct"], "CONS_COST": summary["conservative_avg_cost_saving_pct"]}.items():
            s = re.sub(rf"<!-- {k} -->\d+%<!-- /{k} -->", f"<!-- {k} -->{v}%<!-- /{k} -->", s)
        open(readme, "w").write(s)
    print("built", len(routing["personas"]), "persona skills")


if __name__ == "__main__":
    main()
