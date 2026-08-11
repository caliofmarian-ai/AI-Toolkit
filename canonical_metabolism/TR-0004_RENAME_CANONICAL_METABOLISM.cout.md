.../AI-Projects/AI-Toolkit $ cd ~/storage/shared/AI-Projects/AI-Toolkit || exit 1

set -euo pipefail

TRANSFORMATION="TR-0004"
NAME="RENAME_CANONICAL_METABOLISM"

OLD_DIR="$HOME/storage/shared/AI-Projects/AI-Toolkit/temux_output"
NEW_DIR="$HOME/storage/shared/AI-Projects/AI-Toolkit/canonical_metabolism"

echo "========================================================="
echo "$TRANSFORMATION :: $NAME"
echo "========================================================="
echo

echo "[1/5] Checking existing directory..."

if [ ! -d "$OLD_DIR" ]; then
    echo "ERROR: Directory not found:"
    echo "  $OLD_DIR"
    exit 1
fi

echo
echo "[2/5] Renaming directory..."

mv "$OLD_DIR" "$NEW_DIR"

echo
echo "[3/5] Verifying..."

if [ ! -d "$NEW_DIR" ]; then
    echo "ERROR: Rename failed."
    exit 1
fi

echo
echo "[4/5] Creating next canonical output file..."

OUTPUT_FILE="$NEW_DIR/TR-0004_RENAME_CANONICAL_METABOLISM.cout.md"

touch "$OUTPUT_FILE"

echo
echo "[5/5] Listing contents..."

find "$NEW_DIR" -maxdepth 1 -type f | sort

echo
echo "========================================================="
echo "CANONICAL TRANSFORMATION COMPLETED"
echo "========================================================="
echo
echo "Previous directory : temux_output"
echo "Current directory  : canonical_metabolism"
echo
echo "Output file:"
echo "$OUTPUT_FILE"
echo
echo "State Transition:"
echo "STATE-0003 -> STATE-0004"
echo
echo "Transformation successful."
=========================================================
TR-0004 :: RENAME_CANONICAL_METABOLISM
=========================================================

[1/5] Checking existing directory...

[2/5] Renaming directory...

[3/5] Verifying...

[4/5] Creating next canonical output file...

[5/5] Listing contents...
/data/data/com.termux/files/home/storage/shared/AI-Projects/AI-Toolkit/canonical_metabolism/TR-0001_ESTABLISH_FOUNDATION.cout.md
/data/data/com.termux/files/home/storage/shared/AI-Projects/AI-Toolkit/canonical_metabolism/TR-0002_ESTABLISH_CORE_FOUNDATION.cout.md
/data/data/com.termux/files/home/storage/shared/AI-Projects/AI-Toolkit/canonical_metabolism/TR-0003_FREEZE_ENGINEERING_CHARTER.cout.md
/data/data/com.termux/files/home/storage/shared/AI-Projects/AI-Toolkit/canonical_metabolism/TR-0004_RENAME_CANONICAL_METABOLISM.cout.md

=========================================================
CANONICAL TRANSFORMATION COMPLETED
=========================================================

Previous directory : temux_output
Current directory  : canonical_metabolism

Output file:
/data/data/com.termux/files/home/storage/shared/AI-Projects/AI-Toolkit/canonical_metabolism/TR-0004_RENAME_CANONICAL_METABOLISM.cout.md

State Transition:
STATE-0003 -> STATE-0004

Transformation successful.
~/.../AI-Projects/AI-Toolkit $