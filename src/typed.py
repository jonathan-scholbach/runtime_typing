from functools import wraps

from src.typed_function import TypedFunction
from src.violations import HandleViolationMode
from src.utils import assemble_kwargs, doublewrap


@doublewrap
def typed(
    func, mode: "HandleViolationMode" = "raise", defer: bool = False
) -> "Callable":
    @wraps(func)
    def validated(*args, **kwargs):
        keyword_args = assemble_kwargs(func, *args, **kwargs)
        typed_func = TypedFunction(
            func=func, kwargs=keyword_args, mode=mode, defer=defer
        )
        result = typed_func.execute()
        violations = typed_func.handle_violations()

        return (result, violations) if violations else result

    return validated
