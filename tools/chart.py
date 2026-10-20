#!/usr/bin/env python3
"""Render docs/savings.svg: cost saved per persona x platform (no dependencies)."""
import glob, json, os
import yaml
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = json.load(open(os.path.join(ROOT, "benchmarks/results.json")))
PL = sorted([yaml.safe_load(open(f)) for f in glob.glob(os.path.join(ROOT, "data/platforms/*.yaml"))], key=lambda p: p["order"])
PE = sorted([yaml.safe_load(open(f)) for f in glob.glob(os.path.join(ROOT, "data/personas/*.yaml"))], key=lambda p: p["title"])
left, top, cw, ch = 210, 120, 108, 30
W = left + cw * len(PL) + 24
H = top + ch * (len(PE) + 1) + 56
def col(v):  # 40% -> light, 90% -> dark teal
    t = max(0.0, min(1.0, (v - 40) / 50))
    r, g, b = [int(a + (bb - a) * t) for a, bb in zip((214, 236, 233), (15, 118, 110))]
    return f"rgb({r},{g},{b})", ("#ffffff" if t > 0.55 else "#0f2e2b")
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Inter,Segoe UI,Helvetica,Arial,sans-serif">',
     f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
     '<text x="24" y="38" font-size="20" font-weight="700" fill="#111827">Modeled cost saved, by persona and platform</text>',
     f'<text x="24" y="62" font-size="13" fill="#4b5563">Average {R["overall"]["avg_cost_saving_pct"]}% lower cost, {R["overall"]["avg_token_saving_pct"]}% fewer tokens vs. running everything on each platform\'s strong model.</text>']
for j, pl in enumerate(PL):
    x = left + j * cw + cw / 2
    o.append(f'<text x="{x}" y="{top - 14}" font-size="13" font-weight="700" text-anchor="middle" fill="#111827">{pl["name"]}</text>')
for i, p in enumerate(PE):
    y = top + i * ch
    o.append(f'<text x="{left - 12}" y="{y + 20}" font-size="13" text-anchor="end" fill="#111827">{p["title"].replace(" routing", "")}</text>')
    for j, pl in enumerate(PL):
        v = R["results"][pl["id"]][p["name"]]["cost_saving_pct"]
        bg, fg = col(v)
        x = left + j * cw
        o.append(f'<rect x="{x + 2}" y="{y + 2}" width="{cw - 4}" height="{ch - 4}" rx="3" fill="{bg}"/>')
        o.append(f'<text x="{x + cw / 2}" y="{y + 20}" font-size="12" font-weight="700" text-anchor="middle" fill="{fg}">{v}%</text>')
y = top + len(PE) * ch
o.append(f'<text x="{left - 12}" y="{y + 20}" font-size="13" font-weight="700" text-anchor="end" fill="#111827">Average</text>')
for j, pl in enumerate(PL):
    v = R["platforms"][pl["id"]]["avg_cost_saving_pct"]
    x = left + j * cw
    o.append(f'<rect x="{x + 2}" y="{y + 2}" width="{cw - 4}" height="{ch - 4}" rx="3" fill="#111827"/>')
    o.append(f'<text x="{x + cw / 2}" y="{y + 20}" font-size="12" font-weight="700" text-anchor="middle" fill="#ffffff">{v}%</text>')
o.append(f'<text x="24" y="{H - 20}" font-size="11" fill="#6b7280">github.com/UtpalDasLabs/token-saver-automated-model-picker · list prices checked 2026-10-20 · modeled weekly workloads incl. retries and routing overhead</text>')
o.append("</svg>")
open(os.path.join(ROOT, "docs/savings.svg"), "w").write("\n".join(o))
print("wrote docs/savings.svg")
