---
name: cheap-batch-mode
description: "Overlay for high-volume repetitive jobs: process tens to thousands of similar items (rows, files, clips, tickets, posts) at the lowest cost with scripts, GPT-6 Luna batches and failure-only reruns. Use when the user says bulk, batch, all of these, every row or for each. Not for one-off creative work."
license: MIT
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "openai"
  extends: base-model-routing
---

# Cheap batch mode

Turns "do this to 500 things" into the cheapest reliable pipeline.

## Steps

1. **Sample first.** Take 5 representative items, including the messiest one.
2. **Try T0.** If a formula, regex or script handles all 5, run it on everything and stop.
3. **Write one brief.** Use the base brief template with a strict output schema (JSON lines or CSV, one row per item, item ID echoed back).
4. **Pilot on T1.** Run the 5 samples on GPT-6 Luna at `low`. Validate against the schema. If 4 of 5 pass, continue; otherwise tighten the rules once, or move the job to T2.
5. **Run in chunks.** 20–50 items per call, keeping each prompt small. GPT-6.1 Sol and GPT-6 Luna cost more per token above 272k input tokens. Compact long sessions before that.
6. **Validate every row** with code: schema, required fields, allowed values, length.
7. **Rerun failures only**, first at T1 `high`, then at T2. Never rerun the whole batch.
8. **Spot-check on T3** only when the output is public or high stakes: 10 random rows, not all.

Done when every item has a validated row and the failure list is empty or handed to the user.

## Extra savings

- If results can wait and you are on the API, use the provider's batch or off-peak option where it exists; it is usually about half price.
- Keep the brief and examples as an identical prefix across chunks so they are read from cache.

## Anti-patterns

- One model call per item when 30 fit in one call.
- Sending the whole spreadsheet when only two columns matter.
- Asking for prose when a CSV column would do.
