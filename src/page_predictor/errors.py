"""Custom exception hierarchy for the page predictor."""


class PagePredictorError(Exception):
    """Base exception for all page predictor errors."""


class LatexCompilationError(PagePredictorError):
    """Raised when LaTeX compilation fails.

    Attributes:
        latex_log: The full TeX log output for debugging.
        return_code: The process exit code.
    """

    def __init__(self, message: str, latex_log: str = "", return_code: int = -1):
        self.latex_log = latex_log
        self.return_code = return_code
        super().__init__(message)


class PdfReadError(PagePredictorError):
    """Raised when the page count cannot be read from the compiled PDF."""


class LatexTimeoutError(PagePredictorError):
    """Raised when LaTeX compilation exceeds the configured timeout."""

    def __init__(self, timeout_seconds: float):
        self.timeout_seconds = timeout_seconds
        super().__init__(
            f"LaTeX compilation timed out after {timeout_seconds} seconds"
        )
