---
name: context-diet
description: "Overlay that cuts input tokens: trim, summarise and scope context before any model call, keep cache-friendly prefixes, and cap output length. Use when sessions get long, files or transcripts are large, costs spike, or the user asks to save tokens. Not for choosing which model to use."
license: MIT
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "perplexity"
  extends: base-model-routing
---

# Context diet

Routing makes each token cheaper; the diet means you send fewer of them.

## Rules

1. **Scope before sending.** Pass file paths, row ranges or section headings, then load only what the task touches.
2. **Summarise once, reuse often.** Long docs, transcripts and threads get one T1 summary (max 300 words, with source anchors). Higher tiers read the summary, and pull the raw section only when they need a quote.
3. **Prefer diffs over files**, failing test output over full logs, and the last 50 log lines over all of them.
4. **Compact at task boundaries.** When a session passes about 60% of its useful context, write a 200-word state note (goal, decisions, open items, file list) and start fresh from it.
5. **Watch price cliffs.** Web search and fetch tool calls are billed on top of tokens; search once, then reuse the results.
6. **Keep prefixes stable.** Put the system prompt, style guide and tool list first, byte-identical across calls; put the changing request last. That is what prompt caching rewards.
7. **Cap the output.** Every brief states a format and a limit: "diff only", "JSON only", "max 120 words", "top 3".
8. **Don't re-paste.** Refer to earlier artefacts by name or path instead of copying them back in.

## State note template

```text
GOAL: <one line>
DECIDED: <bullets>
OPEN: <bullets>
FILES: <paths touched>
NEXT: <next action and its tier>
```

## Anti-patterns

- "Here's the whole repo/inbox/drive, figure it out."
- Asking for a full rewrite when a list of edits would do.
- Letting a long chat run for hours without compacting.
