from src import typed


@typed(defer=True)
def return_int(x: int) -> int:
    return x


return_int("")
