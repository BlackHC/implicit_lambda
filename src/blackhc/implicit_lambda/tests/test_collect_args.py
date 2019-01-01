import pytest

from blackhc.implicit_lambda.details import collect_args


def test_no_ordering():
    valid_context = {0: set(("x",)), 3: set(("y",))}
    assert collect_args.resolve_args(valid_context) == {0: "x", 3: "y"}


def test_no_ordering_collision_fail():
    bad_context = {0: set(("x", "y"))}
    with pytest.raises(SyntaxError):
        collect_args.resolve_args(bad_context)


def test_ordering_solves_collision():
    valid_context = {0: set(("x", "z")), 3: set(("y",))}
    assert collect_args.resolve_args(valid_context, ("z", "x")) == {0: "z", 1: "x", 3: "y"}

    valid_context = {0: set(("x", "z"))}
    assert collect_args.resolve_args(valid_context, ("z", "x")) == {0: "z", 1: "x"}


def test_ordering_unsufficient_ordering():
    valid_context = {0: set(("x", "z")), 3: set(("y",))}
    with pytest.raises(SyntaxError):
        collect_args.resolve_args(valid_context, ("x", "y"))
