"""Collect all positional arguments and keyword arguments."""
from dataclasses import dataclass
import typing

from implicit_lambda.details import expression
from implicit_lambda.args_resolver import CollectedArgs, ResolvedArgs, strict_resolver


def add_arg(context: CollectedArgs, accessor: expression.ArgsAccessor):
    order = accessor.order
    if order not in context.args:
        s = context.args[order] = set()
    else:
        s = context.args[order]
    s.add(accessor.name)


def add_kwarg(context: CollectedArgs, accessor: expression.KwArgsAccessor):
    if accessor.name not in context.kwargs:
        context.kwargs.append(accessor.name)


def collect_args_(expr, context: CollectedArgs):
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
            add_arg(context, expr)
        elif isinstance(expr, expression.KwArgsAccessor):
            add_kwarg(context, expr)
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


def collect_args(expr, context: CollectedArgs = None) -> CollectedArgs:
    context = context or CollectedArgs(args={}, kwargs=[])
    collect_args_(expr, context)
    return context


def compute_args(expr, *, args_resolver=None):
    args_resolver = args_resolver or strict_resolver

    context = collect_args(expr)
    computed_args = args_resolver(context)

    return computed_args
