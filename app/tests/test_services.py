from app.services import fib, fact, pow_int


# test for math
def test_fib():
    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(10) == 55


def test_fact():
    assert fact(0) == 1
    assert fact(5) == 120


def test_pow():
    assert pow_int(2, 3) == 8
