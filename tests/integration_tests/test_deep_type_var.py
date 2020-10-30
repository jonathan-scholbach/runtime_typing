from unittest import TestCase
from typing import Union, TypeVar

from src import typed
from src.violations import RuntimeTypingError


T = TypeVar("T")


@typed
def expect_union_with_deep_type_var_as_second_option(x: Union[str, T], y: T):
    pass


@typed
def expect_union_with_deep_type_var_as_first_option(x: Union[T, str], y: T):
    pass


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
