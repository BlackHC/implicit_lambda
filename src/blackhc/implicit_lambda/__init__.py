"""Implicit lambda functions

An object that overloads all operations to make it easy to create implicit lambda functions.
It represents expressions using an AST that can be then interpreted or compiled into a regular
python expression/function.
"""
from blackhc.implicit_lambda.details.lambda_dsl import index, call, kw, arg, literal
from blackhc.implicit_lambda.details.lambda_dsl import get_expr
from blackhc.implicit_lambda.details.placeholders import _, a, b, c, d, x, y, z, w, i, j, k, l, arg0, arg1, arg2, arg3
from blackhc.implicit_lambda.details.glue import auto_lambda, to_lambda, wrap
