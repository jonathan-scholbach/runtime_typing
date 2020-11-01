from abc import ABC, abstractmethod
from typing import Any, List, Literal, Optional
from warnings import warn


class RuntimeTypingError(Exception):
    pass


class RuntimeTypingWarning(Warning):
    pass


HandleViolationMode = Literal["raise", "warn", "return"]


class RuntimeTypingViolation(ABC):
    """Abstract Base Class of Violations of Typing Constraints.

    Attributes
    ----------

    obj
        The object the violation occurred on.

    parameter_name
        The name of the parameter the violation occurred on.

    expected
        The expected value (or type) of the parameter.

    got
        The actual value (or type) of the parameter.

    message
        A human-readable message describing the violation. This is used in RuntimeTypingViolation.handle() when raising or warning.

    mode
        How the violation behaves when it is handled.
    """

    def __init__(self, mode: "HandleViolationMode", defer: bool):
        self.mode = mode
        if not defer:
            self.handle()

    @abstractmethod
    def __add__(self, other: "RuntimeTypingViolation"):
        pass

    def __radd__(
        self, other: Optional["RuntimeTypingViolation"] = None
    ) -> "RuntimeTypingViolation":
        if other is None:
            return self

    def __repr__(self):
        return self.message

    def handle(self, mode: Optional[Literal["raise", "warn", "return"]] = None):
        """Handle the violation (i.e. raise, warn or return it).

        Parameters
        ----------

        mode
            How to handle the violation. If set, overrides the `mode` attribute of the violation.
        """
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


class ComplexRuntimeTypingViolation(RuntimeTypingViolation):
    def __init__(
        self,
        violations: List["SimpleRuntimeTypingViolation"],
        mode: "HandleViolationMode" = "raise",
        defer: bool = False,
    ):
        self.violations = violations

        super().__init__(mode=mode, defer=defer)

    @property
    def message(self) -> str:
        violations_messages = "\n\t".join(
            [violation.message for violation in self.violations]
        )
        return f"ComplexTypingViolation: {violations_messages}."

    def __add__(
        self, other: Optional["RuntimeTypingViolation"] = None
    ) -> "ComplexRuntimeTypingViolation":
        if isinstance(other, ComplexRuntimeTypingViolation):
            return ComplexRuntimeTypingViolation(
                violations=self.violations + other.violations
            )
        if isinstance(other, SimpleRuntimeTypingViolation):
            return ComplexRuntimeTypingViolation(
                violations=self.violations + [other]
            )

        if other is None:
            return self


class SimpleRuntimeTypingViolation(RuntimeTypingViolation):
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

    def __add__(
        self, other: Optional["RuntimeTypingViolation"]
    ) -> "RuntimeTypingViolation":
        if other is None:
            return self

        if isinstance(other, ComplexRuntimeTypingViolation):
            return other + self

        return ComplexRuntimeTypingViolation(violations=[self, other])

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
