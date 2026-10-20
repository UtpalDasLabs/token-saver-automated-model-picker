#!/usr/bin/env bash
# Install Token Saver: Automating the Model Picker.
#   ./install.sh <platform> [--tool <tool>] [persona-skill ...]
#   platforms: anthropic openai google deepseek qwen perplexity
#   tools:     claude-code (anthropic, deepseek), codex (openai), gemini-cli (google),
#              qwen-code (qwen), deepseek-harness (deepseek)
#   PREFIX=.  installs into the current project (./.claude, ./.agents, ...) instead of $HOME
set -euo pipefail
cd "$(dirname "$0")"
P="${1:-}"; shift || true
[ -d "skills/$P" ] || { echo "Usage: ./install.sh <anthropic|openai|google|deepseek|qwen|perplexity> [--tool T] [persona ...]" >&2; exit 1; }
TOOL=""
if [ "${1:-}" = "--tool" ]; then TOOL="$2"; shift 2; fi
if [ -z "$TOOL" ]; then
  case "$P" in anthropic) TOOL=claude-code;; openai) TOOL=codex;; google) TOOL=gemini-cli;; qwen) TOOL=qwen-code;; deepseek) TOOL=deepseek-harness;; perplexity) TOOL=none;; esac
fi
H="${PREFIX:-$HOME}"
case "$TOOL" in
  claude-code)      SK="$H/.claude/skills"; AG="$H/.claude/agents";;
  codex)            SK="$H/.agents/skills"; AG="$H/.codex/agents";;
  gemini-cli)       SK="$H/.gemini/skills"; AG="$H/.gemini/agents";;
  qwen-code)        SK="$H/.qwen/skills";   AG="$H/.qwen/agents";;
  deepseek-harness) SK="$H/.agents/skills"; AG="";;
  none) echo "Perplexity has no local install. In Perplexity Computer: Plugins → Add custom → Import plugin from GitHub,"
        echo "then paste: https://github.com/UtpalDasLabs/token-saver-automated-model-picker/tree/main/dist/perplexity/plugin"
        echo "Or upload single skills from dist/perplexity/*.zip. See platforms/perplexity/README.md."; exit 0;;
  *) echo "Unknown tool: $TOOL" >&2; exit 1;;
esac
CORE="base-model-routing cheap-batch-mode judge-best-output high-stakes-review context-diet"
if [ $# -eq 0 ]; then SKILLS=$(ls "skills/$P"); else SKILLS="$CORE $*"; fi
mkdir -p "$SK"
for s in $SKILLS; do
  [ -f "skills/$P/$s/SKILL.md" ] || { echo "Unknown skill: $s" >&2; exit 1; }
  rm -rf "${SK:?}/$s"; cp -R "skills/$P/$s" "$SK/$s"; echo "  skill   $s"
done
if [ -n "$AG" ] && [ -d "agents/$P/$TOOL" ]; then
  mkdir -p "$AG"; cp agents/"$P"/"$TOOL"/* "$AG/"; echo "  workers micro-worker, standard-worker, strong-reviewer -> $AG"
fi
echo "Installed the $P package for $TOOL into $SK. Restart the tool so it picks up the new skills."
