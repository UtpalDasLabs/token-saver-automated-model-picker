#!/usr/bin/env bash
# Install Token Saver Skills into Claude Code.
#   ./install.sh                       all skills + subagents (personal: ~/.claude)
#   ./install.sh vibe-coder-routing    base + overlays + one persona
#   CLAUDE_DIR=.claude ./install.sh    install into the current project instead
set -euo pipefail
cd "$(dirname "$0")"
DEST="${CLAUDE_DIR:-$HOME/.claude}"
mkdir -p "$DEST/skills" "$DEST/agents"
CORE="base-model-routing cheap-batch-mode judge-best-output high-stakes-review context-diet"
if [ $# -eq 0 ]; then SKILLS=$(ls skills); else SKILLS="$CORE $*"; fi
for s in $SKILLS; do
  [ -f "skills/$s/SKILL.md" ] || { echo "Unknown skill: $s" >&2; exit 1; }
  rm -rf "$DEST/skills/$s"; cp -R "skills/$s" "$DEST/skills/$s"; echo "  skill  $s"
done
cp agents/*.md "$DEST/agents/"; echo "  agents micro-worker, standard-worker, strong-reviewer"
echo "Installed into $DEST. Restart Claude Code, then run /skills and /agents."
