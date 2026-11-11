"""
Chapter 09 - Dictionaries (Key : Value)
=======================================

Today's goal:
  1. Create and access a dict
  2. get(), setdefault(), update()
  3. Loop: keys(), values(), items()
  4. The counting pattern (you will use this a lot)
  5. Nested dicts and sorting by value

Dict = key-value pairs. Curly braces {} with colons.
  student = {"name": "Ravi", "age": 21, "city": "Delhi"}

Access:
  student["name"]          -> "Ravi"  (KeyError if it is missing)
  student.get("marks")     -> None    (safe)
  student.get("marks", 0)  -> 0       (default)

Add/change:
  student["age"] = 22
  student["marks"] = 90

Loop:
  for key in student: ...
  for key, value in student.items(): ...

Remember: a dict keeps its insertion order (Python 3.7+), but you cannot access items by index.
"""

from _kit import main


# ---------------------------------------------------------------------------
# DEMOS
# ---------------------------------------------------------------------------


def demo_basics() -> None:
    student = {"name": "Ravi", "age": 21, "city": "Delhi"}
    print("student:", student)
    print("name:", student["name"])
    print("keys:", list(student.keys()))
    print("values:", list(student.values()))
    print("items:", list(student.items()))

    # Safe access
    print("marks (get):", student.get("marks"))
    print("marks (default):", student.get("marks", 0))

    try:
        print(student["marks"])
    except KeyError as e:
        print("KeyError:", e)

    # Add / update
    student["age"] = 22
    student["marks"] = 90
    print("updated:", student)

    # Delete
    del student["city"]
    print("del city:", student)
    marks = student.pop("marks")
    print("pop marks:", marks, "| remaining:", student)

    # Membership checks the key, not the value
    print("'name' in student:", "name" in student)
    print("'Ravi' in student:", "Ravi" in student)   # not by value

    # Length
    print("len:", len(student))


def demo_loop() -> None:
    marks = {"math": 90, "science": 85, "english": 78}

    print("keys:")
    for subject in marks:
        print(" ", subject)

    print("values:")
    for score in marks.values():
        print(" ", score)

    print("items:")
    for subject, score in marks.items():
        print(f"  {subject}: {score}")

    # Total and average
    total = sum(marks.values())
    print("total:", total, "| average:", total / len(marks))

    # Highest marks
    topper = max(marks, key=marks.get)
    print("topper subject:", topper, marks[topper])


def demo_counting() -> None:
    text = "apple banana apple cherry banana apple"
    counts = {}

    for word in text.split():
        counts[word] = counts.get(word, 0) + 1

    print("counts:", counts)

    # The same idea with setdefault
    groups = {}
    for word in text.split():
        groups.setdefault(word[0], []).append(word)
    print("first letter groups:", groups)

    # Sorted by value (descending)
    top = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    print("sorted by count:", top)


def demo_nested() -> None:
    class_room = {
        "Ravi": {"age": 21, "marks": 90},
        "Sita": {"age": 20, "marks": 95},
    }

    print("Ravi's marks:", class_room["Ravi"]["marks"])

    for name, info in class_room.items():
        print(f"{name}: age {info['age']}, marks {info['marks']}")

    # Nested update
    class_room["Ravi"]["marks"] = 92
    print("updated Ravi:", class_room["Ravi"])

    # Merge (Python 3.9+)
    a = {"x": 1, "y": 2}
    b = {"y": 3, "z": 4}
    print("a | b:", a | b)        # b's value wins

    # The same with update()
    a.update(b)
    print("a.update(b):", a)


def demo_sorting() -> None:
    prices = {"pen": 10, "book": 120, "bag": 500, "pencil": 5}

    print("sorted by key:", dict(sorted(prices.items())))
    print("sorted by value:", dict(sorted(prices.items(), key=lambda kv: kv[1])))
    print("top 2:", sorted(prices, key=prices.get, reverse=True)[:2])

    # Swap keys and values (if the values are unique)
    swapped = {v: k for k, v in prices.items()}
    print("swapped:", swapped)


# ---------------------------------------------------------------------------
# EXERCISES
# ---------------------------------------------------------------------------


def word_count(text: str) -> dict:
    """Count how often each word appears.
    word_count("a b a") -> {"a": 2, "b": 1}
    Lowercase the text first, then split it.
    """
    # TODO: counts.get(word, 0) + 1
    return None


def invert(d: dict) -> dict:
    """Swap keys and values.
    invert({"a": 1, "b": 2}) -> {1: "a", 2: "b"}
    """
    # TODO: dict comprehension
    return None


def merge_sum(a: dict, b: dict) -> dict:
    """Merge both dicts; ADD the values of keys that appear in both.
    merge_sum({"x": 1, "y": 2}, {"y": 3, "z": 4}) -> {"x": 1, "y": 5, "z": 4}
    """
    # TODO: make a copy, then loop
    return None


def group_by_first(words: list) -> dict:
    """Group words by their first letter (uppercase).
    group_by_first(["apple", "avocado", "banana"]) -> {"A": ["apple", "avocado"], "B": ["banana"]}
    """
    # TODO: setdefault or get
    return None


def top_n(d: dict, n: int) -> list:
    """Top n keys by value, highest first; break ties alphabetically by key.
    top_n({"a": 3, "b": 3, "c": 1}, 2) -> ["a", "b"]
    """
    # TODO: use a tuple key in sorted(d, key=...)
    return None


def has_duplicate_values(d: dict) -> bool:
    """Return True if any value appears more than once.
    has_duplicate_values({"a": 1, "b": 2, "c": 1}) -> True
    """
    # TODO: len(values) vs len(set(values))
    return None


# Solutions
def sol_word_count(text: str) -> dict:
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def sol_invert(d: dict) -> dict:
    return {v: k for k, v in d.items()}


def sol_merge_sum(a: dict, b: dict) -> dict:
    result = dict(a)
    for key, value in b.items():
        result[key] = result.get(key, 0) + value
    return result


def sol_group_by_first(words: list) -> dict:
    groups = {}
    for word in words:
        groups.setdefault(word[0].upper(), []).append(word)
    return groups


def sol_top_n(d: dict, n: int) -> list:
    return sorted(d, key=lambda k: (-d[k], k))[:n]


def sol_has_duplicate_values(d: dict) -> bool:
    values = list(d.values())
    return len(values) != len(set(values))


EXERCISES = [
    {"id": "9.1", "task": "word_count(text): count how often each word appears", "func": word_count,
     "tests": [(("a b a",), {"a": 2, "b": 1}), (("Hi hi",), {"hi": 2})],
     "solution": sol_word_count},
    {"id": "9.2", "task": "invert(d): swap keys and values", "func": invert,
     "tests": [(({"a": 1, "b": 2},), {1: "a", 2: "b"})], "solution": sol_invert},
    {"id": "9.3", "task": "merge_sum(a, b): add the values of common keys", "func": merge_sum,
     "tests": [(({"x": 1, "y": 2}, {"y": 3, "z": 4}), {"x": 1, "y": 5, "z": 4})],
     "solution": sol_merge_sum},
    {"id": "9.4", "task": "group_by_first(words): group by first letter", "func": group_by_first,
     "tests": [((["apple", "avocado", "banana"],),
                {"A": ["apple", "avocado"], "B": ["banana"]})],
     "solution": sol_group_by_first},
    {"id": "9.5", "task": "top_n(d, n): top keys by value, ties by name", "func": top_n,
     "tests": [(({"a": 3, "b": 3, "c": 1}, 2), ["a", "b"]),
               (({"x": 1}, 5), ["x"])], "solution": sol_top_n},
    {"id": "9.6", "task": "has_duplicate_values(d): any repeated value?", "func": has_duplicate_values,
     "tests": [(({"a": 1, "b": 2, "c": 1},), True), (({"a": 1, "b": 2},), False)],
     "solution": sol_has_duplicate_values},
]

DEMOS = [
    ("9. Dict basics", demo_basics),
    ("10. Loops and calculations", demo_loop),
    ("11. Counting pattern", demo_counting),
    ("12. Nested dicts and merge", demo_nested),
    ("13. Sorting", demo_sorting),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
