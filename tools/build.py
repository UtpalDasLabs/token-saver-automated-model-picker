#!/usr/bin/env python3
"""Generate every platform package from data/ and templates/.

  python3 benchmarks/calculate.py && python3 tools/build.py

Writes: skills/<platform>/<skill>/, agents/<platform>/, platforms/<platform>/README.md,
dist/<platform>/*.zip, dist/perplexity/plugin/, routing.json, README.md, docs/savings.svg
"""
import glob, json, os, re, shutil, zipfile
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
NAME = "Token Saver: Automating the Model Picker"
SITE = "https://utpaldas.com/labs/token-saver"
J = lambda *a: os.path.join(ROOT, *a)
R = json.load(open(J("benchmarks/results.json")))
PLATFORMS = sorted([yaml.safe_load(open(f)) for f in glob.glob(J("data/platforms/*.yaml"))], key=lambda p: p["order"])
PERSONAS = sorted([yaml.safe_load(open(f)) for f in glob.glob(J("data/personas/*.yaml"))], key=lambda p: p["title"])
OVERLAYS = ["cheap-batch-mode", "judge-best-output", "high-stakes-review", "context-diet"]
USE = {"T0": "Rename, dedupe, link check, format, count, convert, validate",
       "T1": "Classify, extract, tag, short rewrite, summarise logs, check one rule",
       "T2": "Routine production from a clear spec: code to spec, drafts, variants, tables",
       "T3": "Ambiguity, judgement, architecture, strategy, final review, choosing the winner",
       "T4": "Rare. High stakes and T3 at `high` already failed, or very long-horizon work"}
WORKERS = {"T1": ("micro-worker", "low"), "T2": ("standard-worker", "medium"), "T3": ("strong-reviewer", "high")}


def blended(t):
    b = t["prices"][0]
    return 3 * b["input"] + b["output"]


def ratio(pl, tid):
    if tid == "T0":
        return "~0"
    r = blended(pl["tiers"][tid]) / blended(pl["tiers"][pl["baseline_tier"]])
    same = pl["tiers"][tid]["model"] == pl["tiers"][pl["baseline_tier"]]["model"]
    if abs(r - 1) < 0.01:
        return "1x" + (" (same model)" if tid != pl["baseline_tier"] and same else "")
    if r < 1:
        n = 1 / r
        return f"~1/{n:.0f}" if n >= 3 else f"~{r:.2f}x"
    return f"~{r:.1f}x"


def subs(pl):
    T = pl["tiers"]
    d = {f"T{i}S": T[f"T{i}"]["label"] for i in range(1, 5)}
    d.update({"PLATFORM": pl["name"], "PLATFORM_ID": pl["id"], "PRODUCT": pl["product"], "REPO": REPO,
              "CHECKED": pl["checked"], "CONTEXT_RULE": pl["context_rule"]})
    d["COMPAT"] = f"Agent Skills format. Packaged for {pl['name']}: " + ", ".join(t["name"] for t in pl["tools"]) + \
                  ". Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
    if T["T4"]["model"] == T["T3"]["model"]:
        d["T4_COST"] = "same per-token price as T3, but maximum effort uses far more output tokens"
    else:
        d["T4_COST"] = f"about {blended(T['T4']) / blended(T['T3']):.1f}x {T['T3']['label']} pricing"
    rows = ["| Tier | Runs on | Use for | Price vs. T3 |", "|---|---|---|---|",
            f"| T0 Tool | No model: shell, script, formula, regex, linter | {USE['T0']} | ~0 |"]
    names = {"T1": "Micro", "T2": "Standard", "T3": "Strong", "T4": "Frontier"}
    for tid in ["T1", "T2", "T3", "T4"]:
        t = T[tid]
        rows.append(f"| {tid} {names[tid]} | {t['label']} (`{t['model']}`) | {USE[tid]} | {ratio(pl, tid)} |")
    d["TIER_TABLE"] = "\n".join(rows)
    d["HOSTS"] = "\n".join(f"- **{t['name']}**{' (automatic model switching)' if t.get('agents_dir') else ''}: {t['how']} [Docs]({t['doc']})" for t in pl["tools"])
    for i, eff in [(1, "low"), (2, "medium"), (3, "medium")]:
        lab = f"{T[f'T{i}']['short']}/{eff}"
        d[f"PAD{i}"] = " " * max(2, 22 - len(lab))
    d["T1S_SHORT"] = T["T1"]["short"]
    return d


def fill(s, d):
    for k, v in d.items():
        s = s.replace("{{" + k + "}}", str(v))
    left = re.findall(r"\{\{[A-Z0-9_]+\}\}", s)
    assert not left, left
    return s


def prose(s, pl):
    for i in range(1, 5):
        s = s.replace("{T%d}" % i, pl["tiers"][f"T{i}"]["label"])
    return s


def plan(text, pl):
    out = []
    for line in text.rstrip().split("\n"):
        m = re.match(r"^(\s*\d+\.\s+\[(T\d)\])\s+(\S+)\s+(.*)$", line)
        if m and "/" in m.group(3):
            lab = f"{pl['tiers'][m.group(2)]['short']}/{m.group(3).split('/')[1]}"
            line = f"{m.group(1)} {lab.ljust(22)} {m.group(4)}"
        elif m:
            line = f"{m.group(1)} {m.group(3).ljust(22)} {m.group(4)}"
        out.append(line)
    return "\n".join(out)


def delegate_line(pl):
    auto = [t for t in pl["tools"] if t.get("agents_dir")]
    if auto:
        tools = " or ".join(t["name"] for t in auto)
        return (f"In {tools}, send T1 work to the `micro-worker` agent, T2 to `standard-worker` and T3 reviews to `strong-reviewer`; "
                f"each one is pinned to the right {pl['name']} model. Anywhere else, print the routing plan and tell the user which model to use at each step.")
    return ("In Perplexity Computer, write the tier and model into each step of the plan and keep cheap steps on small context or scripts. "
            "On the Agent API, set `model` per request from the routing table.")


def persona_md(p, pl, d):
    r = R["results"][pl["id"]][p["name"]]
    T = pl["tiers"]
    lab = lambda tid: "script / tool" if tid == "T0" else T[tid]["label"]
    budget = lambda k: f"≤{k:g}k"
    rows = "\n".join(f"| {t['task']} | **{t['tier']}** {lab(t['tier'])} | {T[t['tier']].get('force_effort', t['effort']) if t['tier'] != 'T0' else '-'} | {budget(t['routed_in_k'])} | {t['check']} | {prose(t['escalate'], pl)} |"
                     for t in sorted(p["tasks"], key=lambda t: t["tier"]))
    bl = lambda xs: "\n".join(f"- {prose(x, pl)}" for x in xs)
    tiers_line = " · ".join(f"**{tid}** {lab(tid) if tid != 'T0' else 'tool'}" for tid in ["T0", "T1", "T2", "T3", "T4"])
    return f'''---
name: {p["name"]}
description: "{p["description"]}"
license: MIT
compatibility: "{d["COMPAT"]}"
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "{pl["id"]}"
  extends: base-model-routing
  repo: "{REPO}"
  modeled-token-saving: "{r["token_saving_pct"]}%"
  modeled-cost-saving: "{r["cost_saving_pct"]}%"
  pricing-checked: "{pl["checked"]}"
---

# {p["title"]} ({pl["name"]})

{prose(p["purpose"], pl)}

- **For:** {prose(p["persona"], pl)}
- **Win condition:** {p["win"]}
- **Modeled saving on {pl["name"]}:** about {r["cost_saving_pct"]}% lower cost and {r["token_saving_pct"]}% fewer tokens than running everything on {T[pl["baseline_tier"]]["label"]} (pessimistic case: {r["conservative_cost_saving_pct"]}% / {r["conservative_token_saving_pct"]}%). [Method]({REPO}/blob/main/METHODOLOGY.md)

## Core rules

Apply `base-model-routing` if it is installed. If not, these are the rules that matter:

1. Use a tool or script (T0) whenever a deterministic command can do the job.
2. Otherwise pick the lowest tier in the routing table below, at the lowest listed effort.
3. Run the listed check before accepting any output.
4. On failure, retry once with the exact error, then move up one tier. Never skip to the top.
5. Judging, choosing the best option and anything public or irreversible start at T3.
6. Brief workers with only the context they need, and cap the output length.

Tiers on {pl["name"]}: {tiers_line} (rare).

## Routing table

| Task | Tier | Effort | Context in | Check before accepting | Escalate when |
|---|---|---|---|---|---|
{rows}

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

{bl(p["escalate_now"])}

## Context diet

{bl(p["context_diet"])}
- {pl["context_rule"]}

## Do it without a model (T0)

{bl(p["tool_first"])}

## Briefing workers

{prose(p["handoff_tip"], pl)}

{delegate_line(pl)}

## Anti-patterns

{bl(p["anti_patterns"])}

## Example

Request: "{p["example"]["request"]}"

```text
{plan(p["example"]["plan"], pl)}
```
'''


def worker_files(pl, tool):
    fmt = tool["agent_format"]
    out = {}
    for tid, (name, eff) in WORKERS.items():
        src = open(J("templates/workers", name + ".md")).read()
        body = src.split("---", 2)[2].strip()
        t = pl["tiers"][tid]
        desc = re.search(r'description: "(.*)"', src).group(1)
        desc = re.sub(r"on (Haiku|Sonnet|Opus)\.", f"on {t['label']}.", desc)
        eff = t.get("force_effort", eff)
        if fmt == "claude":
            model = {"anthropic": {"T1": "haiku", "T2": "sonnet", "T3": "opus"}}.get(pl["id"], {}).get(tid, t["model"])
            out[f"{name}.md"] = f'---\nname: {name}\ndescription: "{desc}"\nmodel: {model}\neffort: {eff}\n---\n{body}\n'
        elif fmt == "codex":
            out[f"{name}.toml"] = (f'name = "{name}"\ndescription = "{desc}"\nmodel = "{t["model"]}"\nmodel_reasoning_effort = "{eff}"\n'
                                   f'developer_instructions = """\n{body}\n"""\n')
        elif fmt == "gemini":
            temp = "0.2" if tid != "T3" else "0.3"
            out[f"{name}.md"] = f'---\nname: {name}\ndescription: "{desc}"\nkind: local\nmodel: {t["model"]}\ntemperature: {temp}\n---\n{body}\n'
        elif fmt == "qwen":
            out[f"{name}.md"] = f'---\nname: {name}\ndescription: "{desc}"\nmodel: {t["model"]}\n---\n{body}\n'
    return out


def setup_md(pl):
    L = [f"# Setup on {pl['name']}", ""]
    for t in pl["tools"]:
        L += [f"## {t['name']}", "", t["how"], ""]
        if t.get("skills_dir"):
            flag = "" if t["id"] == pl["default_tool"] else f" --tool {t['id']}"
            L += ["```bash", f"./install.sh {pl['id']}{flag}                      # all skills" + (" + worker agents" if t.get("agents_dir") else ""),
                  f"./install.sh {pl['id']}{flag} vibe-coder-routing   # base + overlays + one persona", "```", ""]
            L += [f"Skills: `{t['skills_dir']}`" + (f" · Workers: `{t['agents_dir']}`" if t.get("agents_dir") else ""), ""]
        L += [f"Docs: {t['doc']}", ""]
    return "\n".join(L)


def pricing_md(pl):
    L = [f"# {pl['name']} pricing reference (checked {pl['checked']})", "", f"USD per million tokens. Source: {pl['source']}", "",
         "| Tier | Model | Input | Output | Applies to |", "|---|---|---:|---:|---|"]
    for tid in ["T1", "T2", "T3", "T4"]:
        t = pl["tiers"][tid]
        for b in t["prices"]:
            L.append(f"| {tid} | {t['label']} (`{t['model']}`) | ${b['input']:.2f} | ${b['output']:.2f} | {'prompt ≤ %sk' % b['upto_k'] if b['upto_k'] else 'all prompt sizes' if len(t['prices']) == 1 else 'longer prompts'} |")
    L += ["", *[f"- {n}" for n in pl["price_notes"]], "", "Prices change. Re-check the source page before quoting numbers."]
    return "\n".join(L)


def zip_dir(src, dest, root_is_skill=False):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        base = src if root_is_skill else os.path.dirname(src)
        for dp, _, fs in sorted(os.walk(src)):
            for f in sorted(fs):
                full = os.path.join(dp, f)
                zi = zipfile.ZipInfo(os.path.relpath(full, base), date_time=(2026, 10, 20, 0, 0, 0))
                zi.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(zi, open(full, "rb").read())


def main():
    for d in ["skills", "agents", "platforms", "dist"]:
        shutil.rmtree(J(d), ignore_errors=True)
    routing = {"name": NAME, "version": "2.0.0", "repo": REPO, "platforms": {}, "personas": {}}
    for p in PERSONAS:
        routing["personas"][p["name"]] = [{"task": t["task"], "tier": t["tier"], "effort": t["effort"], "context_in_k": t["routed_in_k"],
                                           "check": t["check"], "escalate": t["escalate"]} for t in p["tasks"]]
    for pl in PLATFORMS:
        d = subs(pl)
        sk = J("skills", pl["id"])
        base = os.path.join(sk, "base-model-routing")
        os.makedirs(os.path.join(base, "references"))
        open(os.path.join(base, "SKILL.md"), "w").write(fill(open(J("templates/base.md")).read(), d))
        open(os.path.join(base, "references/pricing.md"), "w").write(pricing_md(pl))
        open(os.path.join(base, "references/setup.md"), "w").write(setup_md(pl))
        for o in OVERLAYS:
            os.makedirs(os.path.join(sk, o))
            open(os.path.join(sk, o, "SKILL.md"), "w").write(fill(open(J("templates", o + ".md")).read(), d))
        for p in PERSONAS:
            os.makedirs(os.path.join(sk, p["name"]))
            open(os.path.join(sk, p["name"], "SKILL.md"), "w").write(persona_md(p, pl, d))
        for t in pl["tools"]:
            if t.get("agents_dir"):
                ad = J("agents", pl["id"], t["id"])
                os.makedirs(ad)
                for fn, body in worker_files(pl, t).items():
                    open(os.path.join(ad, fn), "w").write(body)
        routing["platforms"][pl["id"]] = {"name": pl["name"], "pricing_checked": pl["checked"], "pricing_source": pl["source"],
                                          "tiers": {"T0": None, **{k: {"model": v["model"], "label": v["label"], **({"effort": v["force_effort"]} if v.get("force_effort") else {})} for k, v in pl["tiers"].items()}}}
        # packages
        dd = J("dist", pl["id"])
        names = sorted(os.listdir(sk))
        for n in names:
            zip_dir(os.path.join(sk, n), os.path.join(dd, n + ".zip"), root_is_skill=(pl["id"] == "perplexity"))
        zip_dir(sk, os.path.join(dd, f"{pl['id']}-all-skills.zip"), root_is_skill=True)
        if os.path.isdir(J("agents", pl["id"])):
            zip_dir(J("agents", pl["id"]), os.path.join(dd, f"{pl['id']}-worker-agents.zip"), root_is_skill=True)
        if pl["id"] == "perplexity":
            pd = J("dist/perplexity/plugin")
            shutil.copytree(sk, os.path.join(pd, "skills"))
            json.dump({"name": "token-saver-model-picker", "version": "2.0.0",
                       "description": "Token Saver: Automating the Model Picker. 18 skills that route each task to the cheapest model that can finish it: base routing, 4 overlays and 13 personas.",
                       "author": {"name": "Utpal Das", "url": "https://utpaldas.com"}, "homepage": SITE, "repository": REPO, "license": "MIT"},
                      open(os.path.join(pd, "plugin.json"), "w"), indent=2)
            zip_dir(pd, J("dist/perplexity/token-saver-perplexity-plugin.zip"), root_is_skill=True)
        os.makedirs(J("platforms", pl["id"]), exist_ok=True)
        open(J("platforms", pl["id"], "README.md"), "w").write(platform_readme(pl, d))
    json.dump(routing, open(J("routing.json"), "w"), indent=2)
    open(J("README.md"), "w").write(readme())
    print("built", len(PLATFORMS), "platforms x", len(PERSONAS) + 5, "skills")


def cell(pl, p):
    r = R["results"][pl["id"]][p["name"]]
    return f"[**−{r['cost_saving_pct']}%**](skills/{pl['id']}/{p['name']}/SKILL.md) · [zip](dist/{pl['id']}/{p['name']}.zip)"


def platform_readme(pl, d):
    s = R["platforms"][pl["id"]]
    L = [f"# {NAME} — {pl['name']}", "", f"The full pack, tuned for **{pl['product']}**. Every skill names {pl['name']} models and prices. "
         f"Average modeled saving across the 13 personas: **{s['avg_cost_saving_pct']}% lower cost, {s['avg_token_saving_pct']}% fewer tokens** "
         f"vs. running everything on {s['baseline_model']} (pessimistic: {s['conservative_avg_cost_saving_pct']}% / {s['conservative_avg_token_saving_pct']}%).", "",
         "## Tiers on this platform", "", d["TIER_TABLE"], "", *[f"- {n}" for n in pl["price_notes"]], "", f"Prices checked {pl['checked']}: {pl['source']}", "",
         "## Install", ""]
    for t in pl["tools"]:
        L += [f"### {t['name']}", "", t["how"], ""]
        if t.get("skills_dir"):
            flag = "" if t["id"] == pl["default_tool"] else f" --tool {t['id']}"
            L += ["```bash", f"git clone {REPO}.git", "cd token-saver-automated-model-picker",
                  f"./install.sh {pl['id']}{flag}                      # everything", f"./install.sh {pl['id']}{flag} social-creator-routing   # base + overlays + one persona", "```", ""]
        L += [f"[Docs]({t['doc']})", ""]
    L += ["## Downloads", "", f"- All skills: [`{pl['id']}-all-skills.zip`](../../dist/{pl['id']}/{pl['id']}-all-skills.zip)"]
    if os.path.isdir(J("agents", pl["id"])):
        L.append(f"- Worker agents: [`{pl['id']}-worker-agents.zip`](../../dist/{pl['id']}/{pl['id']}-worker-agents.zip)")
    if pl["id"] == "perplexity":
        L.append("- Perplexity plugin (all 18 skills): import from GitHub with the folder URL "
                 f"`{REPO}/tree/main/dist/perplexity/plugin`, or upload [`token-saver-perplexity-plugin.zip`](../../dist/perplexity/token-saver-perplexity-plugin.zip)")
    L += ["", "## Pick your persona", "", "| Persona | Who it's for | Cost saved | Tokens saved | Skill | Zip |", "|---|---|---:|---:|---|---|"]
    for p in PERSONAS:
        r = R["results"][pl["id"]][p["name"]]
        L.append(f"| {p['title'].replace(' routing', '')} | {p['who']} | **{r['cost_saving_pct']}%** | {r['token_saving_pct']}% | "
                 f"[SKILL.md](../../skills/{pl['id']}/{p['name']}/SKILL.md) | [zip](../../dist/{pl['id']}/{p['name']}.zip) |")
    L += ["", "Always install `base-model-routing` with a persona skill; the overlays (`cheap-batch-mode`, `judge-best-output`, `high-stakes-review`, `context-diet`) are optional but recommended.", ""]
    return "\n".join(L)


def readme():
    o = R["overall"]
    ids = [pl["id"] for pl in PLATFORMS]
    head = "| Persona | Who it's for | " + " | ".join(f"[{pl['name']}](platforms/{pl['id']}/README.md)" for pl in PLATFORMS) + " |"
    finder = [head, "|---|---|" + "---|" * len(ids)]
    for p in PERSONAS:
        finder.append(f"| **{p['title'].replace(' routing', '')}** | {p['who']} | " + " | ".join(cell(pl, p) for pl in PLATFORMS) + " |")
    plat = ["| Platform | Tools covered | T1 → T3 models | Avg cost saved | Avg tokens saved | Guide |", "|---|---|---|---:|---:|---|"]
    for pl in PLATFORMS:
        s = R["platforms"][pl["id"]]
        plat.append(f"| **{pl['name']}** | {', '.join(t['name'] for t in pl['tools'])} | {pl['tiers']['T1']['label']} → {pl['tiers']['T2']['label']} → {pl['tiers']['T3']['label']} | "
                    f"**{s['avg_cost_saving_pct']}%** | {s['avg_token_saving_pct']}% | [Install guide](platforms/{pl['id']}/README.md) |")
    t = open(J("templates/README.md")).read()
    return fill(t, {"FINDER": "\n".join(finder), "PLATFORM_TABLE": "\n".join(plat), "AVG_COST": o["avg_cost_saving_pct"],
                    "AVG_TOKENS": o["avg_token_saving_pct"], "CONS_COST": o["conservative_avg_cost_saving_pct"],
                    "CONS_TOKENS": o["conservative_avg_token_saving_pct"], "RANGE_LO": o["range_cost_saving_pct"][0],
                    "RANGE_HI": o["range_cost_saving_pct"][1], "REPO": REPO, "SITE": SITE, "NAME": NAME})


if __name__ == "__main__":
    main()
