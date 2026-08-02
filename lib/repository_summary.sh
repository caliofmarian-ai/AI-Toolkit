#!/data/data/com.termux/files/usr/bin/bash

ROOT="${1:-.}"

echo "=================================="
echo "Repository Summary"
echo "=================================="

echo
echo "Repository:"
git -C "$ROOT" rev-parse --show-toplevel 2>/dev/null || exit 1

echo
echo "Branch:"
git -C "$ROOT" branch --show-current

echo
echo "Files:"
find "$ROOT" -type f | wc -l

echo
echo "Directories:"
find "$ROOT" -type d | wc -l

echo
echo "Markdown:"
find "$ROOT" -type f -name "*.md" | wc -l

echo
echo "Python:"
find "$ROOT" -type f -name "*.py" | wc -l

echo
echo "Shell:"
find "$ROOT" -type f \( -name "*.sh" -o -name "*.bash" \) | wc -l

echo
echo "JSON:"
find "$ROOT" -type f -name "*.json" | wc -l

echo
echo "Tests:"
find "$ROOT" -type d -name tests | wc -l

echo
echo "Canonical documents:"
find "$ROOT" -path "*/canonical/*" -type f | wc -l

echo
echo "GitHub Actions:"
find "$ROOT" -path "*/.github/workflows/*" -type f | wc -l

echo
echo "Railway:"
find "$ROOT" \( -name railway.json -o -name railway.toml \) | wc -l

echo
echo "Docker:"
find "$ROOT" \( -name Dockerfile -o -name docker-compose.yml -o -name docker-compose.yaml \) | wc -l

echo
echo "README:"
find "$ROOT" -maxdepth 2 -iname "README.md" | wc -l

echo
echo "LICENSE:"
find "$ROOT" -maxdepth 2 \( -iname "LICENSE" -o -iname "LICENSE.md" \) | wc -l
