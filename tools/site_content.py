#!/usr/bin/env python3
"""Export the website content JSON (utpaldas.com/labs/token-saver) from repo data.
  python3 tools/site_content.py > token-saver.json
"""
import glob, json, os
import yaml
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
R = json.load(open(os.path.join(ROOT, "benchmarks/results.json")))
PL = sorted([yaml.safe_load(open(f)) for f in glob.glob(os.path.join(ROOT, "data/platforms/*.yaml"))], key=lambda p: p["order"])
PE = sorted([yaml.safe_load(open(f)) for f in glob.glob(os.path.join(ROOT, "data/personas/*.yaml"))], key=lambda p: -R["results"]["anthropic"][p["name"]]["cost_saving_pct"])
o = R["overall"]
platforms = []
for pl in PL:
    s = R["platforms"][pl["id"]]
    tools = []
    for t in pl["tools"]:
        cmd = ""
        if t.get("skills_dir"):
            flag = "" if t["id"] == pl["default_tool"] else f" --tool {t['id']}"
            cmd = f"./install.sh {pl['id']}{flag} PERSONA"
        if pl["id"] == "perplexity" and t["id"] == "computer":
            cmd = f"{REPO}/tree/main/dist/perplexity/plugin"
        tools.append({"name": t["name"], "auto": bool(t.get("agents_dir")), "how": t["how"].replace("`", ""), "command": cmd, "docUrl": t["doc"]})
    platforms.append({"id": pl["id"], "name": pl["name"], "product": pl["product"],
                      "avgCostSaved": s["avg_cost_saving_pct"], "avgTokensSaved": s["avg_token_saving_pct"],
                      "pessimisticCost": s["conservative_avg_cost_saving_pct"], "baselineModel": s["baseline_model"],
                      "t1": pl["tiers"]["T1"]["label"], "t2": pl["tiers"]["T2"]["label"], "t3": pl["tiers"]["T3"]["label"], "t4": pl["tiers"]["T4"]["label"],
                      "note": pl["price_notes"][0], "pricingUrl": pl["source"], "tools": tools})
personas = []
for p in PE:
    personas.append({"id": p["name"], "name": p["title"].replace(" routing", ""), "who": p["who"],
                     "topTasks": [t["task"] for t in sorted(p["tasks"], key=lambda t: -t["per_week"])[:3]],
                     "results": [{"platform": pl["id"], "costSaved": R["results"][pl["id"]][p["name"]]["cost_saving_pct"],
                                  "tokensSaved": R["results"][pl["id"]][p["name"]]["token_saving_pct"],
                                  "pessimisticCost": R["results"][pl["id"]][p["name"]]["conservative_cost_saving_pct"]} for pl in PL]})
c = {
 "meta": {"title": "Token Saver: Automating the Model Picker — Labs — Utpal Das",
          "description": f"Open-source AI skills that pick the model for you: each task goes to the cheapest model that can finish it. For Claude, ChatGPT/Codex, Gemini, DeepSeek, Qwen, Perplexity and Kimi. Modeled {o['avg_cost_saving_pct']}% lower cost, {o['avg_token_saving_pct']}% fewer tokens."},
 "hero": {"eyebrow": "Labs · Open source · For anyone who uses AI at work",
          "title": "Token Saver", "subtitle": "Automating the model picker.",
          "lead": "Most of what we ask AI to do in a week is routine: tag this, rename that, draft a caption, write the test. These skills teach your AI assistant to pick the model for you — a script, a small model, a mid model or the flagship — and to move up only when a check fails. Pick your platform and the way you work, and get the exact package for it.",
          "repoUrl": REPO, "methodUrl": REPO + "/blob/main/METHODOLOGY.md", "resultsUrl": REPO + "/blob/main/benchmarks/RESULTS.md"},
 "demo": {"title": "Token Saver product demo", "durationSeconds": 38.5,
          "videoUrl": REPO + "/raw/refs/heads/main/docs/Token-Saver-Product-Demo.mp4",
          "posterUrl": REPO + "/raw/refs/heads/main/docs/token-saver-poster.jpg",
          "chapters": [{"title": "The cost problem", "start": 0},
                       {"title": "Smart model routing", "start": 9.5},
                       {"title": "Your platform and workflow", "start": 19},
                       {"title": "Measurable savings", "start": 28.5}]},
 "stats": {"avgCostSaved": o["avg_cost_saving_pct"], "avgTokensSaved": o["avg_token_saving_pct"],
           "pessimisticCost": o["conservative_avg_cost_saving_pct"], "pessimisticTokens": o["conservative_avg_token_saving_pct"],
           "platformCount": o["platforms"], "personaCount": o["personas"], "skillCount": 18, "pricingChecked": max(pl["checked"] for pl in PL),
           "baseline": "Compared with running every task on each platform's strong everyday model, with the full conversation in context."},
 "finder": {"eyebrow": "Find your package", "title": "Pick your platform, then the way you work",
            "lead": "Every persona skill is packaged for each platform, with that platform's own models and prices. Install the base skill plus your persona; the installer does both."},
 "platforms": platforms,
 "personas": personas,
 "method": {"title": "How the numbers are calculated",
   "points": ["Each persona has a modeled week of real task types — how often, how much context, which tier the skill routes it to.",
              "Baseline: every task on the platform's strong everyday model at default effort, with the full conversation in context.",
              "Routed: each task on its tier's model, with failed attempts paid in full and redone one tier up, plus the cost of writing briefs and loading the skill.",
              f"Prices are official API list prices, checked through {max(pl['checked'] for pl in PL)}. Caching, batch and off-peak discounts are not counted — they stack on top. Kimi Code membership quota is not directly comparable to API spending.",
              f"Pessimistic case (failure rates doubled, half the context savings): {o['conservative_avg_cost_saving_pct']}% lower cost, {o['conservative_avg_token_saving_pct']}% fewer tokens. Cost savings hold up because they come from routing; token savings depend on keeping context lean."],
   "caveat": "These are modeled estimates, not a lab benchmark. Savings differ by platform because the price gap between small and strong models differs. Kimi has no supported cheaper micro model, so its model uses effort and context savings instead. Every assumption is in the repo — change the workload to match your week and re-run the calculator."},
 "labsCard": {"eyebrow": f"Open source · {o['platforms']} AI platforms", "coverHeadline": f"−{o['avg_cost_saving_pct']}% AI COST",
              "coverCaption": f"{o['avg_token_saving_pct']}% fewer tokens · {o['personas']} personas · {o['platforms']} platforms",
              "title": "Token Saver: Automating the Model Picker", "tagline": "Your AI picks the cheapest model that can finish each task.",
              "description": "An open-source skill pack for Claude, ChatGPT and Codex, Gemini, DeepSeek, Qwen, Perplexity and Kimi. Pick your platform and one of 13 personas — vibe coder, social creator, product, research, ops, marketing, writing, data, design, sales, support, teaching or job search — and get the exact package, with its modeled savings and install steps.",
              "tags": [f"{o['platforms']} PLATFORMS", f"{o['personas']} PERSONAS", f"{o['platforms'] * 18} SKILLS", "MIT LICENCE"], "cta": "Find your package"}
}
print(json.dumps(c, indent=2, ensure_ascii=False))
