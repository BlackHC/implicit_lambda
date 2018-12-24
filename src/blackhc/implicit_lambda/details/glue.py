import functools

from blackhc.implicit_lambda.details import lambda_dsl
from blackhc.implicit_lambda.details import codegen


def to_lambda(expr, required_args=None):
    if callable(expr) and not isinstance(expr, lambda_dsl.LambdaDSL):
        # Assuem that this a callable, we'd like to use.
        return expr

    return codegen.compile(lambda_dsl.get_expr(expr), required_args=required_args)


def call(func: callable, *args, **kwargs):
    """Calls a resolved function `func` with `args` and `kwargs` that can contain expressions."""
    return lambda_dsl.call(to_lambda(callable, *args, **kwargs))


def wrap(func):
    """Wraps a given function to support expressions as parameters."""

    return functools.wraps(func)(lambda_dsl.literal(func))


def auto_lambda(func=None, *, args: list = None, kwargs: set = None):
    """Wraps a given function to accept implicit lambdas in addition to regular lambdas."""
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
            + [(f"{kwarg}", f"{kwarg}=to_lambda(arg{i})") for kwarg in kwargs]
            + [("**kwargs", "**kwargs")]
        )
    )

    code = f'lambda {", ".join(params)}: {func}({", ".join(wrapped)})'
    return code
