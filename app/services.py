from functools import lru_cache

def pow_int(x: int, y: int) -> int:
    return x ** y

@lru_cache(maxsize=1024)
def fib(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def fact(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
