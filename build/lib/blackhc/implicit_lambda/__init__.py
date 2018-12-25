"""Implicit lambdas

Import placeholders (_, x, y, z, ...) as needed. `_` is a placeholder for a first positional argument.
The other placeholders come in quadruples (x, y, z, w, or a, b, c, d, and so on).
"""
from blackhc.implicit_lambda.details.lambda_dsl import index, kw, arg, literal
from blackhc.implicit_lambda.details.lambda_dsl import get_expr
from blackhc.implicit_lambda.details.placeholders import _, a, b, c, d, x, y, z, w, i, j, k, l, arg0, arg1, arg2, arg3
from blackhc.implicit_lambda.details.glue import auto_lambda, to_lambda, wrap, call