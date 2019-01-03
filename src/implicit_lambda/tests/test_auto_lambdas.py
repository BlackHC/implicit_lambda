from implicit_lambda import builtins
from implicit_lambda import itertools, functools
from implicit_lambda import _, to_lambda


def test_builtins():
    assert builtins.max(1, 2) == 2
    assert list(builtins.map(_ + 2, range(5))) == list(range(2, 7))
    assert list(builtins.filter(None, [1, 2, 0])) == [1, 2]
    assert list(builtins.filter(_ - 1, [1, 2, 0])) == [2, 0]
    assert not builtins.callable(0)
    assert builtins.callable(_)

    assert to_lambda(builtins.max._(_, 2))(3) == 3
    assert list(to_lambda(builtins.map._(_ + 2, _))([1, 2])) == [3, 4]
    assert list(to_lambda(builtins.filter._(_ - 1, _))([1, 2, 0])) == [2, 0]
