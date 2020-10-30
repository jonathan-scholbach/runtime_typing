__runtime_typing__ is a python module to be used for the easy implementation of runtime type checks. Type constraints provided in terms of the [`typing`](https://docs.python.org/3/library/typing.html) module can be used to validate function parameters and return values during runtime. Functions are exposed to type validation by being decorated with the `@typed` decorator.

# Examples 

## Expecting built-in type

```python3
from runtime_typing import typed

@typed
def expect_int(x: int):
     pass
```

```python3
>>> expect_int("")
RuntimeTypingError: TypingViolation in function `expect_int`: Expected type of argument `x` to be `<class 'int'>` (got `<class 'str'>`).
```

## Return values are also validated
```python3
from typing import Any
from src import typed


@typed
def return_int(x: Any) -> int:
    return x
```

```python3
>>> return_int("")
RuntimeTypingError: TypingViolation in function `return_int`: Expected type of argument `return` to be `<class 'int'>` (got `<class 'str'>`).
```

# Features

## Covered Types and `typing` Constructs

The following types and `typing`-constructs are covered:

+ primitives (python builtin-types, custom classes)
+ `typing.AnyStr`
+ `typing.Callable`
+ `typing.Dict`
+ `typing.Iterable`
+ `typing.Literal`
+ `typing.Tuple`
+ `typing.Type`
+ `typing.TypeVar`
+ `typing.Optional`
+ `typing.Union`


## Optional Argument `mode` to determine Violation Handling Behavior 

The `@typed` decorator accepts an optional argument `mode` which determines how a violation is being dealt with. The value of this argument must be one of `["raise", "warn", "return"]` (default is "raise").

### `mode="raise"`

For any violation of a type constraint, a `runtime_typing.RuntimeTypingError` is raised.

### `mode="warn"`

For any violation of a type constraint, a `runtime_typing.RuntimeTypingWarning` is being thrown.

### `mode="return"`

No exception is raised and no warning is thrown, but in case of violations, the return value of the function is a 2-Tuple, consisting of the original and a list of violations (instances of `runtime_typing.TypingViolation`).
 
Example:

```python3
from typing import Any

from runtime_typing import typed


@typed(mode="return")
def return_int(x: Any) -> int:
    return x
```

```
>>> return_int("This does not raise.")``
('This does not raise.', [TypingViolation in function `return_int`: Expected type of argument `return` to be `<class 'int'>` (got `<class 'str'>`).])
```

## Optional Argument `defer` to defer raising

By default, `@typed` raises on the first violation. This behavior can be changed by setting the optional parameter `defer` to `True` (default: `False`). This will gather all violations before raising a complex Exception which holds information on all the violations:

```python3
from runtime_typing import typed

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