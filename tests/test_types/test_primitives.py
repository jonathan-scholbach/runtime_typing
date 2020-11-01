from unittest import TestCase

from runtime_typing import typed, RuntimeTypingError


@typed
def expect_string(a: str):
    pass


@typed
def expect_float(a: float):
    pass


@typed
def expect_int(a: int):
    pass


@typed
def expect_list(a: list):
    pass


@typed
def expect_tuple(a: tuple):
    pass


@typed
def expect_dict(a: dict):
    pass


@typed
def expect_set(a: set):
    pass


@typed
def expect_none(n: None):
    pass


class CustomClass:
    pass


@typed
def expect_custom_class(a: CustomClass):
    pass


class TestPrimitives(TestCase):
    def test_string(self):
        with self.assertRaises(RuntimeTypingError):
            expect_string(1)

        with self.assertRaises(RuntimeTypingError):
            expect_string(1.0)

        with self.assertRaises(RuntimeTypingError):
            expect_string([1])

        with self.assertRaises(RuntimeTypingError):
            expect_string((1,))

        with self.assertRaises(RuntimeTypingError):
            expect_string({1})

        with self.assertRaises(RuntimeTypingError):
            expect_string({"1": 1})

        expect_string("1")

    def test_float(self):
        with self.assertRaises(RuntimeTypingError):
            expect_float(1)

        with self.assertRaises(RuntimeTypingError):
            expect_float("1.0")

        with self.assertRaises(RuntimeTypingError):
            expect_float([1])

        with self.assertRaises(RuntimeTypingError):
            expect_float((1,))

        with self.assertRaises(RuntimeTypingError):
            expect_float({1})

        with self.assertRaises(RuntimeTypingError):
            expect_float({"1": 1})

        expect_float(1.0)

    def test_int(self):
        with self.assertRaises(RuntimeTypingError):
            expect_int("1")

        with self.assertRaises(RuntimeTypingError):
            expect_int(1.0)

        with self.assertRaises(RuntimeTypingError):
            expect_int([1])

        with self.assertRaises(RuntimeTypingError):
            expect_int((1,))

        with self.assertRaises(RuntimeTypingError):
            expect_int({1})

        with self.assertRaises(RuntimeTypingError):
            expect_int({"1": 1})

        expect_int(1)

    def test_tuple(self):
        with self.assertRaises(RuntimeTypingError):
            expect_tuple("1")

        with self.assertRaises(RuntimeTypingError):
            expect_tuple(1.0)

        with self.assertRaises(RuntimeTypingError):
            expect_tuple([1])

        with self.assertRaises(RuntimeTypingError):
            expect_tuple("1")

        with self.assertRaises(RuntimeTypingError):
            expect_tuple({1})

        with self.assertRaises(RuntimeTypingError):
            expect_tuple({"1": 1})

        expect_tuple((1,))

    def test_dict(self):
        with self.assertRaises(RuntimeTypingError):
            expect_dict("1")

        with self.assertRaises(RuntimeTypingError):
            expect_dict(1.0)

        with self.assertRaises(RuntimeTypingError):
            expect_dict([1])

        with self.assertRaises(RuntimeTypingError):
            expect_dict("1")

        with self.assertRaises(RuntimeTypingError):
            expect_dict({1})

        with self.assertRaises(RuntimeTypingError):
            expect_dict((1,))

        expect_dict({"1": 1})

    def test_set(self):
        with self.assertRaises(RuntimeTypingError):
            expect_set("1")

        with self.assertRaises(RuntimeTypingError):
            expect_set(1.0)

        with self.assertRaises(RuntimeTypingError):
            expect_set([1])

        with self.assertRaises(RuntimeTypingError):
            expect_set("1")

        with self.assertRaises(RuntimeTypingError):
            expect_set({"1": 1})

        with self.assertRaises(RuntimeTypingError):
            expect_set((1,))

        expect_set({1})

    def test_list(self):
        with self.assertRaises(RuntimeTypingError):
            expect_list("1")

        with self.assertRaises(RuntimeTypingError):
            expect_list(1.0)

        with self.assertRaises(RuntimeTypingError):
            expect_list({1})

        with self.assertRaises(RuntimeTypingError):
            expect_list("1")

        with self.assertRaises(RuntimeTypingError):
            expect_list({"1": 1})

        with self.assertRaises(RuntimeTypingError):
            expect_list((1,))

        expect_list([1])

    def test_none(self):
        with self.assertRaises(RuntimeTypingError):
            expect_none("1")

        with self.assertRaises(RuntimeTypingError):
            expect_none(1.0)

        with self.assertRaises(RuntimeTypingError):
            expect_none({1})

        with self.assertRaises(RuntimeTypingError):
            expect_none("1")

        with self.assertRaises(RuntimeTypingError):
            expect_none({"1": 1})

        with self.assertRaises(RuntimeTypingError):
            expect_none((1,))

        expect_none(None)

    def test_expect_custom_class(self):
        with self.assertRaises(RuntimeTypingError):
            expect_custom_class("1")

        with self.assertRaises(RuntimeTypingError):
            expect_custom_class(1.0)

        with self.assertRaises(RuntimeTypingError):
            expect_custom_class([1])

        with self.assertRaises(RuntimeTypingError):
            expect_custom_class("1")

        with self.assertRaises(RuntimeTypingError):
            expect_custom_class({"1": 1})

        with self.assertRaises(RuntimeTypingError):
            expect_custom_class((1,))

        with self.assertRaises(RuntimeTypingError):
            expect_custom_class({1})

        expect_custom_class(CustomClass())
