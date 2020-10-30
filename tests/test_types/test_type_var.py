from typing import Tuple, TypeVar
from unittest import TestCase

from src import typed, RuntimeTypingError


T = TypeVar("T")
S = TypeVar("S")
AmbiguouslyNamedType = TypeVar("T")


@typed
def return_type_var(a: T) -> T:
    return a


@typed
def fail_to_return_type_var(a: T) -> T:
    if type(a) is str:
        return 1
    else:
        return "1"


@typed
def return_type_vars(a: T, b: S) -> Tuple[S, T]:
    return b, a


@typed
def fail_to_return_type_vars(a: T, b: S) -> Tuple[S, T]:
    return a, b


@typed
def ambiguous_type_vars(a: T, b: AmbiguouslyNamedType):
    pass


@typed
def fail_to_return_ambiguous_type_vars(
    a: T, b: AmbiguouslyNamedType
) -> Tuple[T, AmbiguouslyNamedType]:
    return b, a


class TestTypeVar(TestCase):
    def test_return_type_var(self):
        with self.assertRaises(RuntimeTypingError):
            fail_to_return_type_var(1)

        with self.assertRaises(RuntimeTypingError):
            fail_to_return_type_var("1")

        return_type_var(1)
        return_type_var("a")

    def test_return_type_vars(self):
        with self.assertRaises(RuntimeTypingError):
            fail_to_return_type_vars(1, "a")

        return_type_vars(1, "a")

    def test_amibiguous_type_var(self):
        with self.assertRaises(RuntimeTypingError):
            fail_to_return_ambiguous_type_vars("s", 1)

        ambiguous_type_vars("s", 1)
