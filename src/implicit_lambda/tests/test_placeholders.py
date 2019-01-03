import pytest

from implicit_lambda import to_lambda, x, y
from implicit_lambda.details import expression


@pytest.mark.parametrize("op", expression.ComparisonOps)
def test_placeholders(op: expression.Ops):
    code = op.value.template.format("x", "y")
    expr = eval(code)
    dsl_lambda = to_lambda(expr)

    assert dsl_lambda.code == f"(lambda x, y: {code})"
