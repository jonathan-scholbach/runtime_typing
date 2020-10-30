from unittest import TestCase

from src import typed, RuntimeTypingError


@typed
def expect_positional_argument(a):
    pass


@typed
def default_positional_argument(a: str = ""):
    pass


@typed
def positional_and_default_argument(a, s: str = ""):
    pass


class TestPositionalArgument(TestCase):
    def test_missing_argument(self):
        with self.assertRaises(TypeError):
            expect_positional_argument()

    def test_default_argument(self):
        default_positional_argument()

    def test_positional_and_default_argument(self):
        with self.assertRaises(TypeError):
            positional_and_default_argument()

        positional_and_default_argument("s")

    def test_positional_and_keyword_argument(self):
        with self.assertRaises(TypeError):
            positional_and_default_argument(s="s")

        positional_and_default_argument(a="a", s="s")
        positional_and_default_argument(a="a")
