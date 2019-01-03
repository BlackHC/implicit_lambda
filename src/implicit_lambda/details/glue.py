import functools

from implicit_lambda.details import lambda_dsl
from implicit_lambda.details import codegen


def to_lambda(expr, *, args_resolver=None):
    """Convert expr into a Python lambda.

    If `expr` is an implicit lambda or literal compile it into a Python lambda.
    If `expr` is a callable, pass it through.
    """
    if expr is None:
        return expr

    if callable(expr) and not isinstance(expr, lambda_dsl.LambdaDSL):
        # Assume that this a callable that we'd like to use.
        return expr

    return codegen.compile(lambda_dsl.get_expr(expr), args_resolver=args_resolver)


def call(func: callable, *args, **kwargs):
    """Calls `func` with `args` and `kwargs` that can contain expressions."""
    return lambda_dsl.call(to_lambda(func), *args, **kwargs)


def wrap(func):
    """A decorator that wraps a given function to support implicit lambda expressions as parameters."""

    return functools.wraps(func)(lambda_dsl.literal(func))


def auto_lambda(func=None, *, args: list = None, kwargs: set = None):
    """A decorator that wraps a given function to accept implicit lambdas in addition to regular lambdas.

    `args` and `kwargs` specify the arguments that should be converted to Python lambdas if necesary.
    """

    code = auto_lambda_code(args=args, kwargs=kwargs)

    def wrapper(func):
        wrapped = functools.update_wrapper(eval(code, dict(func=func, to_lambda=to_lambda)), func)
        wrapped._ = functools.update_wrapper(eval(code, dict(func=wrap(func), to_lambda=to_lambda)), func)
        return wrapped

    if func is not None:
        return wrapper(func)

    return wrapper


def auto_lambda_code(func=None, args: list = None, kwargs: set = None):
    """Output code to wrap a given function to accept implicit lambdas in addition to regular lambdas."""
    if func is None:
        func = "func"
    if args is None:
        args = []
    if kwargs is None:
        kwargs = set()

    params, wrapped = zip(
        *(
            [(f"arg{i}", f"to_lambda(arg{i})" if convert else f"arg{i}") for i, convert in enumerate(args)]
            + [("*args", "*args")]
            + [(f"{kwarg}", f"{kwarg}=to_lambda({kwarg})") for kwarg in kwargs]
            + [("**kwargs", "**kwargs")]
        )
    )

    code = f'lambda {", ".join(params)}: {func}({", ".join(wrapped)})'
    return code
