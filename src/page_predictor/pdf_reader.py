"""PDF page count extraction with multiple fallback strategies."""

import re
from pathlib import Path
from typing import Optional

from page_predictor.errors import PdfReadError

# Matches pdflatex log: "Output written on doc.pdf (N page(s), M bytes)."
_LOG_PATTERN = re.compile(r"Output written on .+\((\d+) pages?\,")

# Matches root /Pages object with /Count in raw PDF bytes
_PDF_PAGES_PATTERN = re.compile(
    rb"/Type\s*/Pages\b.*?/Count\s+(\d+)", re.DOTALL
)


def count_pdf_pages(pdf_path: Path, log_path: Optional[Path] = None) -> int:
    """Count pages in a PDF using the best available method.

    Strategy priority (when results disagree): pypdf > log > binary.
    All available strategies are attempted for cross-validation.

    Args:
        pdf_path: Path to the compiled PDF file.
        log_path: Optional path to the .log file from compilation.

    Returns:
        Integer page count.

    Raises:
        PdfReadError: If no strategy can determine the page count.
    """
    results: dict[str, int] = {}

    if log_path and log_path.exists():
        count = _count_from_log(log_path)
        if count is not None:
            results["log"] = count

    if pdf_path.exists():
        count = _count_from_pdf_binary(pdf_path)
        if count is not None:
            results["binary"] = count

    count = _count_from_pypdf(pdf_path)
    if count is not None:
        results["pypdf"] = count

    if not results:
        raise PdfReadError(
            f"Could not determine page count from {pdf_path}. "
            "No extraction method succeeded."
        )

    # All agree — return immediately
    if len(set(results.values())) == 1:
        return next(iter(results.values()))

    # Disagreement — prefer most reliable method
    for method in ("pypdf", "log", "binary"):
        if method in results:
            return results[method]

    raise PdfReadError("Could not determine page count")


def _count_from_log(log_path: Path) -> Optional[int]:
    """Extract page count from the TeX log file."""
    try:
        content = log_path.read_text(encoding="utf-8", errors="replace")
        match = _LOG_PATTERN.search(content)
        if match:
            return int(match.group(1))
    except (OSError, ValueError):
        pass
    return None


def _count_from_pdf_binary(pdf_path: Path) -> Optional[int]:
    """Extract page count by parsing raw PDF bytes.

    Finds /Type /Pages objects and reads /Count. The root node has the
    highest count (child nodes hold subsets).
    """
    try:
        data = pdf_path.read_bytes()
        matches = _PDF_PAGES_PATTERN.findall(data)
        if matches:
            counts = [int(m) for m in matches]
            return max(counts)
    except (OSError, ValueError):
        pass
    return None


def _count_from_pypdf(pdf_path: Path) -> Optional[int]:
    """Extract page count using pypdf (if installed)."""
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(pdf_path))
        return len(reader.pages)
    except ImportError:
        return None
    except Exception:
        return None
