"""Two args resolvers that can be used with `to_lambda`"""
import itertools
import typing

from dataclasses import dataclass


@dataclass(frozen=True)
class ResolvedArgs:
    __slots__ = ("args", "kwargs")
    args: tuple
    kwargs: tuple


@dataclass(frozen=True)
class CollectedArgs:
    __slots__ = ("args", "kwargs")
    args: typing.Dict[int, typing.Set]
    kwargs: list


def strict_resolver(context: CollectedArgs):
    for order, arg_set in context.args.items():
        if len(arg_set) > 1:
            raise SyntaxError(f"Arg conflict found for {context} and the strict resolver was used!")
    resolved_args = {order: arg_set.pop() for order, arg_set in context.args.items() if arg_set}

    if resolved_args.keys() & set(context.kwargs):
        raise SyntaxError(f"Conflict between args and kwargs in {context}!")

    args = get_arg_tuple(resolved_args)

    computed_args = ResolvedArgs(args=args, kwargs=tuple(context.kwargs))
    return computed_args


def flexible_args(required_args=None, ordering=None):
    def resolver(context: CollectedArgs):
        resolved_args = resolve_args(context.args, ordering=ordering)
        args = get_arg_tuple(resolved_args, required_args=required_args)

        return ResolvedArgs(args=args, kwargs=tuple(context.kwargs))

    return resolver


def from_allowed_signatures(*signatures):
    def resolver(context: CollectedArgs):
        if context.kwargs:
            assert SyntaxError(f"Kwargs not supported in `from_allowed_signatures`! {context}")

        args = set(itertools.chain.from_iterable(context.args.values()))
        for signature in signatures:
            assert isinstance(signature, (tuple, list))
            if args <= set(signature):
                return ResolvedArgs(signature, ())

        raise SyntaxError(f"{context} does not match any of the allowed signatures {signatures}!")

    return resolver


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
