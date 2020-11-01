from typing import List, Tuple, Union
from unittest import TestCase

from runtime_typing import typed, RuntimeTypingError


@typed
def expect_list_of_int(a: List[int]):
    pass


@typed
def expect_arbitrary_length_tuple_of_int(a: Tuple[int, ...]):
    pass


@typed
def expect_mixed_tuple(a: Tuple[int, str, float, int]):
    pass


@typed
def expect_mixed_tuple_with_union(a: Tuple[Union[int, float], str]):
    pass


class TestSequence(TestCase):
    def test_expect_list_of_int(self):
        with self.assertRaises(RuntimeTypingError):
            expect_list_of_int([1, 2, "s"])

        with self.assertRaises(RuntimeTypingError):
            expect_list_of_int(["s"])

        expect_list_of_int([1, 2, 3])
