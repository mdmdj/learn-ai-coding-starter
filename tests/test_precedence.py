"""Multiplication binds tighter than addition.

The precedence ladder lives in sloperator/parser/parser.py: ``term`` handles
PLUS/MINUS and calls ``factor`` for STAR/SLASH, so multiplication is parsed
deeper in the tree and therefore happens first.
"""

import pytest

from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Binary, ExprStmt, Literal
from sloperator.runner import run_source


def only_expression(source: str):
    (statement,) = parse(tokenize(source))
    assert isinstance(statement, ExprStmt)
    return statement.expression


@pytest.mark.parametrize(
    ("source", "outer_operator", "inner_side"),
    [
        ("2 + 3 * 4✨", TokenType.PLUS, "right"),
        ("2 * 3 + 4✨", TokenType.PLUS, "left"),
    ],
)
def test_multiplication_is_parsed_below_addition(
    source: str, outer_operator: TokenType, inner_side: str
) -> None:
    expr = only_expression(source)
    assert isinstance(expr, Binary)
    assert expr.operator.type is outer_operator

    inner = expr.right if inner_side == "right" else expr.left
    assert isinstance(inner, Binary)
    assert inner.operator.type is TokenType.STAR
    assert isinstance(inner.left, Literal) and isinstance(inner.right, Literal)


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("hallucinate(2 + 3 * 4)✨", "14"),
        ("hallucinate(2 * 3 + 4)✨", "10"),
    ],
)
def test_multiplication_evaluates_before_addition(source: str, expected: str) -> None:
    result = run_source(source)
    assert result.stderr == ""
    assert result.stdout == f"{expected}\n"
