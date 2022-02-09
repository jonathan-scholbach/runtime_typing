import sys

from unittest import TestCase
from typing import Literal, Union, TypeVar

from runtime_typing import typed, RuntimeTypingError


T = TypeVar("T")


@typed
def primitive_union(a: Union[str, int]):
    pass


@typed
def union_with_type_var(a: Union[T, str]) -> Union[T, str]:
    return a


@typed
def complex_union(a: Union[Union[str, int], Literal[1.0]]):
    pass


class TestUnion(TestCase):
    def test_primitive_union(self):
        with self.assertRaises(TypeError):
            primitive_union()

        with self.assertRaises(RuntimeTypingError):
            primitive_union(1.0)

        primitive_union("")
        primitive_union(1)

    def test_primitive_union_with_pipe_operator(self):
        with self.assertRaises(TypeError):
            primitive_union()

        with self.assertRaises(RuntimeTypingError):
            primitive_union(1.0)

        primitive_union("")
        primitive_union(1)

    def test_typed_union(self):
        union_with_type_var(1)
        union_with_type_var([1])

    def test_complex_union(self):
        complex_union(1.0)
        complex_union(1)
        complex_union(1.0)

        with self.assertRaises(RuntimeTypingError):
            complex_union([1, 2])

        with self.assertRaises(RuntimeTypingError):
            complex_union(2.0)


if sys.version_info >= (3, 10):

    @typed
    def primitive_union_with_pipe_operator(a: str | int):
        pass

    @typed
    def union_with_type_var(a: T | str) -> T | str:
        return a

    @typed
    def complex_union_with_pipe_operator(a: str | int | Literal[1.0]):
        pass

    class TestUnionWithPipeOperator(TestCase):
        def test_primitive_union_with_pipe_operator(self):
            with self.assertRaises(TypeError):
                primitive_union_with_pipe_operator()

            with self.assertRaises(RuntimeTypingError):
                primitive_union_with_pipe_operator(1.0)

            primitive_union_with_pipe_operator("")
            primitive_union_with_pipe_operator(1)

        def test_primitive_union_with_pipe_operator_with_pipe_operator(self):
            with self.assertRaises(TypeError):
                primitive_union_with_pipe_operator()

            with self.assertRaises(RuntimeTypingError):
                primitive_union_with_pipe_operator(1.0)

            primitive_union_with_pipe_operator("")
            primitive_union_with_pipe_operator(1)

        def test_typed_union_with_pipe_operator(self):
            union_with_type_var(1)
            union_with_type_var([1])

        def test_complex_union_with_pipe_operator(self):
            complex_union_with_pipe_operator(1.0)
            complex_union_with_pipe_operator(1)
            complex_union_with_pipe_operator(1.0)

            with self.assertRaises(RuntimeTypingError):
                complex_union_with_pipe_operator([1, 2])

            with self.assertRaises(RuntimeTypingError):
                complex_union_with_pipe_operator(2.0)
