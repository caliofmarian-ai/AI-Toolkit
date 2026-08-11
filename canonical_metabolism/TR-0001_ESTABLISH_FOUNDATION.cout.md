Welcome to Termux

Docs:       https://doc.termux.com
Community:  https://community.termux.com

Working with packages:
 - Search:  pkg search <query>
 - Install: pkg install <package>
 - Upgrade: pkg upgrade

Report issues at https://bugs.termux.com
~ $ cd ~/storage/shared/AI-Projects/AI-Toolkit || exit 1

set -euo pipefail

ROOT="work/rebuild"

mkdir -p "$ROOT"

mkdir -p "$ROOT"/CEP-000_CANONICAL_CONSTITUTION
mkdir -p "$ROOT"/CEP-001_ONTOLOGY
mkdir -p "$ROOT"/CEP-002_AXIOMS
mkdir -p "$ROOT"/CEP-003_VALUES
mkdir -p "$ROOT"/CEP-004_IDENTITY
mkdir -p "$ROOT"/CEP-005_PERCEPTION
mkdir -p "$ROOT"/CEP-006_MEMORY
mkdir -p "$ROOT"/CEP-007_JUDGMENT
mkdir -p "$ROOT"/CEP-008_HOMEOSTASIS
mkdir -p "$ROOT"/CEP-009_REALITY
mkdir -p "$ROOT"/CEP-010_CSL

cat > "$ROOT/README.md" <<'EOF'
Canonical Engineering Foundation

Research Status:
FOUNDATION LOCKED

Implementation Phase:
STARTED

The objective of this rebuild is not to create a programming language.

The objective is to formally define the Epistemic Organism and then derive CSL from that organism.

Every document must satisfy:

- Canonical Identity
- Canonical Meaning
- Canonical Purpose
- Canonical Relations
- Canonical Justification

CSL is derived from Canon.

Code is derived from CSL.

Reality continuously validates Canon.
EOF

echo
echo "========================================="
echo "FOUNDATION CREATED"
echo "========================================="

find "$ROOT" -maxdepth 1 -type d | sort

=========================================
FOUNDATION CREATED
=========================================
work/rebuild
work/rebuild/AR
work/rebuild/CDM-000_FOUNDATION
work/rebuild/CEP-000_CANONICAL_CONSTITUTION
work/rebuild/CEP-001_ONTOLOGY
work/rebuild/CEP-002_AXIOMS
work/rebuild/CEP-003_VALUES
work/rebuild/CEP-004_IDENTITY
work/rebuild/CEP-005_PERCEPTION
work/rebuild/CEP-006_MEMORY
work/rebuild/CEP-007_JUDGMENT
work/rebuild/CEP-008_HOMEOSTASIS
work/rebuild/CEP-009_REALITY
work/rebuild/CEP-010_CSL
~/.../AI-Projects/AI-Toolkit $