"""Code generation from expression to Python lambda."""
from dataclasses import dataclass

from blackhc.implicit_lambda.details import expression


def collect_args(expr, args: set, kwargs: set):
    if isinstance(expr, expression.Expression):
        if isinstance(expr, expression.AccessorExpression):
            collect_args(expr.target, args, kwargs)
            collect_args(expr.key, args, kwargs)
        elif isinstance(expr, expression.BinaryExpression):
            collect_args(expr.lhs, args, kwargs)
            collect_args(expr.rhs, args, kwargs)
        elif isinstance(expr, expression.CallExpression):
            collect_args(expr.target, args, kwargs)
            collect_args(expr.args, args, kwargs)
            collect_args(expr.kwargs, args, kwargs)
        elif isinstance(expr, expression.ArgsAccessor):
            args.add(expr.key)
        elif isinstance(expr, expression.KwArgsAccessor):
            kwargs.add(expr.key)
        elif isinstance(expr, expression.LiteralExpression):
            pass
        else:
            raise NotImplementedError(type(expr))
    elif isinstance(expr, tuple):
        for item in expr:
            collect_args(item, args, kwargs)
    elif isinstance(expr, list):
        for item in expr:
            collect_args(item, args, kwargs)
    elif isinstance(expr, dict):
        for key, value in expr.items():
            collect_args(key, args, kwargs)
            collect_args(value, args, kwargs)
    elif isinstance(expr, set):
        for item in expr:
            collect_args(item, args, kwargs)


@dataclass
class Context:
    __slots__ = ("refs", "args", "kwargs")
    refs: dict
    args: dict
    kwargs: dict


def add_ref(context, value):
    ref_name = f"__ref{len(context.refs)}__"
    context.refs[ref_name] = value
    return ref_name


def codegen_expr(expr, context: Context):
    if isinstance(expr, expression.Expression):
        if isinstance(expr, expression.AccessorExpression):
            if expr.op == expression.AccessorOps.GET_ITEM:
                return f"{codegen_expr(expr.target, context)}[{codegen_expr(expr.key, context)}]"
            if expr.op == expression.AccessorOps.GET_ATTRIBUTE:
                if isinstance(expr.key, str):
                    return f"{codegen_expr(expr.target, context)}.{expr.key}"
                return f"getattr({codegen_expr(expr.target, context)}, {codegen_expr(expr.key, context)})"

            raise NotImplementedError(expr.op)

        if isinstance(expr, expression.BinaryExpression):
            return f"{expr.op.value[1].format(codegen_expr(expr.lhs, context), codegen_expr(expr.rhs, context))}"

        if isinstance(expr, expression.CallExpression):
            func = codegen_expr(expr.target, context)
            params = []
            params.extend(codegen_expr(arg, context) for arg in expr.args)
            params.extend(f"{keyword}={codegen_expr(arg, context)}" for keyword, arg in expr.kwargs.items())
            return f'{func}({", ".join(params)})'

        if isinstance(expr, expression.KwArgsAccessor):
            return context.kwargs[expr.key]

        if isinstance(expr, expression.ArgsAccessor):
            return context.args[expr.key]

        if isinstance(expr, expression.LiteralExpression):
            return add_ref(context, expr.literal)

        raise NotImplementedError(type(expr))

    if isinstance(expr, (int, str, float, bool)):
        return repr(expr)

    if isinstance(expr, tuple):
        if expr == ():
            return "()"
        return f'({",".join([codegen_expr(item, context) for item in expr])},)'

    if isinstance(expr, list):
        return f'[{",".join([codegen_expr(item, context) for item in expr])}]'

    if isinstance(expr, dict):
        return f'{{{",".join([f"{codegen_expr(key, context)}:{codegen_expr(value, context)}" for key, value in expr.items()])}}}'

    if isinstance(expr, set):
        return f'{{{",".join([codegen_expr(item, context) for item in expr])}}}'

    return add_ref(context, expr)


def generate_code(expr, required_args=None):
    if required_args is None:
        required_args = 0

    args_set = set()
    kwargs_set = set()
    collect_args(expr, args_set, kwargs_set)

    context = Context({}, {}, {})

    context.kwargs = {kwarg: f"kwargs[{kwarg!r}]" for kwarg in kwargs_set}

    specific_args = False
    if len(args_set) < 4:
        for available_args in [
            ("x", "y", "z", "w"),
            ("a", "b", "c", "d"),
            ("i", "j", "k", "l"),
            ("arg0", "arg1", "arg2", "arg3"),
        ]:
            if not set(available_args).intersection(kwargs_set):
                specific_args = True
                context.args = {j: available_args[i] for i, j in enumerate(sorted(args_set))}
                break
    if not specific_args:
        context.args = {i: f"args[{i}]" for i in args_set}

    required_args = max(max(args_set, default=-1) + 1, required_args)
    context.refs = {}
    expr_code = codegen_expr(expr, context)

    params = []
    if specific_args:
        params.extend(context.args.get(i, f"__unused{i}") for i in range(required_args))
    else:
        params.append("*args")

    if context.kwargs:
        params.append("**kwargs")

    lambda_code = f'lambda {", ".join(params)}: {expr_code}'

    return lambda_code, context.refs


def compile(expr, required_args=None):
    """Compiles `expr` into a Python lambda that takes at least `required_args` positional arguments."""

    lambda_code, refs = generate_code(expr, required_args=required_args)

    func_globals = dict(refs)
    if __debug__:
        func_globals["__refs"] = refs
        func_code = f'type({lambda_code!r}, (object,), dict(__slots__=(), __call__=staticmethod({lambda_code}), refs=__refs, code={lambda_code!r}, __repr__=lambda self: f"<{{self.code}} @ {{self.refs}}>"))()'
        func = eval(func_code, func_globals, {})
    else:
        func = eval(lambda_code, func_globals, {})
        func.code = lambda_code
        func.refs = refs
    return func
