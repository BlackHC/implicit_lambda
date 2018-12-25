import codegen


def test_binary_ops():
    codegen.BinaryExpression.generate_evals()
    codegen.BinaryExpression.generate_implicit_lambda_wrappers()


def test_auto_lamba():
    codegen.auto_lambda_builtins()
    codegen.auto_lambda_functools()
    codegen.auto_lambda_itertools()
