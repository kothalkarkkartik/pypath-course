"""
Chapter 16 - Standard Library, Testing and Debugging
====================================================

Today's goal:
  1. collections: Counter, defaultdict, deque
  2. itertools: combinations, chain
  3. re (regular expressions) basics
  4. logging
  5. Testing with unittest
  6. How to debug

Python comes with "batteries included". No install needed for:
  math, random, datetime, json, csv, pathlib, os, sys, re, collections,
  itertools, functools, statistics, unittest, logging, sqlite3, urllib...

Why testing?
  To check that old features didn't break after you changed the code.
  pytest is the most popular: pip install pytest
  unittest is built into the standard library.

Debugging:
  1. print() - the simplest
  2. assert - check an assumption
  3. breakpoint() - the code pauses and pdb opens
     commands: n (next), s (step), c (continue), p variable, q (quit)
  4. Run and Debug in VS Code (F5), set a breakpoint
"""

import calendar
import json
import logging
import re
import unittest
from collections import Counter, defaultdict, deque
from itertools import chain, combinations

from _kit import main


# ---------------------------------------------------------------------------
# DEMOS
# ---------------------------------------------------------------------------


def demo_collections() -> None:
    # Counter - the counting master
    words = "apple banana apple cherry banana apple".split()
    counts = Counter(words)
    print("Counter:", counts)
    print("apple:", counts["apple"])
    print("most_common(2):", counts.most_common(2))
    print("total items:", sum(counts.values()))

    # Arithmetic on Counters
    c1 = Counter(a=3, b=1)
    c2 = Counter(a=1, b=2)
    print("c1 + c2:", c1 + c2)
    print("c1 - c2:", c1 - c2)

    # defaultdict - a default for missing keys
    groups = defaultdict(list)
    for word in words:
        groups[word[0]].append(word)
    print("defaultdict:", dict(groups))

    # deque - fast add/remove on both ends
    dq = deque([1, 2, 3])
    dq.append(4)          # right
    dq.appendleft(0)      # left
    print("deque:", dq)
    print("pop:", dq.pop(), "| popleft:", dq.popleft())
    dq.rotate(1)
    print("rotate(1):", dq)


def demo_itertools() -> None:
    nums = [1, 2, 3]
    print("combinations:", list(combinations(nums, 2)))
    print("chain:", list(chain([1, 2], [3, 4])))
    print("chain.from_iterable:", list(chain.from_iterable([[1, 2], [3]])))

    # Infinite iterators (limit them with islice)
    from itertools import count, islice
    print("count:", list(islice(count(10, 2), 5)))

    # groupby - you must sort first
    from itertools import groupby
    data = [("A", 1), ("A", 2), ("B", 3)]
    for key, group in groupby(data, key=lambda x: x[0]):
        print(key, list(group))


def demo_regex() -> None:
    text = "Contact: ravi@example.com, sita@test.co.in"

    emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text)
    print("emails:", emails)

    print("match:", bool(re.match(r"^\d{3}-\d{4}$", "123-4567")))
    print("wrong match:", bool(re.match(r"^\d{3}-\d{4}$", "12-4567")))

    print("sub:", re.sub(r"\d+", "#", "a1 b22 c333"))

    m = re.search(r"(\d{3})-(\d{4})", "Call 123-4567 now")
    if m:
        print("search groups:", m.group(0), m.group(1), m.group(2))

    # Common patterns:
    # \d digit, \w letter/digit/_, \s space
    # + one or more, * zero or more, ? optional
    # ^ start, $ end, [] character set


def demo_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    logging.debug("This is debug (it won't show at INFO level)")
    logging.info("The program started")
    logging.warning("This is a warning")
    logging.error("This is an error")

    logger = logging.getLogger("my_logger")
    logger.info("You can also create a separate logger")


def demo_unittest() -> None:
    def add(a, b):
        return a + b

    def is_even(n):
        return n % 2 == 0

    class TestHelpers(unittest.TestCase):
        def test_add(self):
            self.assertEqual(add(2, 3), 5)

        def test_add_negative(self):
            self.assertEqual(add(-1, 1), 0)

        def test_is_even(self):
            self.assertTrue(is_even(4))
            self.assertFalse(is_even(7))

        def test_error(self):
            with self.assertRaises(ZeroDivisionError):
                1 / 0

    suite = unittest.TestLoader().loadTestsFromTestCase(TestHelpers)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print("tests run:", result.testsRun, "| failures:", len(result.failures))

    # Assertions to remember:
    # assertEqual, assertTrue, assertFalse, assertIn,
    # assertRaises, assertAlmostEqual


def demo_debug_tips() -> None:
    # 1) print debugging
    def buggy_average(nums):
        print("  [debug] nums:", nums)
        total = sum(nums)
        print("  [debug] total:", total)
        return total / len(nums)

    print("average:", buggy_average([1, 2, 3]))

    # 2) assert
    def apply_discount(price, percent):
        assert 0 <= percent <= 100, "percent must be between 0 and 100"
        return price * (1 - percent / 100)

    print("discount:", apply_discount(100, 20))
    try:
        apply_discount(100, 150)
    except AssertionError as e:
        print("AssertionError:", e)

    # 3) breakpoint() - we are not auto-running it here
    #    Put breakpoint() in your own file, then in the terminal:
    #    n = next line, s = step into, c = continue, p x = print x, q = quit

    # 4) Read the traceback: from bottom to top, the real line is at the bottom
    print("Tip: when you get an error, read the LAST line of the traceback first.")


# ---------------------------------------------------------------------------
# EXERCISES
# ---------------------------------------------------------------------------


def top_counts(words: list, n: int) -> list:
    """Top n (word, count) tuples using Counter.most_common.
    top_counts(["a", "b", "a"], 2) -> [("a", 2), ("b", 1)]
    """
    # TODO
    return None


def all_pairs(nums: list) -> list:
    """A list of all unique pairs (combinations).
    all_pairs([1, 2, 3]) -> [(1, 2), (1, 3), (2, 3)]
    """
    # TODO: itertools.combinations
    return None


def days_in_month(year: int, month: int) -> int:
    """The number of days using calendar.monthrange(year, month)[1].
    days_in_month(2024, 2) -> 29
    """
    # TODO
    return None


def is_valid_email(email: str) -> bool:
    """Simple email check: something@something.something (domain of 2+ letters).
    is_valid_email("ravi@example.com") -> True
    is_valid_email("ravi@com") -> False
    """
    # TODO: re.fullmatch
    return None


def safe_json_loads(text: str):
    """Parse JSON; return None if it is invalid."""
    # TODO: try/except json.JSONDecodeError
    return None


def slugify(text: str) -> str:
    """Lowercase, turn non-alphanumeric characters into '-', remove extra '-'.
    slugify("Hello World!") -> "hello-world"
    slugify("  Python 3.12 ") -> "python-3-12"
    """
    # TODO: lower, re.sub, strip("-")
    return None


# Solutions
def sol_top_counts(words: list, n: int) -> list:
    return Counter(words).most_common(n)


def sol_all_pairs(nums: list) -> list:
    return list(combinations(nums, 2))


def sol_days_in_month(year: int, month: int) -> int:
    return calendar.monthrange(year, month)[1]


def sol_is_valid_email(email: str) -> bool:
    pattern = r"[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}"
    return re.fullmatch(pattern, email) is not None


def sol_safe_json_loads(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def sol_slugify(text: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", text.lower())
    return cleaned.strip("-")


EXERCISES = [
    {"id": "16.1", "task": "top_counts(words, n): Counter.most_common", "func": top_counts,
     "tests": [((["a", "b", "a"], 2), [("a", 2), ("b", 1)])], "solution": sol_top_counts},
    {"id": "16.2", "task": "all_pairs(nums): combinations", "func": all_pairs,
     "tests": [(([1, 2, 3],), [(1, 2), (1, 3), (2, 3)])], "solution": sol_all_pairs},
    {"id": "16.3", "task": "days_in_month(year, month)", "func": days_in_month,
     "tests": [((2024, 2), 29), ((2023, 2), 28), ((2026, 11), 30)],
     "solution": sol_days_in_month},
    {"id": "16.4", "task": "is_valid_email(email): regex check", "func": is_valid_email,
     "tests": [(("ravi@example.com",), True), (("ravi@com",), False),
               (("bad",), False)], "solution": sol_is_valid_email},
    {"id": "16.5", "task": "safe_json_loads(text): None for invalid JSON", "func": safe_json_loads,
     "tests": [(('{"a": 1}',), {"a": 1}), (("{bad}",), None)], "solution": sol_safe_json_loads},
    {"id": "16.6", "task": "slugify(text): URL-friendly string", "func": slugify,
     "tests": [(("Hello World!",), "hello-world"), (("  Python 3.12 ",), "python-3-12")],
     "solution": sol_slugify},
]

DEMOS = [
    ("16. collections", demo_collections),
    ("17. itertools", demo_itertools),
    ("18. Regular expressions", demo_regex),
    ("19. logging", demo_logging),
    ("20. unittest", demo_unittest),
    ("21. Debugging tips", demo_debug_tips),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
