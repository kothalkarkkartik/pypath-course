"""
DSA 01 - Patterns with loops
============================

Today's goal:
  1. See how nested loops print shapes
  2. Learn the 5 patterns every interview asks first
  3. Dry run a pattern on paper before writing it

Why patterns first?
  - They teach you nested loops properly.
  - Every pattern is a loop inside a loop.
  - The thinking pattern (rows, columns, values) is the same everywhere.

The 3 questions to ask for any pattern:
  1. How many rows?      -> the outer loop
  2. What is in a row?   -> the inner loop
  3. What changes?       -> the number of spaces, stars or values

The shape of the code:
```python
for row in range(rows):
    for col in range(columns):
        print("*", end="")
    print()          # this moves to the next line
```

`end=""` tells print not to add a new line. Without it every star would be
on its own line.

Tip: write the row number on paper first.
  row 0 -> 1 star
  row 1 -> 2 stars
  row 2 -> 3 stars
Then the code becomes obvious.
"""

from _dsa_kit import main


# ---------------------------------------------------------------------------
# DEMOS - run these first, then change the code and experiment
# ---------------------------------------------------------------------------


def demo_star_triangle() -> None:
    # The simplest pattern: 1 star, then 2, then 3...
    n = 5
    for row in range(n):
        for col in range(row + 1):
            print("*", end="")
        print()


def demo_inverted_triangle() -> None:
    # Same loop, but the inner loop shrinks.
    n = 5
    for row in range(n):
        for col in range(n - row):
            print("*", end="")
        print()


def demo_number_triangle() -> None:
    # The value depends on the column, not just a star.
    n = 5
    for row in range(n):
        for col in range(row + 1):
            print(col + 1, end=" ")
        print()


def demo_pyramid_with_spaces() -> None:
    # A real pyramid: spaces decrease, stars increase.
    n = 5
    for row in range(n):
        spaces = n - row - 1
        stars = row * 2 + 1
        print(" " * spaces + "*" * stars)


def demo_diamond() -> None:
    # Two triangles stuck together: up then down.
    n = 5
    for row in range(n):
        print(" " * (n - row - 1) + "*" * (row * 2 + 1))
    for row in range(n - 2, -1, -1):
        print(" " * (n - row - 1) + "*" * (row * 2 + 1))


def demo_dry_run() -> None:
    # Print the row numbers first. This is how you plan a pattern.
    n = 4
    print("row | stars")
    for row in range(n):
        print(row, "  |", "*" * (row + 1))


# ---------------------------------------------------------------------------
# EXERCISES - write your code where you see TODO
# ---------------------------------------------------------------------------


def star_triangle(n: int) -> list:
    """Return n rows of stars, growing by one each row.

    star_triangle(3) -> ["*", "**", "***"]
    """
    # TODO: build the list of rows
    return []


def inverted_triangle(n: int) -> list:
    """Return n rows of stars, shrinking by one each row.

    inverted_triangle(3) -> ["***", "**", "*"]
    """
    # TODO: build the list of rows
    return []


def number_triangle(n: int) -> list:
    """Return rows of numbers, each row one longer.

    number_triangle(3) -> ["1", "1 2", "1 2 3"]
    """
    # TODO: build the list of rows
    return []


def letter_triangle(n: int) -> list:
    """Return rows of letters, each row one longer.

    letter_triangle(3) -> ["A", "A B", "A B C"]
    """
    # TODO: build the list of rows
    return []


def hollow_triangle(n: int) -> list:
    """Return a triangle outline. Only the border has stars.

    hollow_triangle(3) -> ["*", "* *", "*   *"]
    """
    # TODO: build the list of rows
    return []


def diamond(n: int) -> list:
    """Return a diamond of stars made of 2 * n - 1 rows.

    diamond(2) -> [" *", "***", " *"]
    """
    # TODO: build the list of rows
    return []


# Solutions - try it yourself first, then run with `--solutions`
def sol_star_triangle(n: int) -> list:
    return ["*" * (row + 1) for row in range(n)]


def sol_inverted_triangle(n: int) -> list:
    return ["*" * (n - row) for row in range(n)]


def sol_number_triangle(n: int) -> list:
    return [" ".join(str(col + 1) for col in range(row + 1)) for row in range(n)]


def sol_letter_triangle(n: int) -> list:
    rows = []
    for row in range(n):
        rows.append(" ".join(chr(ord("A") + col) for col in range(row + 1)))
    return rows


def sol_hollow_triangle(n: int) -> list:
    rows = []
    for row in range(n):
        if row == 0:
            rows.append("*")
        else:
            rows.append("*" + " " * (row * 2 - 1) + "*")
    return rows


def sol_diamond(n: int) -> list:
    rows = []
    for row in range(n):
        rows.append(" " * (n - row - 1) + "*" * (row * 2 + 1))
    for row in range(n - 2, -1, -1):
        rows.append(" " * (n - row - 1) + "*" * (row * 2 + 1))
    return rows


EXERCISES = [
    {
        "id": "1.1",
        "task": "star_triangle(n): rows of stars that grow by one",
        "func": star_triangle,
        "tests": [((3,), ["*", "**", "***"]), ((1,), ["*"])],
        "solution": sol_star_triangle,
    },
    {
        "id": "1.2",
        "task": "inverted_triangle(n): rows of stars that shrink by one",
        "func": inverted_triangle,
        "tests": [((3,), ["***", "**", "*"]), ((2,), ["**", "*"])],
        "solution": sol_inverted_triangle,
    },
    {
        "id": "1.3",
        "task": "number_triangle(n): rows of numbers, each row one longer",
        "func": number_triangle,
        "tests": [((3,), ["1", "1 2", "1 2 3"]), ((1,), ["1"])],
        "solution": sol_number_triangle,
    },
    {
        "id": "1.4",
        "task": "letter_triangle(n): rows of letters A, B, C...",
        "func": letter_triangle,
        "tests": [((3,), ["A", "A B", "A B C"]), ((2,), ["A", "A B"])],
        "solution": sol_letter_triangle,
    },
    {
        "id": "1.5",
        "task": "hollow_triangle(n): triangle outline only",
        "func": hollow_triangle,
        "tests": [((3,), ["*", "* *", "*   *"]), ((4,), ["*", "* *", "*   *", "*     *"])],
        "solution": sol_hollow_triangle,
    },
    {
        "id": "1.6",
        "task": "diamond(n): 2*n-1 rows of stars",
        "func": diamond,
        "tests": [((2,), [" *", "***", " *"]), ((1,), ["*"])],
        "solution": sol_diamond,
    },
]

DEMOS = [
    ("1. Star triangle", demo_star_triangle),
    ("2. Inverted triangle", demo_inverted_triangle),
    ("3. Number triangle", demo_number_triangle),
    ("4. Pyramid with spaces", demo_pyramid_with_spaces),
    ("5. Diamond", demo_diamond),
    ("6. Dry run on paper", demo_dry_run),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
