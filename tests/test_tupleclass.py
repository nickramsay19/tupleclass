from __future__ import annotations
import unittest

class TestTupleClass(unittest.TestCase):
    def _make_dummy_TupleClass(self) -> type:
        class Dummy(TupleClass):
            x: int # no default
            y: str = 'default'
        
        return Dummy

    def test_tuple_behavior(self):
        Dummy = self._make_dummy_TupleClass()
            
        # a Dummy is a subclass of tuple (not really, but python thinks so)
        assert issubclass(Dummy, tuple)
        
        # a Dummy is a tuple
        d = Dummy(10,'hi')
        assert isinstance(d, tuple)
        assert isinstance(d, Dummy)
        assert d[0] == 10
        assert d[1] == 'hi'
        assert d == (10, 'hi')
        assert list(d) == [10, 'hi']
        assert len(d) == 2

    def test_named_tuple_behavior(self):
        Dummy = self._make_dummy_TupleClass() 

        # a Dummy is a NamedTuple
        d = Dummy(10,'hi')
        assert d.x == 10
        assert d.y == 'hi'

        # a Dummy supports defaults
        assert Dummy(10).y == 'default'

        # correct constructor calling
        assert Dummy(x=10,y='hi') == (10, 'hi')
        assert Dummy(x=10) == (10, 'default')
        assert Dummy(10,y='hi') == (10, 'hi')

    def test_mutability(self):
        d = self._make_dummy_TupleClass()(10,'hi')

        d.x = 11
        assert d.x == 11

    def test_inheritance(self):
        class A(TupleClass):
            a: str = 'a'

        class B(A):
            b: str = 'b'

        b = B()
        assert b.a == 'a'
        assert b.b == 'b'

    def test_inheritance_no_defaults_a(self):
        class A(TupleClass):
            a: str

        class B(A):
            b: str = 'b'

        b = B('a')
        assert b.a == 'a'
        assert b.b == 'b'

    def test_inheritance_no_defaults_b(self):
        class A(TupleClass):
            a: str = 'a'

        class B(A):
            b: str

        b = B('b')
        assert b.a == 'b'
        assert b.b == None

    def test_inheritance_no_defaults_ab(self):
        class A(TupleClass):
            a: str

        class B(A):
            b: str

        b = B('a', 'b')
        assert b.a == 'a'
        assert b.b == 'b'