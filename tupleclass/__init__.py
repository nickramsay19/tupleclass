"""TupleClass

A mutable, inheritable NamedTuple alternative. It exhibits the properties
and behaviours of a tuple including tuple unpacking and iteration.

Alternative names: FieldTuple, Field, Mutple
"""

from __future__ import annotations
from typing import Any
from collections.abc import Mapping
from dataclasses import dataclass, field, fields, MISSING, make_dataclass
import functools
import io

class _TupleClassMeta(type):
    """The metaclass of TupleClass (see below for TupleClass)"""
    def __new__(cls, name, bases, dct):
        annotations = dct.get('__annotations__', {})
        new_cls = make_dataclass(name, [(name, typ, field(default=MISSING)) for name, typ in annotations.items()], bases=bases) # pass tuple superclass in here in bases
        new_cls.__module__ = dct.get('__module__')
        for key, value in dct.items():
            if key != '__annotations__':
                setattr(new_cls, key, value)

        # don't actually use the tuple superclass's __new__
        # TODO if superclass is a subclass of TupleClass, then make smart 
        # constructor chain
        original_new = new_cls.__new__
        def __new__(cls, *args, **kwargs):
            instance = original_new(cls, tuple(args)) # convert args to tuple
            for name, value in zip([f.name for f in fields(cls)], args):
                setattr(instance, name, value)
            for name, value in kwargs.items():
                setattr(instance, name, value)
            return instance
        setattr(new_cls, '__new__', __new__)

        # add an __iter__ method to enable emulated tuple unpacking
        def __iter__(self):
            field_names = list(self.__annotations__.keys())
            for f in field_names:
                yield getattr(self, f)
        setattr(new_cls, '__iter__', __iter__)

        # pseudo-tuple index access
        def __getitem__(self, key: int) -> Any:
            return getattr(self, list(self.__annotations__.keys())[key])
        setattr(new_cls, '__getitem__', __getitem__)

        # pseudo-tuple index set
        def __setitem__(self, key: int, val: Any):
            setattr(self, list(self.__annotations__.keys())[key], val)
        setattr(new_cls, '__setitem__', __setitem__)

        # pretty tuple print
        def __str__(self):
            return self.__class__.__name__ + str(tuple(self))
        setattr(new_cls, '__str__', __str__)        

        # TODO: __repr__ that prints also the field names

        return new_cls

@functools.total_ordering
class TupleClass(tuple, metaclass=_TupleClassMeta):
    """Mutable Named pseudo-Tuple.

    Acts just like a regular NamedTuple and thus a normal tuple, but, is really a subclass of a dataclass instance. 

    Requires each specified field to be typed, since in Python, we can only determine dynamic fields via typed __annotations__.
    """

    def __init__(self, *args, **kwargs):
        # store all annotation names in their defined order
        field_names = []

        # check for inherited annotations
        for base in self.__class__.__mro__[1:-3]:
            field_names.extend(list(base.__annotations__.keys()))

        # add all annotations defined in this class only
        field_names.extend(list(self.__annotations__.keys()))
        if len(args) > len(field_names):
            raise TypeError(f"Expected at most {len(field_names)} arguments, got {len(args)}")

        # set all default
        for name in field_names:
            if not hasattr(self, name): # perhaps a default was already provided
                setattr(self, name, None)

        for name, value in zip(field_names, args):
            setattr(self, name, value)
        for name, value in kwargs.items():
            setattr(self, name, value)

        setattr(self, '__TupleClass_field_names', field_names)

    # allow tuple equivalence w/ total_ordering
    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __lt__(self, other):
        return tuple(self) < tuple(other)