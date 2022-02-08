import sys

from collections import namedtuple
from inspect import isfunction, isclass, getmembers
from functools import wraps
from typing import (
    get_args,
    get_origin,
    Any,
    _GenericAlias,
    Iterable,
    Literal,
    Set,
    Union,
    TypedDict,
    TypeVar,
)


Parameter = namedtuple("Parameter", "value name")


def class_decorator(cls, decorator, *args, **kwargs):
    """Class decorator decorating all methods with decorator."""
    for name, method in getmembers(cls, predicate=isfunction):
        setattr(cls, name, decorator(method, *args, **kwargs))

    return cls


def optional_arguments_to_decorator(decorator):
    """Make decorator accept optional arguments and classes as objects."""

    @wraps(decorator)
    def new_decorator(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            if isfunction(args[0]):
                return decorator(args[0])
            if isclass(args[0]):
                return class_decorator(args[0], decorator)
        else:
            return (
                lambda obj: decorator(obj, *args, **kwargs)
                if isfunction(obj)
                else class_decorator(obj, decorator, *args, **kwargs)
            )

    return new_decorator


def contains(iterable: Iterable, val: Any) -> bool:
    try:
        return val in iterable
    except TypeError:
        for el in iterable:
            if val == el:
                return True
        return False


def valid_args_from_literal(annotation: _GenericAlias) -> Set[Any]:
    args = get_args(annotation)
    valid_values = []

    for arg in args:
        if get_origin(arg) is Literal:
            valid_values += valid_args_from_literal(arg)
        else:
            valid_values += [arg]

    return set(valid_values)


def get_root(annotation: _GenericAlias) -> Union[type, Any, TypeVar]:
    """Wrapper around typing.get_origin to also identify TypeVar and Any."""
    origin = get_origin(annotation)
    if origin:
        return origin

    if type(annotation) is TypeVar:
        return TypeVar

    if version_safe_is_typeddict(annotation):
        return TypedDict

    if annotation is Any:
        return Any


def version_safe_is_typeddict(value: Any) -> bool:
    if sys.version_info < (3, 10):
        from typing import _TypedDictMeta

        return isinstance(value, _TypedDictMeta)

    from typing import is_typeddict

    # Second check is necessary, is_typeddict(TypedDict) is surprisingly False
    return is_typeddict(value) or value is TypedDict
