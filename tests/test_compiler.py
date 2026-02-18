"""Unit tests for the LaTeX compiler module."""

from page_predictor.compiler import _build_deterministic_env, _extract_error_message


class TestDeterministicEnv:
    def test_source_date_epoch_set(self):
        env = _build_deterministic_env()
        assert env["SOURCE_DATE_EPOCH"] == "0"
        assert env["FORCE_SOURCE_DATE"] == "1"

    def test_path_inherited(self):
        env = _build_deterministic_env()
        assert "PATH" in env

    def test_no_locale_leak(self):
        env = _build_deterministic_env()
        assert "LANG" not in env
        assert "LC_ALL" not in env


class TestExtractErrorMessage:
    def test_tex_error_line(self):
        log = "Some stuff\n! Undefined control sequence.\nl.5 \\badcommand\n"
        msg = _extract_error_message(log, b"")
        assert "Undefined control sequence" in msg

    def test_stderr_fallback(self):
        msg = _extract_error_message("", b"something went wrong")
        assert "something went wrong" in msg

    def test_no_info_available(self):
        msg = _extract_error_message("", b"")
        assert "no detailed error" in msg
