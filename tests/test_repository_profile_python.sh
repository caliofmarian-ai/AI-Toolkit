#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 lib/python/repository_profile.py .

test -f .ai/context/repository_profile.json

echo
echo "Repository profile generated successfully."
