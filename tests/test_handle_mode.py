from unittest import TestCase

from src import typed, RuntimeTypingError, RuntimeTypingWarning


@typed("return")
def expect_str_return_mode(a: str):
    return a


@typed("warn")
def expect_str_warn_mode(a: str):
    return a


@typed("raise")
def expect_str_raise_mode(a: str):
    return a


class TestMode(TestCase):
    def test_expect_str_return_mode(self):
        res, errors = expect_str_return_mode(1)
        self.assertEqual(res, 1)

        self.assertEqual(len(errors), 1)
        self.assertEqual(
            errors[0].message,
            "TypingViolation in function `expect_str_return_mode`: Expected "
            "type of argument `a` to be `<class 'str'>` (got `<class 'int'>`).",
        )

    def test_expect_str_warn_mode(self):
        with self.assertWarns(RuntimeTypingWarning):
            expect_str_warn_mode(1)

    def test_expect_str_raise_mode(self):
        with self.assertRaises(RuntimeTypingError):
            expect_str_raise_mode(1)

    raise ValueError