"""Regression tests for lexer error handling bugs fixed after the initial commit."""

import pytest

from sloperator.errors import LexicalError
from sloperator.lexer import TokenType, tokenize


def test_generic_unexpected_character_reports_character_not_charcter():
    """Regression: the fallback branch misspelled "character" as "charcter"."""
    with pytest.raises(LexicalError) as info:
        tokenize("a % b")

    assert info.value.line == 1
    assert info.value.message == "unexpected character '%'"
    assert str(info.value) == ("SlopLang lexical error at line 1: unexpected character '%'")
    assert "charcter" not in str(info.value)


def test_comment_newline_advances_line_number():
    """Regression: consuming a comment's trailing newline skipped the line count."""
    tokens = tokenize("x — comment\ny")

    assert [token.lexeme for token in tokens] == ["x", "y", ""]
    assert tokens[1].line == 2
    assert tokens[2].line == 2


def test_comment_at_end_of_file_does_not_advance_past_last_line():
    tokens = tokenize("x — comment")

    assert tokens[-1].type is TokenType.EOF
    assert tokens[-1].line == 1
