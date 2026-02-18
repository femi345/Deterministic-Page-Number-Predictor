"""Core public API: count_pages() and future optimize_to_fit() stub."""

import tempfile
from pathlib import Path

from page_predictor.compiler import compile_latex
from page_predictor.config import CompilationConfig
from page_predictor.pdf_reader import count_pdf_pages


def count_pages(
    latex_source: str,
    config: CompilationConfig | None = None,
) -> int:
    """Count the number of pages a LaTeX document will produce.

    Compiles the LaTeX source to PDF in a temporary directory, extracts
    the page count, and cleans up all temporary files.

    Args:
        latex_source: A complete LaTeX document string (must include
            \\documentclass, \\begin{document}, etc.).
        config: Optional compilation configuration. Defaults to pdflatex
            with a 30-second timeout.

    Returns:
        The number of pages in the compiled PDF.

    Raises:
        LatexCompilationError: If the LaTeX source fails to compile.
        PdfReadError: If the page count cannot be extracted.
        LatexTimeoutError: If compilation exceeds the timeout.
    """
    if config is None:
        config = CompilationConfig()

    with tempfile.TemporaryDirectory(prefix="page_predictor_") as tmpdir:
        work_dir = Path(tmpdir)
        pdf_path = compile_latex(latex_source, config, work_dir)
        log_path = work_dir / "document.log"
        return count_pdf_pages(pdf_path, log_path)


# ──────────────────────────────────────────────────────────────
# Future extension point: optimize_to_fit()
# ──────────────────────────────────────────────────────────────


def optimize_to_fit(
    latex_source: str,
    target_pages: int = 1,
    job_description: str | None = None,
    config: CompilationConfig | None = None,
) -> str:
    """Optimize LaTeX source to fit within a target page count.

    Not yet implemented. Future implementation will:
    1. Count current pages.
    2. If over target, apply transformations in order of aggressiveness:
       a. Reduce vertical spacing (vspace, itemsep, parsep).
       b. Adjust margins.
       c. Reduce font size.
       d. If job_description is provided, use it to prioritize which
          content sections to trim vs. keep.
    3. Re-count after each transformation until target is met.

    See optimizer.py for the Transformation protocol and stub classes.

    Args:
        latex_source: The original LaTeX document.
        target_pages: Desired maximum page count (default: 1).
        job_description: Optional job description for content prioritization.
        config: Optional compilation configuration.

    Returns:
        Modified LaTeX source that fits within target_pages.

    Raises:
        NotImplementedError: Always (this is a stub).
    """
    raise NotImplementedError(
        "optimize_to_fit() is planned for a future release. "
        "See page_predictor.optimizer for the extension point design."
    )
