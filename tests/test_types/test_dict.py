from unittest import TestCase
from typing import Dict

from runtime_typing import typed
from runtime_typing.violations import RuntimeTypingError


@typed
def expect_dict(d: dict):
    pass


@typed
def expect_dict_of_str_int(d: Dict[str, int]):
    pass


@typed
def expect_complex_dict(d: Dict[str, Dict[str, int]]):
    pass


class TestDict(TestCase):
    def test_expect_dict(self):
        with self.assertRaises(RuntimeTypingError):
            expect_dict(1)
        with self.assertRaises(RuntimeTypingError):
            expect_dict("s")
        with self.assertRaises(RuntimeTypingError):
            expect_dict(1.0)
        with self.assertRaises(RuntimeTypingError):
            expect_dict([1, 2])
        with self.assertRaises(RuntimeTypingError):
            expect_dict((1,))
        with self.assertRaises(RuntimeTypingError):
            expect_dict({1})

        expect_dict({"a": 1})

    def test_expect_dict_of_str_int(self):
        with self.assertRaises(RuntimeTypingError):
            expect_dict_of_str_int({"a": "a"})

        with self.assertRaises(RuntimeTypingError):
            expect_dict_of_str_int({"a": 1.0})

        with self.assertRaises(RuntimeTypingError):
            expect_dict_of_str_int({1: "a"})

        expect_dict_of_str_int({"a": 1})
