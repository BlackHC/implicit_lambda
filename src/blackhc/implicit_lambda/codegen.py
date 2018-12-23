"""
"""
from blackhc.implicit_lambda.expression import *


def collect_args(expr, args: set, kwargs: set):
    if isinstance(expr, Expression):
        if isinstance(expr, AccessorExpression):
            collect_args(expr.target, args, kwargs)
            collect_args(expr.key, args, kwargs)
        elif isinstance(expr, BinaryExpression):
            collect_args(expr.lhs, args, kwargs)
            collect_args(expr.rhs, args, kwargs)
        elif isinstance(expr, CallExpression):
            collect_args(expr.target, args, kwargs)
            collect_args(expr.args, args, kwargs)
            collect_args(expr.kwargs, args, kwargs)
        elif isinstance(expr, ArgsAccessor):
            args.add(expr.key)
        elif isinstance(expr, KwArgsAccessor):
            kwargs.add(expr.key)
        else:
            raise NotImplementedError(type(expr))
    elif isinstance(expr, list):
        for item in expr:
            collect_args(expr.args, args, kwargs)
    elif isinstance(expr, dict):
        for key, value in expr.items():
            collect_args(key, args, kwargs)
            collect_args(value, args, kwargs)
    elif isinstance(expr, set):
        for item in expr:
            collect_args(item, args, kwargs)


def codegen_expr(expr, refs: dict, args: dict, kwargs: dict):
    if isinstance(expr, Expression):
        if isinstance(expr, AccessorExpression):
            if expr.op == AccessorOps.GET_ITEM:
                return f'{codegen_expr(expr.target, refs, args, kwargs)}[{codegen_expr(expr.key, refs, args, kwargs)}]'
            if expr.op == AccessorOps.GET_ATTRIBUTE:
                if isinstance(expr.key, str):
                    return f'{codegen_expr(expr.target, refs, args, kwargs)}.{expr.key}'
                return f'getattr({codegen_expr(expr.target, refs, args, kwargs)},{codegen_expr(expr.key, refs, args, kwargs)})'

            raise NotImplementedError(expr.op)
        if isinstance(expr, BinaryExpression):
            if expr.op == BinaryOp.ADD:
                return f'({codegen_expr(expr.lhs, refs, args, kwargs)} + {codegen_expr(expr.rhs, refs, args, kwargs)})'
            if expr.op == BinaryOp.SUB:
                return f'({codegen_expr(expr.lhs, refs, args, kwargs)} - {codegen_expr(expr.rhs, refs, args, kwargs)})'
            if expr.op == BinaryOp.MUL:
                return f'({codegen_expr(expr.lhs, refs, args, kwargs)} * {codegen_expr(expr.rhs, refs, args, kwargs)})'
            if expr.op == BinaryOp.MATMUL:
                return f'({codegen_expr(expr.lhs, refs, args, kwargs)} @ {codegen_expr(expr.rhs, refs, args, kwargs)})'
            if expr.op == BinaryOp.TRUEDIV:
                return f'({codegen_expr(expr.lhs, refs, args, kwargs)} / {codegen_expr(expr.rhs, refs, args, kwargs)})'
            if expr.op == BinaryOp.FLOORDIV:
                return f'({codegen_expr(expr.lhs, refs, args, kwargs)} // {codegen_expr(expr.rhs, refs, args, kwargs)})'
            if expr.op == BinaryOp.MOD:
                return f'({codegen_expr(expr.lhs, refs, args, kwargs)} % {codegen_expr(expr.rhs, refs, args, kwargs)})'
            if expr.op == BinaryOp.DIVMOD:
                return f'divmod({codegen_expr(expr.lhs, refs, args, kwargs)}, {codegen_expr(expr.rhs, refs, args, kwargs)})'
            if expr.op == BinaryOp.POW:
                return f'({codegen_expr(expr.lhs, refs, args, kwargs)} ** {codegen_expr(expr.rhs, refs, args, kwargs)})'
            if expr.op == BinaryOp.LSHIFT:
                return f'({codegen_expr(expr.lhs, refs, args, kwargs)} << {codegen_expr(expr.rhs, refs, args, kwargs)})'
            if expr.op == BinaryOp.RSHIFT:
                return f'({codegen_expr(expr.lhs, refs, args, kwargs)} >> {codegen_expr(expr.rhs, refs, args, kwargs)})'
            if expr.op == BinaryOp.AND:
                return f'({codegen_expr(expr.lhs, refs, args, kwargs)} & {codegen_expr(expr.rhs, refs, args, kwargs)})'
            if expr.op == BinaryOp.XOR:
                return f'({codegen_expr(expr.lhs, refs, args, kwargs)} ^ {codegen_expr(expr.rhs, refs, args, kwargs)})'
            if expr.op == BinaryOp.OR:
                return f'({codegen_expr(expr.lhs, refs, args, kwargs)} | {codegen_expr(expr.rhs, refs, args, kwargs)})'

            raise NotImplementedError(expr.op)

        if isinstance(expr, CallExpression):
            func = codegen_expr(expr.target, refs, args, kwargs)
            args = ','.join(
                codegen_expr(arg, refs, args, kwargs)
                for arg in expr.args
            )
            kwargs = ','.join(
                f'{keyword}={codegen_expr(arg, refs, args, kwargs)}'
                for keyword, arg in expr.kwargs.items()
            )
            return f'{func}({args}, {kwargs})'

        if isinstance(expr, KwArgsAccessor):
            return kwargs[expr.key]

        if isinstance(expr, ArgsAccessor):
            return args[expr.key]

        raise NotImplementedError(type(expr))

    if isinstance(expr, (int, str, float, bool)):
        return repr(expr)

    if isinstance(expr, list):
        return f'[{",".join([codegen_expr(item, refs, args, kwargs) for item in expr])}]'

    if isinstance(expr, dict):
        return f'{{{",".join([f"{codegen_expr(key, refs, args, kwargs)}:{codegen_expr(value, refs, args, kwargs)}" for key, value in expr.items()])}}}'

    if isinstance(expr, set):
        return f'{{{",".join([codegen_expr(item, refs, args, kwargs) for item in expr])}}}'

    ref_name = f'__ref{len(refs)}__'
    refs[ref_name] = expr
    return ref_name
