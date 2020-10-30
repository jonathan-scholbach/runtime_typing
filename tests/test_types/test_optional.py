from typing import Optional
from unittest import TestCase

from src import typed


@typed
def expect_optional_string(a: Optional[str]):
    pass


@typed
def expect_optional_string_default_none(a: Optional[str] = None):
    pass


class TestOptional(TestCase):
    def test_expect_optional(self):
        with self.assertRaises(TypeError):
            expect_optional_string()

        expect_optional_string(None)
        expect_optional_string("s")

    def test_optional_string_default(self):
        expect_optional_string_default_none()
        expect_optional_string_default_none(None)
        expect_optional_string_default_none("sdlfknsfl")
