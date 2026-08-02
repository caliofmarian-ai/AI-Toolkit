#!/data/data/com.termux/files/usr/bin/bash

set -e

ROOT="${1:-.}"
ROOT="$(cd "$ROOT" && pwd)"

echo "=================================="
echo "Repository Intelligence"
echo "=================================="

detect() {
    if [ -f "$ROOT/$2" ]; then
        echo "  ✓ $1"
    fi
}

echo
echo "Languages"

find "$ROOT" -name "*.py" | grep -q . && echo "  ✓ Python"
find "$ROOT" -name "*.sh" | grep -q . && echo "  ✓ Shell"
find "$ROOT" -name "*.js" | grep -q . && echo "  ✓ JavaScript"
find "$ROOT" -name "*.ts" | grep -q . && echo "  ✓ TypeScript"
find "$ROOT" -name "*.md" | grep -q . && echo "  ✓ Markdown"

echo
echo "Package Managers"

detect "pip" requirements.txt
detect "Poetry" pyproject.toml
detect "npm" package.json
detect "pnpm" pnpm-lock.yaml
detect "Yarn" yarn.lock

echo
echo "CI / CD"

detect "GitHub Actions" .github/workflows
detect "Railway" railway.json
detect "Docker" Dockerfile
detect "Docker Compose" docker-compose.yml

echo
echo "Repository Features"

[ -d "$ROOT/tests" ] && echo "  ✓ Tests"
[ -d "$ROOT/docs" ] && echo "  ✓ Documentation"
[ -d "$ROOT/docs/canonical" ] && echo "  ✓ Canonical Architecture"
[ -d "$ROOT/plugins" ] && echo "  ✓ Plugin System"

echo
echo "Analysis complete."

