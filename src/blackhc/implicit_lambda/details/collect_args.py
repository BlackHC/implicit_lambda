"""Collect all positional arguments and keyword arguments."""
import collections
from dataclasses import dataclass
import typing

from blackhc.implicit_lambda.details import expression


@dataclass(frozen=True)
class ComputedArgs:
    args: tuple
    kwargs: tuple


@dataclass(frozen=True)
class CollectArgsContext:
    __slots__ = ("args", "kwargs")
    args: typing.Dict[int, typing.Set]
    kwargs: list

    def add_arg(self, accessor: expression.ArgsAccessor):
        order = accessor.order
        if order not in self.args:
            s = self.args[order] = set()
        else:
            s = self.args[order]
        s.add(accessor.name)

    def add_kwarg(self, accessor: expression.KwArgsAccessor):
        if accessor.name not in self.kwargs:
            self.kwargs.append(accessor.name)


def resolve_args(args: typing.Dict[int, typing.Set], ordering: tuple = None) -> dict:
    ordering = ordering or ()

    ordering_set = set(ordering)
    max_order = max(args.keys(), default=-1)
    order = 0

    resolved_args = {}
    while order <= max_order:
        if order in args:
            order_args = args[order]
            if len(order_args) > 1:
                if not (order_args <= ordering_set):
                    raise SyntaxError(
                        f"Got arguments: {args}. Cannot order {order_args}: only got ordering {ordering}!"
                    )

                min_index = min(ordering.index(arg) for arg in order_args)
                min_arg = ordering[min_index]
                resolved_args[order] = min_arg

                order_args.remove(min_arg)
                order_args |= args.get(order + 1, set())
                args[order + 1] = order_args
                max_order = max(max_order, order + 1)
            else:
                resolved_args[order] = order_args.pop()
        order += 1

    return resolved_args


def get_arg_tuple(resolved_args: dict, required_args=None) -> tuple:
    required_args = max(max(resolved_args.keys(), default=-1) + 1, required_args or 0)
    return tuple(resolved_args.get(i, f"__unused{i}") for i in range(required_args))


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
    context = context or CollectArgsContext(args={}, kwargs=[])
    collect_args_(expr, context)
    return context


def compute_args(expr, *, required_args=None, ordering=None):
    collect_args_context = collect_args(expr)
    resolved_args = resolve_args(collect_args_context.args, ordering=ordering)
    args = get_arg_tuple(resolved_args, required_args=required_args)

    return ComputedArgs(args=args, kwargs=collect_args_context.kwargs)
