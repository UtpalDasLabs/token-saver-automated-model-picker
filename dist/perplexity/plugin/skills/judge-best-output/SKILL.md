---
name: judge-best-output
description: "Overlay for generate-cheap, judge-smart workflows: produce many variants on Gemini 3.8 Flash or GPT-6 Luna, then let Claude Opus 5.5 rank and pick the winner with reasons. Use for hooks, headlines, taglines, designs, code approaches or any pick-the-best choice. Not for single-answer factual questions."
license: MIT
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "perplexity"
  extends: base-model-routing
---

# Judge the best output

Premium models decide the message; cheaper models multiply the options.

## Steps

1. **Define the rubric on T3 first** (3–5 weighted criteria, for example: hook strength 30%, clarity 25%, brand fit 25%, length 20%). Keep it under 150 words.
2. **Generate on T2** (or T1 for very short items): 6–12 variants, numbered, no commentary.
3. **Filter on T0/T1**: drop variants that break hard rules (length, banned words, missing CTA) before judging.
4. **Judge on T3** at `medium`: score the survivors against the rubric, return the top 3 with one-line reasons and one concrete improvement for the winner.
5. **Polish the winner on T2** with that improvement, unless it is a one-word fix.

Done when the user has a ranked top 3 and one polished winner.

## Judge output format

```text
RANK  ID  SCORE  REASON
1     #7  8.6    Strongest curiosity gap, under 9 words
2     #3  7.9    Clear benefit, weaker opening verb
3     #11 7.4    On brand but generic
IMPROVE #7: swap "learn" for "steal" to match the channel voice.
```

## Anti-patterns

- Generating variants on Claude Opus 5.5. Variants are cheap; judgement is not.
- Asking GPT-6 Luna which variant is best.
- Judging without a written rubric, which makes results inconsistent.
