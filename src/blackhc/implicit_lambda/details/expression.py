"""
Expression AST.
"""
from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class Expression:
    __slots__ = ()


class AccessorOps(Enum):
    GET_ITEM = "getitem"
    GET_ATTRIBUTE = "getattribute"


@dataclass(frozen=True)
class AccessorExpression(Expression):
    __slots__ = ("op", "target", "key")
    op: AccessorOps
    target: Expression
    key: Expression


class BinaryOps(Enum):
    ADD = ("add", "({} + {})")
    SUB = ("sub", "({} - {})")
    MUL = ("mul", "({} * {})")
    MATMUL = ("matmul", "({} @ {})")
    TRUEDIV = ("truediv", "({} / {})")
    FLOORDIV = ("floordiv", "({} // {})")
    MOD = ("mod", "({} % {})")
    DIVMOD = ("divmod", "divmod({}, {})")
    # TODO: POW is actually ternary!
    POW = ("pow", "pow({}, {})")
    LSHIFT = ("lshift", "({} << {})")
    RSHIFT = ("rshift", "({} >> {})")
    AND = ("and", "({} & {})")
    XOR = ("xor", "({} ^ {})")
    OR = ("or", "({} | {})")


@dataclass(frozen=True)
class BinaryExpression(Expression):
    __slots__ = ("op", "lhs", "rhs")
    op: BinaryOps
    lhs: Expression
    rhs: Expression


@dataclass(frozen=True)
class KwArgsAccessor(Expression):
    __slots__ = ("key",)
    key: str


@dataclass(frozen=True)
class ArgsAccessor(Expression):
    __slots__ = ("key",)
    key: int


@dataclass(frozen=True)
class CallExpression(Expression):
    __slots__ = ("target", "args", "kwargs")
    target: Expression
    args: list
    kwargs: dict


@dataclass(frozen=True)
class LiteralExpression(Expression):
    __slots__ = ["literal"]
    literal: object
