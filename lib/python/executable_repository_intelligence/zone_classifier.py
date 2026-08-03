"""
Executable Repository Intelligence — Zone Classifier
CORE-008C

Automatically classifies repository directories into zones:

  Runtime        — directories containing executable runtime code
  Documentation  — directories containing documentation only
  Generated      — directories containing generated artifacts
  Configuration  — directories containing config / environment files
  Testing        — directories containing tests
  Infrastructure — CI/CD, Docker, deployment tooling
  Deployment     — deployment-specific directories
  Canonical      — canonical specification documents
  Experimental   — exploratory or experimental code
"""

from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple

from .models import FileClassification, RepositoryZone, ZONE_CATEGORIES


# Map from file category to zone vote
_CATEGORY_TO_ZONE: Dict[str, str] = {
    "Executable Code": "Runtime",
    "Runtime Entry Point": "Runtime",
    "Bootstrap": "Runtime",
    "Public API": "Runtime",
    "Internal API": "Runtime",
    "Plugin API": "Runtime",
    "Extension Point": "Runtime",
    "Documentation": "Documentation",
    "Canonical Specification": "Canonical",
    "Generated Artifact": "Generated",
    "Reports": "Generated",
    "Tests": "Testing",
    "Scripts": "Runtime",
    "Infrastructure": "Infrastructure",
    "Assets": "Documentation",
    "Configuration": "Configuration",
    "Environment": "Configuration",
    "Temporary": "Generated",
    "Deprecated": "Generated",
    "Unknown": "Runtime",
}

# Explicit directory overrides (path substring → zone)
_DIR_OVERRIDES: List[Tuple[str, str]] = [
    ("/.github/", "Infrastructure"),
    ("/tests/", "Testing"),
    ("/test/", "Testing"),
    ("/spec/", "Testing"),
    ("/docs/", "Documentation"),
    ("/doc/", "Documentation"),
    ("/docs/canonical/", "Canonical"),
    ("/canonical/", "Canonical"),
    ("/deploy/", "Deployment"),
    ("/deployment/", "Deployment"),
    ("/k8s/", "Deployment"),
    ("/helm/", "Deployment"),
    ("/infrastructure/", "Infrastructure"),
    ("/experimental/", "Experimental"),
    ("/experiments/", "Experimental"),
    ("/tmp/", "Generated"),
    ("/build/", "Generated"),
    ("/dist/", "Generated"),
    ("/audit/", "Generated"),
    ("/.ai/", "Generated"),
]


class ZoneClassifier:
    """
    Classifies repository directories into zones.

    Aggregates per-file classifications to determine the dominant
    zone for each directory.  Uses majority-vote over the canonical
    file categories.
    """

    def classify(
        self,
        file_classifications: List[FileClassification],
        root: Path,
    ) -> List[RepositoryZone]:
        """Classify all directories and return a sorted, deterministic list."""
        # Group files by top-level directory (relative path prefix)
        dir_files: Dict[str, List[FileClassification]] = defaultdict(list)

        for fc in file_classifications:
            dir_path = str(Path(fc.path).parent)
            dir_files[dir_path].append(fc)

        zones: List[RepositoryZone] = []
        for dir_path, fcs in sorted(dir_files.items()):
            zone = self._determine_zone(dir_path, fcs)
            zones.append(RepositoryZone(
                path=dir_path,
                zone=zone,
                file_count=len(fcs),
                evidence=self._build_evidence(dir_path, fcs, zone),
            ))

        return zones

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _determine_zone(self, dir_path: str, fcs: List[FileClassification]) -> str:
        # Explicit overrides take highest priority
        check_path = "/" + dir_path + "/"
        for pattern, zone in _DIR_OVERRIDES:
            if pattern in check_path:
                return zone

        # Vote by file category
        votes: Dict[str, int] = defaultdict(int)
        for fc in fcs:
            vote = _CATEGORY_TO_ZONE.get(fc.category, "Runtime")
            votes[vote] += 1

        if not votes:
            return "Runtime"

        # Winner = zone with most votes; tie-break by ZONE_CATEGORIES order
        return max(
            votes.keys(),
            key=lambda z: (votes[z], -ZONE_CATEGORIES.index(z) if z in ZONE_CATEGORIES else 0),
        )

    def _build_evidence(
        self, dir_path: str, fcs: List[FileClassification], zone: str
    ) -> List[str]:
        category_counts: Dict[str, int] = defaultdict(int)
        for fc in fcs:
            category_counts[fc.category] += 1

        evidence = ["Zone: %s (%d files)" % (zone, len(fcs))]
        top = sorted(category_counts.items(), key=lambda kv: -kv[1])[:3]
        for cat, cnt in top:
            evidence.append("%s: %d file(s)" % (cat, cnt))
        return evidence
