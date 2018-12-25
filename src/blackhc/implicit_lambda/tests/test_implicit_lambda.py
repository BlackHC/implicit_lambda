import pytest

from dataclasses import dataclass

from blackhc.implicit_lambda.builtins import next
from blackhc.implicit_lambda import _, x, z, to_lambda, wrap, get_expr, literal, kw, arg, auto_lambda


def test_index():
    a = dict(b=dict(c=1))

    expr = _["b"]["c"]

    expr_lambda = to_lambda(expr)

    assert expr_lambda(a) == 1


def test_field():
    @dataclass
    class TestClass:
        field: object

    expr = _.field
    expr_lambda = to_lambda(expr)

    assert expr_lambda(TestClass(1)) == 1


def test_nested_fields():
    @dataclass
    class TestClass:
        field: object

    expr = _.field.field
    expr_lambda = to_lambda(expr)

    assert expr_lambda(TestClass(TestClass(1))) == 1


def test_call():
    @dataclass
    class TestClass:
        field: object

        def method(self):
            return self.field

    expr = _.method()
    expr_lambda = to_lambda(expr)

    assert expr_lambda(TestClass(1)) == 1


def test_nested_call():
    @dataclass
    class TestClass:
        field: object

        def method(self):
            return self.field

    expr = _.method().method()
    expr_lambda = to_lambda(expr)

    assert expr_lambda(TestClass(TestClass(1))) == 1


def test_args():
    @wrap
    def method(x, y, z):
        return x + y + z

    assert to_lambda(method(x, 0, z))(1, 2, 3) == 4
    assert to_lambda(method(x=x, y=0, z=z))(1, 2, 3) == 4
    assert to_lambda(method(x, 0, z=z))(1, 2, 3) == 4


def test_literal():
    def assert_literal(obj):
        assert to_lambda(literal(obj))() == obj

    assert_literal(_ + 1)
    assert_literal([_ + 1])
    assert_literal({_ + 1})
    assert_literal({_ + 1: _ + 1})


def assert_code(obj, code, required_args=None):
    assert to_lambda(obj, required_args=required_args).code == code


def test_unwrap_literals():
    assert_code([_ + 1], "lambda x: [(x + 1)]")
    assert_code({_ + 1}, "lambda x: {(x + 1)}")
    assert_code({_ + 1: _ + 1}, "lambda x: {(x + 1):(x + 1)}")


def test_kwarg():
    assert_code(kw("x"), "lambda **kwargs: kwargs['x']")
    assert_code(kw("x") + kw("y"), "lambda **kwargs: (kwargs['x'] + kwargs['y'])")
    assert_code(kw("x") + x, "lambda a, **kwargs: (kwargs['x'] + a)")


def test_arg():
    assert_code(arg(2), "lambda __unused0, __unused1, x: x")
    assert_code(arg(0), "lambda x: x")
    assert_code(arg(0), "lambda x, __unused1: x", required_args=2)


def test_auto_lambda():
    @auto_lambda(args=[False, True])
    def take_callable(number, func):
        return func(number)

    assert take_callable(5, lambda x: 2 * x) == 10
    assert take_callable(5, _ * 2) == 10

    # Check that the signature is being copied as expected.
    with pytest.raises(TypeError):
        take_callable(5, _ * 2, 0)

    underscored = to_lambda(take_callable._(_, _ * 2))
    assert underscored(5) == 10
    assert underscored(3) == 6


def test_id_hash():
    assert to_lambda({next._(_), next._(_), next._(_)})(iter(range(3))) == set(range(3))
    assert to_lambda({next._(_): 0, next._(_): 1, next._(_): 2})(iter(range(3))) == {i: i for i in range(3)}


def test_expr_structural_equal_but_id_hash():
    assert next._(_) == next._(_)
    assert hash(next._(_)) != hash(next._(_))
