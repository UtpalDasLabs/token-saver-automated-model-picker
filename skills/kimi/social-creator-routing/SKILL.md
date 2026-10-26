---
name: social-creator-routing
description: "Model routing for social media and video creators: which tier writes scripts, hooks, captions, cutdowns, thumbnails text, hashtags and content calendars. Use when planning, producing or repurposing posts, shorts, reels or videos. Not for paid ad campaigns or SEO."
license: MIT
compatibility: "Agent Skills format. Packaged for Kimi: Kimi Code, Kimi API. Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "kimi"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
  modeled-token-saving: "60%"
  modeled-cost-saving: "48%"
  pricing-checked: "2026-10-26"
---

# Social creator routing (Kimi)

Use premium models to decide the message and cheaper models to multiply the format. Strategy and hooks on Kimi K3.1 Pro, production on Kimi K3.1 Pro, metadata on Kimi K3.1 Pro (low effort) and scripts.

- **For:** Short-form video creators, YouTubers, TikTok, Reels and LinkedIn creators who script, film, cut and repurpose content every week.
- **Win condition:** More publishable posts per week at the same or lower AI spend, with hooks that hold attention.
- **Modeled saving on Kimi:** about 48% lower cost and 60% fewer tokens than running everything on Kimi K3.1 Pro (pessimistic case: 16% / 20%). [Method](https://github.com/UtpalDasLabs/token-saver-automated-model-picker/blob/main/METHODOLOGY.md)

## Core rules

Apply `base-model-routing` if it is installed. If not, these are the rules that matter:

1. Use a tool or script (T0) whenever a deterministic command can do the job.
2. Otherwise pick the lowest tier in the routing table below, at the lowest listed effort.
3. Run the listed check before accepting any output.
4. On failure, retry once with the exact error, then move up one tier. Never skip to the top.
5. Judging, choosing the best option and anything public or irreversible start at T3.
6. Brief workers with only the context they need, and cap the output length.

Tiers on Kimi: **T0** tool · **T1** Kimi K3.1 Pro (low effort) · **T2** Kimi K3.1 Pro · **T3** Kimi K3.1 Pro · **T4** Kimi K3.1 Pro (max effort) (rare).

## Routing table

| Task | Tier | Effort | Context in | Check before accepting | Escalate when |
|---|---|---|---|---|---|
| Rename clips, check links, file housekeeping | **T0** script / tool | - | ≤1.5k | Script output | Never |
| Clean subtitles / transcript | **T1** Kimi K3.1 Pro (low effort) | low | ≤10k | Timestamps preserved, no words dropped | Heavy dialect or code-switching -> T2 |
| Hashtags, keywords, alt text | **T1** Kimi K3.1 Pro (low effort) | low | ≤1.5k | Count and banned-tag list | Never |
| Reply drafts to comments | **T1** Kimi K3.1 Pro (low effort) | low | ≤2k | Tone list, no promises | Complaint, legal or brand-safety risk -> T3 |
| Write a full video script from an outline | **T2** Kimi K3.1 Pro | high | ≤8k | Timed to target length, one CTA | Topic needs facts or claims verified -> T3 review |
| Generate hook, title and caption variants | **T2** Kimi K3.1 Pro | low | ≤3k | Length limits per platform | Never; judging goes to T3 |
| Repurpose long video into 5 shorts | **T2** Kimi K3.1 Pro | high | ≤15k | Each short has timestamp in/out, hook, caption | Transcript is messy or multilingual -> T1 clean first |
| Thumbnail text and image prompt variants | **T2** Kimi K3.1 Pro | low | ≤2k | Max 4 words of overlay text | Pick the winner on T3 |
| Content calendar CSV and upload sheet | **T2** Kimi K3.1 Pro | low | ≤5k | CSV validates against column schema | Never |
| Content strategy, series angle, positioning | **T3** Kimi K3.1 Pro | high | ≤20k | 3 angles with audience, promise, proof | Niche or audience is unclear |
| Pick the strongest hook from variants | **T3** Kimi K3.1 Pro | high | ≤5k | Ranked top 3 with reasons | Never above T3 |
| Analyse last week's performance | **T3** Kimi K3.1 Pro | high | ≤10k | 3 actionable insights tied to numbers | Never above T3 |

Tasks not listed: score them with the base rubric (ambiguity, blast radius, checkability, novelty) and pick the matching tier.

## Go straight to T3

- Brand deals, sponsored claims, health, finance or legal topics.
- A reply to a public complaint or a creator conflict.
- Changing the channel's positioning or series format.

## Context diet

- Give caption workers the 3-line summary and the hook, not the full transcript.
- Summarise long transcripts once on T1 with timestamps; repurposing works from that.
- Keep a stable voice card (tone, banned words, CTA style, emoji rules) as the first block of every brief.
- Paste performance numbers as a small table, not screenshots of analytics dashboards.
- Kimi has no supported cheaper micro model. Use T0 scripts, low effort and tight context for savings; do not use retired K2 models.

## Do it without a model (T0)

- Clip renaming and folder sorting with a script (date_platform_topic_v1.mp4).
- Character counts and hashtag limits with a formula, not a model.
- Link-in-bio and URL checks with `curl -I`.
- Subtitle format conversion (SRT/VTT) with ffmpeg or a converter.

## Briefing workers

Brief T2 with the voice card, the platform, the length limit, the hook to keep, and 'numbered variants, no commentary'.

In Kimi Code, print the routing plan and use `/model` to select K3.1 Pro with the listed effort before each step. `/secondary-model` sets one default for subagents, but custom agents cannot pin different models; do not claim automatic per-tier switching. On the Kimi API, set `model` and `reasoning_effort` per request from the routing table.

## Anti-patterns

- Asking Kimi K3.1 Pro for 50 hashtags.
- Letting a cheap model choose which hook to post.
- Re-sending the full 40-minute transcript for each short.

## Example

Request: "Turn my 25-minute YouTube video into 5 Reels with captions and hashtags, and tell me which to post first."

```text
ROUTING PLAN
1. [T1] k3.1-pro/low           Clean transcript, keep timestamps
2. [T1] k3.1-pro/low           Summarise into 12 key moments with timestamps
3. [T2] k3.1-pro/high          Draft 5 Reels: in/out times, hook, on-screen text
4. [T2] k3.1-pro/low           3 caption variants per Reel
5. [T1] k3.1-pro/low           Hashtags + alt text per Reel (batch of 5)
6. [T3] k3.1-pro/high          Rank the 5 Reels and pick the first to post, with reason
7. [T0] script                 Rename clip files, build upload CSV
```
