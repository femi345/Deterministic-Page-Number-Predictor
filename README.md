# Deterministic Page Number Predictor

A fast, deterministic tool that compiles LaTeX source strings and returns the exact page count of the resulting PDF.

Know exactly how many pages a LaTeX compilation produces, right from your CLI. Built for upstream integration.

## Installation

```bash
pip install -e .
```

Requires a TeX Live installation with `pdflatex` (default), `xelatex`, or `lualatex`.

## Usage

```python
from page_predictor import count_pages

latex = r"""
\documentclass{article}
\begin{document}
Hello, world!
\end{document}
"""

print(count_pages(latex))  # 1
```

### Custom engine

```python
from page_predictor import count_pages, CompilationConfig, LatexEngine

config = CompilationConfig(engine=LatexEngine.XELATEX)
count_pages(latex, config=config)
```

### Error handling

```python
from page_predictor import count_pages
from page_predictor.errors import LatexCompilationError, LatexTimeoutError

try:
    count_pages(bad_latex)
except LatexCompilationError as e:
    print(e)            # Human-readable error message
    print(e.latex_log)  # Full TeX log for debugging
except LatexTimeoutError as e:
    print(e.timeout_seconds)
```

## How it works

1. Writes the LaTeX string to a temp directory
2. Compiles with `pdflatex` in batch mode (no interactive prompts, no shell escape)
3. Extracts page count using three independent strategies (log parsing, raw PDF binary parsing, pypdf) and cross-validates
4. Cleans up all temp files automatically

Determinism is guaranteed by pinning `SOURCE_DATE_EPOCH=0`, inheriting only essential environment variables, and isolating each compilation in its own temp directory.

## Performance

~150-200ms per call for a typical one-page document on Apple Silicon.

## Running tests

```bash
pip install -e ".[dev]"
pytest
```

## Future work

The `optimizer.py` module contains extension points for a resume optimization feature that will:

- Accept a job description as input
- Apply incremental transformations (margin, spacing, font size, content trimming) to fit a resume to exactly one page
- Prioritize content sections by relevance to the target job

See `page_predictor.optimizer` for the `Transformation` protocol and `ContentPrioritizer` abstract base class.
