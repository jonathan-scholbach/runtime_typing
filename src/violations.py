from abc import ABC, abstractmethod
from typing import Any, List, Literal, Optional, Union
from warnings import warn


class RuntimeTypingError(Exception):
    pass


class RuntimeTypingWarning(Warning):
    pass


HandleViolationMode = Literal["raise", "warn", "return"]


class TypingViolation(ABC):
    def __init__(self, mode: "HandleViolationMode", defer: bool):
        self.mode = mode
        if not defer:
            self.handle()

    @abstractmethod
    def __add__(self, other: "TypingViolation"):
        pass

    def __radd__(
        self, other: Optional["TypingViolation"] = None
    ) -> "TypingViolation":
        if other is None:
            return self

    def __repr__(self):
        return self.message

    def handle(self, mode: Optional[HandleViolationMode] = None):
        mode = mode or self.mode

        if mode == "raise":
            raise RuntimeTypingError(self.message)

        if mode == "warn":
            warn(self.message, RuntimeTypingWarning)

        return self

    @property
    @abstractmethod
    def message(self) -> str:
        pass


class ComplexTypingViolation(TypingViolation):
    def __init__(
        self,
        violations: List["SimpleTypingViolation"],
        mode: "HandleViolationMode" = "raise",
        defer: bool = False,
    ):
        self.violations = violations

        super().__init__(mode, defer)

    @property
    def message(self) -> str:
        violations_messages = "\n\t".join(
            [violation.message for violation in self.violations]
        )
        return f"ComplexTypingViolation: {violations_messages}."

    def __add__(
        self, other: Optional["TypingViolation"] = None
    ) -> "ComplexTypingViolation":
        if isinstance(other, ComplexTypingViolation):
            return ComplexTypingViolation(
                violations=self.violations + other.violations
            )
        if isinstance(other, SimpleTypingViolation):
            return ComplexTypingViolation(violations=self.violations + [other])

        if other is None:
            return self


class SimpleTypingViolation(TypingViolation):
    def __init__(
        self,
        obj: object,
        category: str,
        parameter_name: Any,
        expected: Any,
        got: Any,
        mode: HandleViolationMode = "raise",
        defer: bool = False,
    ) -> None:
        self.obj = obj
        self.category = category
        self.parameter_name = parameter_name
        self.expected = expected
        self.got = got
        super().__init__(mode=mode, defer=defer)

    def __add__(self, other: Optional["TypingViolation"]) -> "TypingViolation":
        if other is None:
            return self

        if isinstance(other, ComplexTypingViolation):
            return other + self

        return ComplexTypingViolation(violations=[self, other])

    @property
    def message(self):
        if hasattr(self.expected, "__length__") and not hasattr(
            self.got, "__length__"
        ):
            expected = f"one of `{self.expected}`"
        else:
            expected = f"`{self.expected}`"

        return (
            f"TypingViolation in {self.obj.__class__.__name__} "
            f"`{self.obj.__name__}`: Expected "
            f"{self.category + ' ' if self.category else ''}`{self.parameter_name}` to "
            f"be {expected} (got `{self.got}`)."
        )
