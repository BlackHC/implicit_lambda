import functools
import itertools
import operator
from blackhc.implicit_lambda import wrap, to_lambda


chain = functools.update_wrapper(lambda *args, **kwargs: itertools.chain(*args, **kwargs), itertools.chain)
chain._ = functools.update_wrapper(lambda *args, **kwargs: wrap(itertools.chain)(*args, **kwargs), itertools.chain)
combinations = functools.update_wrapper(lambda *args, **kwargs: itertools.combinations(*args, **kwargs), itertools.combinations)
combinations._ = functools.update_wrapper(lambda *args, **kwargs: wrap(itertools.combinations)(*args, **kwargs), itertools.combinations)
combinations_with_replacement = functools.update_wrapper(lambda *args, **kwargs: itertools.combinations_with_replacement(*args, **kwargs), itertools.combinations_with_replacement)
combinations_with_replacement._ = functools.update_wrapper(lambda *args, **kwargs: wrap(itertools.combinations_with_replacement)(*args, **kwargs), itertools.combinations_with_replacement)
compress = functools.update_wrapper(lambda *args, **kwargs: itertools.compress(*args, **kwargs), itertools.compress)
compress._ = functools.update_wrapper(lambda *args, **kwargs: wrap(itertools.compress)(*args, **kwargs), itertools.compress)
count = functools.update_wrapper(lambda *args, **kwargs: itertools.count(*args, **kwargs), itertools.count)
count._ = functools.update_wrapper(lambda *args, **kwargs: wrap(itertools.count)(*args, **kwargs), itertools.count)
cycle = functools.update_wrapper(lambda *args, **kwargs: itertools.cycle(*args, **kwargs), itertools.cycle)
cycle._ = functools.update_wrapper(lambda *args, **kwargs: wrap(itertools.cycle)(*args, **kwargs), itertools.cycle)
islice = functools.update_wrapper(lambda *args, **kwargs: itertools.islice(*args, **kwargs), itertools.islice)
islice._ = functools.update_wrapper(lambda *args, **kwargs: wrap(itertools.islice)(*args, **kwargs), itertools.islice)
permutations = functools.update_wrapper(lambda *args, **kwargs: itertools.permutations(*args, **kwargs), itertools.permutations)
permutations._ = functools.update_wrapper(lambda *args, **kwargs: wrap(itertools.permutations)(*args, **kwargs), itertools.permutations)
product = functools.update_wrapper(lambda *args, **kwargs: itertools.product(*args, **kwargs), itertools.product)
product._ = functools.update_wrapper(lambda *args, **kwargs: wrap(itertools.product)(*args, **kwargs), itertools.product)
repeat = functools.update_wrapper(lambda *args, **kwargs: itertools.repeat(*args, **kwargs), itertools.repeat)
repeat._ = functools.update_wrapper(lambda *args, **kwargs: wrap(itertools.repeat)(*args, **kwargs), itertools.repeat)
tee = functools.update_wrapper(lambda *args, **kwargs: itertools.tee(*args, **kwargs), itertools.tee)
tee._ = functools.update_wrapper(lambda *args, **kwargs: wrap(itertools.tee)(*args, **kwargs), itertools.tee)
zip_longest = functools.update_wrapper(lambda *args, **kwargs: itertools.zip_longest(*args, **kwargs), itertools.zip_longest)
zip_longest._ = functools.update_wrapper(lambda *args, **kwargs: wrap(itertools.zip_longest)(*args, **kwargs), itertools.zip_longest)

dropwhile = functools.update_wrapper(lambda arg0, *args, **kwargs: itertools.dropwhile(to_lambda(arg0), *args, **kwargs),itertools.dropwhile)
dropwhile._ = functools.update_wrapper(lambda arg0, *args, **kwargs: wrap(itertools.dropwhile)(to_lambda(arg0), *args, **kwargs), itertools.dropwhile)
filterfalse = functools.update_wrapper(lambda arg0, *args, **kwargs: itertools.filterfalse(to_lambda(arg0), *args, **kwargs), itertools.filterfalse)
filterfalse._ = functools.update_wrapper(lambda arg0, *args, **kwargs: wrap(itertools.filterfalse)(to_lambda(arg0), *args, **kwargs), itertools.filterfalse)
starmap = functools.update_wrapper(lambda arg0, *args, **kwargs: itertools.starmap(to_lambda(arg0), *args, **kwargs), itertools.starmap)
starmap._ = functools.update_wrapper(lambda arg0, *args, **kwargs: wrap(itertools.starmap)(to_lambda(arg0), *args, **kwargs), itertools.starmap)
takewhile = functools.update_wrapper(lambda arg0, *args, **kwargs: itertools.takewhile(to_lambda(arg0), *args, **kwargs), itertools.takewhile)
takewhile._ = functools.update_wrapper(lambda arg0, *args, **kwargs: wrap(itertools.takewhile)(to_lambda(arg0), *args, **kwargs), itertools.takewhile)

accumulate = functools.update_wrapper(lambda arg0, arg1=operator.add, *args, **kwargs: itertools.accumulate(arg0, to_lambda(arg1), *args, **kwargs), itertools.accumulate)
accumulate._ = functools.update_wrapper(lambda arg0, arg1=operator.add, *args, **kwargs: wrap(itertools.accumulate)(arg0, to_lambda(arg1), *args, **kwargs), itertools.accumulate)
groupby = functools.update_wrapper(lambda arg0, arg1=None, *args, **kwargs: itertools.groupby(arg0, to_lambda(arg1) if arg1 else None, *args, **kwargs), itertools.groupby)
groupby._ = functools.update_wrapper(lambda arg0, arg1=None, *args, **kwargs: wrap(itertools.groupby)(arg0, to_lambda(arg1) if arg1 else None, *args, **kwargs), itertools.groupby)
