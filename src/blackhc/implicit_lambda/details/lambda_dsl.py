"""Implicit lambda domain-specific language that wraps Python expressions into an internal expression AST."""
from blackhc.implicit_lambda.details import expression
from blackhc.implicit_lambda.details import codegen


_exprs = {}


def get_expr(expr):
    """Unwrap expr into an `expression.Expression`. Handle literals correctly."""
    if isinstance(expr, LambdaDSL):
        return _exprs[id(expr)]
    if isinstance(expr, expression.Expression):
        # Wrap Expressions in a literal, so you can pass them to methods (if you want).
        # This is an extra step, so why this extra work?
        # Locality: without this: `_.f(a)` might either compile to `lambda _: _.f(a)`
        # or to `lambda _: _.f(...)` if a was an Expression.
        # This also means that `to_lambda` will turn an Expression into a constant lambda.
        # This means that glue code only operates on LambdaDSLs, which can be considered
        # ephemeral.
        return literal(expr)
    if isinstance(expr, tuple):
        return tuple(get_expr(item) for item in expr)
    if isinstance(expr, list):
        return [get_expr(item) for item in expr]
    if isinstance(expr, dict):
        return {get_expr(key): get_expr(value) for key, value in expr.items()}
    if isinstance(expr, set):
        return {get_expr(item) for item in expr}
    if isinstance(expr, slice):
        return slice(get_expr(expr.start), get_expr(expr.stop), get_expr(expr.step))

    return expr


class LambdaDSL:
    """Implicit lambda DSL wrapper that casts all possible operations into the internal AST."""

    def __init__(self, expr):
        _exprs[id(self)] = expr

    def __del__(self):
        if _exprs:
            del _exprs[id(self)]

    def __hash__(self):
        return id(self)

    def __str__(self):
        return LambdaDSL.__repr__(self)

    def __repr__(self):
        lambda_code, refs = codegen.generate_lambda(get_expr(self))
        return f"<{type(self).__qualname__}: {lambda_code} @ {refs}>"

    def __call__(self, *args, **kwargs):
        return LambdaDSL(expression.CallExpression(get_expr(self), get_expr(args), get_expr(kwargs)))

    def __getitem__(self, key):
        return LambdaDSL(expression.AccessorExpression(expression.AccessorOps.GET_ITEM, get_expr(self), get_expr(key)))

    def __getattribute__(self, name):
        return LambdaDSL(
            expression.AccessorExpression(expression.AccessorOps.GET_ATTRIBUTE, get_expr(self), get_expr(name))
        )

    # ## begin `cg.OpExpression.generate_lambda_dsl_wrappers()`
    def __add__(self, arg0):
        return LambdaDSL(expression.OpExpression(expression.ArithmeticOps.ADD, 2, get_expr(self), get_expr(arg0), None))

    def __sub__(self, arg0):
        return LambdaDSL(expression.OpExpression(expression.ArithmeticOps.SUB, 2, get_expr(self), get_expr(arg0), None))

    def __mul__(self, arg0):
        return LambdaDSL(expression.OpExpression(expression.ArithmeticOps.MUL, 2, get_expr(self), get_expr(arg0), None))

    def __matmul__(self, arg0):
        return LambdaDSL(
            expression.OpExpression(expression.ArithmeticOps.MATMUL, 2, get_expr(self), get_expr(arg0), None)
        )

    def __truediv__(self, arg0):
        return LambdaDSL(
            expression.OpExpression(expression.ArithmeticOps.TRUEDIV, 2, get_expr(self), get_expr(arg0), None)
        )

    def __floordiv__(self, arg0):
        return LambdaDSL(
            expression.OpExpression(expression.ArithmeticOps.FLOORDIV, 2, get_expr(self), get_expr(arg0), None)
        )

    def __mod__(self, arg0):
        return LambdaDSL(expression.OpExpression(expression.ArithmeticOps.MOD, 2, get_expr(self), get_expr(arg0), None))

    def __divmod__(self, arg0):
        return LambdaDSL(
            expression.OpExpression(expression.ArithmeticOps.DIVMOD, 2, get_expr(self), get_expr(arg0), None)
        )

    def __lshift__(self, arg0):
        return LambdaDSL(
            expression.OpExpression(expression.ArithmeticOps.LSHIFT, 2, get_expr(self), get_expr(arg0), None)
        )

    def __rshift__(self, arg0):
        return LambdaDSL(
            expression.OpExpression(expression.ArithmeticOps.RSHIFT, 2, get_expr(self), get_expr(arg0), None)
        )

    def __and__(self, arg0):
        return LambdaDSL(expression.OpExpression(expression.ArithmeticOps.AND, 2, get_expr(self), get_expr(arg0), None))

    def __xor__(self, arg0):
        return LambdaDSL(expression.OpExpression(expression.ArithmeticOps.XOR, 2, get_expr(self), get_expr(arg0), None))

    def __or__(self, arg0):
        return LambdaDSL(expression.OpExpression(expression.ArithmeticOps.OR, 2, get_expr(self), get_expr(arg0), None))

    def __radd__(self, arg0):
        return LambdaDSL(
            expression.OpExpression(expression.ArithmeticOps.RADD, 2, get_expr(self), get_expr(arg0), None)
        )

    def __rsub__(self, arg0):
        return LambdaDSL(
            expression.OpExpression(expression.ArithmeticOps.RSUB, 2, get_expr(self), get_expr(arg0), None)
        )

    def __rmul__(self, arg0):
        return LambdaDSL(
            expression.OpExpression(expression.ArithmeticOps.RMUL, 2, get_expr(self), get_expr(arg0), None)
        )

    def __rmatmul__(self, arg0):
        return LambdaDSL(
            expression.OpExpression(expression.ArithmeticOps.RMATMUL, 2, get_expr(self), get_expr(arg0), None)
        )

    def __rtruediv__(self, arg0):
        return LambdaDSL(
            expression.OpExpression(expression.ArithmeticOps.RTRUEDIV, 2, get_expr(self), get_expr(arg0), None)
        )

    def __rfloordiv__(self, arg0):
        return LambdaDSL(
            expression.OpExpression(expression.ArithmeticOps.RFLOORDIV, 2, get_expr(self), get_expr(arg0), None)
        )

    def __rmod__(self, arg0):
        return LambdaDSL(
            expression.OpExpression(expression.ArithmeticOps.RMOD, 2, get_expr(self), get_expr(arg0), None)
        )

    def __rdivmod__(self, arg0):
        return LambdaDSL(
            expression.OpExpression(expression.ArithmeticOps.RDIVMOD, 2, get_expr(self), get_expr(arg0), None)
        )

    def __rpow__(self, arg0):
        return LambdaDSL(
            expression.OpExpression(expression.ArithmeticOps.RPOW, 2, get_expr(self), get_expr(arg0), None)
        )

    def __rlshift__(self, arg0):
        return LambdaDSL(
            expression.OpExpression(expression.ArithmeticOps.RLSHIFT, 2, get_expr(self), get_expr(arg0), None)
        )

    def __rrshift__(self, arg0):
        return LambdaDSL(
            expression.OpExpression(expression.ArithmeticOps.RRSHIFT, 2, get_expr(self), get_expr(arg0), None)
        )

    def __rand__(self, arg0):
        return LambdaDSL(
            expression.OpExpression(expression.ArithmeticOps.RAND, 2, get_expr(self), get_expr(arg0), None)
        )

    def __rxor__(self, arg0):
        return LambdaDSL(
            expression.OpExpression(expression.ArithmeticOps.RXOR, 2, get_expr(self), get_expr(arg0), None)
        )

    def __ror__(self, arg0):
        return LambdaDSL(expression.OpExpression(expression.ArithmeticOps.ROR, 2, get_expr(self), get_expr(arg0), None))

    def __lt__(self, arg0):
        return LambdaDSL(expression.OpExpression(expression.ComparisonOps.LT, 2, get_expr(self), get_expr(arg0), None))

    def __le__(self, arg0):
        return LambdaDSL(expression.OpExpression(expression.ComparisonOps.LE, 2, get_expr(self), get_expr(arg0), None))

    def __gt__(self, arg0):
        return LambdaDSL(expression.OpExpression(expression.ComparisonOps.GT, 2, get_expr(self), get_expr(arg0), None))

    def __ge__(self, arg0):
        return LambdaDSL(expression.OpExpression(expression.ComparisonOps.GE, 2, get_expr(self), get_expr(arg0), None))

    def __eq__(self, arg0):
        return LambdaDSL(expression.OpExpression(expression.ComparisonOps.EQ, 2, get_expr(self), get_expr(arg0), None))

    def __ne__(self, arg0):
        return LambdaDSL(expression.OpExpression(expression.ComparisonOps.NE, 2, get_expr(self), get_expr(arg0), None))

    def __pos__(self,):
        return LambdaDSL(expression.OpExpression(expression.UnaryOps.POSITIVE, 1, get_expr(self), None, None))

    def __neg__(self,):
        return LambdaDSL(expression.OpExpression(expression.UnaryOps.NEGATIVE, 1, get_expr(self), None, None))

    def __abs__(self,):
        return LambdaDSL(expression.OpExpression(expression.UnaryOps.ABS, 1, get_expr(self), None, None))

    def __invert__(self,):
        return LambdaDSL(expression.OpExpression(expression.UnaryOps.INVERT, 1, get_expr(self), None, None))

    def __trunc__(self,):
        return LambdaDSL(expression.OpExpression(expression.UnaryOps.TRUNC, 1, get_expr(self), None, None))

    def __floor__(self,):
        return LambdaDSL(expression.OpExpression(expression.UnaryOps.FLOOR, 1, get_expr(self), None, None))

    def __ceil__(self,):
        return LambdaDSL(expression.OpExpression(expression.UnaryOps.CEIL, 1, get_expr(self), None, None))

    # ## end `codegen.OpExpression.generate_lambda_dsl_wrappers()`

    def __pow__(self, other, modulo=None):
        if modulo is None:
            return LambdaDSL(
                expression.OpExpression(expression.OptionalArgOps.POW_2, 2, get_expr(self), get_expr(other), None)
            )
        return LambdaDSL(
            expression.OpExpression(
                expression.OptionalArgOps.POW_3, 3, get_expr(self), get_expr(other), get_expr(modulo)
            )
        )

    def __round__(self, ndigits=None):
        if ndigits is None:
            return LambdaDSL(expression.OpExpression(expression.OptionalArgOps.ROUND_1, 1, get_expr(self), None, None))
        return LambdaDSL(
            expression.OpExpression(expression.OptionalArgOps.ROUND_2, 2, get_expr(self), get_expr(ndigits), None)
        )

    def __int__(self):
        raise NotImplementedError("implicit_lambda does not support int(). Use the wrapped `int._` instead!")

    def __index__(self):
        raise NotImplementedError("implicit_lambda does not support __index__(). Use the wrapped builtins instead!")

    def __complex__(self):
        raise NotImplementedError("implicit_lambda does not support complex(). Use the wrapped `complex._` instead!")

    def __float__(self):
        raise NotImplementedError("implicit_lambda does not support __index__(). Use the wrapped `float._` instead!")

    def __bool__(self):
        raise NotImplementedError("implicit_lambda does not support __bool__(). Use the wrapped `bool._` instead!")

    def __len__(self):
        raise NotImplementedError("implicit_lambda does not support __len__(). Use the wrapped `len._` instead!")

    # TODO: add a helper function or method instead?
    def __contains__(self, other):
        raise NotImplementedError("implicit_lambda does not support __contains__().")


def index(obj, key):
    """Index into a resolved object `obj` with `key` that can be an expression."""
    return LambdaDSL(expression.AccessorExpression(expression.AccessorOps.GET_ITEM, obj, get_expr(key)))


def call(func: callable, *args, **kwargs):
    """Calls a resolved function `func` with `args` and `kwargs` that can contain expressions."""
    return LambdaDSL(expression.CallExpression(func, get_expr(args), get_expr(kwargs)))


def kw(keyword: str):
    """Placeholder for a keyword argument."""
    return LambdaDSL(expression.KwArgsAccessor(keyword))


def arg(pos: int, name: str):
    """Placeholder for a positional argument."""
    return LambdaDSL(expression.ArgsAccessor(pos, name))


def literal(obj: object):
    """Wraps an object, so that it will not be looked at by `get_expr`.dict

    This is mainly to avoid descending into big dictionaries or lists by accident.
    """
    return LambdaDSL(expression.LiteralExpression(obj))


def inline_expr(expr: expression.Expression):
    """Wrap an expression so that it can become part of a LambdaDSL expression (instead of being treated as literal)."""
    return LambdaDSL(expr)
