"""
Expression AST.
"""
from enum import Enum
from dataclasses import dataclass
import typing


id_hash = lambda self: id(self)


@dataclass(frozen=True)
class Expression:
    __slots__ = ()
    __hash__ = id_hash


class AccessorOps(Enum):
    GET_ITEM = "getitem"
    GET_ATTRIBUTE = "getattribute"


@dataclass(frozen=True)
class AccessorExpression(Expression):
    __slots__ = ("op", "target", "key")
    __hash__ = id_hash
    op: AccessorOps
    target: Expression
    key: Expression


@dataclass(frozen=True)
class OpInfo:
    __slots__ = ("name", "num_args", "template")
    name: str
    num_args: typing.Union[int, typing.Tuple[int]]
    template: typing.Union[str, typing.Tuple[str]]


class ArithmeticOps(Enum):
    ADD = OpInfo("__add__", 2, "({} + {})")
    SUB = OpInfo("__sub__", 2, "({} - {})")
    MUL = OpInfo("__mul__", 2, "({} * {})")
    MATMUL = OpInfo("__matmul__", 2, "({} @ {})")
    TRUEDIV = OpInfo("__truediv__", 2, "({} / {})")
    FLOORDIV = OpInfo("__floordiv__", 2, "({} // {})")
    MOD = OpInfo("__mod__", 2, "({} % {})")
    DIVMOD = OpInfo("__divmod__", 2, "divmod({}, {})")
    LSHIFT = OpInfo("__lshift__", 2, "({} << {})")
    RSHIFT = OpInfo("__rshift__", 2, "({} >> {})")
    AND = OpInfo("__and__", 2, "({} & {})")
    XOR = OpInfo("__xor__", 2, "({} ^ {})")
    OR = OpInfo("__or__", 2, "({} | {})")

    RADD = OpInfo("__radd__", 2, "({1} + {0})")
    RSUB = OpInfo("__rsub__", 2, "({1} - {0})")
    RMUL = OpInfo("__rmul__", 2, "({1} * {0})")
    RMATMUL = OpInfo("__rmatmul__", 2, "({1} @ {0})")
    RTRUEDIV = OpInfo("__rtruediv__", 2, "({1} / {0})")
    RFLOORDIV = OpInfo("__rfloordiv__", 2, "({1} // {0})")
    RMOD = OpInfo("__rmod__", 2, "({1} % {0})")
    RDIVMOD = OpInfo("__rdivmod__", 2, "divmod({1}, {0})")
    RPOW = OpInfo("__rpow__", 2, "pow({1}, {0})")
    RLSHIFT = OpInfo("__rlshift__", 2, "({1} << {0})")
    RRSHIFT = OpInfo("__rrshift__", 2, "({1} >> {0})")
    RAND = OpInfo("__rand__", 2, "({1} & {0})")
    RXOR = OpInfo("__rxor__", 2, "({1} ^ {0})")
    ROR = OpInfo("__ror__", 2, "({1} | {0})")


class ComparisonOps(Enum):
    LT = OpInfo("__lt__", 2, "({} < {})")
    LE = OpInfo("__le__", 2, "({} <= {})")
    GT = OpInfo("__gt__", 2, "({} > {})")
    GE = OpInfo("__ge__", 2, "({} >= {})")
    EQ = OpInfo("__eq__", 2, "({} == {})")
    NE = OpInfo("__ne__", 2, "({} != {})")


class UnaryOps(Enum):
    POSITIVE = OpInfo("__pos__", 1, "(+{})")
    NEGATIVE = OpInfo("__neg__", 1, "(-{})")
    ABS = OpInfo("__abs__", 1, "abs({})")
    INVERT = OpInfo("__invert__", 1, "(~{})")
    TRUNC = OpInfo("__trunc__", 1, "math.trunc({})")
    FLOOR = OpInfo("__floor__", 1, "math.floor({})")
    CEIL = OpInfo("__ceil__", 1, "math.ceil({})")


Ops = set(ArithmeticOps) | set(ComparisonOps) | set(UnaryOps)


class OptionalArgOps(Enum):
    ROUND_1 = OpInfo("__round__", 1, "round({})")
    ROUND_2 = OpInfo("__round__", 2, "round({}, {})")
    POW_2 = OpInfo("__pow__", 2, "pow({}, {})")
    POW_3 = OpInfo("__pow__", 3, "pow({}, {}, {})")


class SpecialOps(Enum):
    INT = OpInfo("", 1, "int({})")
    FLOAT = OpInfo("", 1, "float({})")
    COMPLEX = OpInfo("", 1, "complex({})")
    STR = OpInfo("", 1, "str({})")
    REPR = OpInfo("", 1, "repr({})")


@dataclass(frozen=True)
class OpExpression(Expression):
    __slots__ = ("op", "num_args", "arg0", "arg1", "arg2")
    __hash__ = id_hash
    op: OpInfo
    num_args: int
    arg0: Expression
    arg1: Expression
    arg2: Expression


@dataclass(frozen=True)
class KwArgsAccessor(Expression):
    __slots__ = ("key",)
    key: str


@dataclass(frozen=True)
class ArgsAccessor(Expression):
    __slots__ = ("key","name")
    key: int
    name: str


@dataclass(frozen=True)
class CallExpression(Expression):
    __slots__ = ("target", "args", "kwargs")
    __hash__ = id_hash
    target: Expression
    args: list
    kwargs: dict


@dataclass(frozen=True)
class LiteralExpression(Expression):
    __slots__ = ["literal"]
    __hash__ = id_hash
    literal: object
