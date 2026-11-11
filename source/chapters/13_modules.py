"""
Chapter 13 - Modules, Packages, pip and venv
============================================

Today's goal:
  1. The 4 ways to import
  2. Useful modules from the standard library
  3. Making your own module and what __name__ means
  4. Installing packages with pip
  5. Why venv (virtual environment) matters

Import styles:
  import math                 -> math.sqrt(16)
  from math import sqrt       -> sqrt(16)
  from math import sqrt as s  -> s(16)
  import numpy as np          -> np.array(...)

__name__:
  When the file runs directly -> __name__ == "__main__"
  When the file is imported   -> __name__ == the module's name
  That is why we keep test/demo code inside `if __name__ == "__main__":`.

pip and venv (in the terminal):
  python -m venv .venv                 # create a virtual environment
  .venv\\Scripts\\activate               # activate it on Windows
  pip install requests                 # install a package
  pip freeze > requirements.txt        # save the list
  pip install -r requirements.txt      # install from the list
  deactivate                           # turn it off

Why venv? Keep each project's packages separate, so your system stays clean.
"""

import math
import platform
import random
import statistics
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

from _kit import main


# ---------------------------------------------------------------------------
# DEMOS
# ---------------------------------------------------------------------------


def demo_math() -> None:
    print("pi:", math.pi)
    print("sqrt(16):", math.sqrt(16))
    print("floor(3.7):", math.floor(3.7), "| ceil(3.1):", math.ceil(3.1))
    print("gcd(12, 18):", math.gcd(12, 18))
    print("factorial(5):", math.factorial(5))
    print("isclose(0.1+0.2, 0.3):", math.isclose(0.1 + 0.2, 0.3))
    print("inf:", math.inf, "| -inf:", -math.inf)


def demo_random() -> None:
    # Seed = get the same "random" sequence again (handy for testing)
    rng = random.Random(42)
    print("randint(1, 6):", rng.randint(1, 6))
    print("choice:", rng.choice(["rock", "paper", "scissors"]))
    print("sample:", rng.sample(range(1, 50), 5))
    print("shuffle:")
    cards = [1, 2, 3, 4, 5]
    rng.shuffle(cards)
    print(" ", cards)
    print("uniform(0, 1):", round(rng.uniform(0, 1), 3))

    # Global random module
    print("random():", round(random.random(), 3))


def demo_datetime() -> None:
    today = date.today()
    print("today:", today)
    print("year/month/day:", today.year, today.month, today.day)

    now = datetime.now()
    print("now:", now.strftime("%d-%m-%Y %H:%M"))

    # String <-> date
    d = datetime.strptime("2026-11-10", "%Y-%m-%d").date()
    print("parsed:", d)

    # Date math
    print("7 days later:", d + timedelta(days=7))
    print("2 weeks earlier:", d - timedelta(weeks=2))
    print("difference:", (date(2026, 12, 31) - d).days, "days")

    # Format
    print("formatted:", d.strftime("%d %b %Y (%A)"))


def demo_pathlib() -> None:
    here = Path(__file__)
    print("file:", here.name)
    print("folder:", here.parent.name)
    print("suffix:", here.suffix)
    print("absolute:", here.resolve())

    # Path join (works on both Windows and Unix)
    data_file = here.parent.parent / "data" / "notes.txt"
    print("joined path:", data_file)

    # Home directory
    print("home:", Path.home())


def demo_statistics() -> None:
    nums = [4, 8, 6, 5, 9, 2]
    print("mean:", statistics.mean(nums))
    print("median:", statistics.median(nums))
    print("mode:", statistics.mode([1, 2, 2, 3]))
    print("stdev:", round(statistics.stdev(nums), 3))


def demo_name_and_platform() -> None:
    print("__name__:", __name__)
    print("Python version:", sys.version.split()[0])
    print("platform:", platform.system(), platform.release())
    print("executable:", sys.executable)

    # sys.argv - command line arguments
    print("argv:", sys.argv)


def demo_own_module() -> None:
    # Demo of making your own module - we write it in a temp folder and import it
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "greetings.py"
        path.write_text(
            'def hello(name):\n'
            '    return f"Hello {name}"\n'
            '\n'
            'if __name__ == "__main__":\n'
            '    print("the module ran directly")\n',
            encoding="utf-8",
        )

        sys.path.insert(0, tmp)
        try:
            import greetings
            print("imported:", greetings.hello("Ravi"))
            print("module's __name__:", greetings.__name__)
        finally:
            sys.path.remove(tmp)
            sys.modules.pop("greetings", None)


# ---------------------------------------------------------------------------
# EXERCISES
# ---------------------------------------------------------------------------


def circle_area(radius: float) -> float:
    """Area using math.pi, rounded to 2 decimals.
    circle_area(1) -> 3.14
    """
    # TODO
    return None


def gcd_all(nums: list) -> int:
    """GCD of all the numbers (math.gcd in a loop).
    gcd_all([12, 18, 24]) -> 6
    """
    # TODO
    return None


def days_between(start_iso: str, end_iso: str) -> int:
    """Number of days between two ISO dates ("YYYY-MM-DD").
    days_between("2024-01-01", "2024-01-31") -> 30
    """
    # TODO: date.fromisoformat
    return None


def file_stem(path: str) -> str:
    """The file name without its extension.
    file_stem("C:/data/report.csv") -> "report"
    """
    # TODO: Path(path).stem
    return None


def format_date(iso: str) -> str:
    """'2026-11-10' -> '10 Nov 2026'
    """
    # TODO: strptime + month list
    return None


def median(nums: list) -> float:
    """Use statistics.median."""
    # TODO
    return None


# Solutions
def sol_circle_area(radius: float) -> float:
    return round(math.pi * radius ** 2, 2)


def sol_gcd_all(nums: list) -> int:
    result = 0
    for n in nums:
        result = math.gcd(result, n)
    return result


def sol_days_between(start_iso: str, end_iso: str) -> int:
    start = date.fromisoformat(start_iso)
    end = date.fromisoformat(end_iso)
    return (end - start).days


def sol_file_stem(path: str) -> str:
    return Path(path).stem


MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def sol_format_date(iso: str) -> str:
    d = datetime.strptime(iso, "%Y-%m-%d").date()
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def sol_median(nums: list) -> float:
    return statistics.median(nums)


EXERCISES = [
    {"id": "13.1", "task": "circle_area(r): pi*r^2, 2 decimals", "func": circle_area,
     "tests": [((1,), 3.14), ((2,), 12.57)], "solution": sol_circle_area},
    {"id": "13.2", "task": "gcd_all(nums): GCD of them all", "func": gcd_all,
     "tests": [(([12, 18, 24],), 6), (([7],), 7)], "solution": sol_gcd_all},
    {"id": "13.3", "task": "days_between(a, b): difference between ISO dates", "func": days_between,
     "tests": [(("2024-01-01", "2024-01-31"), 30), (("2026-11-10", "2026-11-10"), 0)],
     "solution": sol_days_between},
    {"id": "13.4", "task": "file_stem(path): name without extension", "func": file_stem,
     "tests": [(("C:/data/report.csv",), "report"), (("notes.txt",), "notes")],
     "solution": sol_file_stem},
    {"id": "13.5", "task": "format_date(iso): '10 Nov 2026'", "func": format_date,
     "tests": [(("2026-11-10",), "10 Nov 2026"), (("2024-01-05",), "5 Jan 2024")],
     "solution": sol_format_date},
    {"id": "13.6", "task": "median(nums): statistics.median", "func": median,
     "tests": [(([1, 3, 2],), 2), (([1, 2, 3, 4],), 2.5)], "solution": sol_median},
]

DEMOS = [
    ("13. math", demo_math),
    ("14. random", demo_random),
    ("15. datetime", demo_datetime),
    ("16. pathlib", demo_pathlib),
    ("17. statistics", demo_statistics),
    ("18. __name__, sys, platform", demo_name_and_platform),
    ("19. Importing your own module", demo_own_module),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
