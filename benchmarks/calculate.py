#!/usr/bin/env python3
"""Token and cost savings calculator for token-saver-skills.

Compares, per persona workload, a baseline (every task on Opus 5.5, medium effort,
full context) with the routed plan defined in data/personas/*.yaml, including
failure retries, escalations, delegation overhead and the cost of loading the skill.

Usage:
  python3 benchmarks/calculate.py            # print table, write results files
  python3 benchmarks/calculate.py --json     # print JSON only
"""
import json, sys, glob, os
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEXT = {"T0": "T1", "T1": "T2", "T2": "T3", "T3": "T4", "T4": "T4"}


def load(p):
    with open(os.path.join(ROOT, p)) as f:
        return yaml.safe_load(f)


PRICING = load("benchmarks/pricing.yaml")
A = load("benchmarks/assumptions.yaml")


def call_cost(model, in_k, out_k):
    m = PRICING["models"][model]
    pin, pout = m["input"], m["output"]
    if "long_prompt_k" in m and in_k > m["long_prompt_k"]:
        pin, pout = m["long_input"], m["long_output"]
    return (in_k * pin + out_k * pout) / 1000.0  # k tokens * $/MTok / 1000 = $


def attempt(tier, effort, in_k, out_k):
    model = PRICING["tiers"][tier]
    o = out_k * A["effort_output_multiplier"][str(effort)] * A["verbosity_multiplier"][tier]
    return call_cost(model, in_k, o), in_k + o


def conservative(p):
    """Pessimistic scenario: failure rates doubled, half the context-diet benefit, wordier small models."""
    q = dict(p); q["tasks"] = []
    for t in p["tasks"]:
        t = dict(t)
        t["p_fail"] = min(1.0, t["p_fail"] * 2)
        t["routed_in_k"] = t["routed_in_k"] + 0.5 * (t["base_in_k"] - t["routed_in_k"])
        if t["tier"] in ("T1", "T2"):
            t["out_k"] = t["out_k"] * 1.1
        q["tasks"].append(t)
    return q


def persona_result(p):
    base_model, base_eff = A["baseline"]["model"], A["baseline"]["effort"]
    rows, b_cost, b_tok, r_cost, r_tok = [], 0.0, 0.0, 0.0, 0.0
    ov = A["delegation_overhead_per_task_k"]
    for t in p["tasks"]:
        n = t["per_week"]
        # baseline
        bo = t["out_k"] * A["effort_output_multiplier"][base_eff]
        bc = call_cost(base_model, t["base_in_k"], bo)
        bt = t["base_in_k"] + bo
        # routed: first attempt + expected escalation
        c1, k1 = attempt(t["tier"], t["effort"], t["routed_in_k"], t["out_k"])
        c2, k2 = attempt(NEXT[t["tier"]], "medium", t["routed_in_k"] + A["escalation_extra_input_k"], t["out_k"])
        rc, rt = c1 + t["p_fail"] * c2, k1 + t["p_fail"] * k2
        if t["tier"] in ("T0", "T1", "T2"):
            rc += call_cost("opus", ov["input"], ov["output"])
            rt += ov["input"] + ov["output"]
        rows.append({"task": t["task"], "tier": t["tier"], "per_week": n,
                     "baseline_cost": bc * n, "routed_cost": rc * n,
                     "baseline_tokens_k": bt * n, "routed_tokens_k": rt * n})
        b_cost += bc * n; b_tok += bt * n; r_cost += rc * n; r_tok += rt * n
    s = p.get("sessions_per_week", 10) * A["skill_load_input_k_per_session"]
    r_cost += call_cost("opus", s, 0); r_tok += s
    # comparison: everything on Sonnet, full context
    sonnet_all = sum(call_cost("sonnet", t["base_in_k"], t["out_k"]) * t["per_week"] for t in p["tasks"])
    mix = {}
    for t in p["tasks"]:
        mix[t["tier"]] = mix.get(t["tier"], 0) + t["per_week"]
    total_n = sum(mix.values())
    return {
        "id": p["name"], "title": p["title"],
        "tasks_per_week": round(total_n, 1),
        "tier_mix_pct": {k: round(100 * v / total_n) for k, v in sorted(mix.items())},
        "baseline_usd_week": round(b_cost, 2), "routed_usd_week": round(r_cost, 2),
        "baseline_tokens_m_week": round(b_tok / 1000, 2), "routed_tokens_m_week": round(r_tok / 1000, 2),
        "cost_saving_pct": round(100 * (1 - r_cost / b_cost)),
        "token_saving_pct": round(100 * (1 - r_tok / b_tok)),
        "vs_all_sonnet_cost_saving_pct": round(100 * (1 - r_cost / sonnet_all)),
        "rows": rows,
    }


def run():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "data/personas/*.yaml"))):
        with open(f) as fh:
            p = yaml.safe_load(fh)
        r = persona_result(p)
        c = persona_result(conservative(p))
        r["conservative_cost_saving_pct"] = c["cost_saving_pct"]
        r["conservative_token_saving_pct"] = c["token_saving_pct"]
        out.append(r)
    avg = lambda k: round(sum(r[k] for r in out) / len(out))
    summary = {"pricing_checked": PRICING["checked"], "pricing_source": PRICING["source"],
               "personas": len(out), "avg_token_saving_pct": avg("token_saving_pct"),
               "avg_cost_saving_pct": avg("cost_saving_pct"),
               "conservative_avg_token_saving_pct": avg("conservative_token_saving_pct"),
               "conservative_avg_cost_saving_pct": avg("conservative_cost_saving_pct"),
               "range_cost_saving_pct": [min(r["cost_saving_pct"] for r in out), max(r["cost_saving_pct"] for r in out)],
               "range_token_saving_pct": [min(r["token_saving_pct"] for r in out), max(r["token_saving_pct"] for r in out)]}
    return summary, out


def write(summary, out):
    with open(os.path.join(ROOT, "benchmarks/results.json"), "w") as f:
        json.dump({"summary": summary, "personas": [{k: v for k, v in r.items() if k != "rows"} for r in out]}, f, indent=2)
    lines = ["# Modeled savings by persona", "",
             f"Pricing checked {summary['pricing_checked']} ([source]({summary['pricing_source']})). "
             "Baseline: every task on Opus 5.5 at medium effort with full context. "
             "Generated by `benchmarks/calculate.py`; do not edit by hand.", "",
             "| Persona | Tasks/wk | Tokens saved | Cost saved | Pessimistic (tokens / cost) | Baseline $/wk | Routed $/wk | Saved vs. all-Sonnet |",
             "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for r in sorted(out, key=lambda r: -r["cost_saving_pct"]):
        lines.append(f"| {r['title']} | {r['tasks_per_week']:g} | {r['token_saving_pct']}% | {r['cost_saving_pct']}% | "
                     f"{r['conservative_token_saving_pct']}% / {r['conservative_cost_saving_pct']}% | "
                     f"${r['baseline_usd_week']:.2f} | ${r['routed_usd_week']:.2f} | {r['vs_all_sonnet_cost_saving_pct']}% |")
    lines += ["", f"**Average across {summary['personas']} personas: {summary['avg_token_saving_pct']}% fewer tokens, "
              f"{summary['avg_cost_saving_pct']}% lower cost.** "
              f"Pessimistic scenario (failure rates doubled, half the context savings): "
              f"{summary['conservative_avg_token_saving_pct']}% fewer tokens, {summary['conservative_avg_cost_saving_pct']}% lower cost.", ""]
    for r in out:
        lines += [f"## {r['title']}", "", "| Task | Tier | Per wk | Baseline $ | Routed $ | Baseline k tok | Routed k tok |", "|---|---|---:|---:|---:|---:|---:|"]
        for x in r["rows"]:
            lines.append(f"| {x['task']} | {x['tier']} | {x['per_week']:g} | {x['baseline_cost']:.3f} | {x['routed_cost']:.3f} | {x['baseline_tokens_k']:.0f} | {x['routed_tokens_k']:.0f} |")
        lines.append("")
    with open(os.path.join(ROOT, "benchmarks/RESULTS.md"), "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    summary, out = run()
    if "--json" in sys.argv:
        print(json.dumps(summary, indent=2)); sys.exit()
    write(summary, out)
    for r in sorted(out, key=lambda r: -r["cost_saving_pct"]):
        print(f"{r['title']:<36} tokens -{r['token_saving_pct']:>3}%   cost -{r['cost_saving_pct']:>3}%   "
              f"${r['baseline_usd_week']:>7.2f} -> ${r['routed_usd_week']:>6.2f}/wk   pessimistic -{r['conservative_token_saving_pct']}%/-{r['conservative_cost_saving_pct']}%   mix {r['tier_mix_pct']}")
    print(f"\nAVERAGE tokens -{summary['avg_token_saving_pct']}%  cost -{summary['avg_cost_saving_pct']}%  | pessimistic tokens -{summary['conservative_avg_token_saving_pct']}% cost -{summary['conservative_avg_cost_saving_pct']}%")
