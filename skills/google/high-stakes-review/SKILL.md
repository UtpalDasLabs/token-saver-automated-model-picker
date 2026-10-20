---
name: high-stakes-review
description: "Overlay that forces a strong-model review before anything public, irreversible, legal, financial, medical, security-related or touching production data ships. Use when the user says publish, send, deploy, sign, submit or go live. Not for drafts, internal notes or reversible experiments."
license: MIT
metadata:
  author: "Utpal Das (UtpalDasLabs)"
  version: "2.0.0"
  platform: "google"
  extends: base-model-routing
---

# High-stakes review

The one place this pack spends more, on purpose. Cheap tiers can draft; T3 signs off.

## When it triggers

- Public: a post, release, landing page, press or investor material.
- Irreversible: sending email, deleting data, payments, database migrations, force pushes.
- Regulated or risky claims: legal, financial, medical, safety, privacy, security.

## Steps

1. **Freeze the artefact.** Review the exact version that will ship, not an earlier draft.
2. **Run T0 checks first:** links resolve, numbers match the source, tests pass, spellcheck, no secrets in the diff.
3. **Review on T3 at `high`** with the `strong-reviewer` subagent or Gemini 4 Argon. Give it the artefact, the audience and the worst plausible outcome.
4. **Verdict:** SHIP, FIX (exact fixes) or REJECT. Apply fixes on T2, then re-check only the changed parts on T3.
5. **Escalate to T4** (Gemini 4 Argon (high thinking)) only if the reviewer flags uncertainty it cannot resolve and the stakes justify the extra cost (same per-token price as T3, but maximum effort uses far more output tokens).
6. **Ask the user** before the irreversible action itself.

Done when the reviewer returns SHIP on the frozen version and the user has approved the action.

## Anti-patterns

- Skipping review because "it's only a small change" to production.
- Reviewing with the same cheap model that wrote it.
- Reviewing the whole project instead of the frozen diff or artefact.
