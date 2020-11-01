from typing import AnyStr
from unittest import TestCase

from runtime_typing import typed, RuntimeTypingError


@typed
def expect_any_str(a: AnyStr):
    pass


@typed
def expect_and_return_any_str(a: AnyStr) -> AnyStr:
    return a.upper()


class TestAnyStr(TestCase):
    def test_expect_any_str(self):
        with self.assertRaises(RuntimeTypingError):
            expect_any_str(1)

        expect_any_str("s")

    def test_and_return_any_str(self):
        expect_and_return_any_str("s")
