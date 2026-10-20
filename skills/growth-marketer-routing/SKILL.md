---
name: growth-marketer-routing
description: "Model routing for marketing and growth: which tier does positioning, campaign strategy, ad copy variants, landing pages, email sequences, SEO briefs, keyword clustering and reporting. Use for campaigns, ads, SEO or lifecycle email. Not for organic social video production."
license: MIT
compatibility: "Any Agent Skills host. Automatic model switching in Claude Code with the bundled subagents; elsewhere it outputs a routing plan to apply."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "1.0.0"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-skills"
  modeled-token-saving: "55%"
  modeled-cost-saving: "65%"
  pricing-checked: "2026-10-20"
---

# Growth marketer routing

Strategy, positioning and the final pick live on Opus; volume of variants, briefs and SEO plumbing runs on Sonnet, Haiku and scripts.

- **For:** Performance and content marketers, SEO specialists and growth leads running campaigns, ads, email and landing pages.
- **Win condition:** More tested variants and campaigns shipped per week at a lower cost per winning asset.
- **Modeled saving:** about 55% fewer tokens and 65% lower cost than running everything on Opus 5.5 (pessimistic case: 17% / 50%). [Method](https://github.com/UtpalDasLabs/token-saver-skills/blob/main/METHODOLOGY.md)

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
| UTM links and tracking sheet | **T0** script / tool | - | ≤1.5k | URLs parse, params consistent | Never |
| Keyword clustering and intent tagging | **T1** haiku | low | ≤12k | Every keyword in one cluster | Clusters overlap heavily -> T2 |
| Meta titles, descriptions, alt text | **T1** haiku | low | ≤2k | Length limits by formula | Never |
| Ad copy variants | **T2** sonnet | low | ≤3k | Platform character limits | Regulated claims -> T3 |
| Landing page copy from a brief | **T2** sonnet | medium | ≤8k | Sections match wireframe, one CTA | Offer unclear -> T3 |
| Email sequence drafts | **T2** sonnet | medium | ≤6k | Subject < 50 chars, one goal per mail | Never |
| SEO content brief | **T2** sonnet | low | ≤8k | H2 outline, intent, entities | Never |
| Weekly campaign report | **T2** sonnet | low | ≤6k | Numbers match export | Unexplained swing -> T3 |
| Positioning and campaign strategy | **T3** opus | high | ≤20k | ICP, message, offer, channels, metrics | Never above T3 |
| Pick winners and plan the next test | **T3** opus | medium | ≤6k | Ranked with rationale + hypothesis | Never above T3 |
| Competitor ad and message teardown | **T3** opus | medium | ≤12k | Angles, offers, gaps to exploit | Never above T3 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Health, finance, legal or comparative claims in ads.
- Pricing, offer or discount decisions.
- Brand repositioning or a rename.

## Context diet

- Keep one stable brand card (voice, ICP, offer, banned claims) at the top of every brief.
- Send keyword lists as CSV columns, not pasted SERP pages.
- For reports, export only the metric columns the report needs.

## Do it without a model (T0)

- UTM building and URL validation with a sheet or script.
- Character counts for ads and meta tags with formulas.
- Pulling performance numbers via export or API, not by asking a model to read screenshots.

## Briefing workers

Brief T2 with the brand card, the audience, the platform limits and 'N numbered variants, no commentary'.

In Claude Code, send T1 work to the `micro-worker` subagent, T2 to `standard-worker` and T3 reviews to `strong-reviewer`. In chat apps, print the plan and tell the user which model to switch to at each step.

## Anti-patterns

- Opus writing 40 headline variants.
- Haiku choosing which ad to scale.
- Re-explaining the brand in every prompt instead of a cached brand card.

## Example

Request: "Launch a Google Ads + email campaign for our new B2B pricing tier."

```text
ROUTING PLAN
1. [T3] opus/high      Positioning, offer framing, success metrics
2. [T1] haiku/low      Cluster 300 keywords by intent
3. [T2] sonnet/low     20 RSA headlines + 8 descriptions
4. [T0] formula        Length checks, UTM links
5. [T3] opus/medium    Pick the 10 strongest headlines (judge-best-output)
6. [T2] sonnet/medium  3-email launch sequence
7. [T3] opus/high      Claims review before launch (high-stakes-review)
```
