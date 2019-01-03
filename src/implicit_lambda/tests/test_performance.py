import pytest_benchmark
import operator
import functools

from implicit_lambda import _, to_lambda


def test_normal_lambda(benchmark):
    benchmark.extra_info["Debug Mode"] = __debug__

    def normal_lambda(x):
        return x + 2

    benchmark(lambda: normal_lambda(5))


def test_il_lambda(benchmark):
    benchmark.extra_info["Debug Mode"] = __debug__
    il_lambda = to_lambda(_ + 2)
    benchmark(lambda: il_lambda(5))


def test_op_chain(benchmark):
    benchmark.extra_info["Debug Mode"] = __debug__
    partial_add = functools.partial(operator.add, 2)
    benchmark(lambda: partial_add(5))
