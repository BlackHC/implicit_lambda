import builtins
import functools
from blackhc.implicit_lambda import wrap, to_lambda

partial = functools.update_wrapper(
    lambda arg0, *args, **kwargs: functools.partial(to_lambda(arg0), *args, **kwargs), functools.partial
)
partial._ = functools.update_wrapper(
    lambda arg0, *args, **kwargs: wrap(functools.partial)(to_lambda(arg0), *args, **kwargs), functools.partial
)
partialmethod = functools.update_wrapper(
    lambda arg0, *args, **kwargs: functools.partialmethod(to_lambda(arg0), *args, **kwargs), functools.partialmethod
)
partialmethod._ = functools.update_wrapper(
    lambda arg0, *args, **kwargs: wrap(functools.partialmethod)(to_lambda(arg0), *args, **kwargs),
    functools.partialmethod,
)
update_wrapper = functools.update_wrapper(
    lambda arg0, *args, **kwargs: functools.update_wrapper(to_lambda(arg0), *args, **kwargs), functools.update_wrapper
)
update_wrapper._ = functools.update_wrapper(
    lambda arg0, *args, **kwargs: wrap(functools.update_wrapper)(to_lambda(arg0), *args, **kwargs),
    functools.update_wrapper,
)
wraps = functools.update_wrapper(
    lambda arg0, *args, **kwargs: functools.wraps(to_lambda(arg0), *args, **kwargs), functools.wraps
)
wraps._ = functools.update_wrapper(
    lambda arg0, *args, **kwargs: wrap(functools.wraps)(to_lambda(arg0), *args, **kwargs), functools.wraps
)

reduce = functools.update_wrapper(
    lambda arg0, *args, **kwargs: functools.reduce(to_lambda(arg0, required_args=2), *args, **kwargs), functools.reduce
)
reduce._ = functools.update_wrapper(
    lambda arg0, *args, **kwargs: wrap(functools.reduce)(to_lambda(arg0, required_args=2), *args, **kwargs),
    functools.reduce,
)
