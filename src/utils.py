from collections import namedtuple
from inspect import _empty, signature
from functools import wraps
from typing import (
    get_args,
    get_origin,
    Any,
    Callable,
    _GenericAlias,
    Iterable,
    Literal,
    Set,
    Union,
    TypeVar,
)


Parameter = namedtuple("Parameter", "value name")


def doublewrap(f):
    """This recipe of creating a decorator with optional parameters is taken
    from https://stackoverflow.com/a/14412901/3566606."""

    @wraps(f)
    def new_dec(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            return f(args[0])
        else:
            return lambda realf: f(realf, *args, **kwargs)

    return new_dec


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

    if annotation is Any:
        return Any
