"""Configuration for LaTeX compilation."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class LatexEngine(Enum):
    """Supported LaTeX compilation engines."""

    PDFLATEX = "pdflatex"
    XELATEX = "xelatex"
    LUALATEX = "lualatex"


@dataclass(frozen=True)
class CompilationConfig:
    """Immutable configuration for LaTeX compilation.

    Frozen to prevent accidental mutation, supporting deterministic behavior.
    """

    engine: LatexEngine = LatexEngine.PDFLATEX
    timeout_seconds: float = 30.0
    extra_args: tuple[str, ...] = ()

    # Future extension points for resume optimization (unused for now)
    job_description: Optional[str] = field(default=None, repr=False)
    target_pages: Optional[int] = field(default=None, repr=False)
