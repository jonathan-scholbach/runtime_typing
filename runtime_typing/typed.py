"""
runtime_typing
====================================

Providing a function decorator to perform type checks during runtime.
"""

from inspect import _empty, signature
from functools import wraps
from typing import Callable, Literal

from runtime_typing.typed_function import TypedFunction
from runtime_typing.utils import doublewrap


@doublewrap
def typed(
    func: "Callable",
    mode: Literal["raise", "warn", "return"] = "raise",
    defer: bool = False,
) -> "Callable":
    """Function decorator for validating arguments against type annotations.

    Parameters
    ----------

    func
        The function to be typed.

    mode
        Mode how to handle typing violations. Default: `'raise'`

        + `'raise'`: For any violation of a type constraint, a `runtime_typing.RuntimeTypingError` is raised.

        + `'warn'`: For any violation of a type constraint, a `runtime_typing.RuntimeTypingWarning` is being thrown.

        + `'return'`: No exception is raised and no warning is thrown, but the return value of the function is a 2-Tuple, consisting of the original result of the function and a (possibly empty) list of `runtime_typing.TypingViolation`.

    defer
        Whether to defer the handling of a violation. Default: `False`. By default, `@typed` handles every violation as soon as it occurs. This behavior can be changed by setting `defer` to `True`. This will gather all violations before handling them (i.e. throwing an Exception or a Warning)

    Example
    -------
    .. code-block:: python

        @typed(mode="return")
        def return_int(x: int) -> int:
           return x

        return_int("This does not raise.")

    .. code-block:: python

        ('This does not raise.', [TypingViolation in function `return_int`: Expected type of argument `x` to be `<class 'int'>` (got `<class 'str'>`)., TypingViolation in function `return_int`: Expected type of argument `return` to be `<class 'int'>` (got `<class 'str'>`).])

    Example
    ----------
    .. code-block:: python

        @typed(defer=True)
        def return_int(x: int) -> int:
            return x

        return_int("")

    .. code-block:: python

        RuntimeTypingError:
            + TypingViolation in function `return_int`: Expected type of argument `x` to be `<class 'int'>` (got `<class 'str'>`).
            + TypingViolation in function `return_int`: Expected type of argument `return` to be `<class 'int'>` (got `<class 'str'>`).
    """

    @wraps(func)
    def validated(*args, **kwargs):
        func_parameters = signature(func).parameters

        given_args = dict(zip(func_parameters.keys(), args))
        given_args.update(kwargs)
        default_args = {
            name: parameter.default
            for name, parameter in func_parameters.items()
            if parameter.default is not _empty
        }
        kwargs = {**default_args, **given_args}

        typed_func = TypedFunction(
            func=func, kwargs=kwargs, mode=mode, defer=defer
        )
        result = typed_func.execute()

        return result

    return validated
