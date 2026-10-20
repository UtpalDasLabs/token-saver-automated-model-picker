---
name: social-creator-routing
description: "Model routing for social media and video creators: which tier writes scripts, hooks, captions, cutdowns, thumbnails text, hashtags and content calendars. Use when planning, producing or repurposing posts, shorts, reels or videos. Not for paid ad campaigns or SEO."
license: MIT
compatibility: "Agent Skills format. Packaged for Anthropic: Claude Code, Claude.ai, Claude API. Model switching is automatic where worker agents are supported; elsewhere the skill outputs a routing plan."
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "anthropic"
  extends: base-model-routing
  repo: "https://github.com/UtpalDasLabs/token-saver-automated-model-picker"
  modeled-token-saving: "59%"
  modeled-cost-saving: "73%"
  pricing-checked: "2026-10-20"
---

# Social creator routing (Anthropic)

Use premium models to decide the message and cheaper models to multiply the format. Strategy and hooks on Claude Opus 5.5, production on Claude Sonnet 5.5, metadata on Claude Haiku 5.5 and scripts.

- **For:** Short-form video creators, YouTubers, TikTok, Reels and LinkedIn creators who script, film, cut and repurpose content every week.
- **Win condition:** More publishable posts per week at the same or lower AI spend, with hooks that hold attention.
- **Modeled saving on Anthropic:** about 73% lower cost and 59% fewer tokens than running everything on Claude Opus 5.5 (pessimistic case: 58% / 19%). [Method](https://github.com/UtpalDasLabs/token-saver-automated-model-picker/blob/main/METHODOLOGY.md)

## Core rules

Apply `base-model-routing` if it is installed. If not, these are the rules that matter:

1. Use a tool or script (T0) whenever a deterministic command can do the job.
2. Otherwise pick the lowest tier in the routing table below, at the lowest listed effort.
3. Run the listed check before accepting any output.
4. On failure, retry once with the exact error, then move up one tier. Never skip to the top.
5. Judging, choosing the best option and anything public or irreversible start at T3.
6. Brief workers with only the context they need, and cap the output length.

Tiers on Anthropic: **T0** tool · **T1** Claude Haiku 5.5 · **T2** Claude Sonnet 5.5 · **T3** Claude Opus 5.5 · **T4** Claude Fable 5.1 (rare).

## Routing table

| Task | Tier | Effort | Context in | Check before accepting | Escalate when |
|---|---|---|---|---|---|
| Rename clips, check links, file housekeeping | **T0** script / tool | - | ≤1.5k | Script output | Never |
| Clean subtitles / transcript | **T1** Claude Haiku 5.5 | low | ≤10k | Timestamps preserved, no words dropped | Heavy dialect or code-switching -> T2 |
| Hashtags, keywords, alt text | **T1** Claude Haiku 5.5 | low | ≤1.5k | Count and banned-tag list | Never |
| Reply drafts to comments | **T1** Claude Haiku 5.5 | low | ≤2k | Tone list, no promises | Complaint, legal or brand-safety risk -> T3 |
| Write a full video script from an outline | **T2** Claude Sonnet 5.5 | medium | ≤8k | Timed to target length, one CTA | Topic needs facts or claims verified -> T3 review |
| Generate hook, title and caption variants | **T2** Claude Sonnet 5.5 | low | ≤3k | Length limits per platform | Never; judging goes to T3 |
| Repurpose long video into 5 shorts | **T2** Claude Sonnet 5.5 | medium | ≤15k | Each short has timestamp in/out, hook, caption | Transcript is messy or multilingual -> T1 clean first |
| Thumbnail text and image prompt variants | **T2** Claude Sonnet 5.5 | low | ≤2k | Max 4 words of overlay text | Pick the winner on T3 |
| Content calendar CSV and upload sheet | **T2** Claude Sonnet 5.5 | low | ≤5k | CSV validates against column schema | Never |
| Content strategy, series angle, positioning | **T3** Claude Opus 5.5 | medium | ≤20k | 3 angles with audience, promise, proof | Niche or audience is unclear |
| Pick the strongest hook from variants | **T3** Claude Opus 5.5 | medium | ≤5k | Ranked top 3 with reasons | Never above T3 |
| Analyse last week's performance | **T3** Claude Opus 5.5 | medium | ≤10k | 3 actionable insights tied to numbers | Never above T3 |

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
- Claude Haiku 5.5 costs 5x more per token once a prompt passes 100k tokens. Split or compact before that line.

## Do it without a model (T0)

- Clip renaming and folder sorting with a script (date_platform_topic_v1.mp4).
- Character counts and hashtag limits with a formula, not a model.
- Link-in-bio and URL checks with `curl -I`.
- Subtitle format conversion (SRT/VTT) with ffmpeg or a converter.

## Briefing workers

Brief T2 with the voice card, the platform, the length limit, the hook to keep, and 'numbered variants, no commentary'.

In Claude Code, send T1 work to the `micro-worker` agent, T2 to `standard-worker` and T3 reviews to `strong-reviewer`; each one is pinned to the right Anthropic model. Anywhere else, print the routing plan and tell the user which model to use at each step.

## Anti-patterns

- Asking Claude Opus 5.5 for 50 hashtags.
- Letting a cheap model choose which hook to post.
- Re-sending the full 40-minute transcript for each short.

## Example

Request: "Turn my 25-minute YouTube video into 5 Reels with captions and hashtags, and tell me which to post first."

```text
ROUTING PLAN
1. [T1] haiku/low              Clean transcript, keep timestamps
2. [T1] haiku/low              Summarise into 12 key moments with timestamps
3. [T2] sonnet/medium          Draft 5 Reels: in/out times, hook, on-screen text
4. [T2] sonnet/low             3 caption variants per Reel
5. [T1] haiku/low              Hashtags + alt text per Reel (batch of 5)
6. [T3] opus/medium            Rank the 5 Reels and pick the first to post, with reason
7. [T0] script                 Rename clip files, build upload CSV
```
