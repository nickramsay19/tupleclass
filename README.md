# TupleClass

A mutable, inheritable NamedTuple alternative. It exhibits the properties and behaviours of a tuple including tuple unpacking and iteration.

Existing solutions all have issues:
1. `NamedTuple` - Elements are immutable, since the data is stored in a tuple
2. `dataclass` - Inheritance doesn't work.

## Examples

```py
from tupleclass import TupleClass

class Data(TupleClass):
    x: int # no default
    y: str = 'default'

d = Data(5.0)

print(d.x) # Prints "5.0"
print(d.y) # Prints "default"
```

Tuple classes behave like tuples, despite being mutable.

```py
# Data is a subclass of tuple (not really, but python thinks so)
assert issubclass(Data, tuple)

# Data is a tuple
d = Data(10,'hi')
assert isinstance(d, tuple)

assert list(d) == [10, 'hi']
assert len(d) == 2
```

Tuple classes can also be inherited to form more tupleclasses. New annotations defined in subtypes get added in order.

```py
class A(TupleClass):
    a: str = 'a'

class B(A):
    b: str = 'b'

b = B()
assert b.a == 'a'
assert b.b == 'b'
```

