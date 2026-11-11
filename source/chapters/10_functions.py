"""
Chapter 10 - Functions (Reusing code)
=====================================

Today's goal:
  1. def, parameters, return
  2. Default and keyword arguments
  3. *args and **kwargs
  4. Scope (local vs global)
  5. Lambda, map/filter, functions as values
  6. The danger of mutable default arguments

Syntax:
  def function_name(param1, param2=default):
      \"\"\"Docstring - what the function does\"\"\"
      return result

return vs print:
  print -> shows something on the screen
  return -> gives the value back (you can use it later)

Remember:
  - A function without return gives you None.
  - Default arguments are created only once, when the function is defined.
    So don't use [] or {} as a default (see the demo below).
"""

from _kit import main


# ---------------------------------------------------------------------------
# DEMOS
# ---------------------------------------------------------------------------


def demo_basics() -> None:
    def add(a, b):
        """Returns the sum of two numbers."""
        return a + b

    result = add(2, 3)
    print("add(2, 3) =", result)
    print("docstring:", add.__doc__)

    # Print vs return
    def greet_print(name):
        print("Hello", name)

    def greet_return(name):
        return "Hello " + name

    x = greet_print("Ravi")
    y = greet_return("Ravi")
    print("result from the print version:", x)
    print("result from the return version:", y)

    # No return -> None
    def do_nothing():
        pass

    print("do_nothing():", do_nothing())


def demo_arguments() -> None:
    def introduce(name, age=18, city="Delhi"):
        return f"{name}, {age}, {city}"

    print(introduce("Ravi"))
    print(introduce("Ravi", 21))
    print(introduce("Ravi", city="Mumbai"))          # keyword argument
    print(introduce(age=25, name="Sita"))            # order does not matter

    # Positional first, keyword after
    def power(base, exp=2):
        return base ** exp

    print("power(5):", power(5))
    print("power(2, 10):", power(2, 10))
    print("power(exp=3, base=2):", power(exp=3, base=2))

    # Wrong: positional after keyword
    # power(exp=2, 5)   # SyntaxError


def demo_args_kwargs() -> None:
    def total(*numbers):
        """Take any number of positional arguments."""
        print("  numbers tuple:", numbers)
        return sum(numbers)

    print("total(1, 2, 3):", total(1, 2, 3))
    print("total():", total())

    def profile(**info):
        """Take any number of keyword arguments."""
        print("  info dict:", info)
        return info.get("name", "Unknown")

    print("profile(name='Ravi', age=21):", profile(name="Ravi", age=21))

    def mixed(a, b, *args, **kwargs):
        print(f"  a={a} b={b} args={args} kwargs={kwargs}")

    mixed(1, 2, 3, 4, x=5, y=6)

    # Pass a list/tuple by unpacking it
    nums = [1, 2, 3]
    print("total(*nums):", total(*nums))

    data = {"name": "Sita", "age": 20}
    print("profile(**data):", profile(**data))


def demo_scope() -> None:
    x = "global"

    def show():
        x = "local"
        print("inside:", x)

    show()
    print("outside:", x)

    counter = 0

    def increment():
        nonlocal counter   # the enclosing function's variable
        counter += 1

    increment()
    increment()
    print("nonlocal counter:", counter)

    global GLOBAL_COUNTER
    GLOBAL_COUNTER = 0

    def increment_global():
        global GLOBAL_COUNTER
        GLOBAL_COUNTER += 1

    increment_global()
    print("global counter:", GLOBAL_COUNTER)

    # Assigning without global/nonlocal can cause UnboundLocalError
    y = 10

    def broken():
        # print(y)   # here y will be treated as local
        y = 20
        return y

    print("broken():", broken(), "| outside y:", y)


def demo_mutable_default() -> None:
    # WRONG way
    def add_item_bad(item, items=[]):
        items.append(item)
        return items

    print("bad 1:", add_item_bad("a"))
    print("bad 2:", add_item_bad("b"))     # the previous "a" is still there!

    # RIGHT way
    def add_item_good(item, items=None):
        if items is None:
            items = []
        items.append(item)
        return items

    print("good 1:", add_item_good("a"))
    print("good 2:", add_item_good("b"))


def demo_lambda_hof() -> None:
    square = lambda x: x * x
    print("square(5):", square(5))

    add = lambda a, b: a + b
    print("add(2, 3):", add(2, 3))

    nums = [1, 2, 3, 4, 5]
    print("map square:", list(map(lambda n: n * n, nums)))
    print("filter even:", list(filter(lambda n: n % 2 == 0, nums)))

    # sorted with key
    words = ["banana", "kiwi", "apple"]
    print("sorted by len:", sorted(words, key=len))

    # Pass a function as an argument
    def apply(fn, value):
        return fn(value)

    print("apply(square, 6):", apply(square, 6))

    # Nested function
    def make_multiplier(n):
        def multiply(x):
            return x * n
        return multiply

    triple = make_multiplier(3)
    print("triple(7):", triple(7))


def demo_type_hints() -> None:
    def average(numbers: list[float]) -> float:
        """Type hints are only for help; Python does not enforce them."""
        return sum(numbers) / len(numbers)

    print("average:", average([1.0, 2.0, 3.0]))
    print("annotations:", average.__annotations__)


# ---------------------------------------------------------------------------
# EXERCISES
# ---------------------------------------------------------------------------


def apply_twice(fn, x):
    """Run fn twice: fn(fn(x)).
    apply_twice(lambda n: n + 1, 5) -> 7
    """
    # TODO
    return None


def safe_divide(a: float, b: float):
    """Divide, but return None when b == 0 (no error)."""
    # TODO
    return None


def total(*numbers) -> int:
    """Sum of any number of numbers. total() -> 0"""
    # TODO
    return None


def make_adder(n: int):
    """Return a function that adds n to x.
    add5 = make_adder(5); add5(3) -> 8
    """
    # TODO: nested function
    return None


def describe_person(**info) -> str:
    """A string like 'Ravi is 21', using the name and age kwargs.
    describe_person(name="Ravi", age=21) -> "Ravi is 21"
    """
    # TODO
    return None


def greet_all(names: list, greeting: str = "Hello") -> str:
    """Greet every name and join the greetings with commas.
    greet_all(["Ravi", "Sita"]) -> "Hello Ravi, Hello Sita"
    greet_all(["Ravi"], greeting="Hi") -> "Hi Ravi"
    """
    # TODO
    return None


# Wrappers - you don't need to change these
def check_make_adder():
    fn = make_adder(5)
    if fn is None:
        return None
    return (fn(3), fn(10))


def check_describe_person():
    return describe_person(name="Ravi", age=21)


# Solutions
def sol_apply_twice(fn, x):
    return fn(fn(x))


def sol_safe_divide(a: float, b: float):
    if b == 0:
        return None
    return a / b


def sol_total(*numbers) -> int:
    return sum(numbers)


def sol_make_adder(n: int):
    def add(x):
        return x + n
    return add


def sol_describe_person(**info) -> str:
    return f"{info.get('name')} is {info.get('age')}"


def sol_greet_all(names: list, greeting: str = "Hello") -> str:
    return ", ".join(f"{greeting} {name}" for name in names)


def sol_check_make_adder():
    fn = sol_make_adder(5)
    return (fn(3), fn(10))


def sol_check_describe_person():
    return sol_describe_person(name="Ravi", age=21)


EXERCISES = [
    {"id": "10.1", "task": "apply_twice(fn, x): fn(fn(x))", "func": apply_twice,
     "tests": [((lambda n: n + 1, 5), 7), ((lambda n: n * 2, 3), 12)],
     "solution": sol_apply_twice},
    {"id": "10.2", "task": "safe_divide(a, b): None when b==0", "func": safe_divide,
     "tests": [((10, 2), 5.0), ((1, 0), None)], "solution": sol_safe_divide},
    {"id": "10.3", "task": "total(*numbers): sum of all of them", "func": total,
     "tests": [((1, 2, 3), 6), ((), 0)], "solution": sol_total},
    {"id": "10.4", "task": "make_adder(n): return a closure", "func": check_make_adder,
     "tests": [((), (8, 15))], "solution": sol_check_make_adder,
     "starter_name": "make_adder", "solution_name": "sol_make_adder"},
    {"id": "10.5", "task": "describe_person(**info): 'Ravi is 21'", "func": check_describe_person,
     "tests": [((), "Ravi is 21")], "solution": sol_check_describe_person,
     "starter_name": "describe_person", "solution_name": "sol_describe_person"},
    {"id": "10.6", "task": "greet_all(names, greeting='Hello')", "func": greet_all,
     "tests": [((["Ravi", "Sita"],), "Hello Ravi, Hello Sita"),
               ((["Ravi"], "Hi"), "Hi Ravi")], "solution": sol_greet_all},
]

DEMOS = [
    ("10. Function basics", demo_basics),
    ("11. Default and keyword arguments", demo_arguments),
    ("12. *args and **kwargs", demo_args_kwargs),
    ("13. Scope", demo_scope),
    ("14. The danger of mutable defaults", demo_mutable_default),
    ("15. Lambda and higher-order functions", demo_lambda_hof),
    ("16. Type hints", demo_type_hints),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
