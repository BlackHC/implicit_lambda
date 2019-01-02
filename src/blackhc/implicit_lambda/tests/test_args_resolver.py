import pytest

from blackhc.implicit_lambda.args_resolver import (
    from_allowed_signatures,
    flexible_args,
    resolve_args,
    strict_resolver,
    CollectedArgs,
    ResolvedArgs,
)


def test_resolve_args_no_ordering():
    valid_context = {0: set(("x",)), 3: set(("y",))}
    assert resolve_args(valid_context) == {0: "x", 3: "y"}


def test_resolve_args_no_ordering_collision_fail():
    bad_context = {0: set(("x", "y"))}
    with pytest.raises(SyntaxError):
        resolve_args(bad_context)


def test_resolve_args_ordering_solves_collision():
    valid_context = {0: set(("x", "z")), 3: set(("y",))}
    assert resolve_args(valid_context, ("z", "x")) == {0: "z", 1: "x", 3: "y"}

    valid_context = {0: set(("x", "z"))}
    assert resolve_args(valid_context, ("z", "x")) == {0: "z", 1: "x"}


def test_resolve_args_ordering_unsufficient_ordering():
    valid_context = {0: set(("x", "z")), 3: set(("y",))}
    with pytest.raises(SyntaxError):
        resolve_args(valid_context, ("x", "y"))


def test_strict_resolver_accepts_valid():
    valid_context = CollectedArgs({0: set(("x",)), 2: set(("y",))}, [])
    assert strict_resolver(valid_context) == ResolvedArgs(("x", "__unused1", "y"), ())


def test_strict_resolver_rejects_invalid():
    valid_context = CollectedArgs({0: set(("x", "z")), 3: set(("y",))}, [])
    with pytest.raises(SyntaxError):
        strict_resolver(valid_context)


def test_flexible_args_no_ordering():
    valid_context = CollectedArgs({0: set(("x",)), 2: set(("y",))}, [])
    assert flexible_args(4)(valid_context) == ResolvedArgs(("x", "__unused1", "y", "__unused3"), ())


def test_flexible_args_no_ordering_collision_fail():
    bad_context = CollectedArgs({0: set(("x", "y"))}, [])
    with pytest.raises(SyntaxError):
        flexible_args(4)(bad_context)


def test_from_allowed_signatures_accepts_valid():
    valid_context = CollectedArgs({0: set(("x", "y"))}, [])
    assert from_allowed_signatures(("x"), ("y", "x"))(valid_context) == ResolvedArgs(("y", "x"), ())


def test_from_allowed_signatures_rejects_invalid():
    valid_context = CollectedArgs({0: set(("x", "y"))}, [])

    with pytest.raises(SyntaxError):
        from_allowed_signatures()(valid_context)
