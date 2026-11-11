"""
Chapter 02 - Variables, data types and f-strings
================================================

Today's goal:
  1. Create a variable and give it a name
  2. The 4 basic types: int, float, str, bool (+ None)
  3. Check a type with type()
  4. Convert one type into another (conversion)
  5. Build nice output with f-strings

Variable = a named box that holds a value.
  name = "Ravi"      # str
  age = 21           # int
  height = 5.8       # float
  is_student = True  # bool

Rules:
  - A name starts with a letter or _. Not with a number.
  - No spaces, use underscores: first_name
  - Case sensitive: Age and age are different.
  - In Python you don't have to write the type; it is understood from the value.

f-string (the most useful thing):
  f"Hello {name}, you are {age} years old"
  f"{price:.2f}"     -> 2 decimals
  f"{n:,}"           -> 1,000,000
  f"{name:>10}"      -> right align
"""

from _kit import main


# ---------------------------------------------------------------------------
# DEMOS
# ---------------------------------------------------------------------------


def demo_types() -> None:
    name = "Ravi"
    age = 21
    height = 5.8
    is_student = True
    nothing = None

    print("name      =", name, "| type:", type(name).__name__)
    print("age       =", age, "| type:", type(age).__name__)
    print("height    =", height, "| type:", type(height).__name__)
    print("is_student=", is_student, "| type:", type(is_student).__name__)
    print("nothing   =", nothing, "| type:", type(nothing).__name__)

    # Multiple assignment
    x, y, z = 1, 2, 3
    print("x, y, z =", x, y, z)

    # One value, two variables
    a = b = 100
    print("a =", a, "b =", b)

    # Python is dynamic: the same variable can hold a new type
    value = 10
    print("value:", value, type(value).__name__)
    value = "now a string"
    print("value:", value, type(value).__name__)


def demo_conversion() -> None:
    print(int("42"))        # string -> int
    print(float("3.14"))    # string -> float
    print(str(99))          # int -> str
    print(int(3.99))        # float -> int (decimals cut, not rounded)
    print(round(3.99))      # round -> 4

    # bool() and truthiness: empty = False, non-empty = True
    print("bool(0)     =", bool(0))
    print("bool(1)     =", bool(1))
    print("bool('')    =", bool(""))
    print("bool('0')   =", bool("0"))      # note: a non-empty string is True!
    print("bool([])    =", bool([]))
    print("bool('False') =", bool("False"))  # this is True too!

    # A wrong conversion raises an error
    try:
        int("12abc")
    except ValueError as e:
        print("ValueError:", e)


def demo_fstrings() -> None:
    name = "Ravi"
    age = 21
    price = 1234.5678

    print(f"Hello {name}, you are {age} years old.")
    print(f"Price: {price:.2f}")        # 2 decimals
    print(f"Price: {price:,.2f}")       # comma + 2 decimals
    print(f"Table: |{name:>10}|")       # right align, width 10
    print(f"Table: |{name:<10}|")       # left align
    print(f"Table: |{name:^10}|")       # center
    print(f"2 + 3 = {2 + 3}")           # expressions work too
    print(f"Percentage: {0.873:.1%}")   # 87.3%

    # The old way (you can ignore this for now)
    print("Hello {}, age {}".format(name, age))


def demo_swap() -> None:
    a, b = 10, 20
    print("before:", a, b)
    a, b = b, a          # Python's magic swap
    print("after:", a, b)


# ---------------------------------------------------------------------------
# EXERCISES
# ---------------------------------------------------------------------------


def to_int(text: str) -> int:
    """Convert a string to an int. to_int("42") -> 42"""
    # TODO
    return None


def to_float(text: str) -> float:
    """Convert a string to a float. to_float("3.5") -> 3.5"""
    # TODO
    return None


def describe(name: str, age: int) -> str:
    """Build a sentence with an f-string.
    describe("Ravi", 21) -> "Ravi is 21 years old"
    """
    # TODO
    return None


def swap(a, b):
    """Return the tuple (b, a).
    swap(1, 2) -> (2, 1)
    """
    # TODO
    return None


def type_name(value) -> str:
    """Return the name of the value's type.
    type_name(3) -> "int", type_name("hi") -> "str"
    """
    # TODO: use type(value).__name__
    return None


def celsius_to_f(c: float) -> float:
    """Convert Celsius to Fahrenheit, rounded to 1 decimal.
    formula: F = C * 9/5 + 32
    celsius_to_f(0) -> 32.0
    """
    # TODO
    return None


# Solutions
def sol_to_int(text: str) -> int:
    return int(text)


def sol_to_float(text: str) -> float:
    return float(text)


def sol_describe(name: str, age: int) -> str:
    return f"{name} is {age} years old"


def sol_swap(a, b):
    return (b, a)


def sol_type_name(value) -> str:
    return type(value).__name__


def sol_celsius_to_f(c: float) -> float:
    return round(c * 9 / 5 + 32, 1)


EXERCISES = [
    {"id": "2.1", "task": "to_int(text): turn the string into an int", "func": to_int,
     "tests": [(("42",), 42), (("-7",), -7)], "solution": sol_to_int},
    {"id": "2.2", "task": "to_float(text): turn the string into a float", "func": to_float,
     "tests": [(("3.5",), 3.5), (("10",), 10.0)], "solution": sol_to_float},
    {"id": "2.3", "task": "describe(name, age): 'Ravi is 21 years old'", "func": describe,
     "tests": [(("Ravi", 21), "Ravi is 21 years old")], "solution": sol_describe},
    {"id": "2.4", "task": "swap(a, b): swap the values and return a tuple", "func": swap,
     "tests": [((1, 2), (2, 1)), (("a", "b"), ("b", "a"))], "solution": sol_swap},
    {"id": "2.5", "task": "type_name(value): give the type name as a string", "func": type_name,
     "tests": [((3,), "int"), (("hi",), "str"), ((3.5,), "float"), ((True,), "bool")],
     "solution": sol_type_name},
    {"id": "2.6", "task": "celsius_to_f(c): Fahrenheit rounded to 1 decimal", "func": celsius_to_f,
     "tests": [((0,), 32.0), ((100,), 212.0), ((37,), 98.6)], "solution": sol_celsius_to_f},
]

DEMOS = [
    ("2. Types and variables", demo_types),
    ("3. Type conversion and truthiness", demo_conversion),
    ("4. f-strings", demo_fstrings),
    ("5. Swap", demo_swap),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
