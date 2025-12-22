import sys
from pathlib import Path

import pytest

# codegen.py is a dev tool at the project root, not part of the package
# test_codegen.py -> tests/ -> implicit_lambda/ -> src/ -> project_root
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import codegen  # noqa: E402


def test_binary_ops():
    codegen.OpExpression.generate_evals()
    codegen.OpExpression.generate_lambda_dsl_wrappers()


def test_auto_lambda():
    codegen.auto_lambda_builtins()
    codegen.auto_lambda_functools()
    codegen.auto_lambda_itertools()
