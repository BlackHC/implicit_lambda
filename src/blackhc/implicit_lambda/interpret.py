"""
"""
from dataclasses import dataclass
from blackhc.implicit_lambda.expression import *

@dataclass
class Context:
    __slots__ = ('args', 'kwargs')
    args: list
    kwargs: dict


def eval_expr(expr, context):
    if isinstance(expr, Expression):
        if isinstance(expr, AccessorExpression):
            if expr.op == AccessorOps.GET_ITEM:
                return eval_expr(expr.target, context)[eval_expr(expr.key, context)]
            if expr.op == AccessorOps.GET_ATTRIBUTE:
                return getattr(eval_expr(expr.target, context), eval_expr(expr.key, context))

            raise NotImplementedError(expr.op)
        if isinstance(expr, BinaryExpression):
            if expr.op == BinaryOp.ADD:
                return eval_expr(expr.lhs, context) + eval_expr(expr.rhs, context)
            if expr.op == BinaryOp.SUB:
                return eval_expr(expr.lhs, context) - eval_expr(expr.rhs, context)
            if expr.op == BinaryOp.MUL:
                return eval_expr(expr.lhs, context) * eval_expr(expr.rhs, context)
            if expr.op == BinaryOp.MATMUL:
                return eval_expr(expr.lhs, context) @ eval_expr(expr.rhs, context)
            if expr.op == BinaryOp.TRUEDIV:
                return eval_expr(expr.lhs, context) / eval_expr(expr.rhs, context)
            if expr.op == BinaryOp.FLOORDIV:
                return eval_expr(expr.lhs, context) // eval_expr(expr.rhs, context)
            if expr.op == BinaryOp.MOD:
                return eval_expr(expr.lhs, context) % eval_expr(expr.rhs, context)
            if expr.op == BinaryOp.DIVMOD:
                return divmod(eval_expr(expr.lhs, context), eval_expr(expr.rhs, context))
            if expr.op == BinaryOp.POW:
                return eval_expr(expr.lhs, context) ** eval_expr(expr.rhs, context)
            if expr.op == BinaryOp.LSHIFT:
                return eval_expr(expr.lhs, context) << eval_expr(expr.rhs, context)
            if expr.op == BinaryOp.RSHIFT:
                return eval_expr(expr.lhs, context) >> eval_expr(expr.rhs, context)
            if expr.op == BinaryOp.AND:
                return eval_expr(expr.lhs, context) & eval_expr(expr.rhs, context)
            if expr.op == BinaryOp.XOR:
                return eval_expr(expr.lhs, context) ^ eval_expr(expr.rhs, context)
            if expr.op == BinaryOp.OR:
                return eval_expr(expr.lhs, context) | eval_expr(expr.rhs, context)

            raise NotImplementedError(expr.op)

        if isinstance(expr, CallExpression):
            func = eval_expr(expr.target, context)
            args = eval_expr(expr.args, context)
            kwargs = eval_expr(expr.kwargs, context)
            return func(*args, **kwargs)

        if isinstance(expr, KwArgsAccessor):
            # NOTE: the key is not an expression but a literal
            # This makes it easier to optimize.
            return context.kwargs[expr.key]

        if isinstance(expr, ArgsAccessor):
            # NOTE: they key is not an expression but a literal
            # This makes it easier to optimize.
            return context.args[expr.key]

        raise NotImplementedError(type(expr))

    if isinstance(expr, list):
        return [eval_expr(item, context) for item in expr]

    if isinstance(expr, dict):
        return {eval_expr(key, context): eval_expr(value, context) for key, value in expr.items()}

    if isinstance(expr, set):
        return {eval_expr(item, context) for item in expr}
        
    return expr
