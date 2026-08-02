#!/data/data/com.termux/files/usr/bin/bash
set -e

python3 lib/python/development_validator.py \
development/BATCH-000_DEVELOPMENT_VALIDATOR_v1.0.md

echo
echo "Development Validator PASS"
