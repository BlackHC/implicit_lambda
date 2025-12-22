import math
import pytest
import hypothesis
import hypothesis.strategies as strategies

import implicit_lambda as implicit_lambda
from implicit_lambda.details import lambda_dsl
from implicit_lambda.details import expression
from implicit_lambda.details import codegen
from implicit_lambda.details import interpret


def capture_exception(func):
    try:
        func()
    except Exception as e:
        return e
    return None


@hypothesis.given(x=strategies.integers(-1024, 1024), y=strategies.integers(-63, 63))
@pytest.mark.parametrize(
    "op", expression.Ops - set([expression.ArithmeticOps.MATMUL, expression.ArithmeticOps.RMATMUL])
)
def test_exprs(op, x: int, y: int):
    expr = expression.OpExpression(op, op.value.num_args, x, y, None)
    elambda = interpret.to_lambda(expr)

    hypothesis.assume(not capture_exception(elambda))

    clambda = codegen.compile(expr)
    hypothesis.note(clambda.code)
    assert elambda() == clambda()


@hypothesis.given(x=strategies.integers(-1024, 1024), y=strategies.integers(-63, 63))
@pytest.mark.parametrize(
    "op", expression.Ops - set([expression.ArithmeticOps.MATMUL, expression.ArithmeticOps.RMATMUL])
)
def test_implicit_lambdas(op: expression.Ops, x: int, y: int):
    code = op.value.template.format("x", "y")

    def code_lambda():
        return eval(code, None, dict(x=x, y=y))

    dsl = op.value.template.format("lambda_dsl.LambdaDSL(x)", "lambda_dsl.LambdaDSL(y)")
    dsl_lambda = implicit_lambda.to_lambda(eval(dsl))

    hypothesis.assume(not capture_exception(code_lambda))

    hypothesis.note(code)
    hypothesis.note(dsl_lambda.code)
    assert code_lambda() == dsl_lambda()


@hypothesis.given(x=strategies.integers(-1024, 1024), y=strategies.integers(0, 15))
def test_pow(x, y):
    expr = expression.OpExpression(expression.OptionalArgOps.POW_2, 2, x, y, None)
    assert codegen.compile(expr)() == x ** y

    expr = expression.OpExpression(expression.OptionalArgOps.POW_3, 3, x, y, 1024)
    assert codegen.compile(expr)() == pow(x, y, 1024)


@hypothesis.given(x=strategies.floats(allow_infinity=False, allow_nan=False), n=strategies.integers(1, 10))
def test_round(x, n):
    expr = expression.OpExpression(expression.OptionalArgOps.ROUND_1, 1, x, None, None)
    assert codegen.compile(expr)() == round(x)

    expr = expression.OpExpression(expression.OptionalArgOps.ROUND_2, 2, x, n, None)
    assert codegen.compile(expr)() == round(x, n)


@hypothesis.given(x=strategies.floats(allow_infinity=False, allow_nan=False), n=strategies.integers(1, 10))
def test_round_interpreter(x, n):
    """Test that interpreter correctly handles round operations (regression test for math.round bug)."""
    # Test ROUND_1 with interpreter
    expr = expression.OpExpression(expression.OptionalArgOps.ROUND_1, 1, x, None, None)
    elambda = interpret.to_lambda(expr)
    clambda = codegen.compile(expr)
    assert elambda() == clambda() == round(x)

    # Test ROUND_2 with interpreter
    expr = expression.OpExpression(expression.OptionalArgOps.ROUND_2, 2, x, n, None)
    elambda = interpret.to_lambda(expr)
    clambda = codegen.compile(expr)
    assert elambda() == clambda() == round(x, n)


def test_logical_not_num_args():
    """Test that LOGICAL_NOT has correct num_args (regression test for num_args=2 bug)."""
    logical_not_op = expression.SpecialOps.LOGICAL_NOT.value
    # LOGICAL_NOT should have 1 argument, not 2
    assert logical_not_op.num_args == 1
    # Template should have exactly 1 placeholder
    assert logical_not_op.template.count("{}") == 1
