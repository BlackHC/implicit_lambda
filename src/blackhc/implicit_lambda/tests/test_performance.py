import pytest
import pytest_benchmark
from blackhc.implicit_lambda import _, to_lambda


def test_normal_lambda(benchmark):
    normal_lambda = lambda x: x + 2
    benchmark(lambda: normal_lambda(5))


def test_il_lambda(benchmark):
    il_lambda = to_lambda(_ + 2)
    benchmark(lambda: il_lambda(5))
