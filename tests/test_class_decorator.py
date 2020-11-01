from unittest import TestCase

from runtime_typing import typed, RuntimeTypingError, RuntimeTypingWarning


@typed(mode="warn")
class WarningClass:
    def __init__(self, x: int):
        pass


class SomeSuperClass:
    def some_super_instance_method(self, x: int):
        pass


@typed
class SomeClass(SomeSuperClass):
    @classmethod
    def some_classmethod(cls, x: int):
        pass

    @staticmethod
    def some_staticmethod(x: int):
        pass

    def __init__(self, x: int):
        pass

    def some_instance_method(self, x: int):
        pass

    class SomeSubClass:
        def __init__(self, x: int):
            pass


class ClassMethodTestClass:
    @classmethod
    @typed
    def class_method(cls, x: int):
        pass


class TestClassDecorator(TestCase):
    def setUp(self):
        self.some_class_instance = SomeClass(1)

    def test_init(self):
        with self.assertRaises(RuntimeTypingError):
            SomeClass("not an int")

        with self.assertWarns(RuntimeTypingWarning):
            WarningClass("not an int")

    def test_instance_method(self):
        with self.assertRaises(RuntimeTypingError):
            self.some_class_instance.some_instance_method("not an int")

    def test_staticmethod(self):
        with self.assertRaises(RuntimeTypingError):
            self.some_class_instance.some_staticmethod("not an int")

    def test_inherited_method(self):
        with self.assertRaises(RuntimeTypingError):
            self.some_class_instance.some_super_instance_method("not an int")

    def test_class_method(self):
        SomeClass.some_classmethod("not an int")

    def test_subclass(self):
        self.some_class_instance.SomeSubClass("not an int")
        SomeClass.SomeSubClass("not an int")

    def test_typed_class_method(self):
        with self.assertRaises(RuntimeTypingError):
            ClassMethodTestClass.class_method("not an int")
