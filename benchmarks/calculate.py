#!/usr/bin/env python3
"""Token and cost savings calculator: every persona x every platform.

Baseline: every task on the platform's strong everyday model (tier T3) at medium
effort with full context. Routed: the plan in data/personas/*.yaml, mapped to the
platform's models in data/platforms/*.yaml, including failed attempts, escalations,
delegation overhead and the cost of loading the skill.

  python3 benchmarks/calculate.py           # print summary, write results files
"""
import glob, json, os, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEXT = {"T0": "T1", "T1": "T2", "T2": "T3", "T3": "T4", "T4": "T4"}
A = yaml.safe_load(open(os.path.join(ROOT, "benchmarks/assumptions.yaml")))


def load_dir(d):
    return [yaml.safe_load(open(f)) for f in sorted(glob.glob(os.path.join(ROOT, d, "*.yaml")))]


PLATFORMS = sorted(load_dir("data/platforms"), key=lambda p: p["order"])
PERSONAS = load_dir("data/personas")


def price_band(tier, in_k):
    for band in tier["prices"]:
        if band["upto_k"] is None or in_k <= band["upto_k"]:
            return band
    return tier["prices"][-1]


def call(pl, tier_id, in_k, out_k):
    t = pl["tiers"]["T1" if tier_id == "T0" else tier_id]
    b = price_band(t, in_k)
    return (in_k * b["input"] + out_k * b["output"]) / 1000.0


def attempt(pl, tier_id, effort, in_k, out_k):
    t = pl["tiers"]["T1" if tier_id == "T0" else tier_id]
    eff = t.get("force_effort", effort) if tier_id != "T0" else "-"
    base_model = pl["tiers"][pl["baseline_tier"]]["model"]
    verb = A["verbosity_multiplier"][tier_id] if t["model"] != base_model else 1.0
    o = out_k * A["effort_output_multiplier"][str(eff)] * verb
    return call(pl, tier_id, in_k, o), in_k + o


def persona_result(pl, p):
    bt_id, b_eff = pl["baseline_tier"], pl["baseline_effort"]
    ov = A["delegation_overhead_per_task_k"]
    bc = bt = rc = rt = 0.0
    rows = []
    for t in p["tasks"]:
        n = t["per_week"]
        bo = t["out_k"] * A["effort_output_multiplier"][b_eff]
        c0, k0 = call(pl, bt_id, t["base_in_k"], bo), t["base_in_k"] + bo
        c1, k1 = attempt(pl, t["tier"], t["effort"], t["routed_in_k"], t["out_k"])
        c2, k2 = attempt(pl, NEXT[t["tier"]], "medium", t["routed_in_k"] + A["escalation_extra_input_k"], t["out_k"])
        c, k = c1 + t["p_fail"] * c2, k1 + t["p_fail"] * k2
        if t["tier"] in ("T0", "T1", "T2"):
            c += call(pl, bt_id, ov["input"], ov["output"]); k += ov["input"] + ov["output"]
        rows.append({"task": t["task"], "tier": t["tier"], "per_week": n, "baseline_cost": c0 * n,
                     "routed_cost": c * n, "baseline_tokens_k": k0 * n, "routed_tokens_k": k * n})
        bc += c0 * n; bt += k0 * n; rc += c * n; rt += k * n
    s = p.get("sessions_per_week", 10) * A["skill_load_input_k_per_session"]
    rc += call(pl, bt_id, s, 0); rt += s
    return {"cost_saving_pct": round(100 * (1 - rc / bc)), "token_saving_pct": round(100 * (1 - rt / bt)),
            "baseline_usd_week": round(bc, 2), "routed_usd_week": round(rc, 2),
            "baseline_tokens_m_week": round(bt / 1000, 2), "routed_tokens_m_week": round(rt / 1000, 2), "rows": rows}


def conservative(p):
    q = dict(p); q["tasks"] = []
    for t in p["tasks"]:
        t = dict(t)
        t["p_fail"] = min(1.0, t["p_fail"] * 2)
        t["routed_in_k"] = t["routed_in_k"] + 0.5 * (t["base_in_k"] - t["routed_in_k"])
        if t["tier"] in ("T1", "T2"):
            t["out_k"] *= 1.1
        q["tasks"].append(t)
    return q


def run():
    res, summ = {}, {}
    for pl in PLATFORMS:
        res[pl["id"]] = {}
        for p in PERSONAS:
            r = persona_result(pl, p)
            c = persona_result(pl, conservative(p))
            r["conservative_cost_saving_pct"] = c["cost_saving_pct"]
            r["conservative_token_saving_pct"] = c["token_saving_pct"]
            res[pl["id"]][p["name"]] = r
        vals = list(res[pl["id"]].values())
        avg = lambda k: round(sum(v[k] for v in vals) / len(vals))
        summ[pl["id"]] = {"name": pl["name"], "checked": pl["checked"], "source": pl["source"],
                          "baseline_model": pl["tiers"][pl["baseline_tier"]]["label"],
                          "avg_cost_saving_pct": avg("cost_saving_pct"), "avg_token_saving_pct": avg("token_saving_pct"),
                          "conservative_avg_cost_saving_pct": avg("conservative_cost_saving_pct"),
                          "conservative_avg_token_saving_pct": avg("conservative_token_saving_pct")}
    allv = [v for d in res.values() for v in d.values()]
    g = lambda k: round(sum(v[k] for v in allv) / len(allv))
    overall = {"platforms": len(PLATFORMS), "personas": len(PERSONAS),
               "avg_cost_saving_pct": g("cost_saving_pct"), "avg_token_saving_pct": g("token_saving_pct"),
               "conservative_avg_cost_saving_pct": g("conservative_cost_saving_pct"),
               "conservative_avg_token_saving_pct": g("conservative_token_saving_pct"),
               "range_cost_saving_pct": [min(v["cost_saving_pct"] for v in allv), max(v["cost_saving_pct"] for v in allv)]}
    return overall, summ, res


def write(overall, summ, res):
    titles = {p["name"]: p["title"].replace(" routing", "") for p in PERSONAS}
    slim = {pid: {k: {kk: vv for kk, vv in v.items() if kk != "rows"} for k, v in d.items()} for pid, d in res.items()}
    json.dump({"overall": overall, "platforms": summ, "results": slim}, open(os.path.join(ROOT, "benchmarks/results.json"), "w"), indent=2)
    L = ["# Modeled savings: every persona on every platform", "",
         "Generated by `benchmarks/calculate.py`; do not edit by hand. Baseline per platform: every task on its T3 model at medium effort with full context. "
         "Cells show **cost saved / tokens saved**.", ""]
    ids = [pl["id"] for pl in PLATFORMS]
    L.append("| Persona | " + " | ".join(summ[i]["name"] for i in ids) + " |")
    L.append("|---|" + "---:|" * len(ids))
    for p in sorted(PERSONAS, key=lambda p: titles[p["name"]]):
        L.append(f"| {titles[p['name']]} | " + " | ".join(f"{res[i][p['name']]['cost_saving_pct']}% / {res[i][p['name']]['token_saving_pct']}%" for i in ids) + " |")
    L.append("| **Average** | " + " | ".join(f"**{summ[i]['avg_cost_saving_pct']}% / {summ[i]['avg_token_saving_pct']}%**" for i in ids) + " |")
    L.append("| Pessimistic | " + " | ".join(f"{summ[i]['conservative_avg_cost_saving_pct']}% / {summ[i]['conservative_avg_token_saving_pct']}%" for i in ids) + " |")
    L += ["", "Baseline models: " + "; ".join(f"{summ[i]['name']}: {summ[i]['baseline_model']} ([prices]({summ[i]['source']}), checked {summ[i]['checked']})" for i in ids) + ".", ""]
    for pl in PLATFORMS:
        L += [f"## {pl['name']}: task by task", ""]
        for p in PERSONAS:
            r = res[pl["id"]][p["name"]]
            L += [f"### {titles[p['name']]} — {r['cost_saving_pct']}% cost, {r['token_saving_pct']}% tokens", "",
                  "| Task | Tier | Per wk | Baseline $ | Routed $ | Baseline k tok | Routed k tok |", "|---|---|---:|---:|---:|---:|---:|"]
            for x in r["rows"]:
                L.append(f"| {x['task']} | {x['tier']} | {x['per_week']:g} | {x['baseline_cost']:.3f} | {x['routed_cost']:.3f} | {x['baseline_tokens_k']:.0f} | {x['routed_tokens_k']:.0f} |")
            L.append("")
    open(os.path.join(ROOT, "benchmarks/RESULTS.md"), "w").write("\n".join(L))


if __name__ == "__main__":
    overall, summ, res = run()
    write(overall, summ, res)
    for i, s in summ.items():
        print(f"{s['name']:<11} cost -{s['avg_cost_saving_pct']:>3}%  tokens -{s['avg_token_saving_pct']:>3}%  | pessimistic -{s['conservative_avg_cost_saving_pct']}% / -{s['conservative_avg_token_saving_pct']}%  baseline {s['baseline_model']}")
    print("OVERALL", json.dumps(overall))
