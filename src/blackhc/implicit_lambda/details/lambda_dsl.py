"""
"""
import weakref
from blackhc.implicit_lambda.details import expression
from blackhc.implicit_lambda.details import codegen


_exprs = weakref.WeakKeyDictionary()


def get_expr(expr):
    if isinstance(expr, LambdaDSL):
        return _exprs[expr]
    if isinstance(expr, tuple):
        return tuple(get_expr(item) for item in expr)
    if isinstance(expr, list):
        return [get_expr(item) for item in expr]
    if isinstance(expr, dict):
        return {get_expr(key): get_expr(value) for key, value in expr.items()}
    if isinstance(expr, set):
        return {get_expr(item) for item in expr}
    return expr


class LambdaDSL:
    def __init__(self, expr):
        _exprs[self] = expr

    def __repr__(self):
        lambda_code, refs = codegen.generate_code(get_expr(self))
        return f"<{type(self).__qualname__}: {lambda_code} @ {refs}>"

    def __call__(self, *args, **kwargs):
        return LambdaDSL(expression.CallExpression(get_expr(self), get_expr(args), get_expr(kwargs)))

    def __getitem__(self, key):
        return LambdaDSL(expression.AccessorExpression(expression.AccessorOps.GET_ITEM, get_expr(self), get_expr(key)))

    def __getattribute__(self, name):
        return LambdaDSL(
            expression.AccessorExpression(expression.AccessorOps.GET_ATTRIBUTE, get_expr(self), get_expr(name))
        )

    def __add__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.ADD, get_expr(self), get_expr(other)))

    def __radd__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.ADD, get_expr(other), get_expr(self)))

    def __sub__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.SUB, get_expr(self), get_expr(other)))

    def __rsub__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.SUB, get_expr(other), get_expr(self)))

    def __mul__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.MUL, get_expr(self), get_expr(other)))

    def __rmul__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.MUL, get_expr(other), get_expr(self)))

    def __matmul__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.MATMUL, get_expr(self), get_expr(other)))

    def __rmatmul__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.MATMUL, get_expr(other), get_expr(self)))

    def __truediv__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.TRUEDIV, get_expr(self), get_expr(other)))

    def __rtruediv__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.TRUEDIV, get_expr(other), get_expr(self)))

    def __floordiv__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.FLOORDIV, get_expr(self), get_expr(other)))

    def __rfloordiv__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.FLOORDIV, get_expr(other), get_expr(self)))

    def __mod__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.MOD, get_expr(self), get_expr(other)))

    def __rmod__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.MOD, get_expr(other), get_expr(self)))

    def __divmod__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.DIVMOD, get_expr(self), get_expr(other)))

    def __rdivmod__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.DIVMOD, get_expr(other), get_expr(self)))

    def __pow__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.POW, get_expr(self), get_expr(other)))

    def __rpow__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.POW, get_expr(other), get_expr(self)))

    def __lshift__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.LSHIFT, get_expr(self), get_expr(other)))

    def __rlshift__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.LSHIFT, get_expr(other), get_expr(self)))

    def __rshift__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.RSHIFT, get_expr(self), get_expr(other)))

    def __rrshift__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.RSHIFT, get_expr(other), get_expr(self)))

    def __and__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.AND, get_expr(self), get_expr(other)))

    def __rand__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.AND, get_expr(other), get_expr(self)))

    def __xor__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.XOR, get_expr(self), get_expr(other)))

    def __rxor__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.XOR, get_expr(other), get_expr(self)))

    def __or__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.OR, get_expr(self), get_expr(other)))

    def __ror__(self, other):
        return LambdaDSL(expression.BinaryExpression(expression.BinaryOps.OR, get_expr(other), get_expr(self)))


def index(obj, key):
    """Index into a resolved object `obj` with `key` that can be an expression."""
    return LambdaDSL(expression.AccessorExpression(expression.AccessorOps.GET_ITEM, obj, get_expr(key)))


def call(func: callable, *args, **kwargs):
    """Calls a resolved function `func` with `args` and `kwargs` that can contain expressions."""
    return LambdaDSL(expression.CallExpression(func, get_expr(args), get_expr(kwargs)))


def kw(keyword: str):
    return LambdaDSL(expression.KwArgsAccessor(keyword))


def arg(pos: int):
    return LambdaDSL(expression.ArgsAccessor(pos))


def literal(obj: object):
    return LambdaDSL(expression.LiteralExpression(obj))
