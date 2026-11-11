# Python Cheatsheet (one-page revision)

## Print and input

```python
print("hello", 42, sep="-", end="\n")
name = input("Name: ")       # always a string
age = int(input("Age: "))
```

## Variables and types

```python
x = 10            # int
y = 3.14          # float
s = "hello"       # str
b = True          # bool
n = None          # empty / no value

type(x)                    # <class 'int'>
type(x).__name__           # 'int'
int("42"), float("3.5"), str(10), bool(0)
```

## f-strings

```python
f"{name} is {age}"
f"{price:.2f}"        # 2 decimal places
f"{1234567:,}"        # 1,234,567
f"{name:>10}"         # right align
f"{name:<10}"         # left align
f"{0.87:.1%}"         # 87.0%
```

## Operators

```python
7 / 2      # 3.5
7 // 2     # 3
7 % 2      # 1
2 ** 10    # 1024
divmod(7, 2)   # (3, 1)
pow(2, 10, 1000)  # 24

a == b     # value
a is b     # same object
1 < x < 10 # chained comparison
```

## Strings

```python
s = "Python"
s[0], s[-1]        # 'P', 'n'
s[1:4]             # 'yth'
s[::-1]            # 'nohtyP'
len(s), "th" in s

s.upper(), s.lower(), s.strip(), s.title()
s.replace("Py", "My")
s.split(","), "-".join(["a", "b"])
s.find("th"), s.count("t")
s.startswith("Py"), s.endswith("on")
```

## Conditionals

```python
if x > 10:
    ...
elif x > 5:
    ...
else:
    ...

status = "adult" if age >= 18 else "minor"

match command:
    case "start":
        ...
    case _:
        ...
```

## Loops

```python
for i in range(5):          # 0..4
for i in range(2, 6):       # 2..5
for i in range(10, 0, -2):  # 10,8,6,4,2

for i, value in enumerate(items, start=1):
for a, b in zip(list1, list2):

while n > 0:
    n -= 1

break      # exit the loop
continue   # skip to the next iteration
```

## Lists

```python
nums = [3, 1, 2]
nums[0], nums[-1], nums[1:3]
nums.append(x)      # add at the end
nums.insert(1, x)   # at an index
nums.extend(other)  # join lists
nums.remove(x)      # by value
nums.pop()          # remove the last item
nums.sort()         # changes the original
sorted(nums)        # new list
nums.reverse()
len, sum, min, max, any, all

b = a               # alias (same list!)
b = a.copy()        # real copy
```

## Tuples and sets

```python
t = (1, 2)
x, y = t
single = (5,)       # comma is required

s = {1, 2, 2}       # {1, 2}
s.add(3), s.discard(2)
a | b   # union
a & b   # intersection
a - b   # difference
a ^ b   # symmetric difference
```

## Dicts

```python
d = {"name": "Ravi", "age": 21}
d["name"]
d.get("marks")          # None
d.get("marks", 0)       # default
d["city"] = "Delhi"
del d["age"]
d.pop("age")
d.keys(), d.values(), d.items()

for key, value in d.items():
    ...

d1 | d2                 # merge (3.9+)
```

## Functions

```python
def add(a, b=0):
    """Docstring."""
    return a + b

def total(*args):        # tuple
def profile(**kwargs):   # dict

lambda x: x * 2
map(fn, items), filter(fn, items)
sorted(items, key=lambda x: x[1], reverse=True)
```

**Do not use a mutable default:**

```python
def f(items=None):
    if items is None:
        items = []
```

## Comprehensions

```python
[n * n for n in range(5)]
[n for n in nums if n % 2 == 0]
["even" if n % 2 == 0 else "odd" for n in nums]
{n: len(n) for n in words}
{n % 3 for n in range(10)}
sum(n * n for n in range(100))
```

## Files and JSON

```python
from pathlib import Path
import json

path = Path("data.txt")
path.write_text("hello", encoding="utf-8")
text = path.read_text(encoding="utf-8")

with open("data.txt", "a", encoding="utf-8") as f:
    f.write("line\n")

json.dumps(data)        # dict -> string
json.loads(text)        # string -> dict
json.dump(data, f)      # to a file
json.load(f)            # from a file
```

## Exceptions

```python
try:
    risky()
except ValueError as e:
    print(e)
except (TypeError, KeyError):
    ...
else:
    print("no error")
finally:
    print("always")

raise ValueError("invalid value")

class MyError(Exception):
    pass
```

## OOP

```python
class Dog:
    species = "dog"              # class attribute

    def __init__(self, name):    # constructor
        self.name = name         # instance attribute

    def bark(self):
        return f"{self.name} says woof"

class Puppy(Dog):
    def __init__(self, name):
        super().__init__(name)

    def bark(self):              # override
        return "small woof"

d = Dog("Tommy")
d.bark()
```

Dunder: `__str__`, `__repr__`, `__eq__`, `__add__`, `__len__`

## Iterators, generators, decorators

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

list(countdown(3))     # [3, 2, 1]

def my_decorator(fn):
    def wrapper(*args, **kwargs):
        print("before")
        result = fn(*args, **kwargs)
        print("after")
        return result
    return wrapper

@my_decorator
def hello():
    print("hi")
```

## Standard library

```python
from collections import Counter, defaultdict, deque
from itertools import combinations, chain
from datetime import date, datetime, timedelta
from pathlib import Path
import math, random, json, re, statistics

Counter(words).most_common(3)
defaultdict(list)
deque([1, 2, 3])
date.today()
datetime.strptime("2026-11-10", "%Y-%m-%d")
math.gcd(12, 18), math.sqrt(16)
re.findall(r"\d+", "a1 b22")
```

## Testing

```python
import unittest

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(1 + 1, 2)

    def test_error(self):
        with self.assertRaises(ZeroDivisionError):
            1 / 0

if __name__ == "__main__":
    unittest.main()
```

## Terminal commands

```powershell
python file.py                 # run it
python -i file.py              # run it, then stay in the REPL
python -m venv .venv           # create a venv
.venv\Scripts\activate         # activate
pip install requests
pip freeze > requirements.txt
python -m pytest               # tests
```
