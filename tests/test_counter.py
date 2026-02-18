"""Integration tests for the count_pages() public API."""

import glob
import tempfile

import pytest

from page_predictor import CompilationConfig, LatexEngine, count_pages
from page_predictor.errors import LatexCompilationError, LatexTimeoutError


class TestCountPages:
    def test_single_page(self, minimal_latex):
        assert count_pages(minimal_latex) == 1

    def test_two_pages(self, two_page_latex):
        assert count_pages(two_page_latex) == 2

    def test_realistic_resume(self, realistic_resume):
        assert count_pages(realistic_resume) == 1

    def test_deterministic(self, minimal_latex):
        """Same input must always produce the same output."""
        results = [count_pages(minimal_latex) for _ in range(3)]
        assert len(set(results)) == 1

    def test_compilation_error(self, invalid_latex):
        with pytest.raises(LatexCompilationError) as exc_info:
            count_pages(invalid_latex)
        assert exc_info.value.latex_log  # log should be populated

    def test_timeout(self, minimal_latex):
        config = CompilationConfig(timeout_seconds=0.001)
        with pytest.raises(LatexTimeoutError):
            count_pages(minimal_latex, config=config)

    def test_custom_engine_xelatex(self, minimal_latex):
        config = CompilationConfig(engine=LatexEngine.XELATEX)
        assert count_pages(minimal_latex, config=config) == 1

    def test_no_temp_files_leaked(self, minimal_latex):
        before = set(glob.glob(f"{tempfile.gettempdir()}/page_predictor_*"))
        count_pages(minimal_latex)
        after = set(glob.glob(f"{tempfile.gettempdir()}/page_predictor_*"))
        assert after == before

    def test_fixture_file(self):
        """Test with the sample_resume.tex fixture file."""
        from pathlib import Path

        fixture = Path(__file__).parent / "fixtures" / "sample_resume.tex"
        latex_source = fixture.read_text()
        assert count_pages(latex_source) == 1
