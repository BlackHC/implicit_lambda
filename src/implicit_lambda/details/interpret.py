"""
"""
import math
from dataclasses import dataclass
from implicit_lambda.details import expression
from implicit_lambda.details import collect_args


@dataclass
class Context:
    __slots__ = ("args", "kwargs")
    args: dict
    kwargs: dict


def eval_expr(expr, context):
    """Evaluate `expr` within `context` without compiling it. This is for testing only."""
    if isinstance(expr, expression.Expression):
        if isinstance(expr, expression.AccessorExpression):
            if expr.op == expression.AccessorOps.GET_ITEM:
                return eval_expr(expr.target, context)[eval_expr(expr.key, context)]
            if expr.op == expression.AccessorOps.GET_ATTRIBUTE:
                return getattr(eval_expr(expr.target, context), eval_expr(expr.key, context))

            raise NotImplementedError(expr.op)
        if isinstance(expr, expression.OpExpression):
            # ## begin `cg.OpExpression.generate_evals()`
            if expr.op == expression.ArithmeticOps.ADD:
                return eval_expr(expr.arg0, context) + eval_expr(expr.arg1, context)

            if expr.op == expression.ArithmeticOps.SUB:
                return eval_expr(expr.arg0, context) - eval_expr(expr.arg1, context)

            if expr.op == expression.ArithmeticOps.MUL:
                return eval_expr(expr.arg0, context) * eval_expr(expr.arg1, context)

            if expr.op == expression.ArithmeticOps.MATMUL:
                return eval_expr(expr.arg0, context) @ eval_expr(expr.arg1, context)

            if expr.op == expression.ArithmeticOps.TRUEDIV:
                return eval_expr(expr.arg0, context) / eval_expr(expr.arg1, context)

            if expr.op == expression.ArithmeticOps.FLOORDIV:
                return eval_expr(expr.arg0, context) // eval_expr(expr.arg1, context)

            if expr.op == expression.ArithmeticOps.MOD:
                return eval_expr(expr.arg0, context) % eval_expr(expr.arg1, context)

            if expr.op == expression.ArithmeticOps.DIVMOD:
                return divmod(eval_expr(expr.arg0, context), eval_expr(expr.arg1, context))

            if expr.op == expression.ArithmeticOps.LSHIFT:
                return eval_expr(expr.arg0, context) << eval_expr(expr.arg1, context)

            if expr.op == expression.ArithmeticOps.RSHIFT:
                return eval_expr(expr.arg0, context) >> eval_expr(expr.arg1, context)

            if expr.op == expression.ArithmeticOps.AND:
                return eval_expr(expr.arg0, context) & eval_expr(expr.arg1, context)

            if expr.op == expression.ArithmeticOps.XOR:
                return eval_expr(expr.arg0, context) ^ eval_expr(expr.arg1, context)

            if expr.op == expression.ArithmeticOps.OR:
                return eval_expr(expr.arg0, context) | eval_expr(expr.arg1, context)

            if expr.op == expression.ArithmeticOps.RADD:
                return eval_expr(expr.arg1, context) + eval_expr(expr.arg0, context)

            if expr.op == expression.ArithmeticOps.RSUB:
                return eval_expr(expr.arg1, context) - eval_expr(expr.arg0, context)

            if expr.op == expression.ArithmeticOps.RMUL:
                return eval_expr(expr.arg1, context) * eval_expr(expr.arg0, context)

            if expr.op == expression.ArithmeticOps.RMATMUL:
                return eval_expr(expr.arg1, context) @ eval_expr(expr.arg0, context)

            if expr.op == expression.ArithmeticOps.RTRUEDIV:
                return eval_expr(expr.arg1, context) / eval_expr(expr.arg0, context)

            if expr.op == expression.ArithmeticOps.RFLOORDIV:
                return eval_expr(expr.arg1, context) // eval_expr(expr.arg0, context)

            if expr.op == expression.ArithmeticOps.RMOD:
                return eval_expr(expr.arg1, context) % eval_expr(expr.arg0, context)

            if expr.op == expression.ArithmeticOps.RDIVMOD:
                return divmod(eval_expr(expr.arg1, context), eval_expr(expr.arg0, context))

            if expr.op == expression.ArithmeticOps.RPOW:
                return pow(eval_expr(expr.arg1, context), eval_expr(expr.arg0, context))

            if expr.op == expression.ArithmeticOps.RLSHIFT:
                return eval_expr(expr.arg1, context) << eval_expr(expr.arg0, context)

            if expr.op == expression.ArithmeticOps.RRSHIFT:
                return eval_expr(expr.arg1, context) >> eval_expr(expr.arg0, context)

            if expr.op == expression.ArithmeticOps.RAND:
                return eval_expr(expr.arg1, context) & eval_expr(expr.arg0, context)

            if expr.op == expression.ArithmeticOps.RXOR:
                return eval_expr(expr.arg1, context) ^ eval_expr(expr.arg0, context)

            if expr.op == expression.ArithmeticOps.ROR:
                return eval_expr(expr.arg1, context) | eval_expr(expr.arg0, context)

            if expr.op == expression.ComparisonOps.LT:
                return eval_expr(expr.arg0, context) < eval_expr(expr.arg1, context)

            if expr.op == expression.ComparisonOps.LE:
                return eval_expr(expr.arg0, context) <= eval_expr(expr.arg1, context)

            if expr.op == expression.ComparisonOps.GT:
                return eval_expr(expr.arg0, context) > eval_expr(expr.arg1, context)

            if expr.op == expression.ComparisonOps.GE:
                return eval_expr(expr.arg0, context) >= eval_expr(expr.arg1, context)

            if expr.op == expression.ComparisonOps.EQ:
                return eval_expr(expr.arg0, context) == eval_expr(expr.arg1, context)

            if expr.op == expression.ComparisonOps.NE:
                return eval_expr(expr.arg0, context) != eval_expr(expr.arg1, context)

            if expr.op == expression.UnaryOps.POSITIVE:
                return +eval_expr(expr.arg0, context)

            if expr.op == expression.UnaryOps.NEGATIVE:
                return -eval_expr(expr.arg0, context)

            if expr.op == expression.UnaryOps.ABS:
                return abs(eval_expr(expr.arg0, context))

            if expr.op == expression.UnaryOps.INVERT:
                return ~eval_expr(expr.arg0, context)

            if expr.op == expression.UnaryOps.TRUNC:
                return math.trunc(eval_expr(expr.arg0, context))

            if expr.op == expression.UnaryOps.FLOOR:
                return math.floor(eval_expr(expr.arg0, context))

            if expr.op == expression.UnaryOps.CEIL:
                return math.ceil(eval_expr(expr.arg0, context))
            # ## end `cg.OpExpression.generate_evals()`

            if expr.op == expression.SpecialOps.CONTAINS:
                return eval_expr(expr.arg1, context) in eval_expr(expr.arg0, context)

            if expr.op == expression.SpecialOps.NOT_CONTAINS:
                return eval_expr(expr.arg1, context) not in eval_expr(expr.arg0, context)

            if expr.op == expression.OptionalArgOps.POW_2:
                return pow(eval_expr(expr.arg0, context), eval_expr(expr.arg1, context))

            if expr.op == expression.OptionalArgOps.POW_3:
                return pow(eval_expr(expr.arg0, context), eval_expr(expr.arg1, context), eval_expr(expr.arg2, context))

            if expr.op == expression.OptionalArgOps.ROUND_1:
                return round(eval_expr(expr.arg0, context))

            if expr.op == expression.OptionalArgOps.ROUND_2:
                return round(eval_expr(expr.arg0, context), eval_expr(expr.arg1, context))

            raise NotImplementedError(expr.op)

        if isinstance(expr, expression.CallExpression):
            func = eval_expr(expr.target, context)
            args = eval_expr(expr.args, context)
            kwargs = eval_expr(expr.kwargs, context)
            return func(*args, **kwargs)

        if isinstance(expr, expression.KwArgsAccessor):
            # NOTE: the key is not an expression but a literal
            # This makes it easier to optimize.
            return context.kwargs[expr.name]

        if isinstance(expr, expression.ArgsAccessor):
            # NOTE: the key is not an expression but a literal
            # This makes it easier to optimize.
            return context.args[expr.name]

        if isinstance(expr, expression.LiteralExpression):
            return expr.literal

        if isinstance(expr, expression.LambdaExpression):
            return lambda *args_values, **kwargs_values: eval_expr(
                expr.expr,
                Context(
                    {
                        name: args_values[order] if order in args_values else expr.defaults[name]
                        for order, name in enumerate(expr.args)
                    },
                    {
                        name: kwargs_values[name] if name in kwargs_values else expr.defaults[name]
                        for name in expr.kwargs
                    },
                ),
            )

        raise NotImplementedError(type(expr))

    if isinstance(expr, tuple):
        return tuple(eval_expr(item, context) for item in expr)

    if isinstance(expr, list):
        return [eval_expr(item, context) for item in expr]

    if isinstance(expr, dict):
        return {eval_expr(key, context): eval_expr(value, context) for key, value in expr.items()}

    if isinstance(expr, set):
        return {eval_expr(item, context) for item in expr}

    if isinstance(expr, slice):
        return slice(eval_expr(expr.start, context), eval_expr(expr.stop, context), eval_expr(expr.step, context))

    return expr


def to_lambda(expr: expression.Expression, *, args_resolver=None):
    """Convert `expr` to a Python lambda without compiling it. This is slow!"""
    computed_args = collect_args.compute_args(expr, args_resolver=args_resolver)
    lambda_expr = expression.LambdaExpression(expr, computed_args.args, computed_args.kwargs, {})
    return eval_expr(lambda_expr, Context({}, {}))
