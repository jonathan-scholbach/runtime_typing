from typing import Any, TypedDict
from unittest import TestCase


from runtime_typing import typed, RuntimeTypingError


SomeTypedDict = TypedDict('SomeTypedDict', {'color': str})


class SomeNestedTypedDict(TypedDict):
    count: int
    child: SomeTypedDict


@typed
def expect_typed_dict(obj: TypedDict) -> None:
    pass


@typed
def expect_some_typed_dict(obj: SomeTypedDict) -> None:
    pass


@typed
def expect_some_nested_typed_dict(obj: SomeNestedTypedDict) -> None:
    pass


class TestTypedDict(TestCase):
    def test_expect_typed_dict(self):
        with self.assertRaises(TypeError):
            expect_typed_dict()

        with self.assertRaises(RuntimeTypingError):
            expect_typed_dict(1)

    def test_expect_typed_dict_with_required_keys(self):
        with self.assertRaises(TypeError):
            expect_some_typed_dict()

        with self.assertRaises(RuntimeTypingError):
            expect_some_typed_dict(1)

        with self.assertRaises(RuntimeTypingError):
            expect_some_typed_dict({'no-color': 'blue'})

        with self.assertRaises(RuntimeTypingError):
            expect_some_typed_dict({'color': 1})

        expect_some_typed_dict({'color': 'blue'})

    def test_expect_some_nested_type_dict(self):
        with self.assertRaises(TypeError):
            expect_some_nested_typed_dict()

        with self.assertRaises(RuntimeTypingError):
            expect_some_nested_typed_dict(1)

        with self.assertRaises(RuntimeTypingError):
            expect_some_nested_typed_dict({'count': 'not an int'})

        with self.assertRaises(RuntimeTypingError):
            expect_some_nested_typed_dict({'count': 1})

        with self.assertRaises(RuntimeTypingError):
            expect_some_nested_typed_dict({
                'count': 'not an int',
                'child': 1,
            })

        with self.assertRaises(RuntimeTypingError):
            expect_some_nested_typed_dict({
                'count': 1,
                'child': 'not some dict',
            })

        expect_some_nested_typed_dict({
             'count': 1,
             'child': {'color': "blue"},
        })
