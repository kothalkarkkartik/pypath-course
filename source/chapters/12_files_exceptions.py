"""
Chapter 12 - Files and Exceptions
=================================

Today's goal:
  1. Write and read files (with open)
  2. Modern file handling with pathlib
  3. Save and load JSON
  4. try / except / else / finally
  5. Raising your own errors (raise) and custom exceptions

File modes:
  "r"  read (default) - the file must exist
  "w"  write - the old file is wiped out!
  "a"  append - adds to the end
  "x"  create - error if the file already exists

Always use `with` - the file closes automatically:
  with open("data.txt", "w", encoding="utf-8") as f:
      f.write("hello")

Exception handling:
  try:
      risky_work()
  except ValueError as e:
      print("problem:", e)
  except (TypeError, KeyError):
      ...
  else:
      print("no error happened")
  finally:
      print("always runs")

An uncaught error = the program crashes. Catching it = the program recovers and keeps going.
"""

import json
import tempfile
from pathlib import Path

from _kit import main


# ---------------------------------------------------------------------------
# DEMOS
# ---------------------------------------------------------------------------


def demo_write_read() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "notes.txt"

        # Write (the old content is wiped out)
        path.write_text("Line 1\nLine 2\n", encoding="utf-8")
        print("wrote:", repr(path.read_text(encoding="utf-8")))

        # Append
        with open(path, "a", encoding="utf-8") as f:
            f.write("Line 3\n")
        print("after append:")
        print(path.read_text(encoding="utf-8"))

        # Read line by line
        with open(path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, start=1):
                print(f"  line {i}: {line.rstrip()}")

        # All lines in a list
        lines = path.read_text(encoding="utf-8").splitlines()
        print("lines:", lines)

        # File info
        print("exists:", path.exists(), "| size:", path.stat().st_size, "bytes")
        print("name:", path.name, "| stem:", path.stem, "| suffix:", path.suffix)


def demo_json() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "student.json"
        data = {
            "name": "Ravi",
            "age": 21,
            "marks": [90, 85, 88],
            "active": True,
        }

        # Save
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print("JSON file:")
        print(path.read_text(encoding="utf-8"))

        # Load
        loaded = json.loads(path.read_text(encoding="utf-8"))
        print("loaded name:", loaded["name"])
        print("average marks:", sum(loaded["marks"]) / len(loaded["marks"]))

        # Python dict -> JSON string
        print(json.dumps({"a": 1, "b": [1, 2]}))

        # Bad JSON -> JSONDecodeError
        try:
            json.loads("{bad json}")
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", e)


def demo_exceptions() -> None:
    def divide(a, b):
        try:
            result = a / b
        except ZeroDivisionError:
            print("  You cannot divide by zero")
            return None
        except TypeError:
            print("  Give me numbers, not text")
            return None
        else:
            print("  else: everything went fine")
            return result
        finally:
            print("  finally: always runs")

    print("divide(10, 2):", divide(10, 2))
    print("divide(10, 0):", divide(10, 0))
    print("divide('a', 2):", divide("a", 2))

    # Catch a specific error
    try:
        int("hello")
    except ValueError as e:
        print("caught ValueError:", e)

    # Multiple exceptions
    try:
        data = {}
        print(data["missing"])
    except (KeyError, IndexError) as e:
        print("caught KeyError/IndexError:", repr(e))

    # Catch anything (usually avoid this)
    try:
        x = 1 / 0
    except Exception as e:
        print("Exception:", type(e).__name__, "-", e)


def demo_raise() -> None:
    class InsufficientFunds(Exception):
        """Our own custom exception."""

    def withdraw(balance, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > balance:
            raise InsufficientFunds(f"Balance is {balance}, cannot withdraw {amount}")
        return balance - amount

    print("withdraw(100, 30):", withdraw(100, 30))

    try:
        withdraw(100, 500)
    except InsufficientFunds as e:
        print("Custom error:", e)

    try:
        withdraw(100, -5)
    except ValueError as e:
        print("ValueError:", e)

    # assert - for debugging
    age = 21
    assert age >= 18, "Age is below 18"
    print("assert passed")


def demo_eafp() -> None:
    # EAFP = "Easier to Ask Forgiveness than Permission"
    # Try first, then handle the error if it happens (the Python style)
    data = {"a": 1}
    try:
        value = data["b"]
    except KeyError:
        value = 0
    print("EAFP value:", value)

    # LBYL = "Look Before You Leap"
    value = data["b"] if "b" in data else 0
    print("LBYL value:", value)


# ---------------------------------------------------------------------------
# EXERCISES
# ---------------------------------------------------------------------------


def safe_int(text: str):
    """Try int(text); return None if it fails.
    safe_int("42") -> 42, safe_int("abc") -> None
    """
    # TODO: try/except ValueError
    return None


def parse_age(text: str) -> int:
    """Valid age 0..120 -> int, otherwise -1.
    parse_age("21") -> 21, parse_age("abc") -> -1, parse_age("200") -> -1
    """
    # TODO
    return None


def count_lines(text: str) -> int:
    """How many lines are not empty (after strip).
    count_lines("a\\n\\n b \\n") -> 2
    """
    # TODO: splitlines + strip
    return None


def read_numbers(text: str) -> list:
    """Turn each line into a float, skipping bad lines.
    read_numbers("1\\n2.5\\nbad\\n3") -> [1.0, 2.5, 3.0]
    """
    # TODO: loop + try/except
    return None


def safe_divide(a: float, b: float):
    """None when b == 0, otherwise the division."""
    # TODO
    return None


def save_and_load(text: str) -> str:
    """Write the text to a temp file in UTF-8, then read it back and return it."""
    # TODO: tempfile.TemporaryDirectory + pathlib
    return None


# Solutions
def sol_safe_int(text: str):
    try:
        return int(text)
    except (ValueError, TypeError):
        return None


def sol_parse_age(text: str) -> int:
    try:
        age = int(text)
    except (ValueError, TypeError):
        return -1
    if 0 <= age <= 120:
        return age
    return -1


def sol_count_lines(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip())


def sol_read_numbers(text: str) -> list:
    numbers = []
    for line in text.splitlines():
        try:
            numbers.append(float(line.strip()))
        except ValueError:
            continue
    return numbers


def sol_safe_divide(a: float, b: float):
    try:
        return a / b
    except ZeroDivisionError:
        return None


def sol_save_and_load(text: str) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "data.txt"
        path.write_text(text, encoding="utf-8")
        return path.read_text(encoding="utf-8")


EXERCISES = [
    {"id": "12.1", "task": "safe_int(text): int or None", "func": safe_int,
     "tests": [(("42",), 42), (("abc",), None)], "solution": sol_safe_int},
    {"id": "12.2", "task": "parse_age(text): 0..120 valid, otherwise -1", "func": parse_age,
     "tests": [(("21",), 21), (("abc",), -1), (("200",), -1), (("-3",), -1)],
     "solution": sol_parse_age},
    {"id": "12.3", "task": "count_lines(text): non-empty lines", "func": count_lines,
     "tests": [(("a\n\n b \n",), 2), (("",), 0)], "solution": sol_count_lines},
    {"id": "12.4", "task": "read_numbers(text): floats, skip bad lines", "func": read_numbers,
     "tests": [(("1\n2.5\nbad\n3",), [1.0, 2.5, 3.0]), (("x",), [])],
     "solution": sol_read_numbers},
    {"id": "12.5", "task": "safe_divide(a, b): None when b is 0", "func": safe_divide,
     "tests": [((10, 4), 2.5), ((1, 0), None)], "solution": sol_safe_divide},
    {"id": "12.6", "task": "save_and_load(text): write to a file and read it back",
     "func": save_and_load,
     "tests": [(("hello\nworld",), "hello\nworld"), (("",), "")], "solution": sol_save_and_load},
]

DEMOS = [
    ("12. File write/read", demo_write_read),
    ("13. JSON", demo_json),
    ("14. Exceptions", demo_exceptions),
    ("15. raise and custom exceptions", demo_raise),
    ("16. EAFP style", demo_eafp),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
