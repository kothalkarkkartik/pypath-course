"""
Chapter 03 - Operators and expressions
======================================

Today's goal:
  1. Arithmetic: + - * / // % **
  2. Comparison: == != > < >= <=
  3. Logical: and or not
  4. Assignment shortcuts: += -= *= /=
  5. Precedence (what runs first)

The most important difference:
  /   -> always gives a float: 7 / 2 = 3.5
  //  -> floor division (the whole number below): 7 // 2 = 3
  %   -> remainder: 7 % 2 = 1
  **  -> power: 2 ** 3 = 8

Uses of the remainder:
  n % 2 == 0  -> even
  n % 10      -> last digit
  total // people, total % people -> each share and what is left over
"""

from _kit import main


# ---------------------------------------------------------------------------
# DEMOS
# ---------------------------------------------------------------------------


def demo_arithmetic() -> None:
    a, b = 7, 2
    print("a =", a, "b =", b)
    print("a + b  =", a + b)
    print("a - b  =", a - b)
    print("a * b  =", a * b)
    print("a / b  =", a / b)
    print("a // b =", a // b)
    print("a % b  =", a % b)
    print("a ** b =", a ** b)

    # With negative numbers, // and % behave a little differently
    print("-7 // 2 =", -7 // 2)   # -4 (floor)
    print("-7 % 2  =", -7 % 2)    # 1
    print("7 // -2 =", 7 // -2)   # -4
    print("7 % -2  =", 7 % -2)    # -1

    # divmod: both at once
    print("divmod(7, 2) =", divmod(7, 2))

    # Big numbers are easier to read
    print(1_000_000 + 1)


def demo_comparison() -> None:
    print("5 == 5   ->", 5 == 5)
    print("5 != 5   ->", 5 != 5)
    print("5 > 3    ->", 5 > 3)
    print("5 <= 5   ->", 5 <= 5)

    # Chained comparison - Python's favourite trick
    age = 25
    print("18 <= age < 60 ->", 18 <= age < 60)   # (18 <= age) and (age < 60)

    # == checks the value, = stores the value
    x = 10
    print("x == 10 ->", x == 10)


def demo_logical() -> None:
    print("True and False ->", True and False)
    print("True or False  ->", True or False)
    print("not True       ->", not True)

    # Short-circuit: in `and`, if the first value is False it does not look further
    def bolta_hoon(tag, value):
        print("  called:", tag)
        return value

    print("and test:")
    result = bolta_hoon("A", False) and bolta_hoon("B", True)
    print("result:", result)

    print("or test:")
    result = bolta_hoon("C", True) or bolta_hoon("D", False)
    print("result:", result)

    # With truthiness
    name = ""
    print("name or 'Guest' ->", name or "Guest")   # default value trick


def demo_assignment_and_precedence() -> None:
    score = 10
    score += 5      # score = score + 5
    print("score += 5  ->", score)
    score -= 3
    print("score -= 3  ->", score)
    score *= 2
    print("score *= 2  ->", score)
    score //= 4
    print("score //= 4 ->", score)

    print("2 + 3 * 4   =", 2 + 3 * 4)     # 14, * first
    print("(2 + 3) * 4 =", (2 + 3) * 4)   # 20
    print("2 ** 3 ** 2 =", 2 ** 3 ** 2)   # 512, from the right
    print("not 1 == 2  =", not 1 == 2)    # comparison first

    # Precedence order (the top one runs first):
    #  ()  **  * / // %  + -  comparisons  not  and  or


# ---------------------------------------------------------------------------
# EXERCISES
# ---------------------------------------------------------------------------


def is_even(n: int) -> bool:
    """True if n is even. is_even(4) -> True"""
    # TODO: use %
    return None


def last_digit(n: int) -> int:
    """Return the last digit. For negative numbers too, return a positive digit.
    last_digit(1234) -> 4, last_digit(-57) -> 7
    """
    # TODO: abs(n) % 10
    return None


def split_bill(total: int, people: int):
    """Return (per_person, remainder).
    split_bill(100, 3) -> (33, 1)
    """
    # TODO: use divmod
    return None


def is_between(n: int, low: int, high: int) -> bool:
    """True if low <= n <= high (both inclusive)."""
    # TODO: chained comparison
    return None


def average3(a: float, b: float, c: float) -> float:
    """The average of three numbers."""
    # TODO
    return None


def power_mod(base: int, exp: int, mod: int) -> int:
    """(base ** exp) % mod, but use pow(base, exp, mod) (fast)."""
    # TODO
    return None


# Solutions
def sol_is_even(n: int) -> bool:
    return n % 2 == 0


def sol_last_digit(n: int) -> int:
    return abs(n) % 10


def sol_split_bill(total: int, people: int):
    return divmod(total, people)


def sol_is_between(n: int, low: int, high: int) -> bool:
    return low <= n <= high


def sol_average3(a: float, b: float, c: float) -> float:
    return (a + b + c) / 3


def sol_power_mod(base: int, exp: int, mod: int) -> int:
    return pow(base, exp, mod)


EXERCISES = [
    {"id": "3.1", "task": "is_even(n): True if even", "func": is_even,
     "tests": [((4,), True), ((7,), False), ((0,), True)], "solution": sol_is_even},
    {"id": "3.2", "task": "last_digit(n): the last digit (negatives too)", "func": last_digit,
     "tests": [((1234,), 4), ((-57,), 7), ((9,), 9)], "solution": sol_last_digit},
    {"id": "3.3", "task": "split_bill(total, people): (share, leftover)", "func": split_bill,
     "tests": [((100, 3), (33, 1)), ((50, 5), (10, 0))], "solution": sol_split_bill},
    {"id": "3.4", "task": "is_between(n, low, high): inclusive check", "func": is_between,
     "tests": [((5, 1, 10), True), ((1, 1, 10), True), ((0, 1, 10), False)],
     "solution": sol_is_between},
    {"id": "3.5", "task": "average3(a, b, c): the average", "func": average3,
     "tests": [((1, 2, 3), 2.0), ((10, 20, 30), 20.0)], "solution": sol_average3},
    {"id": "3.6", "task": "power_mod(base, exp, mod): pow(base, exp, mod)", "func": power_mod,
     "tests": [((2, 10, 1000), 24), ((3, 4, 5), 1)], "solution": sol_power_mod},
]

DEMOS = [
    ("3. Arithmetic operators", demo_arithmetic),
    ("4. Comparison", demo_comparison),
    ("5. Logical operators and short-circuit", demo_logical),
    ("6. Assignment and precedence", demo_assignment_and_precedence),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
