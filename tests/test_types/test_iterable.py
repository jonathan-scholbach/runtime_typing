from typing import Iterable
from unittest import TestCase

from src import typed, RuntimeTypingError


@typed
def expect_iterable(a: Iterable):
    pass


@typed
def expect_iterable_of_ints(a: Iterable[int]):
    pass


class TestIterable(TestCase):
    def test_expect_iterable(self):
        with self.assertRaises(TypeError):
            expect_iterable()

        with self.assertRaises(RuntimeTypingError):
            expect_iterable(1)

        expect_iterable([1, 2, 3])
        expect_iterable((1, 2, 3))
        expect_iterable({1, 2, 3})
        expect_iterable("123")

    def test_expect_iterable_of_ints(self):
        with self.assertRaises(TypeError):
            expect_iterable_of_ints()

        with self.assertRaises(RuntimeTypingError):
            expect_iterable_of_ints(1)
        with self.assertRaises(RuntimeTypingError):
            expect_iterable_of_ints("123")

        expect_iterable_of_ints([1, 2, 3])
        expect_iterable_of_ints((1, 2, 3))
        expect_iterable_of_ints({1, 2, 3})
