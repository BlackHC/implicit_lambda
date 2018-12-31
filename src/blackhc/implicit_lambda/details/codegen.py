"""Code generation from expression to Python lambda."""
import builtins
import math
from dataclasses import dataclass

from blackhc.implicit_lambda.details import expression


@dataclass
class CollectArgsContext:
    __slots__ = ('args', 'kwargs')
    args: dict
    kwargs: set

    def add_arg(self, accessor: expression.ArgsAccessor):
        if accessor.key in self.args:
            if self.args[accessor.key] != accessor.name:
                raise SyntaxError(f'Argument name mismatch: trying to use argument accessor {accessor}'
                                  f'when the argument name has already been bound to {self.args[accessor.key]}!')
        else:
            self.args[accessor.key] = accessor.name

    def add_kwarg(self, accessor: expression.KwArgsAccessor):
        self.kwargs.add(accessor.key)


def collect_args_(expr, context: CollectArgsContext):
    if expr is None:
        return

    if isinstance(expr, expression.Expression):
        if isinstance(expr, expression.AccessorExpression):
            collect_args_(expr.target, context)
            collect_args_(expr.key, context)
        elif isinstance(expr, expression.OpExpression):
            collect_args_(expr.arg0, context)
            collect_args_(expr.arg1, context)
            collect_args_(expr.arg2, context)
        elif isinstance(expr, expression.CallExpression):
            collect_args_(expr.target, context)
            collect_args_(expr.args, context)
            collect_args_(expr.kwargs, context)
        elif isinstance(expr, expression.ArgsAccessor):
            context.add_arg(expr)
        elif isinstance(expr, expression.KwArgsAccessor):
            context.add_kwarg(expr)
        elif isinstance(expr, expression.LiteralExpression):
            pass
        else:
            raise NotImplementedError(type(expr))
    elif isinstance(expr, tuple):
        for item in expr:
            collect_args_(item, context)
    elif isinstance(expr, list):
        for item in expr:
            collect_args_(item, context)
    elif isinstance(expr, dict):
        for key, value in expr.items():
            collect_args_(key, context)
            collect_args_(value, context)
    elif isinstance(expr, set):
        for item in expr:
            collect_args_(item, context)
    elif isinstance(expr, slice):
        collect_args_(expr.start, context)
        collect_args_(expr.stop, context)
        collect_args_(expr.step, context)


def collect_args(expr, context: CollectArgsContext = None) -> CollectArgsContext:
    context = context or CollectArgsContext(args={}, kwargs=set())
    collect_args_(expr, context)
    return context


@dataclass
class CodegenContext:
    __slots__ = ("refs", "args", "kwargs")
    refs: dict
    args: dict
    kwargs: dict


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

    if isinstance(expr, slice):
        return f"slice({codegen_expr(expr.start, context)}, {codegen_expr(expr.stop, context)}, {codegen_expr(expr.step, context)})"

    return add_ref(context, expr)


def generate_lambda(expr, required_args=None):
    if required_args is None:
        required_args = 0

    collect_args_context = collect_args(expr)

    context = CodegenContext({}, {}, {})

    context.args = collect_args_context.args
    context.kwargs = {kwarg: f"kwargs[{kwarg!r}]" for kwarg in collect_args_context.kwargs}

    required_args = max(max(context.args.keys(), default=-1) + 1, required_args)
    context.refs = {}
    expr_code = codegen_expr(expr, context)

    params = []
    params.extend(context.args.get(i, f"__unused{i}") for i in range(required_args))

    if context.kwargs:
        params.append("**kwargs")

    lambda_code = f'lambda {", ".join(params)}: {expr_code}'

    return lambda_code, context.refs


def compile(expr, required_args=None):
    """Compiles `expr` into a Python lambda that takes at least `required_args` positional arguments."""

    lambda_code, refs = generate_lambda(expr, required_args=required_args)

    func_globals = dict(refs)
    func_globals["__builtins__"] = builtins
    func_globals["math"] = math
    if __debug__:
        func_globals["__refs"] = refs
        func_code = f'type({lambda_code!r}, (object,), dict(__slots__=(), __call__=staticmethod({lambda_code}), refs=__refs, code={lambda_code!r}, __repr__=lambda self: f"<{{self.code}} @ {{self.refs}}>"))()'
        func = eval(func_code, func_globals, {})
    else:
        func = eval(lambda_code, func_globals, {})
        func.code = lambda_code
        func.refs = refs
    return func
