from abc import ABC, abstractmethod
from contextlib import suppress
from typing import Any, List, Literal, Optional
from warnings import warn


class RuntimeTypingError(Exception):
    pass


class RuntimeTypingWarning(Warning):
    pass


HandleViolationMode = Literal["raise", "warn", "return"]


class RuntimeTypingViolationBase(ABC):
    """Abstract Base Class of Violations of Typing Constraints.
    """

    def __init__(self, mode: "HandleViolationMode", defer: bool):
        self._mode = mode
        self._defer = defer
        if not defer:
            self.handle()

    @abstractmethod
    def __add__(self, other: "RuntimeTypingViolationBase"):
        pass

    def __radd__(
        self, other: Optional["RuntimeTypingViolationBase"] = None
    ) -> "RuntimeTypingViolationBase":
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
        mode = mode or self._mode

        if mode == "raise":
            raise RuntimeTypingError(self.message)

        if mode == "warn":
            warn(self.message, RuntimeTypingWarning)

        return selfmae

    @property
    @abstractmethod
    def message(self) -> str:
        pass


class ComplexRuntimeTypingViolation(RuntimeTypingViolationBase):
    """Container of multiple TypingViolations.

    Attributes
    ----------

    violations
        List of the TypingViolations.

    conjunction
        Whether the TypingViolations are AND- or OR-combined.

    message
        A human-readable message used for raising and warning.
    """
    def __init__(
        self,
        violations: List["RuntimeTypingViolation"],
        mode: "HandleViolationMode" = "raise",
        defer: bool = False,
        conjunction: Literal["and", "or"] = "or",
    ):
        self.violations = violations
        self.conjunction = conjunction

        super().__init__(mode=mode, defer=defer)

    @property
    def message(self) -> str:
        with suppress(KeyError):
            if self.conjunction == "or":
                obj = self.violations[0].obj
                category = self.violations[0].category
                parameter_name = self.violations[0].parameter_name
                got = self.violations[0].got

                return (
                    f"TypingViolation in {obj.__class__.__name__} "
                    f"`{obj.__name__}`: Expected "
                    f"{category + ' ' if category else ''}`{parameter_name}` to "
                    f"be one of {[v.expected for v in self.violations]} (got `{got}`)."
                )

        violations_messages = f"\n\t".join(
            [violation.message for violation in self.violations]
        )

        return f"TypingViolation:\n\t{violations_messages}"

    def __add__(
        self, other: Optional["RuntimeTypingViolationBase"] = None
    ) -> "ComplexRuntimeTypingViolation":
        if isinstance(other, ComplexRuntimeTypingViolation):
            return ComplexRuntimeTypingViolation(
                violations=self.violations + other.violations
            )
        if isinstance(other, RuntimeTypingViolation):
            return ComplexRuntimeTypingViolation(
                violations=self.violations + [other]
            )

        if other is None:
            return self


class RuntimeTypingViolation(RuntimeTypingViolationBase):
    """Violation against Typing Annotation.

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
    """
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
        self, other: Optional["RuntimeTypingViolationBase"]
    ) -> "RuntimeTypingViolationBase":
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
