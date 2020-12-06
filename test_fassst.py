import pytest

from fassst import fast


def test_add():
    def loop():
        x = 0
        for i in range(5):
            x += i
        return x

    fast_loop = fast(loop)
    for i in range(-30, 30):
        assert fast_loop() == loop()


def range_loop():
    x = 0
    for i in range(10):
        x += i
    return x


def enumerate_loop():
    x = 0
    for (i, j) in enumerate(range(10)):
        x += i * j
    return x


def list_str_loop():
    x = ""
    for c in ["a", "b", "c", "d", "e"]:
        x += c
    return x


def list_int_loop():
    x = 0
    for i in [1, 2, 3, 4, 5]:
        x += i
    return x


@pytest.mark.parametrize(
    "fn",
    [
        range_loop,
        enumerate_loop,
        list_str_loop,
        list_int_loop,
    ],
)
def test_original(benchmark, fn):
    result = benchmark(fn)


@pytest.mark.parametrize(
    "fn",
    [
        range_loop,
        enumerate_loop,
        list_str_loop,
        list_int_loop,
    ],
)
def test_fast(benchmark, fn):
    result = benchmark(fast(fn))

    assert result == fn()
