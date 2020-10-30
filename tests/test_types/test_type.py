from unittest import TestCase
from typing import Type, TypeVar, Union

from src import typed
from src.violations import RuntimeTypingError


class CustomClass:
    pass


class SubClass(CustomClass):
    pass


class AnotherClass:
    pass


class CustomIntSubclass(int):
    pass


T = TypeVar("T")


@typed
def expect_type(a: type):
    pass


@typed
def expect_type_int(a: Type[int]):
    pass


@typed
def expect_type_custom_class(a: Type["CustomClass"]):
    pass


@typed
def expect_type_from_typevar(a: Type[T], b: Type[T]):
    pass


@typed
def expect_type_of_union_str_int(a: Type[Union[str, int]]):
    pass


class TestType(TestCase):
    def test_expect_type(self):
        with self.assertRaises(RuntimeTypingError):
            expect_type(1)

        with self.assertRaises(RuntimeTypingError):
            expect_type("")

        with self.assertRaises(RuntimeTypingError):
            expect_type(1.0)

        expect_type(str)
        expect_type(dict)
        expect_type(int)
        expect_type(float)
        expect_type(bool)
        expect_type(type)
        expect_type(CustomClass)

    def test_expect_type_int(self):
        with self.assertRaises(RuntimeTypingError):
            expect_type_int(1)

        expect_type_int(int)
        expect_type_int(bool)
        expect_type_int(CustomIntSubclass)

    def test_expect_type_custom_class(self):
        with self.assertRaises(RuntimeTypingError):
            expect_type_custom_class(AnotherClass)

        expect_type_custom_class(SubClass)

    def test_expect_type_from_typevar(self):
        with self.assertRaises(RuntimeTypingError):
            expect_type_from_typevar(str, int)

        with self.assertRaises(RuntimeTypingError):
            expect_type_from_typevar(AnotherClass, CustomClass)

        with self.assertRaises(RuntimeTypingError):
            expect_type_from_typevar(SubClass, CustomClass)

        expect_type_from_typevar(str, str)
        expect_type_from_typevar(CustomClass, CustomClass)
        expect_type_from_typevar(CustomClass, SubClass)

    def test_expect_type_of_union(self):
        with self.assertRaises(RuntimeTypingError):
            expect_type_of_union_str_int(1.0)

        with self.assertRaises(RuntimeTypingError):
            expect_type_of_union_str_int(float)

        with self.assertRaises(RuntimeTypingError):
            expect_type_of_union_str_int(type)

        expect_type_of_union_str_int(bool)
        expect_type_of_union_str_int(int)
        expect_type_of_union_str_int(CustomIntSubclass)
        expect_type_of_union_str_int(str)
