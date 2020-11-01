from inspect import _empty, signature
from functools import wraps

from src.typed_function import TypedFunction
from src.violations import HandleViolationMode
from src.utils import doublewrap


@doublewrap
def typed(
    func, mode: "HandleViolationMode" = "raise", defer: bool = False
) -> "Callable":
    """
    :param func: The function to be typed.

    :param mode: {'raise', 'warn', 'return'} Mode how to handle
    typingviolations. Default: "raise". + "raise": For any violation of a type constraint,
    a `runtime_typing.RuntimeTypingError` is raised.

    + "warn": For any violation of a type constraint,
    a `runtime_typing.RuntimeTypingWarning` is being thrown.

    + "return"`: No exception is raised and no warning is thrown, but in case
    of violations, the return value of the function is a 2-Tuple, consisting of the original and a list of violations (instances of `runtime_typing.TypingViolation`).

    :type mode: str

    :param defer: Whether to defer the handling of a violation, By default, `@typed` handles every violation as soon as it occurs. This
    behavior can be changed by setting `defer` to `True`. This will gather
    all violations before raising a complex Exception which holds information on all the violations:


    False
    :type defer: bool

    :Example mode:

    ```python3
    from typing import Any

    @typed(mode="return")
    def return_int(x: Any) -> int:
        return x
    ```
    ```
    >>> return_int("This does not raise.")``
    ('This does not raise.', [TypingViolation in function `return_int`: Expected type of argument `return` to be `<class 'int'>` (got `<class 'str'>`).])
    ```

    :Example defer:

    ```python3
    @typed(defer=True)
    def return_int(x: int) -> int:
        return x
    ```

    ```python3
    >>> return_int("")
    RuntimeTypingError:
        + TypingViolation in function `return_int`: Expected type of argument `x` to be `<class 'int'>` (got `<class 'str'>`).
        + TypingViolation in function `return_int`: Expected type of argument `return` to be `<class 'int'>` (got `<class 'str'>`).
    ```

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
        kwargs = {
            **default_args,
            **given_args
        }

        typed_func = TypedFunction(
            func=func, kwargs=kwargs, mode=mode, defer=defer
        )
        result = typed_func.execute()
        violations = typed_func.handle_violations()

        return (result, violations) if violations else result

    return validated
