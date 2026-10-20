#!/usr/bin/env python3
"""Render docs/savings.svg from benchmarks/results.json (no dependencies)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(ROOT, "benchmarks/results.json")))
ps = sorted(d["personas"], key=lambda r: -r["cost_saving_pct"])
W, row, top, left, barw = 880, 34, 92, 250, 560
H = top + row * len(ps) + 60
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Inter,Segoe UI,Helvetica,Arial,sans-serif">',
     f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
     '<text x="24" y="38" font-size="20" font-weight="700" fill="#111827">Modeled savings vs. running everything on Opus 5.5</text>',
     f'<text x="24" y="62" font-size="13" fill="#4b5563">Average: {d["summary"]["avg_token_saving_pct"]}% fewer tokens, {d["summary"]["avg_cost_saving_pct"]}% lower cost. Pessimistic: {d["summary"]["conservative_avg_token_saving_pct"]}% / {d["summary"]["conservative_avg_cost_saving_pct"]}%. Prices checked {d["summary"]["pricing_checked"]}.</text>',
     f'<rect x="{left}" y="74" width="12" height="12" fill="#0f766e"/><text x="{left+18}" y="85" font-size="12" fill="#374151">Cost saved</text>',
     f'<rect x="{left+110}" y="74" width="12" height="12" fill="#99c9c3"/><text x="{left+128}" y="85" font-size="12" fill="#374151">Tokens saved</text>']
for i, r in enumerate(ps):
    y = top + i * row + 8
    name = r["title"].replace(" routing", "")
    o.append(f'<text x="{left-12}" y="{y+16}" font-size="13" text-anchor="end" fill="#111827">{name}</text>')
    cw, tw = barw * r["cost_saving_pct"] / 100, barw * r["token_saving_pct"] / 100
    o.append(f'<rect x="{left}" y="{y+2}" width="{cw:.1f}" height="11" rx="2" fill="#0f766e"/>')
    o.append(f'<rect x="{left}" y="{y+15}" width="{tw:.1f}" height="8" rx="2" fill="#99c9c3"/>')
    o.append(f'<text x="{left+cw+6:.1f}" y="{y+12}" font-size="11" font-weight="700" fill="#0f766e">{r["cost_saving_pct"]}%</text>')
    o.append(f'<text x="{left+tw+6:.1f}" y="{y+23}" font-size="10" fill="#4b5563">{r["token_saving_pct"]}%</text>')
o.append(f'<text x="24" y="{H-20}" font-size="11" fill="#6b7280">github.com/UtpalDasLabs/token-saver-skills · modeled weekly workloads incl. retries and routing overhead · see METHODOLOGY.md</text>')
o.append("</svg>")
os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
open(os.path.join(ROOT, "docs/savings.svg"), "w").write("\n".join(o))
print("wrote docs/savings.svg")
