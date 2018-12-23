"""
Expression AST
"""
from enum import Enum
from dataclasses import dataclass


@dataclass
class Expression:
    __slots__ = ()


class AccessorOps(Enum):
    GET_ITEM = "getitem"
    GET_ATTRIBUTE = "getattribute"


@dataclass
class AccessorExpression(Expression):
    __slots__ = ('op', 'target', 'key')
    op: AccessorOps
    target: Expression
    key: Expression


class BinaryOp(Enum):
    ADD = ("add", "({} + {})")
    SUB = ("sub", "({} - {})")
    MUL = ("mul", "({} * {})")
    MATMUL = ("matmul", "({} @ {})")
    TRUEDIV = ("truediv", "({} / {})")
    FLOORDIV = ("floordiv", "({} // {})")
    MOD = ("mod", "({} % {})")
    DIVMOD = ("divmod", "divmod({}, {})")
    # TODO: POW is actually ternary!
    POW = ("pow", "({} ** {})")
    LSHIFT = ("lshift", "({} << {})")
    RSHIFT = ("rshift", "({} >> {})")
    AND = ("and", "({} & {})")
    XOR = ("xor", "({} ^ {})")
    OR = ("or", "({} | {})")

    @classmethod
    def print_wrappers(cls):
        for op in cls:
            print(f"""
    def __{op.value[0]}__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.{op.name}, self.expr, get_expr(other)))

    def __r{op.value[0]}__(self, other):
        return ImplicitLambda(BinaryExpression(BinaryOp.{op.name}, get_expr(other), self.expr))"""
                  )

    @classmethod
    def print_evals(cls):
        for op in cls:
            print(f"""
if expr.op == BinaryOp.{op.name}:
    return {op.value[1].format('eval_expr(expr.lhs, context)', 'eval_expr(expr.rhs, context)')}"""
                  )


@dataclass
class BinaryExpression(Expression):
    __slots__ = ('op', 'lhs', 'rhs')
    op: BinaryOp
    lhs: Expression
    rhs: Expression


@dataclass
class KwArgsAccessor(Expression):
    __slots__ = ('key',)
    key: str


@dataclass
class ArgsAccessor(Expression):
    __slots__ = ('key',)
    key: int


@dataclass
class CallExpression(Expression):
    __slots__ = ('target', 'args', 'kwargs')
    target: Expression
    args: list
    kwargs: dict