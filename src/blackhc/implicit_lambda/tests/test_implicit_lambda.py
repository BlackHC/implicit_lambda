import pytest

from dataclasses import dataclass

from blackhc.implicit_lambda.builtins import next
from blackhc.implicit_lambda import _, x, z, to_lambda, wrap, get_expr, literal, kw, arg, auto_lambda, call
from blackhc.implicit_lambda import args_resolver


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


def test_method_call():
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
        assert to_lambda(literal(obj))() is obj

    assert_literal(_ + 1)
    assert_literal([_ + 1])
    assert_literal({_ + 1})
    assert_literal({_ + 1: _ + 1})


def assert_code(obj, code, required_args=None):
    assert to_lambda(obj, args_resolver=args_resolver.flexible_args(required_args=required_args)).code == code


def test_unwrap_literals():
    assert_code([_ + 1], "(lambda _: [(_ + 1)])")
    assert_code({_ + 1}, "(lambda _: {(_ + 1)})")
    assert_code({_ + 1: _ + 1}, "(lambda _: {(_ + 1):(_ + 1)})")
    assert_code((_ + 1,), "(lambda _: ((_ + 1),))")

    assert_code((), "(lambda : ())")

    assert_code(slice(1, 5), "(lambda : slice(1, 5, None))")
    assert_code(slice(1, _), "(lambda _: slice(1, _, None))")
    assert_code(slice(1, 5, 1), "(lambda : slice(1, 5, 1))")
    assert_code(slice(1, 5, _), "(lambda _: slice(1, 5, _))")

    assert_code(_[1:5:_], "(lambda _: _[slice(1, 5, _)])")


def test_kwarg():
    assert_code(kw("x"), "(lambda *, x: x)")
    assert_code(kw("x") + kw("y"), "(lambda *, x, y: (x + y))")
    assert_code(kw("y") + x, "(lambda x, *, y: (y + x))")


def test_arg():
    assert_code(arg(2, "xx"), "(lambda __unused0, __unused1, xx: xx)")
    assert_code(arg(0, "y"), "(lambda y: y)")
    assert_code(arg(0, "z"), "(lambda z, __unused1: z)", required_args=2)


def test_arg_collision_fails():
    with pytest.raises(SyntaxError):
        to_lambda(arg(0, "x") + arg(0, "y"))


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
    assert get_expr(next._(_)) == get_expr(next._(_))
    assert hash(get_expr(next._(_))) != hash(get_expr(next._(_)))


def test_call():
    def f(x):
        return x + 1

    assert to_lambda(call(f, 1))() == 2
