import pytest
import hypothesis
import hypothesis.strategies as strategies

import blackhc.implicit_lambda as implicit_lambda
from blackhc.implicit_lambda.details import lambda_dsl
from blackhc.implicit_lambda.details import expression
from blackhc.implicit_lambda.details import codegen
from blackhc.implicit_lambda.details import interpret


def capture_exception(func):
    try:
        func()
    except Exception as e:
        return e
    return None


@hypothesis.given(x=strategies.integers(-1024, 1024), y=strategies.integers(-63, 63))
@pytest.mark.parametrize("op", set(expression.BinaryOps) - set([expression.BinaryOps.MATMUL]))
def test_exprs(op, x: int, y: int):
    expr = expression.BinaryExpression(op, x, y)
    elambda = interpret.to_lambda(expr)

    hypothesis.assume(not capture_exception(elambda))

    clambda = codegen.compile(expr)
    hypothesis.note(clambda.code)
    assert elambda() == clambda()


@hypothesis.given(x=strategies.integers(-1024, 1024), y=strategies.integers(-63, 63))
@pytest.mark.parametrize("op", set(expression.BinaryOps) - set([expression.BinaryOps.MATMUL]))
def test_implicit_lambdas(op: expression.BinaryOps, x: int, y: int):
    code = op.value[1].format("x", "y")
    code_lambda = lambda: eval(code, None, dict(x=x, y=y))

    dsl = op.value[1].format("lambda_dsl.LambdaDSL(x)", "lambda_dsl.LambdaDSL(y)")
    dsl_lambda = implicit_lambda.to_lambda(eval(dsl))

    hypothesis.assume(not capture_exception(code_lambda))

    hypothesis.note(code)
    hypothesis.note(dsl_lambda.code)
    assert code_lambda() == dsl_lambda()
