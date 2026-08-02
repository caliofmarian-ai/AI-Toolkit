#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 lib/python/development_validator/main.py \
development/BATCH-000_DEVELOPMENT_VALIDATOR_v1.0.md

test -f .ai/work/development_validation.json

echo
echo "Validator v2 PASS"
