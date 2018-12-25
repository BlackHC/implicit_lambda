from blackhc.implicit_lambda.details import expression
from blackhc.implicit_lambda.details import glue


class BinaryExpression:
    @staticmethod
    def generate_implicit_lambda_wrappers():
        for op in expression.BinaryOps:
            print(
                f"""
    def __{op.value[0]}__(self, other):
        return ImplicitLambda(expression.BinaryExpression(expression.BinaryOp.{op.name}, self.expr, get_expr(other)))

    def __r{op.value[0]}__(self, other):
        return ImplicitLambda(expression.BinaryExpression(expression.BinaryOp.{op.name}, get_expr(other), self.expr))"""
            )

    @staticmethod
    def generate_evals():
        for op in expression.BinaryOps:
            print(
                f"""
    if expr.op == expression.BinaryOp.{op.name}:
        return {op.value[1].format('eval_expr(expr.lhs, context)', 'eval_expr(expr.rhs, context)')}"""
            )


def auto_lambda_static_code(func, *, module="builtins", args=None, kwargs=None):
    wrapped_func = f"{module}.{func}"
    code = glue.auto_lambda_code(wrapped_func, args=args, kwargs=kwargs)
    wrapped_code = glue.auto_lambda_code(f"wrap({wrapped_func})", args=args, kwargs=kwargs)
    if code != wrapped_func:
        print(f"{func} = functools.update_wrapper({code}, {wrapped_func})")
    else:
        print(f"{func} = {wrapped_func}")
    print(f"{func}._ = functools.update_wrapper({wrapped_code}, {wrapped_func})")


def auto_lambda_builtins():
    auto_lambda_static_code("abs")
    auto_lambda_static_code("all")
    auto_lambda_static_code("any")
    auto_lambda_static_code("ascii")
    auto_lambda_static_code("bin")
    auto_lambda_static_code("bool")
    auto_lambda_static_code("breakpoint")
    auto_lambda_static_code("bytearray")
    auto_lambda_static_code("bytes")
    auto_lambda_static_code("chr")
    auto_lambda_static_code("compile")
    auto_lambda_static_code("complex")
    auto_lambda_static_code("delattr")
    auto_lambda_static_code("dict")
    auto_lambda_static_code("dir")
    auto_lambda_static_code("divmod")
    auto_lambda_static_code("enumerate")
    auto_lambda_static_code("eval")
    auto_lambda_static_code("exec")
    auto_lambda_static_code("float")
    auto_lambda_static_code("format")
    auto_lambda_static_code("frozenset")
    auto_lambda_static_code("getattr")
    auto_lambda_static_code("globals")
    auto_lambda_static_code("hasattr")
    auto_lambda_static_code("hash")
    auto_lambda_static_code("hex")
    auto_lambda_static_code("id")
    auto_lambda_static_code("input")
    auto_lambda_static_code("int")
    auto_lambda_static_code("isinstance")
    auto_lambda_static_code("issubclass")
    auto_lambda_static_code("iter")
    auto_lambda_static_code("len")
    auto_lambda_static_code("list")
    auto_lambda_static_code("locals")
    auto_lambda_static_code("max")
    auto_lambda_static_code("memoryview")
    auto_lambda_static_code("min")
    auto_lambda_static_code("next")
    auto_lambda_static_code("oct")
    auto_lambda_static_code("open")
    auto_lambda_static_code("ord")
    auto_lambda_static_code("pow")
    auto_lambda_static_code("print")
    auto_lambda_static_code("range")
    auto_lambda_static_code("repr")
    auto_lambda_static_code("reversed")
    auto_lambda_static_code("round")
    auto_lambda_static_code("set")
    auto_lambda_static_code("setattr")
    auto_lambda_static_code("slice")
    auto_lambda_static_code("sorted")
    auto_lambda_static_code("str")
    auto_lambda_static_code("sum")
    auto_lambda_static_code("tuple")
    auto_lambda_static_code("type")
    auto_lambda_static_code("vars")
    auto_lambda_static_code("zip")

    # NOTE: to_lambda converts everything that is not already callable into something callable...
    auto_lambda_static_code("callable", args=[False])

    auto_lambda_static_code("map", args=[True])
    # auto_lambda_static_code('filter', args=[True])

    print(
        """
filter = functools.update_wrapper(lambda arg0, *args, **kwargs: builtins.filter(to_lambda(arg0, required_args=1) if arg0 is not None else None, *args, **kwargs), builtins.filter)
filter._ = functools.update_wrapper(lambda arg0, *args, **kwargs: wrap(builtins.filter)(to_lambda(arg0, required_args=1) if arg0 is not None else None, *args, **kwargs), builtins.filter)
    """
    )


def auto_lambda_functools():
    auto_lambda_static_code("partial", module="functools", args=[True])
    auto_lambda_static_code("partialmethod", module="functools", args=[True])
    auto_lambda_static_code("update_wrapper", module="functools", args=[True])
    auto_lambda_static_code("wraps", module="functools", args=[True])

    # auto_lambda_static_code('reduce', module='functools', args=[True])
    print(
        """
reduce = functools.update_wrapper(lambda arg0, *args, **kwargs: functools.reduce(to_lambda(arg0, required_args=2), *args, **kwargs), functools.reduce)
reduce._ = functools.update_wrapper(lambda arg0, *args, **kwargs: wrap(functools.reduce)(to_lambda(arg0, required_args=2), *args, **kwargs), functools.reduce)
    """
    )


def auto_lambda_itertools():
    auto_lambda_static_code("chain", module="itertools")
    auto_lambda_static_code("combinations", module="itertools")
    auto_lambda_static_code("combinations_with_replacement", module="itertools")
    auto_lambda_static_code("compress", module="itertools")
    auto_lambda_static_code("count", module="itertools")
    auto_lambda_static_code("cycle", module="itertools")
    auto_lambda_static_code("islice", module="itertools")
    auto_lambda_static_code("permutations", module="itertools")
    auto_lambda_static_code("product", module="itertools")
    auto_lambda_static_code("repeat", module="itertools")
    auto_lambda_static_code("tee", module="itertools")
    auto_lambda_static_code("zip_longest", module="itertools")

    auto_lambda_static_code("dropwhile", module="itertools", args=[True])
    auto_lambda_static_code("filterfalse", module="itertools", args=[True])
    auto_lambda_static_code("takewhile", module="itertools", args=[True])
    auto_lambda_static_code("starmap", module="itertools", args=[True])

    # auto_lambda_static_code('groupby', module='itertools', args=[False, True])
    # auto_lambda_static_code('accumulate', module='itertools', args=[False, True])
    print(
        """
accumulate = functools.update_wrapper(lambda arg0, arg1=operator.add, *args, **kwargs: itertools.accumulate(arg0, to_lambda(arg1), *args, **kwargs), itertools.accumulate)
accumulate._ = functools.update_wrapper(lambda arg0, arg1=operator.add, *args, **kwargs: wrap(itertools.accumulate)(arg0, to_lambda(arg1), *args, **kwargs), itertools.accumulate)
groupby = functools.update_wrapper(lambda arg0, arg1=None, *args, **kwargs: itertools.groupby(arg0, to_lambda(arg1) if arg1 else None, *args, **kwargs), itertools.groupby)
groupby._ = functools.update_wrapper(lambda arg0, arg1=None, *args, **kwargs: wrap(itertools.groupby)(arg0, to_lambda(arg1) if arg1 else None, *args, **kwargs), itertools.groupby)
    """
    )
