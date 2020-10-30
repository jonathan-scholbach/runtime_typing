from typing import Any, Callable
from unittest import TestCase

from src import typed, RuntimeTypingError


@typed
def expect_callable(func: Callable):
    pass


@typed
def expect_callable_expecting_string(func: Callable[[str], Any]):
    pass


def string_expecting(s: str) -> Any:
    return s


def int_expecting(i: int) -> Any:
    return i


@typed
def expect_callabale_expecting_and_returning_string(func: Callable[[str], str]):
    pass


def string_expecting_and_returning(s: str) -> str:
    return s


class TestCallable(TestCase):
    def test_expect_callable(self):
        with self.assertRaises(TypeError):
            expect_callable()

        with self.assertRaises(RuntimeTypingError):
            expect_callable(1)

        expect_callable(lambda x: x)
        expect_callable(str.upper)

    def test_string_expecting_callable(self):
        with self.assertRaises(TypeError):
            expect_callable_expecting_string()

        with self.assertRaises(RuntimeTypingError):
            expect_callable_expecting_string(1)

        with self.assertRaises(RuntimeTypingError):
            expect_callable_expecting_string(int_expecting)

        expect_callable_expecting_string(string_expecting)

    def test_expect_callable_expecting_and_returning_callable(self):
        with self.assertRaises(TypeError):
            expect_callabale_expecting_and_returning_string()

        with self.assertRaises(RuntimeTypingError):
            expect_callabale_expecting_and_returning_string(1)

        with self.assertRaises(RuntimeTypingError):
            expect_callabale_expecting_and_returning_string(int_expecting)

        with self.assertRaises(RuntimeTypingError):
            expect_callabale_expecting_and_returning_string(string_expecting)

        expect_callabale_expecting_and_returning_string(
            string_expecting_and_returning
        )
