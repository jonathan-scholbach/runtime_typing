from unittest import TestCase
from typing import Any

from runtime_typing import typed
from runtime_typing.violations import RuntimeTypingError


@typed
def expect_any(a: Any):
    pass


@typed
def return_any(a: Any) -> Any:
    return a


class TestAny(TestCase):
    def test_expect_any(self):
        expect_any(1)
        expect_any("1")
        expect_any(1.0)
        expect_any([1])
        expect_any({1})
        expect_any((1,))
        expect_any({"1": 1})

    def test_return_any(self):
        return_any(1)
        return_any("1")
        return_any(1.0)
        return_any([1])
        return_any({1})
        return_any((1,))
        return_any({"1": 1})
