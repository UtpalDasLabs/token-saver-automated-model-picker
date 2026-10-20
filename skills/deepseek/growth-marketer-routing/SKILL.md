---
name: growth-marketer-routing
description: "Model routing for marketing and growth: which tier does positioning, campaign strategy, ad copy variants, landing pages, email sequences, SEO briefs, keyword clustering and reporting. Use for campaigns, ads, SEO or lifecycle email. Not for organic social video production."
license: MIT
compatibility: "Agent Skills format. Packaged for DeepSeek: DeepSeek Harness, Claude Code or Codex on the DeepSeek API, DeepSeek API. Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "deepseek"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
  modeled-token-saving: "55%"
  modeled-cost-saving: "72%"
  pricing-checked: "2026-10-20"
---

# Growth marketer routing (DeepSeek)

Strategy, positioning and the final pick live on DeepSeek V4 Pro; volume of variants, briefs and SEO plumbing runs on DeepSeek V4.1 Flash (thinking), DeepSeek V4.1 Flash (non-thinking) and scripts.

- **For:** Performance and content marketers, SEO specialists and growth leads running campaigns, ads, email and landing pages.
- **Win condition:** More tested variants and campaigns shipped per week at a lower cost per winning asset.
- **Modeled saving on DeepSeek:** about 72% lower cost and 55% fewer tokens than running everything on DeepSeek V4 Pro (pessimistic case: 58% / 17%). [Method](https://github.com/UtpalDasLabs/token-saver-automated-model-picker/blob/main/METHODOLOGY.md)

## Core rules

Apply `base-model-routing` if it is installed. If not, these are the rules that matter:

1. Use a tool or script (T0) whenever a deterministic command can do the job.
2. Otherwise pick the lowest tier in the routing table below, at the lowest listed effort.
3. Run the listed check before accepting any output.
4. On failure, retry once with the exact error, then move up one tier. Never skip to the top.
5. Judging, choosing the best option and anything public or irreversible start at T3.
6. Brief workers with only the context they need, and cap the output length.

Tiers on DeepSeek: **T0** tool · **T1** DeepSeek V4.1 Flash (non-thinking) · **T2** DeepSeek V4.1 Flash (thinking) · **T3** DeepSeek V4 Pro · **T4** DeepSeek V4 Pro (max effort) (rare).

## Routing table

| Task | Tier | Effort | Context in | Check before accepting | Escalate when |
|---|---|---|---|---|---|
| UTM links and tracking sheet | **T0** script / tool | - | ≤1.5k | URLs parse, params consistent | Never |
| Keyword clustering and intent tagging | **T1** DeepSeek V4.1 Flash (non-thinking) | low | ≤12k | Every keyword in one cluster | Clusters overlap heavily -> T2 |
| Meta titles, descriptions, alt text | **T1** DeepSeek V4.1 Flash (non-thinking) | low | ≤2k | Length limits by formula | Never |
| Ad copy variants | **T2** DeepSeek V4.1 Flash (thinking) | low | ≤3k | Platform character limits | Regulated claims -> T3 |
| Landing page copy from a brief | **T2** DeepSeek V4.1 Flash (thinking) | medium | ≤8k | Sections match wireframe, one CTA | Offer unclear -> T3 |
| Email sequence drafts | **T2** DeepSeek V4.1 Flash (thinking) | medium | ≤6k | Subject < 50 chars, one goal per mail | Never |
| SEO content brief | **T2** DeepSeek V4.1 Flash (thinking) | low | ≤8k | H2 outline, intent, entities | Never |
| Weekly campaign report | **T2** DeepSeek V4.1 Flash (thinking) | low | ≤6k | Numbers match export | Unexplained swing -> T3 |
| Positioning and campaign strategy | **T3** DeepSeek V4 Pro | high | ≤20k | ICP, message, offer, channels, metrics | Never above T3 |
| Pick winners and plan the next test | **T3** DeepSeek V4 Pro | medium | ≤6k | Ranked with rationale + hypothesis | Never above T3 |
| Competitor ad and message teardown | **T3** DeepSeek V4 Pro | medium | ≤12k | Angles, offers, gaps to exploit | Never above T3 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Health, finance, legal or comparative claims in ads.
- Pricing, offer or discount decisions.
- Brand repositioning or a rename.

## Context diet

- Keep one stable brand card (voice, ICP, offer, banned claims) at the top of every brief.
- Send keyword lists as CSV columns, not pasted SERP pages.
- For reports, export only the metric columns the report needs.
- Use off-peak hours (half price) for big batch jobs that can wait.

## Do it without a model (T0)

- UTM building and URL validation with a sheet or script.
- Character counts for ads and meta tags with formulas.
- Pulling performance numbers via export or API, not by asking a model to read screenshots.

## Briefing workers

Brief T2 with the brand card, the audience, the platform limits and 'N numbered variants, no commentary'.

In Claude Code or Codex on the DeepSeek API, send T1 work to the `micro-worker` agent, T2 to `standard-worker` and T3 reviews to `strong-reviewer`; each one is pinned to the right DeepSeek model. Anywhere else, print the routing plan and tell the user which model to use at each step.

## Anti-patterns

- DeepSeek V4 Pro writing 40 headline variants.
- DeepSeek V4.1 Flash (non-thinking) choosing which ad to scale.
- Re-explaining the brand in every prompt instead of a cached brand card.

## Example

Request: "Launch a Google Ads + email campaign for our new B2B pricing tier."

```text
ROUTING PLAN
1. [T3] v4-pro/high            Positioning, offer framing, success metrics
2. [T1] flash/low              Cluster 300 keywords by intent
3. [T2] flash-think/low        20 RSA headlines + 8 descriptions
4. [T0] formula                Length checks, UTM links
5. [T3] v4-pro/medium          Pick the 10 strongest headlines (judge-best-output)
6. [T2] flash-think/medium     3-email launch sequence
7. [T3] v4-pro/high            Claims review before launch (high-stakes-review)
```
