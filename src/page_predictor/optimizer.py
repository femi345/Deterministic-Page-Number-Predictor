"""Future resume optimization module.

Defines interfaces and extension points for the resume optimization
feature. The actual implementation is not yet built, but the architecture
is designed here so future work can plug in without restructuring.

Architecture:
    1. ResumeOptimizer (future) orchestrates the optimization loop.
    2. Transformation objects represent individual tweaks (margin changes,
       font size changes, content removal).
    3. Each Transformation has an apply() method and an aggressiveness score.
    4. The optimizer applies transformations least-aggressive-first,
       checking page count after each.
    5. When a job_description is provided, a ContentPrioritizer
       scores resume sections by relevance, and the optimizer
       removes least-relevant sections first.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol


class Transformation(Protocol):
    """Protocol for LaTeX transformations that reduce page count."""

    @property
    def name(self) -> str: ...

    @property
    def aggressiveness(self) -> float:
        """0.0 (subtle) to 1.0 (drastic). Lower values are applied first."""
        ...

    def apply(self, latex_source: str) -> str:
        """Return modified LaTeX source with this transformation applied."""
        ...


class ContentPrioritizer(ABC):
    """Abstract base for scoring resume sections by job relevance."""

    @abstractmethod
    def score_sections(
        self, latex_source: str, job_description: str
    ) -> dict[str, float]:
        """Score each section by relevance (0.0-1.0, higher = keep)."""
        ...


# ── Stub transformations (not implemented) ──────────────────


@dataclass
class MarginAdjustment:
    """Reduce page margins to gain space."""

    name: str = "margin_adjustment"
    aggressiveness: float = 0.2

    def apply(self, latex_source: str) -> str:
        raise NotImplementedError


@dataclass
class SpacingReduction:
    """Reduce vertical spacing between sections."""

    name: str = "spacing_reduction"
    aggressiveness: float = 0.3

    def apply(self, latex_source: str) -> str:
        raise NotImplementedError


@dataclass
class FontSizeReduction:
    """Reduce font size by one step."""

    name: str = "font_size_reduction"
    aggressiveness: float = 0.4

    def apply(self, latex_source: str) -> str:
        raise NotImplementedError


@dataclass
class ContentTrimming:
    """Remove least-relevant content sections."""

    name: str = "content_trimming"
    aggressiveness: float = 0.8

    def apply(self, latex_source: str) -> str:
        raise NotImplementedError
