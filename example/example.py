import pytest

from blackhc.implicit_lambda import _, x, y, to_lambda
from blackhc.implicit_lambda.builtins import map, filter


def main():
    # ... has wrappers around all common builtins.
    a_list = list(range(10))

    mapped_list = map(_ + 2, a_list)

    assert list(mapped_list) == list(range(2, 12))

    # ... has wrappers that turn builtins into lazy functions, too
    mapper = to_lambda(map._(x + 2, _))

    mapped_list = mapper(a_list)

    assert list(mapped_list) == list(range(2, 12))

    # ... supports nested expressions
    mapped_list = map((_ << 3) * 3 - 23 * _ + 2, a_list)

    assert list(mapped_list) == list(range(2, 12))

    # ... has useful reprs in __debug__ mode (don't specify -O)
    another_lambda = to_lambda((_ << 3) * 3 - 23 * _ + 2)
    assert repr(another_lambda) == '<lambda x: ((((x << 3) * 3) - (23 * x)) + 2) @ {}>'

    # ... (or, but not executable)
    assert repr((_ << 3) * 3 - 23 * _ + 2) == '<LambdaDSL: lambda x: ((((x << 3) * 3) - (23 * x)) + 2) @ {}>'

    # ... supports multiple arguments
    assert to_lambda(x * y)(5, 3) == 15


if __name__ == "__main__":
    main()
