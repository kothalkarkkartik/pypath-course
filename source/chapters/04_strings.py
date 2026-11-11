"""
Chapter 04 - Strings (working with text)
========================================

Today's goal:
  1. Create a string, index it and slice it
  2. Important methods: upper, lower, strip, split, join, replace, find
  3. Strings are immutable (you can't change them, you build a new one)
  4. f-string formatting

Indexing (starts at 0):
  s = "Python"
  s[0] = 'P'   s[1] = 'y'   s[-1] = 'n' (the last one)

Slicing: s[start:stop:step]  (stop is NOT included)
  s[0:3] = "Pyt"    s[:3] = "Pyt"    s[3:] = "hon"
  s[::-1] = "nohtyP" (reverse)

Immutability:
  s[0] = "J"   -> TypeError!  Instead: s = "J" + s[1:]

Split and join (you will use these the most):
  "a,b,c".split(",")      -> ["a", "b", "c"]
  " ".join(["a", "b"])    -> "a b"
"""

from _kit import main


# ---------------------------------------------------------------------------
# DEMOS
# ---------------------------------------------------------------------------


def demo_index_slice() -> None:
    s = "Python"
    print("s =", s, "| length:", len(s))
    print("s[0]   =", s[0])
    print("s[-1]  =", s[-1])
    print("s[1:4] =", s[1:4])
    print("s[:3]  =", s[:3])
    print("s[3:]  =", s[3:])
    print("s[::2] =", s[::2])      # every second character
    print("s[::-1]=", s[::-1])     # reverse

    # Slicing with negative indexes
    print("s[-3:] =", s[-3:])

    # Out of range index -> error, slice -> safely empty
    try:
        print(s[100])
    except IndexError as e:
        print("IndexError:", e)
    print("s[100:] =", repr(s[100:]))

    # Membership
    print("'th' in s ->", "th" in s)
    print("'z' in s  ->", "z" in s)


def demo_immutable() -> None:
    s = "Python"
    try:
        s[0] = "J"
    except TypeError as e:
        print("TypeError:", e)
        print("Strings are immutable. Build a new string:")
    s = "J" + s[1:]
    print("new s =", s)


def demo_methods() -> None:
    text = "  Hello Python World  "
    print("original :", repr(text))
    print("strip()  :", repr(text.strip()))
    print("upper()  :", text.upper())
    print("lower()  :", text.lower())
    print("title()  :", text.title())
    print("replace():", text.replace("Python", "DSA"))
    print("count('l'):", text.count("l"))
    print("find('Py'):", text.find("Py"))
    print("find('zz'):", text.find("zz"))     # -1 means not found

    print("startswith('  He'):", text.startswith("  He"))
    print("endswith('  '):", text.endswith("  "))

    print("'123'.isdigit() :", "123".isdigit())
    print("'abc'.isalpha() :", "abc".isalpha())
    print("'  '.isspace()  :", "  ".isspace())

    print("'7'.zfill(3)    :", "7".zfill(3))   # "007"


def demo_split_join() -> None:
    line = "Ravi,21,Delhi,student"
    parts = line.split(",")
    print("split:", parts)
    print("name:", parts[0], "| age:", parts[1])

    words = "Learning Python is very easy".split()
    print("words:", words)
    print("join:", "-".join(words))
    print("join with newline:")
    print("\n".join(words))

    # Capitalise the first letter of every word
    print(" ".join(w.capitalize() for w in words))

    # strip + split = cleaning up user input
    raw = "   apple, banana ,  mango  "
    fruits = [f.strip() for f in raw.split(",")]
    print("fruits:", fruits)


def demo_formatting() -> None:
    name, marks = "Ravi", 87.5
    print(f"{name}'s marks: {marks}")
    print(f"{name:10}|")        # left
    print(f"{name:>10}|")       # right
    print(f"{marks:.2f}")
    print(f"{marks:6.1f}|")
    print(f"{'YES':^9}|")

    # Escape characters
    print("Line1\nLine2")
    print("Tab:\there")
    print("Quote: \"double\" and 'single'")
    print(r"Raw string: C:\Users\new")   # r = don't treat backslash as special


# ---------------------------------------------------------------------------
# EXERCISES
# ---------------------------------------------------------------------------


def reverse_str(s: str) -> str:
    """Reverse the string. reverse_str("abc") -> "cba" """
    # TODO: slicing [::-1]
    return None


def is_palindrome(s: str) -> bool:
    """True if it reads the same forwards and backwards (ignore case and spaces).
    is_palindrome("Madam") -> True
    is_palindrome("race car") -> True
    is_palindrome("hello") -> False
    """
    # TODO: compare with lower() + replace(" ", "") + reverse
    return None


def count_vowels(s: str) -> int:
    """How many vowels (a, e, i, o, u) there are, ignoring case.
    count_vowels("Hello World") -> 3
    """
    # TODO: use a loop or sum()
    return None


def initials(full_name: str) -> str:
    """The first letter of every word in the name, plus a dot.
    initials("Ravi Kumar Sharma") -> "R.K.S."
    """
    # TODO: split + loop
    return None


def truncate(s: str, n: int) -> str:
    """If the length is <= n, keep it as is; otherwise the first n chars + '...'.
    truncate("Python", 3) -> "Pyt..."
    truncate("Hi", 5) -> "Hi"
    """
    # TODO
    return None


def normalize_spaces(s: str) -> str:
    """Remove extra spaces and keep a single space.
    normalize_spaces("  a   b  c ") -> "a b c"
    """
    # TODO: split() + join()
    return None


# Solutions
def sol_reverse_str(s: str) -> str:
    return s[::-1]


def sol_is_palindrome(s: str) -> bool:
    cleaned = s.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


def sol_count_vowels(s: str) -> int:
    return sum(1 for ch in s.lower() if ch in "aeiou")


def sol_initials(full_name: str) -> str:
    return "".join(word[0].upper() + "." for word in full_name.split())


def sol_truncate(s: str, n: int) -> str:
    return s if len(s) <= n else s[:n] + "..."


def sol_normalize_spaces(s: str) -> str:
    return " ".join(s.split())


EXERCISES = [
    {"id": "4.1", "task": "reverse_str(s): reverse the string", "func": reverse_str,
     "tests": [(("abc",), "cba"), (("",), ""), (("a",), "a")], "solution": sol_reverse_str},
    {"id": "4.2", "task": "is_palindrome(s): ignore case and spaces", "func": is_palindrome,
     "tests": [(("Madam",), True), (("race car",), True), (("hello",), False)],
     "solution": sol_is_palindrome},
    {"id": "4.3", "task": "count_vowels(s): count the vowels", "func": count_vowels,
     "tests": [(("Hello World",), 3), (("PYTHON",), 1), (("xyz",), 0)],
     "solution": sol_count_vowels},
    {"id": "4.4", "task": "initials(name): 'Ravi Kumar' -> 'R.K.'", "func": initials,
     "tests": [(("Ravi Kumar Sharma",), "R.K.S."), (("sita",), "S.")], "solution": sol_initials},
    {"id": "4.5", "task": "truncate(s, n): add '...' if it is too long", "func": truncate,
     "tests": [(("Python", 3), "Pyt..."), (("Hi", 5), "Hi"), (("Hello", 5), "Hello")],
     "solution": sol_truncate},
    {"id": "4.6", "task": "normalize_spaces(s): remove extra spaces", "func": normalize_spaces,
     "tests": [(("  a   b  c ",), "a b c"), (("hi",), "hi")], "solution": sol_normalize_spaces},
]

DEMOS = [
    ("4. Indexing and slicing", demo_index_slice),
    ("5. Strings are immutable", demo_immutable),
    ("6. String methods", demo_methods),
    ("7. split() and join()", demo_split_join),
    ("8. Formatting and escapes", demo_formatting),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
