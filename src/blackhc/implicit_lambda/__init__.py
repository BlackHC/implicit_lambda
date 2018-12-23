"""Implicit lambda functions

An object that overloads all operations to make it easy to create implicit lambda functions.
It represents expressions using an AST that can be then interpreted or compiled into a regular
python expression/function.
"""
from blackhc.implicit_lambda import implicit_lambda
from blackhc.implicit_lambda import codegen
from blackhc.implicit_lambda import interpret
from blackhc.implicit_lambda import expression

from blackhc.implicit_lambda.implicit_lambda import index, call


def to_lambda(expr, required_args=0):
    if not isinstance(expr, implicit_lambda.ImplicitLambda):
        return expr
    expr = implicit_lambda.get_expr(expr)

    args_set = set()
    kwargs_set = set()
    codegen.collect_args(expr, args_set, kwargs_set)
    kwargs = {kwarg: f'kwargs[{kwarg!r}]' for kwarg in kwargs_set}

    specific_args = False
    if len(args_set) < 4:
        for available_args in [
            ('x', 'y', 'z', 'w'),
            ('a', 'b', 'c', 'd'),
            ('i', 'j', 'k', 'l'),
            ('arg0', 'arg1', 'arg2', 'arg3')
        ]:
            if not set(available_args).intersection(kwargs_set):
                specific_args = True
                args = {j: available_args[i] for i, j in enumerate(sorted(args_set))}
                break
    if not specific_args:
        args = {i: f'args[{i}]' for i in args_set}

    required_args = max(max(args_set, default=-1) + 1, required_args)
    refs = {}
    expr_code = codegen.codegen_expr(expr, refs, args, kwargs)

    if specific_args:
        args_code = ','.join(
            [args[i] if i in args else f'__unused_arg_{i}' for i in range(required_args)])
    else:
        args_code = '*args'
        
    if kwargs:
        func_code = f'lambda {args_code}, **kwargs: {expr_code}'
    else:
        func_code = f'lambda {args_code}: {expr_code}'
    
    func = eval(func_code, refs, {})
    func.sourcecode = func_code
    return func

def interpreted_lambda(expr: implicit_lambda.ImplicitLambda):
    return lambda *args, **kwargs: interpret.eval_expr(implicit_lambda.get_expr(expr), interpret.Context(args, kwargs))


_ = implicit_lambda.ImplicitLambda(expression.ArgsAccessor(0))
