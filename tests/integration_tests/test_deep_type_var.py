from unittest import TestCase
from typing import Union, Tuple, TypeVar

from src import typed
from src.violations import RuntimeTypingError


T = TypeVar("T")
S = TypeVar("")

@typed
def expect_union_with_deep_type_var_as_second_option(x: Union[str, T], y: T):
    pass


@typed
def expect_union_with_deep_type_var_as_first_option(x: Union[T, str], y: T):
    pass


@typed
def expect_tuple_of_type_var(x: Tuple[T, T]):
    pass


@typed
def expect_tuple_and_union_of_type_var(x: Tuple[T, T], y: Union[S, T]):
    pass


@typed
def expect_and_return_type_var(x: T, fail: bool = False) -> T:
    if fail:
        if type(x) is str:
            return 1
        else:
            return str(x)

    return x*5


class TestDeepTypeVar(TestCase):
    def test_expect_union_with_deep_type_var(self):
        with self.assertRaises(RuntimeTypingError):
            expect_union_with_deep_type_var_as_first_option(1, 1.0)

        with self.assertRaises(RuntimeTypingError):
            # `T` should be confined to str by the assignment of `T` at x
            expect_union_with_deep_type_var_as_first_option("s", 1.0)

        # `T` should not be confined on y argument, because x should match on
        #  str, not on T.
        expect_union_with_deep_type_var_as_second_option("s", 1.0)

    def test_tuple_of_type_var(self):
        with self.assertRaises(RuntimeTypingError):
            expect_tuple_of_type_var((1, "s"))

        with self.assertRaises(RuntimeTypingError):
            expect_tuple_of_type_var(("s", 1))

        with self.assertRaises(RuntimeTypingError):
            expect_tuple_of_type_var((False, 1))

        with self.assertRaises(RuntimeTypingError):
            expect_tuple_of_type_var((1.0, 1))

        with self.assertRaises(RuntimeTypingError):
            expect_tuple_of_type_var(([1], 1))

        with self.assertRaises(RuntimeTypingError):
            expect_tuple_of_type_var(({1}, 1))

        expect_tuple_of_type_var((1, False))

    def test_expect_tuple_and_union_of_type_var(self):
        with self.assertRaises(RuntimeTypingError):
            expect_tuple_and_union_of_type_var((1, "1"), "1")

    def test_expect_and_return_type_var(self):
        with self.assertRaises(RuntimeTypingError):
            expect_and_return_type_var(1, fail=True)

        with self.assertRaises(RuntimeTypingError):
            expect_and_return_type_var(1.0, fail=True)

        with self.assertRaises(RuntimeTypingError):
            expect_and_return_type_var([1, 2, 3], fail=True)

        expect_and_return_type_var(1)
