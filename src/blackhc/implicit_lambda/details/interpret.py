"""
"""
from dataclasses import dataclass
from blackhc.implicit_lambda.details import expression


@dataclass
class Context:
    __slots__ = ("args", "kwargs")
    args: list
    kwargs: dict


def eval_expr(expr, context):
    if isinstance(expr, expression.Expression):
        if isinstance(expr, expression.AccessorExpression):
            if expr.op == expression.AccessorOps.GET_ITEM:
                return eval_expr(expr.target, context)[eval_expr(expr.key, context)]
            if expr.op == expression.AccessorOps.GET_ATTRIBUTE:
                return getattr(eval_expr(expr.target, context), eval_expr(expr.key, context))

            raise NotImplementedError(expr.op)
        if isinstance(expr, expression.BinaryExpression):
            if expr.op == expression.BinaryOps.ADD:
                return eval_expr(expr.lhs, context) + eval_expr(expr.rhs, context)
            if expr.op == expression.BinaryOps.SUB:
                return eval_expr(expr.lhs, context) - eval_expr(expr.rhs, context)
            if expr.op == expression.BinaryOps.MUL:
                return eval_expr(expr.lhs, context) * eval_expr(expr.rhs, context)
            if expr.op == expression.BinaryOps.MATMUL:
                return eval_expr(expr.lhs, context) @ eval_expr(expr.rhs, context)
            if expr.op == expression.BinaryOps.TRUEDIV:
                return eval_expr(expr.lhs, context) / eval_expr(expr.rhs, context)
            if expr.op == expression.BinaryOps.FLOORDIV:
                return eval_expr(expr.lhs, context) // eval_expr(expr.rhs, context)
            if expr.op == expression.BinaryOps.MOD:
                return eval_expr(expr.lhs, context) % eval_expr(expr.rhs, context)
            if expr.op == expression.BinaryOps.DIVMOD:
                return divmod(eval_expr(expr.lhs, context), eval_expr(expr.rhs, context))
            if expr.op == expression.BinaryOps.POW:
                return pow(eval_expr(expr.lhs, context), eval_expr(expr.rhs, context))
            if expr.op == expression.BinaryOps.LSHIFT:
                return eval_expr(expr.lhs, context) << eval_expr(expr.rhs, context)
            if expr.op == expression.BinaryOps.RSHIFT:
                return eval_expr(expr.lhs, context) >> eval_expr(expr.rhs, context)
            if expr.op == expression.BinaryOps.AND:
                return eval_expr(expr.lhs, context) & eval_expr(expr.rhs, context)
            if expr.op == expression.BinaryOps.XOR:
                return eval_expr(expr.lhs, context) ^ eval_expr(expr.rhs, context)
            if expr.op == expression.BinaryOps.OR:
                return eval_expr(expr.lhs, context) | eval_expr(expr.rhs, context)

            raise NotImplementedError(expr.op)

        if isinstance(expr, expression.CallExpression):
            func = eval_expr(expr.target, context)
            args = eval_expr(expr.args, context)
            kwargs = eval_expr(expr.kwargs, context)
            return func(*args, **kwargs)

        if isinstance(expr, expression.KwArgsAccessor):
            # NOTE: the key is not an expression but a literal
            # This makes it easier to optimize.
            return context.kwargs[expr.key]

        if isinstance(expr, expression.ArgsAccessor):
            # NOTE: they key is not an expression but a literal
            # This makes it easier to optimize.
            return context.args[expr.key]

        if isinstance(expr, expression.LiteralExpression):
            return expr.literal

        raise NotImplementedError(type(expr))

    if isinstance(expr, tuple):
        return tuple(eval_expr(item, context) for item in expr)

    if isinstance(expr, list):
        return [eval_expr(item, context) for item in expr]

    if isinstance(expr, dict):
        return {eval_expr(key, context): eval_expr(value, context) for key, value in expr.items()}

    if isinstance(expr, set):
        return {eval_expr(item, context) for item in expr}

    return expr


def to_lambda(expr: expression.Expression):
    return lambda *args, **kwargs: eval_expr(expr, Context(args, kwargs))
