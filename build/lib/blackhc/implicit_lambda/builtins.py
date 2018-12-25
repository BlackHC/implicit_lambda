"""Implicit lambda wrappers around all Python builtins functions."""

import builtins
import functools
from blackhc.implicit_lambda import wrap, to_lambda

abs = functools.update_wrapper(lambda *args, **kwargs: builtins.abs(*args, **kwargs), builtins.abs)
abs._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.abs)(*args, **kwargs), builtins.abs)
all = functools.update_wrapper(lambda *args, **kwargs: builtins.all(*args, **kwargs), builtins.all)
all._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.all)(*args, **kwargs), builtins.all)
any = functools.update_wrapper(lambda *args, **kwargs: builtins.any(*args, **kwargs), builtins.any)
any._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.any)(*args, **kwargs), builtins.any)
ascii = functools.update_wrapper(lambda *args, **kwargs: builtins.ascii(*args, **kwargs), builtins.ascii)
ascii._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.ascii)(*args, **kwargs), builtins.ascii)
bin = functools.update_wrapper(lambda *args, **kwargs: builtins.bin(*args, **kwargs), builtins.bin)
bin._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.bin)(*args, **kwargs), builtins.bin)
bool = functools.update_wrapper(lambda *args, **kwargs: builtins.bool(*args, **kwargs), builtins.bool)
bool._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.bool)(*args, **kwargs), builtins.bool)
breakpoint = functools.update_wrapper(lambda *args, **kwargs: builtins.breakpoint(*args, **kwargs), builtins.breakpoint)
breakpoint._ = functools.update_wrapper(
    lambda *args, **kwargs: wrap(builtins.breakpoint)(*args, **kwargs), builtins.breakpoint
)
bytearray = functools.update_wrapper(lambda *args, **kwargs: builtins.bytearray(*args, **kwargs), builtins.bytearray)
bytearray._ = functools.update_wrapper(
    lambda *args, **kwargs: wrap(builtins.bytearray)(*args, **kwargs), builtins.bytearray
)
bytes = functools.update_wrapper(lambda *args, **kwargs: builtins.bytes(*args, **kwargs), builtins.bytes)
bytes._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.bytes)(*args, **kwargs), builtins.bytes)
chr = functools.update_wrapper(lambda *args, **kwargs: builtins.chr(*args, **kwargs), builtins.chr)
chr._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.chr)(*args, **kwargs), builtins.chr)
compile = functools.update_wrapper(lambda *args, **kwargs: builtins.compile(*args, **kwargs), builtins.compile)
compile._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.compile)(*args, **kwargs), builtins.compile)
complex = functools.update_wrapper(lambda *args, **kwargs: builtins.complex(*args, **kwargs), builtins.complex)
complex._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.complex)(*args, **kwargs), builtins.complex)
delattr = functools.update_wrapper(lambda *args, **kwargs: builtins.delattr(*args, **kwargs), builtins.delattr)
delattr._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.delattr)(*args, **kwargs), builtins.delattr)
dict = functools.update_wrapper(lambda *args, **kwargs: builtins.dict(*args, **kwargs), builtins.dict)
dict._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.dict)(*args, **kwargs), builtins.dict)
dir = functools.update_wrapper(lambda *args, **kwargs: builtins.dir(*args, **kwargs), builtins.dir)
dir._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.dir)(*args, **kwargs), builtins.dir)
divmod = functools.update_wrapper(lambda *args, **kwargs: builtins.divmod(*args, **kwargs), builtins.divmod)
divmod._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.divmod)(*args, **kwargs), builtins.divmod)
enumerate = functools.update_wrapper(lambda *args, **kwargs: builtins.enumerate(*args, **kwargs), builtins.enumerate)
enumerate._ = functools.update_wrapper(
    lambda *args, **kwargs: wrap(builtins.enumerate)(*args, **kwargs), builtins.enumerate
)
eval = functools.update_wrapper(lambda *args, **kwargs: builtins.eval(*args, **kwargs), builtins.eval)
eval._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.eval)(*args, **kwargs), builtins.eval)
exec = functools.update_wrapper(lambda *args, **kwargs: builtins.exec(*args, **kwargs), builtins.exec)
exec._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.exec)(*args, **kwargs), builtins.exec)
float = functools.update_wrapper(lambda *args, **kwargs: builtins.float(*args, **kwargs), builtins.float)
float._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.float)(*args, **kwargs), builtins.float)
format = functools.update_wrapper(lambda *args, **kwargs: builtins.format(*args, **kwargs), builtins.format)
format._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.format)(*args, **kwargs), builtins.format)
frozenset = functools.update_wrapper(lambda *args, **kwargs: builtins.frozenset(*args, **kwargs), builtins.frozenset)
frozenset._ = functools.update_wrapper(
    lambda *args, **kwargs: wrap(builtins.frozenset)(*args, **kwargs), builtins.frozenset
)
getattr = functools.update_wrapper(lambda *args, **kwargs: builtins.getattr(*args, **kwargs), builtins.getattr)
getattr._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.getattr)(*args, **kwargs), builtins.getattr)
globals = functools.update_wrapper(lambda *args, **kwargs: builtins.globals(*args, **kwargs), builtins.globals)
globals._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.globals)(*args, **kwargs), builtins.globals)
hasattr = functools.update_wrapper(lambda *args, **kwargs: builtins.hasattr(*args, **kwargs), builtins.hasattr)
hasattr._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.hasattr)(*args, **kwargs), builtins.hasattr)
hash = functools.update_wrapper(lambda *args, **kwargs: builtins.hash(*args, **kwargs), builtins.hash)
hash._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.hash)(*args, **kwargs), builtins.hash)
hex = functools.update_wrapper(lambda *args, **kwargs: builtins.hex(*args, **kwargs), builtins.hex)
hex._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.hex)(*args, **kwargs), builtins.hex)
id = functools.update_wrapper(lambda *args, **kwargs: builtins.id(*args, **kwargs), builtins.id)
id._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.id)(*args, **kwargs), builtins.id)
input = functools.update_wrapper(lambda *args, **kwargs: builtins.input(*args, **kwargs), builtins.input)
input._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.input)(*args, **kwargs), builtins.input)
int = functools.update_wrapper(lambda *args, **kwargs: builtins.int(*args, **kwargs), builtins.int)
int._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.int)(*args, **kwargs), builtins.int)
isinstance = functools.update_wrapper(lambda *args, **kwargs: builtins.isinstance(*args, **kwargs), builtins.isinstance)
isinstance._ = functools.update_wrapper(
    lambda *args, **kwargs: wrap(builtins.isinstance)(*args, **kwargs), builtins.isinstance
)
issubclass = functools.update_wrapper(lambda *args, **kwargs: builtins.issubclass(*args, **kwargs), builtins.issubclass)
issubclass._ = functools.update_wrapper(
    lambda *args, **kwargs: wrap(builtins.issubclass)(*args, **kwargs), builtins.issubclass
)
iter = functools.update_wrapper(lambda *args, **kwargs: builtins.iter(*args, **kwargs), builtins.iter)
iter._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.iter)(*args, **kwargs), builtins.iter)
len = functools.update_wrapper(lambda *args, **kwargs: builtins.len(*args, **kwargs), builtins.len)
len._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.len)(*args, **kwargs), builtins.len)
list = functools.update_wrapper(lambda *args, **kwargs: builtins.list(*args, **kwargs), builtins.list)
list._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.list)(*args, **kwargs), builtins.list)
locals = functools.update_wrapper(lambda *args, **kwargs: builtins.locals(*args, **kwargs), builtins.locals)
locals._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.locals)(*args, **kwargs), builtins.locals)
max = functools.update_wrapper(lambda *args, **kwargs: builtins.max(*args, **kwargs), builtins.max)
max._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.max)(*args, **kwargs), builtins.max)
memoryview = functools.update_wrapper(lambda *args, **kwargs: builtins.memoryview(*args, **kwargs), builtins.memoryview)
memoryview._ = functools.update_wrapper(
    lambda *args, **kwargs: wrap(builtins.memoryview)(*args, **kwargs), builtins.memoryview
)
min = functools.update_wrapper(lambda *args, **kwargs: builtins.min(*args, **kwargs), builtins.min)
min._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.min)(*args, **kwargs), builtins.min)
next = functools.update_wrapper(lambda *args, **kwargs: builtins.next(*args, **kwargs), builtins.next)
next._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.next)(*args, **kwargs), builtins.next)
oct = functools.update_wrapper(lambda *args, **kwargs: builtins.oct(*args, **kwargs), builtins.oct)
oct._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.oct)(*args, **kwargs), builtins.oct)
open = functools.update_wrapper(lambda *args, **kwargs: builtins.open(*args, **kwargs), builtins.open)
open._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.open)(*args, **kwargs), builtins.open)
ord = functools.update_wrapper(lambda *args, **kwargs: builtins.ord(*args, **kwargs), builtins.ord)
ord._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.ord)(*args, **kwargs), builtins.ord)
pow = functools.update_wrapper(lambda *args, **kwargs: builtins.pow(*args, **kwargs), builtins.pow)
pow._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.pow)(*args, **kwargs), builtins.pow)
print = functools.update_wrapper(lambda *args, **kwargs: builtins.print(*args, **kwargs), builtins.print)
print._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.print)(*args, **kwargs), builtins.print)
range = functools.update_wrapper(lambda *args, **kwargs: builtins.range(*args, **kwargs), builtins.range)
range._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.range)(*args, **kwargs), builtins.range)
repr = functools.update_wrapper(lambda *args, **kwargs: builtins.repr(*args, **kwargs), builtins.repr)
repr._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.repr)(*args, **kwargs), builtins.repr)
reversed = functools.update_wrapper(lambda *args, **kwargs: builtins.reversed(*args, **kwargs), builtins.reversed)
reversed._ = functools.update_wrapper(
    lambda *args, **kwargs: wrap(builtins.reversed)(*args, **kwargs), builtins.reversed
)
round = functools.update_wrapper(lambda *args, **kwargs: builtins.round(*args, **kwargs), builtins.round)
round._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.round)(*args, **kwargs), builtins.round)
set = functools.update_wrapper(lambda *args, **kwargs: builtins.set(*args, **kwargs), builtins.set)
set._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.set)(*args, **kwargs), builtins.set)
setattr = functools.update_wrapper(lambda *args, **kwargs: builtins.setattr(*args, **kwargs), builtins.setattr)
setattr._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.setattr)(*args, **kwargs), builtins.setattr)
slice = functools.update_wrapper(lambda *args, **kwargs: builtins.slice(*args, **kwargs), builtins.slice)
slice._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.slice)(*args, **kwargs), builtins.slice)
sorted = functools.update_wrapper(lambda *args, **kwargs: builtins.sorted(*args, **kwargs), builtins.sorted)
sorted._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.sorted)(*args, **kwargs), builtins.sorted)
str = functools.update_wrapper(lambda *args, **kwargs: builtins.str(*args, **kwargs), builtins.str)
str._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.str)(*args, **kwargs), builtins.str)
sum = functools.update_wrapper(lambda *args, **kwargs: builtins.sum(*args, **kwargs), builtins.sum)
sum._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.sum)(*args, **kwargs), builtins.sum)
tuple = functools.update_wrapper(lambda *args, **kwargs: builtins.tuple(*args, **kwargs), builtins.tuple)
tuple._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.tuple)(*args, **kwargs), builtins.tuple)
type = functools.update_wrapper(lambda *args, **kwargs: builtins.type(*args, **kwargs), builtins.type)
type._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.type)(*args, **kwargs), builtins.type)
vars = functools.update_wrapper(lambda *args, **kwargs: builtins.vars(*args, **kwargs), builtins.vars)
vars._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.vars)(*args, **kwargs), builtins.vars)
zip = functools.update_wrapper(lambda *args, **kwargs: builtins.zip(*args, **kwargs), builtins.zip)
zip._ = functools.update_wrapper(lambda *args, **kwargs: wrap(builtins.zip)(*args, **kwargs), builtins.zip)
callable = functools.update_wrapper(
    lambda arg0, *args, **kwargs: builtins.callable(arg0, *args, **kwargs), builtins.callable
)
callable._ = functools.update_wrapper(
    lambda arg0, *args, **kwargs: wrap(builtins.callable)(arg0, *args, **kwargs), builtins.callable
)

map = functools.update_wrapper(
    lambda arg0, *args, **kwargs: builtins.map(to_lambda(arg0), *args, **kwargs), builtins.map
)
map._ = functools.update_wrapper(
    lambda arg0, *args, **kwargs: wrap(builtins.map)(to_lambda(arg0), *args, **kwargs), builtins.map
)

filter = functools.update_wrapper(
    lambda arg0, *args, **kwargs: builtins.filter(
        to_lambda(arg0, required_args=1) if arg0 is not None else None, *args, **kwargs
    ),
    builtins.filter,
)
filter._ = functools.update_wrapper(
    lambda arg0, *args, **kwargs: wrap(builtins.filter)(
        to_lambda(arg0, required_args=1) if arg0 is not None else None, *args, **kwargs
    ),
    builtins.filter,
)
