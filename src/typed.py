from inspect import _empty, signature
from functools import wraps

from src.typed_function import TypedFunction
from src.violations import HandleViolationMode
from src.utils import doublewrap


@doublewrap
def typed(
    func, mode: "HandleViolationMode" = "raise", defer: bool = False
) -> "Callable":
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
