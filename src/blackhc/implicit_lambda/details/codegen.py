"""Code generation from expression to Python lambda."""
import builtins
import math
from dataclasses import dataclass

from blackhc.implicit_lambda.details import collect_args
from blackhc.implicit_lambda.details import expression


@dataclass
class CodegenContext:
    __slots__ = "refs"
    refs: dict


def add_ref(context, value):
    ref_name = f"__ref{len(context.refs)}__"
    context.refs[ref_name] = value
    return ref_name


def codegen_expr(expr, context: CodegenContext):
    if expr is None:
        return repr(None)

    if isinstance(expr, expression.Expression):
        if isinstance(expr, expression.AccessorExpression):
            if expr.op == expression.AccessorOps.GET_ITEM:
                return f"{codegen_expr(expr.target, context)}[{codegen_expr(expr.key, context)}]"
            if expr.op == expression.AccessorOps.GET_ATTRIBUTE:
                if isinstance(expr.key, str):
                    return f"{codegen_expr(expr.target, context)}.{expr.key}"
                return f"getattr({codegen_expr(expr.target, context)}, {codegen_expr(expr.key, context)})"

            raise NotImplementedError(expr.op)

        if isinstance(expr, expression.OpExpression):
            return expr.op.value.template.format(
                codegen_expr(expr.arg0, context), codegen_expr(expr.arg1, context), codegen_expr(expr.arg2, context)
            )

        if isinstance(expr, expression.CallExpression):
            func = codegen_expr(expr.target, context)
            params = []
            params.extend(codegen_expr(arg, context) for arg in expr.args)
            params.extend(f"{keyword}={codegen_expr(arg, context)}" for keyword, arg in expr.kwargs.items())
            return f'{func}({", ".join(params)})'

        if isinstance(expr, expression.KwArgsAccessor):
            return expr.name

        if isinstance(expr, expression.ArgsAccessor):
            return expr.name

        if isinstance(expr, expression.LiteralExpression):
            return add_ref(context, expr.literal)

        if isinstance(expr, expression.LambdaExpression):
            # TODO: support globals to allow nested lambdas that access outer arguments?
            params = []
            params.extend(
                f"{arg}={codegen_expr(expr.defaults[arg])}" if arg in expr.defaults else arg for arg in expr.args
            )
            if expr.kwargs:
                params.append("*")
                params.extend(
                    f"{arg}={codegen_expr(expr.defaults[arg])}" if arg in expr.defaults else arg for arg in expr.kwargs
                )

            sub_context = CodegenContext(context.refs)
            expr_code = codegen_expr(expr.expr, sub_context)
            return f'(lambda {", ".join(params)}: {expr_code})'
        raise NotImplementedError(type(expr))

    if isinstance(expr, (int, str, float, bool)):
        return repr(expr)

    if isinstance(expr, tuple):
        if expr == ():
            return "()"
        return f'({", ".join([codegen_expr(item, context) for item in expr])},)'

    if isinstance(expr, list):
        return f'[{", ".join([codegen_expr(item, context) for item in expr])}]'

    if isinstance(expr, dict):
        return f'{{{", ".join([f"{codegen_expr(key, context)}:{codegen_expr(value, context)}" for key, value in expr.items()])}}}'

    if isinstance(expr, set):
        return f'{{{", ".join([codegen_expr(item, context) for item in expr])}}}'

    if isinstance(expr, slice):
        return f"slice({codegen_expr(expr.start, context)}, {codegen_expr(expr.stop, context)}, {codegen_expr(expr.step, context)})"

    return add_ref(context, expr)


def generate_lambda(expr, args_resolver=None):
    resolved_args = collect_args.compute_args(expr, args_resolver=args_resolver)

    lambda_expr = expression.LambdaExpression(expr, resolved_args.args, resolved_args.kwargs, {})

    context = CodegenContext({})
    lambda_source = codegen_expr(lambda_expr, context)
    return lambda_source, context.refs, resolved_args


def compile(expr, args_resolver=None):
    """Compiles `expr` into a Python lambda that takes at least `required_args` positional arguments."""

    lambda_source, refs, resolved_args = generate_lambda(expr, args_resolver=args_resolver)

    func_globals = dict(refs)
    func_globals["__builtins__"] = builtins
    func_globals["math"] = math
    if __debug__:
        func_globals["__refs"] = refs
        func_source = f'type({lambda_source!r}, (object,), dict(__slots__=(), __call__=staticmethod({lambda_source}), args={resolved_args.args!r}, kwargs={resolved_args.kwargs!r}, refs=__refs, code={lambda_source!r}, __repr__=lambda self: f"<{{self.code}} @ {{self.refs}}>"))()'
        func_code = builtins.compile(func_source, lambda_source, 'eval', 0, True)
        func = eval(func_code, func_globals, {})
    else:
        func_code = builtins.compile(lambda_source, lambda_source, 'eval', 0, True)
        func = eval(func_code, func_globals, {})
        func.code = lambda_source
        func.refs = refs
        func.args = resolved_args.args
        func.kwargs = resolved_args.kwargs
    return func
