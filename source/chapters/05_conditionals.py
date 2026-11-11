"""
Chapter 05 - Conditionals (Making decisions)
===========================================

Today's goal:
  1. if / elif / else
  2. Conditions with comparisons and truthiness
  3. Nested if
  4. Ternary (a one-line if)
  5. match-case (Python 3.10+)

Syntax:
  if condition:
      do_something()
  elif another_condition:
      do_something_else()
  else:
      do_the_last_thing()

Watch out:
  - Don't forget the colon (:).
  - The code inside is indented 4 spaces.
  - = stores a value, == compares values.
  - Conditions are checked from top to bottom, and the first True one wins.
"""

from _kit import main


# ---------------------------------------------------------------------------
# DEMOS
# ---------------------------------------------------------------------------


def demo_if_elif_else() -> None:
    marks = 78

    if marks >= 90:
        print("Grade A")
    elif marks >= 75:
        print("Grade B")
    elif marks >= 60:
        print("Grade C")
    else:
        print("Work harder")

    # Just an if - it's fine if nothing happens
    age = 20
    if age >= 18:
        print("Adult")

    # Truthiness: 0, "", [], {}, None, False -> False. Everything else is True.
    name = ""
    if name:
        print("Name is:", name)
    else:
        print("The name is empty")

    items = [1, 2]
    if items:
        print("The list has", len(items), "items")


def demo_nested() -> None:
    age = 22
    has_id = True

    if age >= 18:
        if has_id:
            print("Entry allowed")
        else:
            print("Bring your ID")
    else:
        print("You are under 18")

    # Flat version (better) - join the conditions with and
    if age >= 18 and has_id:
        print("Flat check: Entry allowed")


def demo_ternary() -> None:
    age = 17
    status = "adult" if age >= 18 else "minor"
    print("status:", status)

    # Nested ternary (hard to read, but you will see it)
    marks = 82
    grade = "A" if marks >= 90 else ("B" if marks >= 75 else "C")
    print("grade:", grade)

    # Using a boolean like a number
    print("True + True =", True + True)


def demo_match_case() -> None:
    command = "start"

    match command:
        case "start":
            print("Let's start")
        case "stop":
            print("Stopped")
        case "help" | "h":
            print("Help")
        case _:
            print("I didn't understand:", command)

    # Pattern with values
    point = (0, 5)
    match point:
        case (0, 0):
            print("Origin")
        case (0, y):
            print("On the Y-axis, y =", y)
        case (x, 0):
            print("On the X-axis, x =", x)
        case (x, y):
            print("Point:", x, y)


def demo_common_mistakes() -> None:
    # 1) = vs ==
    x = 5
    if x == 5:
        print("Correct comparison")

    # 2) Comparing a string with a number
    age_text = "18"
    # if age_text >= 18:   # TypeError
    if int(age_text) >= 18:
        print("Correct after converting")

    # 3) Brackets with multiple conditions
    temp = 30
    is_humid = True
    if temp > 25 and (is_humid or temp > 35):
        print("Hot and humid")

    # 4) An empty block is not allowed - use pass
    if temp > 50:
        pass
    else:
        print("temp is below 50")


# ---------------------------------------------------------------------------
# EXERCISES
# ---------------------------------------------------------------------------


def grade(marks: int) -> str:
    """90+ -> 'A', 75+ -> 'B', 60+ -> 'C', 40+ -> 'D', otherwise 'F'."""
    # TODO
    return None


def max3(a: int, b: int, c: int) -> int:
    """The largest of the three numbers."""
    # TODO: if/elif or max()
    return None


def is_leap(year: int) -> bool:
    """Leap year: divisible by 4, not by 100, OR divisible by 400.
    is_leap(2024) -> True, is_leap(1900) -> False, is_leap(2000) -> True
    """
    # TODO
    return None


def ticket_price(age: int) -> int:
    """Under 5 -> 0, under 18 -> 100, under 60 -> 200, otherwise 120."""
    # TODO
    return None


def fizz_value(n: int) -> str:
    """Divisible by 3 -> 'Fizz', by 5 -> 'Buzz', by both -> 'FizzBuzz', otherwise str(n)."""
    # TODO: check the "both" case first!
    return None


def sign(n: float) -> str:
    """'positive', 'negative', or 'zero'."""
    # TODO
    return None


# Solutions
def sol_grade(marks: int) -> str:
    if marks >= 90:
        return "A"
    elif marks >= 75:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 40:
        return "D"
    else:
        return "F"


def sol_max3(a: int, b: int, c: int) -> int:
    if a >= b and a >= c:
        return a
    elif b >= c:
        return b
    else:
        return c


def sol_is_leap(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def sol_ticket_price(age: int) -> int:
    if age < 5:
        return 0
    elif age < 18:
        return 100
    elif age < 60:
        return 200
    else:
        return 120


def sol_fizz_value(n: int) -> str:
    if n % 15 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)


def sol_sign(n: float) -> str:
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    else:
        return "zero"


EXERCISES = [
    {"id": "5.1", "task": "grade(marks): A/B/C/D/F", "func": grade,
     "tests": [((95,), "A"), ((80,), "B"), ((65,), "C"), ((45,), "D"), ((20,), "F")],
     "solution": sol_grade},
    {"id": "5.2", "task": "max3(a, b, c): the largest one", "func": max3,
     "tests": [((1, 2, 3), 3), ((9, 2, 3), 9), ((1, 8, 3), 8)], "solution": sol_max3},
    {"id": "5.3", "task": "is_leap(year): leap year check", "func": is_leap,
     "tests": [((2024,), True), ((1900,), False), ((2000,), True), ((2023,), False)],
     "solution": sol_is_leap},
    {"id": "5.4", "task": "ticket_price(age): price based on age", "func": ticket_price,
     "tests": [((3,), 0), ((15,), 100), ((30,), 200), ((65,), 120)], "solution": sol_ticket_price},
    {"id": "5.5", "task": "fizz_value(n): Fizz/Buzz/FizzBuzz/number", "func": fizz_value,
     "tests": [((9,), "Fizz"), ((10,), "Buzz"), ((15,), "FizzBuzz"), ((7,), "7")],
     "solution": sol_fizz_value},
    {"id": "5.6", "task": "sign(n): positive/negative/zero", "func": sign,
     "tests": [((5,), "positive"), ((-2,), "negative"), ((0,), "zero")], "solution": sol_sign},
]

DEMOS = [
    ("5. if / elif / else", demo_if_elif_else),
    ("6. Nested if", demo_nested),
    ("7. Ternary", demo_ternary),
    ("8. match-case", demo_match_case),
    ("9. Common mistakes", demo_common_mistakes),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
