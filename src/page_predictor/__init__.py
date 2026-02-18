"""Deterministic LaTeX page counter."""

from page_predictor.config import CompilationConfig, LatexEngine
from page_predictor.counter import count_pages, optimize_to_fit
from page_predictor.errors import (
    LatexCompilationError,
    LatexTimeoutError,
    PagePredictorError,
    PdfReadError,
)

__all__ = [
    "count_pages",
    "optimize_to_fit",
    "CompilationConfig",
    "LatexEngine",
    "PagePredictorError",
    "LatexCompilationError",
    "PdfReadError",
    "LatexTimeoutError",
]
