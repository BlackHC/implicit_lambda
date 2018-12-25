# Implicit lambdas

[![Build Status](https://www.travis-ci.com/BlackHC/implicit_lambda.svg?branch=master)](https://www.travis-ci.com/BlackHC/implicit_lambda) [![codecov](https://codecov.io/gh/BlackHC/implicit_lambda/branch/master/graph/badge.svg)](https://codecov.io/gh/BlackHC/implicit_lambda) [![PyPI](https://img.shields.io/badge/PyPI-blackhc.implicit_lambda-blue.svg)](https://pypi.python.org/pypi/blackhc.implicit_lambda/)

This package adds support for implicit lambdas, so you can write `map(_ + 5, a_list)` instead of `map(lambda x: x + 5, a_list)`.

The code uses Python 3.7 features for brevity. The package could easily be made to work with earlier version. Please submit an issue if there is need.

Implicit lambdas are implemented using code generation. They are as fast as regular lambdas when running python with `-O` to enable optimizations.

```
--------------------------------------------- benchmark: 3 tests -----------------------------------
Name (time in ns)         Mean              StdDev              Median         OPS (Mops/s)
----------------------------------------------------------------------------------------------------
test_normal_lambda    196.3468 (1.01)     140.7775 (2.32)     166.9600 (1.0)         5.0930 (0.99)
test_il_lambda        196.6705 (1.01)     113.9049 (1.88)     171.6000 (1.03)        5.0846 (0.99)
test_op_chain         195.0673 (1.0)       60.6268 (1.0)      176.2300 (1.06)        5.1264 (1.0)
----------------------------------------------------------------------------------------------------
```
`il_lambda` uses implicit lambdas. `normal_lambda` uses a regular lambda. `op_chain` uses functools.partial and the operator module.

Without `-O`, lambdas with a more verbose `repr` are created:

```python
assert repr(_ + 5) == <LambdaDSL: lambda x: (x + 5) @ {}>
```

This results in up to 20% slower execution for very simple expressions. (A new type is created on the fly to hold the expression and resolving a call using a custom `__call__` is sufficient to incur such a penalty.)

For more complex expressions, the overhead will become negligible.

Python expressions are fully wrapped, including index operations `[]` (using `__getitem__`), member access (using `__getattribute__`) and any calls (`__calls`). This results in great flexibility.

To disambiguate between calls within the lambda and calling a lambda, implicit lambdas have to be explicitly converted into a callable/regular Python lambda.

`to_lambda` turns an implicit lambda expression into a Python lambda.

`auto_lambda` adds support for implicit lambdas to existing functions that take callables.

Wrapped versions of `builtin`, `functools` and `itertools` are provided out-of-the-box.

## Installation

To install using pip, use:

```
pip install blackhc.implicit_lambda
```

To run the tests, use:

```
python setup.py test
```

## Example

To enable implicit lambdas, import placeholder symbols as needed and import wrapped builtin functions to use implicit lambdas interchangably with regular ones.

Usually, `to_lambda` and other helper functions don't need to be called.

```python
from blackhc.implicit_lambda import _, x, y, to_lambda
from blackhc.implicit_lambda.builtins import map
```

Implicit lambda provides wrappers around all common builtins.

```python
    a_list = list(range(10))

    mapped_list = map(_ + 2, a_list)

    assert list(mapped_list) == list(range(2, 12))
```

There are also wrappers that turn builtins into lazy functions. A wrapped function provides a `._` version that can be used within an implicit lambda.

```python
    mapper = to_lambda(map._(x + 2, _))

    mapped_list = mapper(a_list)

    assert list(mapped_list) == list(range(2, 12))
```

Implicit lambdas supports nested expressions

```python
    mapped_list = map((_ << 3) * 3 - 23 * _ + 2, a_list)

    assert list(mapped_list) == list(range(2, 12))
```

More useful reprs are available in __debug__ mode (just don't use `-O` when running python):

```python
    another_lambda = to_lambda((_ << 3) * 3 - 23 * _ + 2)
    assert repr(another_lambda) == "<lambda x: ((((x << 3) * 3) - (23 * x)) + 2) @ {}>"
```

or:

```python
    assert (repr((_ << 3) * 3 - 23 * _ + 2) ==
            "<LambdaDSL: lambda x: ((((x << 3) * 3) - (23 * x)) + 2) @ {}>)"
```

Implicit lambdas support multiple arguments, too:

```python
    assert to_lambda(x * y)(5, 3) == 15
```

## Performance measurement

Run

```python
python -O -m pytest -k test_performance --benchmark-warmup=on --benchmark-autosave --benchmark-disable-gc
```
