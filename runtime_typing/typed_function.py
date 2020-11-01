from collections.abc import Callable, Iterable
from typing import (
    get_args,
    get_type_hints,
    Any,
    Callable as TypingCallable,
    _GenericAlias,
    List,
    Literal,
    Optional,
    Tuple,
    TypeVar,
    Union,
)
from warnings import warn

from src.violations import (
    SimpleTypingViolation,
    ComplexTypingViolation,
    TypingViolation,
    HandleViolationMode,
    RuntimeTypingError,
    RuntimeTypingWarning,
)
from src.utils import contains, get_root, valid_args_from_literal, Parameter


ReturnType = TypeVar("ReturnType")


class TypedFunction:
    def __init__(
        self,
        func: TypingCallable[[], "ReturnType"],
        kwargs: dict,
        mode: "HandleViolationMode",
        defer: bool,
        type_var_registry: Optional[dict] = None,
    ) -> None:
        self.func = func
        self.kwargs = kwargs
        self.mode = mode
        self.defer = defer
        if type_var_registry is None:
            self.type_var_registry = {}
        else:
            self.type_var_registry = type_var_registry

        self.violations = []
        self.return_value = None

    def execute(self) -> "ReturnType":
        for arg_name, condition in get_type_hints(self.func).items():
            if arg_name == "return":
                continue

            try:
                val = self.kwargs[arg_name]
            except KeyError:
                raise TypeError(
                    f"`{self.func.__name__}()` missing required positional "
                    f"argument `{arg_name}`."
                )

            self.validate_entity(
                parameter=Parameter(value=val, name=arg_name),
                condition=condition,
            )

        result = self.func(**self.kwargs)

        if "return" in get_type_hints(self.func):
            self.validate_entity(
                parameter=Parameter(value=result, name="return"),
                condition=get_type_hints(self.func)["return"],
            )

        self.result = result

        return self.result

    def handle_violations(self) -> List[TypingViolation]:
        message = "\n    + " + "\n    + ".join(
            [violation.message for violation in self.violations]
        )

        if self.violations:
            if self.mode == "raise":
                raise RuntimeTypingError(message)

            if self.mode == "warn":
                warn(message, RuntimeTypingWarning)

        return self.violations

    def validate_entity(
        self, parameter: "Parameter", condition: _GenericAlias
    ) -> "TypingViolation":
        """Check whether entity of `name` and `val` violates condition,
        recursively walking through nested condition."""
        root = get_root(condition)

        try:
            validation_method = {
                # Annotated: self.__validate_annotated,
                Any: self.__validate_any,
                Union: self.__validate_union,
                Literal: self.__validate_literal,
                Callable: self.__validate_callable,
                Iterable: self.__validate_iterable,
                TypeVar: self.__validate_type_var,
                type: self.__validate_type,
                dict: self.__validate_dict,
                list: self.__validate_list,
                set: self.__validate_set,
                frozenset: self.__validate_frozenset,
                tuple: self.__validate_tuple,
            }[root]

            validation_method(parameter=parameter, condition=condition)

        except KeyError:
            self.__validate_primitive(
                parameter=parameter,
                expected_type=condition,
                constraints=tuple(),
            )

    def __add_violation(
        self, expected: Any, got: Any, category: str, parameter_name: str
    ) -> None:
        self.violations.append(
            SimpleTypingViolation(
                obj=self.func,
                expected=expected,
                got=got,
                category=category,
                parameter_name=parameter_name,
                mode=self.mode,
                defer=self.defer,
            )
        )

    def __validate_any(
        self, parameter: "Parameter", condition: _GenericAlias
    ) -> None:
        pass

    def __validate_primitive(
        self,
        parameter: "Parameter",
        expected_type: _GenericAlias,
        constraints: Tuple[type, ...],
    ):
        if constraints:
            if not any(
                isinstance(parameter.value, constraint)
                for constraint in constraints
            ):
                self.__add_violation(
                    expected=constraints,
                    got=type(parameter.value),
                    category="type of argument",
                    parameter_name=parameter.name,
                )

        if not isinstance(parameter.value, expected_type):
            self.__add_violation(
                expected=expected_type,
                got=type(parameter.value),
                category="type of argument",
                parameter_name=parameter.name,
            )

    def __validate_type_var(
        self,
        parameter: "Parameter",
        condition: _GenericAlias,
    ) -> None:
        if condition in self.type_var_registry:
            expected_type = self.type_var_registry[condition]
        else:
            expected_type = type(parameter.value)

        self.type_var_registry[condition] = type(parameter.value)

        self.__validate_primitive(
            parameter=parameter,
            expected_type=expected_type,
            constraints=condition.__constraints__,
        )

    def __validate_sequence(
        self,
        parameter: "Parameter",
        condition: _GenericAlias,
        sequence_type: type,
    ) -> None:
        """Validate sequence types (with potential inner_condition)."""
        if not isinstance(parameter.value, sequence_type):
            self.__add_violation(
                expected=sequence_type,
                got=type(parameter.value),
                parameter_name=parameter.name,
                category="type of argument",
            )

        try:
            inner_condition = get_args(condition)[0]
            for element_val in parameter.value:
                self.validate_entity(
                    parameter=Parameter(element_val, parameter.name),
                    condition=inner_condition,
                )

        except IndexError:
            pass

    def __validate_list(
        self, parameter: "Parameter", condition: _GenericAlias
    ) -> None:
        return self.__validate_sequence(parameter, condition, list)

    def __validate_set(
        self, parameter: "Parameter", condition: _GenericAlias
    ) -> None:
        return self.__validate_sequence(parameter, condition, set)

    def __validate_frozenset(
        self, parameter: "Parameter", condition: _GenericAlias
    ) -> None:
        return self.__validate_sequence(parameter, condition, frozenset)

    def __validate_iterable(
        self,
        parameter: "Parameter",
        condition: _GenericAlias,
    ) -> None:
        return self.__validate_sequence(
            parameter=parameter, condition=condition, sequence_type=Iterable
        )

    def __validate_tuple(
        self,
        parameter: "Parameter",
        condition: _GenericAlias,
    ) -> None:
        if not isinstance(parameter.value, tuple):
            self.__add_violation(
                expected=tuple,
                got=typ(parameter.value),
                category="type of argument",
                parameter_name=parameter.name,
            )

        inner_condition = get_args(condition)

        if inner_condition[-1] is Ellipsis:
            for element_val in parameter.value:
                self.validate_entity(
                    parameter=Parameter(element_val, parameter.name),
                    condition=inner_condition[-2],
                )
        else:
            if not len(parameter.value) == len(inner_condition):
                self.__add_violation(
                    expected=len(inner_condition),
                    got=len(parameter.value),
                    category="length of argument",
                    parameter_name=parameter.name,
                )

            for element_val, element_condition in zip(
                parameter.value, inner_condition
            ):
                self.validate_entity(
                    parameter=Parameter(value=element_val, name=parameter.name),
                    condition=element_condition,
                )

    def __validate_union(
        self,
        parameter: "Parameter",
        condition: _GenericAlias,
        entity_or_type: Literal["entity", "type"] = "entity",
    ) -> None:
        inner_condition = get_args(condition)
        union_violations = []

        for inner_argument in inner_condition:
            aux = TypedFunction(
                func=self.func,
                defer=True,
                mode=self.mode,
                kwargs=self.kwargs,
                type_var_registry=self.type_var_registry,
            )
            if entity_or_type == "entity":
                aux.validate_entity(
                    parameter=parameter, condition=inner_argument
                )

            if entity_or_type == "type":
                aux.__validate_type(
                    parameter=parameter, condition=inner_argument
                )

            if not aux.violations:
                return

            union_violations += aux.violations

        if union_violations:
            self.violations.append(
                ComplexTypingViolation(
                    violations=union_violations,
                    mode=self.mode,
                    defer=self.defer,
                )
            )

    def __validate_literal(
        self,
        parameter: "Parameter",
        condition: _GenericAlias,
    ) -> None:
        valid_values = valid_args_from_literal(condition)

        if not contains(valid_values, parameter.value):
            self.__add_violation(
                expected=valid_values,
                got=parameter.value,
                parameter_name=parameter.name,
                category="value of argument",
            )

    def __validate_callable(
        self,
        parameter: "Parameter",
        condition: _GenericAlias,
    ) -> None:
        if not callable(parameter.value):
            self.__add_violation(
                expected="collections.abc.Callable",
                got=type(parameter.value),
                parameter_name=parameter.name,
                category="type of argument",
            )

        inner_condition = get_args(condition)

        if inner_condition:
            condition_arg_types, condition_return_type = inner_condition

            val_hints = get_type_hints(parameter.value)
            val_arg_types = list(
                val_hints[arg] for arg in val_hints.keys() if arg != "return"
            )
            try:
                val_return_type = val_hints["return"]
            except KeyError:
                val_return_type = None

            if len(val_arg_types) != len(condition_arg_types):
                self.__add_violation(
                    expected=len(condition_arg_types),
                    got=len(val_arg_types),
                    parameter_name=parameter.name,
                    category="length of value of argument",
                )

            for index, (val_arg_type, condition_arg_type) in enumerate(
                zip(val_arg_types, condition_arg_types)
            ):
                if val_arg_type != condition_arg_type:
                    self.__add_violation(
                        expected=condition_arg_type,
                        got=val_arg_type,
                        parameter_name=parameter.name,
                        category=f"{index + 1}. argument's type in callable "
                        f"argument ",
                    )

            if val_return_type != condition_return_type:
                self.__add_violation(
                    expected=condition_return_type,
                    got=val_return_type,
                    parameter_name=parameter.name,
                    category="return type of callable argument",
                )

    def __validate_dict(
        self, parameter: "Parameter", condition: _GenericAlias
    ) -> None:
        if not isinstance(parameter.value, dict):
            self.__add_violation(
                expected=dict,
                got=type(parameter.value),
                parameter_name=parameter.name,
                category="type of argument",
            )

        inner_condition = get_args(condition)

        if inner_condition:

            key_type, value_type = inner_condition

            aux = TypedFunction(
                func=self.func,
                defer=True,
                mode=self.mode,
                kwargs=self.kwargs,
                type_var_registry=self.type_var_registry,
            )

            for key in parameter.value.keys():
                aux.validate_entity(
                    parameter=Parameter(
                        value=key,
                        name=f"key in `{parameter.name}`",
                    ),
                    condition=key_type,
                )

            for value in parameter.value.values():
                aux.validate_entity(
                    parameter=Parameter(
                        value=value,
                        name=f"value in `{parameter.name}`",
                    ),
                    condition=value_type,
                )

            if aux.violations:
                self.violations.append(
                    ComplexTypingViolation(
                        aux.violations, mode=self.mode, defer=self.defer
                    )
                )

    def __validate_type(
        self,
        parameter: "Parameter",
        condition: _GenericAlias,
    ) -> None:
        if type(parameter.value) is not type:
            self.__add_violation(
                expected=type,
                got=type(parameter.value),
                parameter_name=parameter.name,
                category="type of argument",
            )

        if type(condition) is type:
            if not issubclass(parameter.value, condition):
                self.__add_violation(
                    expected=condition,
                    got=parameter.value,
                    parameter_name=parameter.name,
                    category="argument",
                )

        else:
            inner_condition = get_args(condition)

            if inner_condition:
                for inner_type in inner_condition:
                    root = get_root(inner_type)
                    if root is Any:
                        continue

                    if root is Union:
                        self.__validate_union(
                            parameter=parameter,
                            condition=inner_type,
                            entity_or_type="type",
                        )
                        continue

                    if root is TypeVar:
                        if inner_type in self.type_var_registry:
                            self.__validate_type(
                                parameter=parameter,
                                condition=self.type_var_registry[inner_type],
                            )
                            inner_type = self.type_var_registry[inner_type]

                        else:
                            self.type_var_registry[inner_type] = parameter.value
                            continue

                    if not issubclass(parameter.value, inner_type):
                        self.__add_violation(
                            expected=inner_condition,
                            got=type(parameter.value),
                            parameter_name=parameter.name,
                            category="type of argument",
                        )
