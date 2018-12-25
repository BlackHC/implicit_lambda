import math
import pytest
import hypothesis
import hypothesis.strategies as strategies

import blackhc.implicit_lambda as implicit_lambda
from blackhc.implicit_lambda.details import lambda_dsl
from blackhc.implicit_lambda.details import expression
from blackhc.implicit_lambda.details import codegen
from blackhc.implicit_lambda.details import interpret


def test_repr():
    assert repr(implicit_lambda._ + 5) == "<LambdaDSL: lambda x: (x + 5) @ {}>"


def test_str():
    assert repr(implicit_lambda._ + 5) == "<LambdaDSL: lambda x: (x + 5) @ {}>"


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
