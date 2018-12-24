from blackhc.implicit_lambda import _, to_lambda, interpreted_lambda, index
from dataclasses import dataclass
import timeit

my_dict = dict(hello="world")

l = to_lambda(_ + _)
a = to_lambda(_["hello"])
b = to_lambda(_.the_field)
c = to_lambda(_.echo("hello world"))

print(to_lambda(index(my_dict, _))("hello"))

expr = 2 * _ * 3 * _ * 5
expr_eval_lambda = to_lambda(expr)
print(expr_eval_lambda.sourcecode)
expr_compile_lambda = interpreted_lambda(expr)
print(interpreted_lambda(2 * _ * 3 * _ * 5)(10))

direct_lambda = lambda *args, **kwargs: ((((2) * (args[0])) * (3)) * (args[0])) * (5)


@dataclass
class T:
    the_field: str

    def echo(self, text):
        print(text)


print(l(2))
print(b(T("hello world")))
c(T("a"))

# print(a(dict(hello='world')))
# print(to_lambda(_ - 5)(4))


print(timeit.timeit(lambda: direct_lambda(10)))
print(timeit.timeit(lambda: expr_eval_lambda(10)))
print(timeit.timeit(lambda: expr_compile_lambda(10)))
