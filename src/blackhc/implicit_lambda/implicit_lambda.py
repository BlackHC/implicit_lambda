"""
"""
from blackhc.implicit_lambda.expression import * 


# TODO: weakrefs
ImplicitExprs = {}


def get_expr(expr):
    if isinstance(expr, ImplicitLambda):
        return ImplicitExprs[expr]
    return expr


class ImplicitLambda:
    def __init__(self, expr):
        ImplicitExprs[self] = expr

    def __call__(self, *args, **kwargs):
        return ImplicitLambda(CallExpression(get_expr(self), args, kwargs))

    def __getitem__(self, key):
        return ImplicitLambda(AccessorExpression(AccessorOps.GET_ITEM, get_expr(self), get_expr(key)))

    def __getattribute__(self, name):
        return ImplicitLambda(AccessorExpression(AccessorOps.GET_ATTRIBUTE, get_expr(self), get_expr(name)))

    def __add__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.ADD, get_expr(self), get_expr(other)))

    def __radd__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.ADD, get_expr(other), get_expr(self)))

    def __sub__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.SUB, get_expr(self), get_expr(other)))

    def __rsub__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.SUB, get_expr(other), get_expr(self)))

    def __mul__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.MUL, get_expr(self), get_expr(other)))

    def __rmul__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.MUL, get_expr(other), get_expr(self)))

    def __matmul__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.MATMUL, get_expr(self), get_expr(other)))

    def __rmatmul__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.MATMUL, get_expr(other), get_expr(self)))

    def __truediv__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.TRUEDIV, get_expr(self), get_expr(other)))

    def __rtruediv__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.TRUEDIV, get_expr(other), get_expr(self)))

    def __floordiv__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.FLOORDIV, get_expr(self), get_expr(other)))

    def __rfloordiv__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.FLOORDIV, get_expr(other), get_expr(self)))

    def __mod__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.MOD, get_expr(self), get_expr(other)))

    def __rmod__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.MOD, get_expr(other), get_expr(self)))

    def __divmod__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.DIVMOD, get_expr(self), get_expr(other)))

    def __rdivmod__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.DIVMOD, get_expr(other), get_expr(self)))

    def __pow__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.POW, get_expr(self), get_expr(other)))

    def __rpow__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.POW, get_expr(other), get_expr(self)))

    def __lshift__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.LSHIFT, get_expr(self), get_expr(other)))

    def __rlshift__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.LSHIFT, get_expr(other), get_expr(self)))

    def __rshift__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.RSHIFT, get_expr(self), get_expr(other)))

    def __rrshift__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.RSHIFT, get_expr(other), get_expr(self)))

    def __and__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.AND, get_expr(self), get_expr(other)))

    def __rand__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.AND, get_expr(other), get_expr(self)))

    def __xor__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.XOR, get_expr(self), get_expr(other)))

    def __rxor__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.XOR, get_expr(other), get_expr(self)))

    def __or__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.OR, get_expr(self), get_expr(other)))

    def __ror__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.OR, get_expr(other), get_expr(self)))


def index(obj, key):
    return ImplicitLambda(AccessorExpression(AccessorOps.GET_ITEM, get_expr(obj), get_expr(key)))


def call(func, *args, **kwargs):
    return ImplicitLambda(CallExpression(get_expr(func), get_expr(args), get_expr(kwargs)))

