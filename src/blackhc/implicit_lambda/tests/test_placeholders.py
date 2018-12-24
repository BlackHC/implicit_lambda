import pytest

from blackhc.implicit_lambda import to_lambda, x, y
from blackhc.implicit_lambda.details import expression


@pytest.mark.parametrize("op", set(expression.BinaryOps) - set([expression.BinaryOps.MATMUL]))
def test_placeholders(op: expression.BinaryOps):
    code = op.value[1].format("x", "y")
    expr = eval(code)
    dsl_lambda = to_lambda(expr)

    assert dsl_lambda.code == f"lambda x, y: {code}"
