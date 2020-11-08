"""
runtime_typing
====================================

Providing a function decorator to perform type checks during runtime.
"""

from inspect import _empty, signature
from functools import wraps
from typing import Callable, Literal, Iterable, Optional

from runtime_typing.typed_function import TypedFunction
from runtime_typing.utils import optional_arguments_to_decorator


@optional_arguments_to_decorator
def typed(
    obj: "Callable",
    mode: Literal["raise", "warn", "return"] = "raise",
    defer: bool = False,
    exclude: Optional[Iterable[str]] = None,
    include: Optional[Iterable[str]] = None,
) -> "Callable":
    """Decorator for validating arguments against type annotations.

    Parameters
    ----------

    obj
        The object to be typed (either a function or a class). When a class is decorated, all its methods are typed, except for classmethods. Subclasses are not typed subsequently. See Examples below.

    mode
        Mode how to handle typing violations. Default: `'raise'`

        + `'raise'`: For any violation of a type constraint, a `runtime_typing.RuntimeTypingError` is raised.

        + `'warn'`: For any violation of a type constraint, a `runtime_typing.RuntimeTypingWarning` is being thrown.

        + `'return'`: No exception is raised and no warning is thrown, but the return value of the function is a 2-Tuple, consisting of the original result of the function and a (possibly empty) list of `runtime_typing.TypingViolation`.

    defer
        Whether to defer the handling of a violation. Default: `False`. By default, `@typed` handles every violation as soon as it occurs. This behavior can be changed by setting `defer` to `True`. This will gather all violations before handling them (i.e. throwing an Exception or a Warning)

    include
        Iterable of names of arguments (can also contain "return") to be taken into account for type-checking. If falsey (an empty iterable, or not provided), all type-annotated arguments of the function are taken into account (except for those listed in the `exclude` parameter).

    exclude
        Iterable of names of arguments (can also contatin "return") to be ignored during type-checking. Definitions via `exclude` prevail over those via `include`.


    Example
    -------

    Simple usage of the `@typed` decorator on a function.

    .. code-block:: python

        @typed
        def identity_of_int(x: int) -> int:
           return x

    >>> identity_of_int("not an int")
    RuntimeTypingError: TypingViolation in function `identity_of_int`: Expected type of argument `x` to be `<class 'int'>` (got `<class 'str'>`).

    Example
    -------

    Usage with `typing` types.

    .. code-block:: python

        from typing import Union


        @typed
        def identity_of_number(x: "Union[int, float]") -> "Union[int, float]":
            return x


    >>> identity_of_number("not a number")
    RuntimeTypingError: TypingViolation in function `identity_of_number`: Expected type of argument `x` to be one of [<class 'int'>, <class 'float'>] (got `<class 'str'>`).


    Example
    -------

    Make function return violations instead of raising with `mode="return"`.

    .. code-block:: python

        @typed(mode="return")
        def identity_of_int(x: int) -> int:
           return x

    >>> identity_of_int("This does not raise.")
    ('This does not raise.', [TypingViolation in function `identity_of_int`: Expected type of argument `x` to be `<class 'int'>` (got `<class 'str'>`)., TypingViolation in function `identity_of_int`: Expected type of argument `return` to be `<class 'int'>` (got `<class 'str'>`).])


    Example
    ----------

    Defer raising violations with `defer=True`.

    .. code-block:: python

        @typed(defer=True)
        def identity_of_int(x: int) -> int:
            return x

    >>> identity_of_int("not an int")
    RuntimeTypingError:
        + TypingViolation in function `identity_of_int`: Expected type of argument `x` to be `<class 'int'>` (got `<class 'str'>`).
        + TypingViolation in function `identity_of_int`: Expected type of argument `return` to be `<class 'int'>` (got `<class 'str'>`).



    Example
    -------

    Use `include` and `exclude` parameters to restrict the function-arguments which are exposed to typechecking:

    No Exception is raised in the following example, because only the return value is type-checked:

    .. code-block:: python

        @typed(include=("return",))
        def check_return_only(x: int) -> str:
            return str(x)

    >>> check_only("not an int")
    "not an int"


    Here, `x` is not typ-checked, because it is excluded:

    .. code-block:: python

        @typed(exclude=("x",))
        def do_not_check_x(x: int, y: int, z: int) -> str:
            return ", ".join([str(x), str(y), str(z)])

    >>> do_not_check_x("not an int", 2, 3)
    "not an int, 2, 3"


    The following function is effectively not type-checked, because the included parameter `x` is also excluded. (`exclude` prevails `include`):

    .. code-block:: python

        @typed(exclude=("x", "y", "return"), include=("x",))
        def effectively_check_nothing(x: int, y: float) -> str:
            return (x, y)

    Example
    -------
    Use `@typed` on a class: Instance methods and staticmethods are typed, even if they are inherited from an un-typed class; classmethods and nested classes are not typed.

    .. code-block:: python

        class SomeSuperClass:
            def some_super_instance_method(self, x: int):
                pass


        @typed
        class SomeClass(SomeSuperClass):
            @classmethod
            def some_classmethod(cls, x: int):
                pass

            @staticmethod
            def some_staticmethod(cls, x: int):
                pass

            def __init__(self, x: int):
                pass

            def some_instance_method(self, x: int):
                pass

            class SomeNestedClass:
                def __init__(self, x: int):
                    pass

    >>> SomeClass("not an int")
    RuntimeTypingError: TypingViolation in function `__init__`: Expected type of argument `x` to be `<class 'int'>` (got `<class 'str'>`).

    >>> SomeClass(1).some_instance_method("not an int")
    RuntimeTypingError: TypingViolation in function `some_instance_method`: Expected type of argument `x` to be `<class 'int'>` (got `<class 'str'>`)

    >>> SomeClass(1).some_super_instance_method("not an int")
    RuntimeTypingError: TypingViolation in function `some_super_instance_method`: Expected type of argument `x` to be `<class 'int'>` (got `<class 'str'>`).

    >>> SomeClass.some_staticmethod("not an int")
    RuntimeTypingError: TypingViolation in function `some_staticmethod`: Expected type of argument `x` to be `<class 'int'>` (got `<class 'str'>`).

    >>> SomeClass.some_classmethod("not an int")  # does not raise
    >>> SomeClass(1).SomeNestedClass("not an int")  # does not raise
    >>> SomeClass.SomeNestedClass("not an int")  # does not raise

    Example
    -------

    Typing a classmethod. If you want to type a classmethod of a class, you can do so by explicitely decorating it:

    .. code-block:: python

        class TypedClassMethodClass:
            @classmethod
            @typed
            def some_class_method(cls, x: int):
                pass

    >>> TypedClassMethodClass.some_class_method("not an int")
    RuntimeTypingError: TypingViolation in function `some_class_method`: Expected type of argument `x` to be `<class 'int'>` (got `<class 'str'>`).
    """

    @wraps(obj)
    def validated(*args, **kwargs):
        func_parameters = signature(obj).parameters

        given_args = dict(zip(func_parameters.keys(), args))
        given_args.update(kwargs)
        default_args = {
            name: parameter.default
            for name, parameter in func_parameters.items()
            if parameter.default is not _empty
        }
        kwargs = {**default_args, **given_args}

        typed_func = TypedFunction(
            func=obj,
            kwargs=kwargs,
            mode=mode,
            defer=defer,
            exclude=exclude,
            include=include,
        )
        result = typed_func()

        return result

    return validated
