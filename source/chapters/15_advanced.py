"""
Chapter 15 - Advanced: Iterators, Generators, Decorators
========================================================

Today's goal:
  1. Iterator protocol (__iter__, __next__)
  2. Generator (yield) - lazy values
  3. Closure
  4. Decorator (a function on top of a function)
  5. functools.lru_cache, context manager
  6. Type hints (a little more)

Iterator: give values only when they are needed.
  A for loop calls iter() and next() under the hood.

Generator: a function with yield. It pauses at every yield and
continues from the same spot on the next next(). It uses less memory.

  def countdown(n):
      while n > 0:
          yield n
          n -= 1

  list(countdown(3)) -> [3, 2, 1]

Decorator: wrap a function to give it new behaviour.
  @timer
  def slow(): ...

  This means: slow = timer(slow)

Closure: an inner function remembers a variable from the outer function.
"""

import functools
import time
from contextlib import contextmanager

from _kit import main


# ---------------------------------------------------------------------------
# DEMOS
# ---------------------------------------------------------------------------


def demo_iterator() -> None:
    class Countdown:
        def __init__(self, start):
            self.current = start

        def __iter__(self):
            return self

        def __next__(self):
            if self.current <= 0:
                raise StopIteration
            value = self.current
            self.current -= 1
            return value

    print("iterator:")
    for n in Countdown(3):
        print(" ", n)

    it = Countdown(2)
    print("next:", next(it))
    print("next:", next(it))
    try:
        next(it)
    except StopIteration:
        print("StopIteration: finished")

    # Built-in iterators
    nums = [10, 20]
    it2 = iter(nums)
    print("list iterator:", next(it2), next(it2))


def demo_generator() -> None:
    def countdown(n):
        while n > 0:
            yield n
            n -= 1

    gen = countdown(3)
    print("generator type:", type(gen).__name__)
    print("next:", next(gen))
    print("rest:", list(gen))

    # Fibonacci generator
    def fib(limit):
        a, b = 0, 1
        for _ in range(limit):
            yield a
            a, b = b, a + b

    print("fib(10):", list(fib(10)))

    # Generator pipeline (memory efficient)
    def read_numbers(nums):
        for n in nums:
            yield n

    def square(numbers):
        for n in numbers:
            yield n * n

    def only_even(numbers):
        for n in numbers:
            if n % 2 == 0:
                yield n

    pipeline = only_even(square(read_numbers(range(10))))
    print("pipeline:", list(pipeline))

    # send() - advanced
    def echo():
        while True:
            received = yield
            if received is None:
                break
            print("  received:", received)

    e = echo()
    next(e)          # start the generator
    e.send("hello")
    e.send("world")


def demo_closure() -> None:
    def make_counter():
        count = 0

        def counter():
            nonlocal count
            count += 1
            return count

        return counter

    c1 = make_counter()
    c2 = make_counter()
    print("c1:", c1(), c1(), c1())
    print("c2:", c2())          # a separate counter

    # A multiplier from a closure
    def multiplier(n):
        return lambda x: x * n

    double = multiplier(2)
    triple = multiplier(3)
    print("double(5):", double(5), "| triple(5):", triple(5))


def demo_decorator() -> None:
    def timer(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = fn(*args, **kwargs)
            elapsed = time.perf_counter() - start
            print(f"  {fn.__name__} took {elapsed:.6f}s")
            return result
        return wrapper

    @timer
    def slow_add(a, b):
        time.sleep(0.01)
        return a + b

    print("result:", slow_add(2, 3))
    print("name is safe:", slow_add.__name__)

    # Also works without @
    def shout(fn):
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs).upper()
        return wrapper

    @shout
    def greet(name):
        return f"hello {name}"

    print(greet("ravi"))

    # A decorator with arguments
    def repeat(times):
        def decorator(fn):
            def wrapper(*args, **kwargs):
                return [fn(*args, **kwargs) for _ in range(times)]
            return wrapper
        return decorator

    @repeat(3)
    def say_hi():
        return "hi"

    print("repeat:", say_hi())


def demo_functools() -> None:
    @functools.lru_cache(maxsize=None)
    def fib(n):
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)

    print("fib(50):", fib(50))
    print("cache info:", fib.cache_info())

    # partial - fix a few arguments
    def power(base, exp):
        return base ** exp

    square = functools.partial(power, exp=2)
    print("square(7):", square(7))


def demo_context_manager() -> None:
    @contextmanager
    def section(title):
        print(f"\n--- {title} starts ---")
        try:
            yield
        finally:
            print(f"--- {title} ends ---")

    with section("work"):
        print("the work inside is happening")

    # Class based context manager
    class Timer:
        def __enter__(self):
            self.start = time.perf_counter()
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.elapsed = time.perf_counter() - self.start
            print(f"  elapsed: {self.elapsed:.6f}s")
            return False     # returning True would hide the error

    with Timer():
        sum(range(100000))


def demo_typing() -> None:
    from typing import Optional

    def find_user(user_id: int) -> Optional[dict]:
        if user_id == 1:
            return {"id": 1, "name": "Ravi"}
        return None

    print("find_user(1):", find_user(1))
    print("find_user(2):", find_user(2))

    # Modern syntax (Python 3.9+)
    def total(nums: list[int]) -> int:
        return sum(nums)

    print("total:", total([1, 2, 3]))


# ---------------------------------------------------------------------------
# EXERCISES
# ---------------------------------------------------------------------------


def countdown(n: int):
    """Generator: yield from n down to 1.
    list(countdown(3)) -> [3, 2, 1]
    """
    # TODO: use yield
    return None


def fib_gen(n: int):
    """Generator: the first n Fibonacci numbers (0, 1, 1, 2, ...).
    list(fib_gen(5)) -> [0, 1, 1, 2, 3]
    """
    # TODO
    return None


def chunked(items: list, size: int) -> list:
    """Break the list into chunks of the given size.
    chunked([1, 2, 3, 4, 5], 2) -> [[1, 2], [3, 4], [5]]
    """
    # TODO: range(0, len, size) + slicing
    return None


def double(fn):
    """Decorator: multiply the function's result by 2."""
    # TODO: build a wrapper, use functools.wraps
    return None


def memoize(fn):
    """Decorator: cache the result (in a dict) so it isn't calculated again."""
    # TODO
    return None


# Wrappers - you don't need to change these
def add(a, b):
    return a + b


def check_countdown():
    gen = countdown(3)
    if gen is None:
        return None
    return list(gen)


def check_fib_gen():
    gen = fib_gen(5)
    if gen is None:
        return None
    return list(gen)


def check_double():
    wrapped = double(add)
    if wrapped is None:
        return None
    return wrapped(1, 2)


def check_memoize():
    calls = {"count": 0}

    def slow_square(x):
        calls["count"] += 1
        return x * x

    fast = memoize(slow_square)
    if fast is None:
        return None
    first = fast(4)
    second = fast(4)
    return (first, second, calls["count"])


# Solutions
def sol_countdown(n: int):
    while n > 0:
        yield n
        n -= 1


def sol_fib_gen(n: int):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def sol_chunked(items: list, size: int) -> list:
    return [items[i:i + size] for i in range(0, len(items), size)]


def sol_double(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs) * 2
    return wrapper


def sol_memoize(fn):
    cache = {}

    @functools.wraps(fn)
    def wrapper(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]
    return wrapper


def sol_check_countdown():
    return list(sol_countdown(3))


def sol_check_fib_gen():
    return list(sol_fib_gen(5))


def sol_check_double():
    return sol_double(add)(1, 2)


def sol_check_memoize():
    calls = {"count": 0}

    def slow_square(x):
        calls["count"] += 1
        return x * x

    fast = sol_memoize(slow_square)
    return (fast(4), fast(4), calls["count"])


EXERCISES = [
    {"id": "15.1", "task": "countdown(n): generator 3,2,1", "func": check_countdown,
     "tests": [((), [3, 2, 1])], "solution": sol_check_countdown,
     "starter_name": "countdown", "solution_name": "sol_countdown"},
    {"id": "15.2", "task": "fib_gen(n): first n Fibonacci numbers", "func": check_fib_gen,
     "tests": [((), [0, 1, 1, 2, 3])], "solution": sol_check_fib_gen,
     "starter_name": "fib_gen", "solution_name": "sol_fib_gen"},
    {"id": "15.3", "task": "chunked(items, size): split the list into pieces", "func": chunked,
     "tests": [(([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]]),
               (([], 3), [])], "solution": sol_chunked,
     "starter_name": "chunked", "solution_name": "sol_chunked"},
    {"id": "15.4", "task": "double(fn): decorator, result x2", "func": check_double,
     "tests": [((), 6)], "solution": sol_check_double,
     "starter_name": "double", "solution_name": "sol_double"},
    {"id": "15.5", "task": "memoize(fn): cache the result, only 1 call", "func": check_memoize,
     "tests": [((), (16, 16, 1))], "solution": sol_check_memoize,
     "starter_name": "memoize", "solution_name": "sol_memoize"},
]

DEMOS = [
    ("15. Iterator protocol", demo_iterator),
    ("16. Generators", demo_generator),
    ("17. Closures", demo_closure),
    ("18. Decorators", demo_decorator),
    ("19. functools", demo_functools),
    ("20. Context managers", demo_context_manager),
    ("21. Type hints", demo_typing),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
