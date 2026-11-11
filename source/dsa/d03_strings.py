"""
DSA 03 - Strings and string algorithms
======================================

Today's goal:
  1. Treat a string as a row of single characters
  2. Count how many times each character appears
  3. Check if a word reads the same backwards
  4. Check if two words are made of the same letters
  5. Reverse the order of the words in a sentence
  6. Find the longest word in a sentence
  7. Find the first character that does not repeat

What is a string?
  A string is just text. In Python it is written inside quotes:

    name = "Ravi"

  You can pick one character out of it with the square brackets:

    name[0]    -> "R"    the first letter
    name[-1]   -> "i"    the last letter
    name[1:4]  -> "avi"  a slice, index 1 up to index 3

  Strings are immutable: you cannot change a letter inside one.
  To change it you build a brand new string.

Three string tools worth remembering:
  1. `s.lower()` and `s.upper()`  -> change the case
  2. `s.split()`                  -> cut a sentence into a list of words
  3. `s.replace(a, b)`            -> swap one piece of text for another

The counting pattern:
```python
counts = {}
for letter in s:
    counts[letter] = counts.get(letter, 0) + 1
```
  We walk the string once and remember how many times each letter showed
  up. The time is O(n) - we look at every character one time, no more.

Palindrome and anagram - do not mix them up:
  A palindrome reads the same both ways: "level", "racecar".
  An anagram uses the same letters in a different order:
  "listen" and "silent".
  Palindrome = same order. Anagram = same letters.

Small detail for this chapter: the checks below ignore the case and they
skip spaces and punctuation, so "A man, a plan" counts as a palindrome.

Tip: write the characters of the string in a row before you code.
Tip: `print` the string first so you can see exactly what you work with.
"""

from collections import Counter

from _dsa_kit import main


# ---------------------------------------------------------------------------
# DEMOS - run these first, then change the code and experiment
# ---------------------------------------------------------------------------


def demo_char_frequency() -> None:
    # Count how many times every character shows up.
    text = "banana"
    counts = {}
    for letter in text:
        counts[letter] = counts.get(letter, 0) + 1
    print("  text:  ", text)
    print("  counts:", counts)
    # The built-in shortcut does exactly the same thing:
    print("  Counter:", Counter(text))


def demo_palindrome() -> None:
    # A palindrome reads the same from both sides.
    words = ["level", "racecar", "hello", "rotator"]
    for word in words:
        clean = "".join(ch for ch in word.lower() if ch.isalnum())
        print(f"  {word:<9} -> {clean == clean[::-1]}")
    print("  clean[::-1] means: read the string backwards.")


def demo_anagram() -> None:
    # An anagram uses the same letters in a different order.
    pairs = [("listen", "silent"), ("hello", "world"), ("triangle", "integral")]
    for first, second in pairs:
        first_sorted = sorted(first.lower())
        second_sorted = sorted(second.lower())
        print(f"  {first:<9} vs {second:<9} -> {first_sorted == second_sorted}")


def demo_reverse_words() -> None:
    # Split a sentence into words, flip the list, glue it back together.
    sentence = "the quick brown fox"
    words = sentence.split()
    reversed_sentence = " ".join(reversed(words))
    print("  sentence:", sentence)
    print("  words:   ", words)
    print("  reversed:", reversed_sentence)


def demo_longest_word() -> None:
    # Keep the longest word while walking the words one by one.
    sentence = "learn python step by step today"
    longest = ""
    for word in sentence.split():
        if len(word) > len(longest):
            longest = word
    print("  sentence:", sentence)
    print("  longest: ", longest, f"({len(longest)} letters)")


def demo_first_non_repeating() -> None:
    # Count everything first, then look for the first letter seen once.
    text = "swiss"
    counts = {}
    for letter in text:
        counts[letter] = counts.get(letter, 0) + 1
    answer = None
    for letter in text:
        if counts[letter] == 1:
            answer = letter
            break
    print("  text:  ", text)
    print("  counts:", counts)
    print("  first character that appears once:", answer)


# ---------------------------------------------------------------------------
# EXERCISES - write your code where you see TODO
# ---------------------------------------------------------------------------


def is_palindrome(s: str) -> bool:
    """Return True if s reads the same backwards (ignore case and spaces).

    is_palindrome("level") -> True
    """
    # TODO: clean the string, then compare it with its backwards version
    return None


def are_anagrams(a: str, b: str) -> bool:
    """Return True if a and b use exactly the same letters.

    are_anagrams("listen", "silent") -> True
    """
    # TODO: count the letters of both strings and compare the counts
    return None


def reverse_words(s: str) -> str:
    """Return the sentence with the words in the opposite order.

    reverse_words("hello world") -> "world hello"
    """
    # TODO: split into words, turn the list around, join it back
    return None


def char_frequency(s: str) -> dict:
    """Return a dict with every character and how many times it shows up.

    char_frequency("hello") -> {"h": 1, "e": 1, "l": 2, "o": 1}
    """
    # TODO: use a dict and count every character
    return None


def longest_word(s: str) -> str:
    """Return the longest word in the sentence ("" if there is none).

    longest_word("the quick brown fox") -> "quick"
    """
    # TODO: split the sentence and keep the longest word
    return None


def count_vowels(s: str) -> int:
    """Return how many vowels (a, e, i, o, u) are in the string.

    count_vowels("hello") -> 2
    """
    # TODO: check every character and count the vowels
    return None


def first_unique_char(s: str):
    """Return the first character that appears only once, or None.

    first_unique_char("swiss") -> "w"
    """
    # TODO: count the characters first, then find the first one seen once
    return None


# Solutions - try it yourself first, then run with `--solutions`
def sol_is_palindrome(s: str) -> bool:
    clean = "".join(ch for ch in s.lower() if ch.isalnum())
    return clean == clean[::-1]


def sol_are_anagrams(a: str, b: str) -> bool:
    first = "".join(ch for ch in a.lower() if ch.isalnum())
    second = "".join(ch for ch in b.lower() if ch.isalnum())
    if len(first) != len(second):
        return False
    return Counter(first) == Counter(second)


def sol_reverse_words(s: str) -> str:
    return " ".join(reversed(s.split()))


def sol_char_frequency(s: str) -> dict:
    counts = {}
    for letter in s:
        counts[letter] = counts.get(letter, 0) + 1
    return counts


def sol_longest_word(s: str) -> str:
    longest = ""
    for word in s.split():
        if len(word) > len(longest):
            longest = word
    return longest


def sol_count_vowels(s: str) -> int:
    vowels = "aeiou"
    total = 0
    for letter in s.lower():
        if letter in vowels:
            total += 1
    return total


def sol_first_unique_char(s: str):
    counts = {}
    for letter in s:
        counts[letter] = counts.get(letter, 0) + 1
    for letter in s:
        if counts[letter] == 1:
            return letter
    return None


EXERCISES = [
    {
        "id": "3.1",
        "task": "is_palindrome(s): does it read the same backwards?",
        "func": is_palindrome,
        "tests": [(("racecar",), True), (("hello",), False)],
        "solution": sol_is_palindrome,
    },
    {
        "id": "3.2",
        "task": "are_anagrams(a, b): same letters in a different order?",
        "func": are_anagrams,
        "tests": [(("listen", "silent"), True), (("hello", "world"), False)],
        "solution": sol_are_anagrams,
    },
    {
        "id": "3.3",
        "task": "reverse_words(s): put the words in the opposite order",
        "func": reverse_words,
        "tests": [(("hello world",), "world hello"), (("the quick brown fox",), "fox brown quick the")],
        "solution": sol_reverse_words,
    },
    {
        "id": "3.4",
        "task": "char_frequency(s): count how often every character shows up",
        "func": char_frequency,
        "tests": [(("hello",), {"h": 1, "e": 1, "l": 2, "o": 1}), (("",), {})],
        "solution": sol_char_frequency,
    },
    {
        "id": "3.5",
        "task": "longest_word(s): the longest word in the sentence",
        "func": longest_word,
        "tests": [(("the quick brown fox",), "quick"), (("a bb ccc",), "ccc")],
        "solution": sol_longest_word,
    },
    {
        "id": "3.6",
        "task": "count_vowels(s): how many vowels are in the string",
        "func": count_vowels,
        "tests": [(("hello",), 2), (("AEIOU xyz",), 5)],
        "solution": sol_count_vowels,
    },
    {
        "id": "3.7",
        "task": "first_unique_char(s): the first character seen only once",
        "func": first_unique_char,
        "tests": [(("swiss",), "w"), (("aabb",), None)],
        "solution": sol_first_unique_char,
    },
]

DEMOS = [
    ("1. Character frequency", demo_char_frequency),
    ("2. Palindrome check", demo_palindrome),
    ("3. Anagram check", demo_anagram),
    ("4. Reverse the words", demo_reverse_words),
    ("5. Longest word", demo_longest_word),
    ("6. First non-repeating character", demo_first_non_repeating),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
