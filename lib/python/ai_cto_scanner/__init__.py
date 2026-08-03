"""
AI CTO Integration Scanner — CORE-008A

First intelligence layer of AI CTO.
Inspects an arbitrary software repository and understands its architecture.
"""

from .engine import AICTOScanner, AICTOScannerEngine

__all__ = ["AICTOScannerEngine", "AICTOScanner"]
