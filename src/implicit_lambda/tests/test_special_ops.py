import math
import pytest
import hypothesis
import hypothesis.strategies as strategies

import implicit_lambda as implicit_lambda
from implicit_lambda.details import lambda_dsl
from implicit_lambda.details import expression
from implicit_lambda.details import codegen
from implicit_lambda.details import interpret


def test_repr():
    assert repr(implicit_lambda._ + 5) == "<LambdaDSL: (lambda _: (_ + 5)) @ {}>"


def test_str():
    assert repr(implicit_lambda._ + 5) == "<LambdaDSL: (lambda _: (_ + 5)) @ {}>"


def test_index():
    with pytest.raises(NotImplementedError):
        hex(implicit_lambda._ + 5)

    with pytest.raises(NotImplementedError):
        oct(implicit_lambda._ + 5)

    with pytest.raises(NotImplementedError):
        bin(implicit_lambda._ + 5)


def test_int():
    with pytest.raises(NotImplementedError):
        int(implicit_lambda._)


def test_float():
    with pytest.raises(NotImplementedError):
        float(implicit_lambda._)


def test_complex():
    with pytest.raises(NotImplementedError):
        complex(implicit_lambda._)


def test_len():
    with pytest.raises(NotImplementedError):
        len(implicit_lambda._)


def test_bool():
    with pytest.raises(NotImplementedError):
        bool(implicit_lambda._)


def test_contains():
    with pytest.raises(NotImplementedError):
        None in implicit_lambda._


def test_not_contains():
    with pytest.raises(NotImplementedError):
        None not in implicit_lambda._


def test_contains_wrappers():
    assert (
        repr(implicit_lambda.contains(implicit_lambda.a, implicit_lambda.b))
        == "<LambdaDSL: (lambda a, b: (b) in (a)) @ {}>"
    )


def test_not_contains_wrappers():
    assert (
        repr(implicit_lambda.not_contains(implicit_lambda.a, implicit_lambda.b))
        == "<LambdaDSL: (lambda a, b: (b) not in (a)) @ {}>"
    )


def test_logical_and():
    assert (
        repr(implicit_lambda.logical_and(implicit_lambda.a, implicit_lambda.b))
        == "<LambdaDSL: (lambda a, b: (a) and (b)) @ {}>"
    )
    assert (
        repr(implicit_lambda.logical_and(implicit_lambda.a, implicit_lambda.b, implicit_lambda.c))
        == "<LambdaDSL: (lambda a, b, c: (a) and ((b) and (c))) @ {}>"
    )


def test_logical_or():
    assert (
        repr(implicit_lambda.logical_or(implicit_lambda.a, implicit_lambda.b))
        == "<LambdaDSL: (lambda a, b: (a) or (b)) @ {}>"
    )
    assert (
        repr(implicit_lambda.logical_or(implicit_lambda.a, implicit_lambda.b, implicit_lambda.c))
        == "<LambdaDSL: (lambda a, b, c: (a) or ((b) or (c))) @ {}>"
    )


def test_logical_not():
    assert (
        repr(implicit_lambda.logical_not(implicit_lambda.a))
        == "<LambdaDSL: (lambda a: not(a)) @ {}>"
    )
