"""
Chapter 11 - Comprehensions (Shorter, faster code)
==================================================

Today's goal:
  1. List comprehension
  2. Comprehension with a condition (filter)
  3. Comprehension with if-else (transform)
  4. Dict and set comprehension
  5. Generator expressions and any/all

List comprehension:
  [expr for item in iterable]
  [expr for item in iterable if condition]
  [expr_if_true if condition else expr_if_false for item in iterable]

Examples:
  [n * n for n in range(5)]            -> [0, 1, 4, 9, 16]
  [n for n in range(10) if n % 2 == 0] -> [0, 2, 4, 6, 8]
  ["even" if n % 2 == 0 else "odd" for n in range(3)]

Dict comprehension:
  {k: v for k, v in pairs}

Set comprehension:
  {n % 3 for n in range(10)}

Generator expression (lazy, memory efficient):
  (n * n for n in range(1000000))
  sum(n * n for n in range(100))
"""

from _kit import main


# ---------------------------------------------------------------------------
# DEMOS
# ---------------------------------------------------------------------------


def demo_list_comp() -> None:
    squares = [n * n for n in range(1, 6)]
    print("squares:", squares)

    evens = [n for n in range(10) if n % 2 == 0]
    print("evens:", evens)

    # if-else (transform)
    labels = ["even" if n % 2 == 0 else "odd" for n in range(5)]
    print("labels:", labels)

    # On a string
    upper = [ch.upper() for ch in "hello"]
    print("upper chars:", upper)

    # Nested loop
    pairs = [(x, y) for x in range(2) for y in range(2)]
    print("pairs:", pairs)

    # Flatten a nested list (matrix)
    matrix = [[1, 2], [3, 4]]
    flat = [n for row in matrix for n in row]
    print("flat:", flat)

    # Condition + expression
    nums = [1, -2, 3, -4]
    positive_squares = [n * n for n in nums if n > 0]
    print("positive squares:", positive_squares)

    # Walrus operator (Python 3.8+) - advanced
    values = [y for x in range(6) if (y := x * 2) > 4]
    print("walrus:", values)


def demo_dict_set_comp() -> None:
    words = ["apple", "banana", "kiwi"]
    lengths = {word: len(word) for word in words}
    print("lengths:", lengths)

    # Condition
    long_words = {word: len(word) for word in words if len(word) > 4}
    print("long words:", long_words)

    # Swap keys and values
    prices = {"pen": 10, "book": 120}
    print("swapped:", {v: k for k, v in prices.items()})

    # Set comprehension
    remainders = {n % 3 for n in range(10)}
    print("remainders:", remainders)

    # Unique first letters
    print("first letters:", {w[0].upper() for w in words})


def demo_generator_expr() -> None:
    # Generator expression - parentheses instead of brackets
    gen = (n * n for n in range(5))
    print("gen type:", type(gen).__name__)
    print("next:", next(gen))
    print("next:", next(gen))
    print("rest:", list(gen))

    # Memory efficient sum
    print("sum of squares 1..100:", sum(n * n for n in range(1, 101)))

    # any / all
    nums = [2, 4, 6]
    print("all even:", all(n % 2 == 0 for n in nums))
    print("any odd:", any(n % 2 != 0 for n in nums))
    print("any negative:", any(n < 0 for n in nums))


def demo_practical() -> None:
    # Data like a CSV file
    rows = [
        {"name": "Ravi", "marks": 90},
        {"name": "Sita", "marks": 95},
        {"name": "Amit", "marks": 60},
    ]

    names = [r["name"] for r in rows]
    print("names:", names)

    toppers = [r["name"] for r in rows if r["marks"] >= 90]
    print("toppers:", toppers)

    average = sum(r["marks"] for r in rows) / len(rows)
    print("average:", average)

    # Matrix transpose
    matrix = [[1, 2, 3], [4, 5, 6]]
    transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
    print("transposed:", transposed)

    # Comprehension vs loop
    result_loop = []
    for n in range(5):
        if n % 2 == 0:
            result_loop.append(n * 10)
    result_comp = [n * 10 for n in range(5) if n % 2 == 0]
    print("loop:", result_loop, "| comp:", result_comp)


# ---------------------------------------------------------------------------
# EXERCISES
# ---------------------------------------------------------------------------


def evens_squared(nums: list) -> list:
    """Square only the even numbers, using a list comprehension.
    evens_squared([1, 2, 3, 4]) -> [4, 16]
    """
    # TODO
    return None


def lengths(words: list) -> list:
    """A list with the length of each word.
    lengths(["hi", "hello"]) -> [2, 5]
    """
    # TODO
    return None


def word_lengths(words: list) -> dict:
    """A {word: length} dict, using a dict comprehension."""
    # TODO
    return None


def transpose(matrix: list) -> list:
    """Transpose the matrix.
    transpose([[1, 2], [3, 4]]) -> [[1, 3], [2, 4]]
    """
    # TODO
    return None


def flatten(matrix: list) -> list:
    """Flatten a nested list, using a comprehension."""
    # TODO
    return None


def filter_words(words: list, min_len: int) -> list:
    """Only the words whose length is at least min_len.
    filter_words(["a", "abc", "abcde"], 3) -> ["abc", "abcde"]
    """
    # TODO
    return None


# Solutions
def sol_evens_squared(nums: list) -> list:
    return [n * n for n in nums if n % 2 == 0]


def sol_lengths(words: list) -> list:
    return [len(w) for w in words]


def sol_word_lengths(words: list) -> dict:
    return {w: len(w) for w in words}


def sol_transpose(matrix: list) -> list:
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]


def sol_flatten(matrix: list) -> list:
    return [n for row in matrix for n in row]


def sol_filter_words(words: list, min_len: int) -> list:
    return [w for w in words if len(w) >= min_len]


EXERCISES = [
    {"id": "11.1", "task": "evens_squared(nums): square of the evens", "func": evens_squared,
     "tests": [(([1, 2, 3, 4],), [4, 16]), (([1, 3],), [])], "solution": sol_evens_squared},
    {"id": "11.2", "task": "lengths(words): length of each word", "func": lengths,
     "tests": [((["hi", "hello"],), [2, 5])], "solution": sol_lengths},
    {"id": "11.3", "task": "word_lengths(words): dict comprehension", "func": word_lengths,
     "tests": [((["hi", "hello"],), {"hi": 2, "hello": 5})], "solution": sol_word_lengths},
    {"id": "11.4", "task": "transpose(matrix): rows <-> columns", "func": transpose,
     "tests": [(([[1, 2], [3, 4]],), [[1, 3], [2, 4]])], "solution": sol_transpose},
    {"id": "11.5", "task": "flatten(matrix): nested to flat", "func": flatten,
     "tests": [(([[1, 2], [3, 4]],), [1, 2, 3, 4])], "solution": sol_flatten},
    {"id": "11.6", "task": "filter_words(words, min_len)", "func": filter_words,
     "tests": [((["a", "abc", "abcde"], 3), ["abc", "abcde"])], "solution": sol_filter_words},
]

DEMOS = [
    ("11. List comprehension", demo_list_comp),
    ("12. Dict and set comprehension", demo_dict_set_comp),
    ("13. Generator expressions, any/all", demo_generator_expr),
    ("14. Practical examples", demo_practical),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
