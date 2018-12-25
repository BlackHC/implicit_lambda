import codegen


def test_binary_ops():
    codegen.OpExpression.generate_evals()
    codegen.OpExpression.generate_lambda_dsl_wrappers()


def test_auto_lamba():
    codegen.auto_lambda_builtins()
    codegen.auto_lambda_functools()
    codegen.auto_lambda_itertools()
