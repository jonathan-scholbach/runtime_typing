from unittest import TestCase

from runtime_typing import typed, RuntimeTypingError


@typed(include=("return",))
def check_return_only(x: int) -> str:
    return str(x)


@typed(include=("return",))
def fail_to_check_return_only(x: int) -> str:
    return x


@typed(exclude=("x",))
def do_not_check_x(x: int) -> str:
    return str(x)


@typed(exclude=("x",))
def fail_do_not_check_x(x: int) -> str:
    return x


@typed(exclude=("x", "y"), include=("x",))
def check_nothing(x: int, y: float) -> str:
    return (x, y)


class TestIncludeExclude(TestCase):
    def test_check_return_only(self):
        with self.assertRaises(RuntimeTypingError):
            fail_to_check_return_only(3)

        check_return_only("2")

    def test_do_not_check_x(self):
        with self.assertRaises(RuntimeTypingError):
            fail_do_not_check_x(3)

        do_not_check_x("2")

    def test_check_noting(self):
        check_nothing("1", "1")
