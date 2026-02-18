"""LaTeX compilation via subprocess with deterministic output."""

import os
import subprocess
from pathlib import Path

from page_predictor.config import CompilationConfig
from page_predictor.errors import LatexCompilationError, LatexTimeoutError

# Environment variables that ensure deterministic PDF output
_DETERMINISTIC_ENV = {
    "SOURCE_DATE_EPOCH": "0",
    "FORCE_SOURCE_DATE": "1",
}

# Flags applied to every compilation for safety and non-interactivity
_BASE_ARGS = (
    "-interaction=batchmode",
    "-halt-on-error",
    "-no-shell-escape",
)


def compile_latex(
    latex_source: str,
    config: CompilationConfig,
    work_dir: Path,
) -> Path:
    """Compile LaTeX source to PDF in the given working directory.

    Args:
        latex_source: Complete LaTeX document source code.
        config: Compilation configuration.
        work_dir: Directory to write temporary files into.

    Returns:
        Path to the generated PDF file.

    Raises:
        LatexCompilationError: If compilation fails.
        LatexTimeoutError: If compilation exceeds the timeout.
    """
    tex_file = work_dir / "document.tex"
    pdf_file = work_dir / "document.pdf"
    log_file = work_dir / "document.log"

    tex_file.write_text(latex_source, encoding="utf-8")

    cmd = [
        config.engine.value,
        *_BASE_ARGS,
        *config.extra_args,
        f"-output-directory={work_dir}",
        "-jobname=document",
        str(tex_file),
    ]

    env = _build_deterministic_env()

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=config.timeout_seconds,
            cwd=str(work_dir),
            env=env,
        )
    except subprocess.TimeoutExpired:
        raise LatexTimeoutError(config.timeout_seconds)

    if result.returncode != 0 or not pdf_file.exists():
        log_content = ""
        if log_file.exists():
            log_content = log_file.read_text(encoding="utf-8", errors="replace")
        error_msg = _extract_error_message(log_content, result.stderr)
        raise LatexCompilationError(
            message=error_msg,
            latex_log=log_content,
            return_code=result.returncode,
        )

    return pdf_file


def _build_deterministic_env() -> dict[str, str]:
    """Build environment variables for deterministic compilation.

    Inherits only what TeX needs (PATH, HOME, TEXMF vars) and adds
    determinism-ensuring variables.
    """
    inherited_keys = ("PATH", "HOME", "TEXMFHOME", "TEXMFVAR", "TEXMFCONFIG")
    env = {k: v for k, v in os.environ.items() if k in inherited_keys}
    env.update(_DETERMINISTIC_ENV)
    return env


def _extract_error_message(log_content: str, stderr: bytes) -> str:
    """Extract a human-readable error message from TeX output.

    Looks for lines starting with '!' in the log, which is TeX's
    convention for error messages.
    """
    if log_content:
        error_lines = [
            line.strip()
            for line in log_content.splitlines()
            if line.strip().startswith("!")
        ]
        if error_lines:
            return f"LaTeX compilation failed: {error_lines[0]}"

    stderr_text = stderr.decode("utf-8", errors="replace").strip()
    if stderr_text:
        return f"LaTeX compilation failed: {stderr_text[:500]}"

    return "LaTeX compilation failed (no detailed error available)"
