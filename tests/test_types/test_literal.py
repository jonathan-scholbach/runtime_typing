from unittest import TestCase
from typing import Literal

from src import typed, RuntimeTypingError


@typed
def expect_character(a: Literal["a"]):
    pass


@typed
def expect_nested_literal(a: Literal[Literal["a"], "b", Literal["c"]]):
    pass


@typed
def expect_multiple_literals(char: Literal["a", "b"], binary: Literal[0, 1]):
    pass


@typed
def return_character(a) -> Literal["a", "b"]:
    return a


class TestLiteral(TestCase):
    def test_expect_character(self):
        with self.assertRaises(RuntimeTypingError):
            expect_character(1)

        expect_character("a")

    def test_expect_nested_literal(self):
        with self.assertRaises(RuntimeTypingError):
            expect_nested_literal("d")

        expect_nested_literal("a")
        expect_nested_literal("b")
        expect_nested_literal("c")

    def test_expect_multiple_literals(self):
        with self.assertRaises(RuntimeTypingError):
            expect_multiple_literals("a", 2)

        with self.assertRaises(RuntimeTypingError):
            expect_multiple_literals("c", 1)

        with self.assertRaises(RuntimeTypingError):
            expect_multiple_literals("c", 3)

        expect_multiple_literals("a", 0)
        expect_multiple_literals("a", 1)
        expect_multiple_literals("b", 0)
        expect_multiple_literals("b", 1)

    def test_return_character(self):
        with self.assertRaises(RuntimeTypingError):
            return_character(1)

        self.assertEqual(return_character("a"), "a")
        self.assertEqual(return_character("b"), "b")
