"""Unit tests for PDF page count extraction strategies."""

import pytest

from page_predictor.errors import PdfReadError
from page_predictor.pdf_reader import (
    _count_from_log,
    _count_from_pdf_binary,
    count_pdf_pages,
)


class TestLogParsing:
    def test_single_page(self, tmp_path):
        log = tmp_path / "test.log"
        log.write_text("Output written on doc.pdf (1 page, 12345 bytes).\n")
        assert _count_from_log(log) == 1

    def test_multiple_pages(self, tmp_path):
        log = tmp_path / "test.log"
        log.write_text("Output written on doc.pdf (3 pages, 54321 bytes).\n")
        assert _count_from_log(log) == 3

    def test_missing_log(self, tmp_path):
        assert _count_from_log(tmp_path / "nonexistent.log") is None


class TestBinaryParsing:
    def test_missing_file(self, tmp_path):
        assert _count_from_pdf_binary(tmp_path / "no.pdf") is None

    def test_not_a_pdf(self, tmp_path):
        fake = tmp_path / "fake.pdf"
        fake.write_bytes(b"not a pdf at all")
        assert _count_from_pdf_binary(fake) is None


class TestCountPdfPages:
    def test_no_methods_succeed(self, tmp_path):
        fake_pdf = tmp_path / "empty.pdf"
        fake_pdf.write_bytes(b"not a pdf")
        with pytest.raises(PdfReadError):
            count_pdf_pages(fake_pdf)
