#!/usr/bin/env bash
# Build Claude.ai-ready zips (each zip has <skill>/SKILL.md at its root) into dist/.
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf dist && mkdir dist
cd skills
for s in */; do s=${s%/}; zip -qr "../dist/$s.zip" "$s"; done
zip -qr ../dist/token-saver-skills-all.zip .
cd .. && cp -R agents dist/ && (cd dist && zip -qr claude-code-subagents.zip agents && rm -rf agents)
ls dist
