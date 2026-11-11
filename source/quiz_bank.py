"""
quiz_bank.py - Rapid-fire Python questions.
practice.py picks 10 random questions from here.

Format:
  q       -> question
  options -> 4 choices
  answer  -> index of the correct option (0-based)
  explain -> short explanation
"""

QUESTIONS = [
    {
        "q": "What does print(7 // 2) output?",
        "options": ["3.5", "3", "4", "2"],
        "answer": 1,
        "explain": "// is floor division: 7 // 2 = 3.",
    },
    {
        "q": "What is the result of 2 ** 3?",
        "options": ["6", "8", "9", "5"],
        "answer": 1,
        "explain": "** is power: 2 * 2 * 2 = 8.",
    },
    {
        "q": "What is type(10 / 2).__name__?",
        "options": ["int", "float", "str", "double"],
        "answer": 1,
        "explain": "/ always gives a float, so the result is 5.0.",
    },
    {
        "q": "What is len('Python')?",
        "options": ["5", "6", "7", "Error"],
        "answer": 1,
        "explain": "P-y-t-h-o-n = 6 characters.",
    },
    {
        "q": "What does 'Python'[::-1] return?",
        "options": ["'Python'", "'nohtyP'", "'P'", "'n'"],
        "answer": 1,
        "explain": "A step of -1 means reverse.",
    },
    {
        "q": "What is the result of bool('')?",
        "options": ["True", "False", "None", "Error"],
        "answer": 1,
        "explain": "An empty string is falsy.",
    },
    {
        "q": "What is the result of bool('False')?",
        "options": ["True", "False", "None", "Error"],
        "answer": 0,
        "explain": "A non-empty string is truthy, even if the text says 'False'.",
    },
    {
        "q": "What does [1, 2] + [3] return?",
        "options": ["[1, 2, 3]", "[1, 2, [3]]", "[4, 5]", "Error"],
        "answer": 0,
        "explain": "+ joins lists (like extend).",
    },
    {
        "q": "What is len({1, 2, 2, 3})?",
        "options": ["4", "3", "2", "Error"],
        "answer": 1,
        "explain": "A set removes duplicates.",
    },
    {
        "q": "Which type is immutable?",
        "options": ["list", "tuple", "dict", "set"],
        "answer": 1,
        "explain": "Once a tuple is created, you cannot change it.",
    },
    {
        "q": "What does 'a,b,c'.split(',') return?",
        "options": ["['a,b,c']", "['a', 'b', 'c']", "('a', 'b', 'c')", "'abc'"],
        "answer": 1,
        "explain": "split breaks the string at the comma and returns a list.",
    },
    {
        "q": "What does '-'.join(['a', 'b']) return?",
        "options": ["'a-b'", "['a-b']", "'ab'", "Error"],
        "answer": 0,
        "explain": "join connects the list items with the separator.",
    },
    {
        "q": "What does int('3.5') do?",
        "options": ["3", "3.5", "4", "ValueError"],
        "answer": 3,
        "explain": "int() does not accept a decimal string; call float() first.",
    },
    {
        "q": "What does int(3.9) return?",
        "options": ["3", "4", "3.9", "Error"],
        "answer": 0,
        "explain": "int() cuts off the decimal part, it does not round.",
    },
    {
        "q": "What is 10 % 3?",
        "options": ["3", "1", "0", "3.33"],
        "answer": 1,
        "explain": "% gives the remainder: 10 = 3*3 + 1.",
    },
    {
        "q": "What is -7 // 2?",
        "options": ["-3", "-4", "-3.5", "3"],
        "answer": 1,
        "explain": "Floor division goes down: -4.",
    },
    {
        "q": "What is the result of 0.1 + 0.2 == 0.3?",
        "options": ["True", "False", "Error", "None"],
        "answer": 1,
        "explain": "It is False because of floating point precision. Use math.isclose.",
    },
    {
        "q": "x = (5); what is type(x).__name__?",
        "options": ["tuple", "int", "list", "str"],
        "answer": 1,
        "explain": "A one-element tuple needs a comma: (5,).",
    },
    {
        "q": "Which numbers does range(1, 5) give?",
        "options": ["1,2,3,4,5", "1,2,3,4", "0,1,2,3,4", "2,3,4,5"],
        "answer": 1,
        "explain": "The stop value is not included.",
    },
    {
        "q": "for i in range(3): how many times does the loop run?",
        "options": ["2", "3", "4", "1"],
        "answer": 1,
        "explain": "0, 1, 2 - 3 times in total.",
    },
    {
        "q": "What does a function without a return statement give back?",
        "options": ["0", "None", "''", "Error"],
        "answer": 1,
        "explain": "The default return value is None.",
    },
    {
        "q": "What type is *args inside a function?",
        "options": ["list", "tuple", "dict", "set"],
        "answer": 1,
        "explain": "*args is a tuple of positional values.",
    },
    {
        "q": "What type is **kwargs?",
        "options": ["list", "tuple", "dict", "set"],
        "answer": 2,
        "explain": "**kwargs is a dict of keyword arguments.",
    },
    {
        "q": "What is the main problem with def f(x, items=[]):?",
        "options": [
            "It is a syntax error",
            "The default list is shared by all calls",
            "You cannot pass a list",
            "There is no problem",
        ],
        "answer": 1,
        "explain": "A mutable default is created only once, so use None instead.",
    },
    {
        "q": "What is the difference between `is` and `==`?",
        "options": [
            "They are the same",
            "is checks identity, == compares values",
            "is compares values, == checks identity",
            "is only works for numbers",
        ],
        "answer": 1,
        "explain": "is checks for the same object, == checks equality.",
    },
    {
        "q": "a = [1,2]; b = a; b.append(3). What is a now?",
        "options": ["[1,2]", "[1,2,3]", "[3]", "Error"],
        "answer": 1,
        "explain": "b is an alias, both are the same list. Use a.copy() to copy.",
    },
    {
        "q": "nums = [10,20,30,40]; what is nums[1:3]?",
        "options": ["[10,20]", "[20,30]", "[20,30,40]", "[30,40]"],
        "answer": 1,
        "explain": "From index 1 up to 2 (3 is excluded).",
    },
    {
        "q": "d = {'a': 1}; what does d.get('b') return?",
        "options": ["KeyError", "None", "0", "False"],
        "answer": 1,
        "explain": "get() returns None for a missing key.",
    },
    {
        "q": "d = {'a': 1}; what does d['b'] do?",
        "options": ["None", "0", "KeyError", "False"],
        "answer": 2,
        "explain": "Square brackets raise KeyError for a missing key.",
    },
    {
        "q": "What does list.append() return?",
        "options": ["A new list", "None", "An index", "True"],
        "answer": 1,
        "explain": "append works in place and returns None.",
    },
    {
        "q": "Does sorted(nums) change the original list?",
        "options": ["Yes", "No, it returns a new sorted list", "Only for numbers", "Error"],
        "answer": 1,
        "explain": "sorted() returns a new list; list.sort() changes the original.",
    },
    {
        "q": "What is [x*x for x in range(3)]?",
        "options": ["[1, 4, 9]", "[0, 1, 4]", "[0, 1, 2]", "[1, 2, 3]"],
        "answer": 1,
        "explain": "0*0, 1*1, 2*2 = 0, 1, 4.",
    },
    {
        "q": "What does any([False, True]) return?",
        "options": ["False", "True", "None", "Error"],
        "answer": 1,
        "explain": "any() returns True when at least one item is True.",
    },
    {
        "q": "What does all([]) return?",
        "options": ["False", "True", "None", "Error"],
        "answer": 1,
        "explain": "all() on an empty list is True (vacuously true).",
    },
    {
        "q": "What is special about a generator (yield)?",
        "options": [
            "It keeps all values in memory at once",
            "It gives values lazily",
            "It only works for numbers",
            "It finishes immediately like return",
        ],
        "answer": 1,
        "explain": "A generator gives one value at a time when needed, saving memory.",
    },
    {
        "q": "Writing @decorator is the same as what?",
        "options": [
            "func = decorator(func)",
            "decorator = func()",
            "func()",
            "import decorator",
        ],
        "answer": 0,
        "explain": "A decorator wraps a function and returns a new function.",
    },
    {
        "q": "When does the finally block run?",
        "options": [
            "Only on an error",
            "Only when there is no error",
            "Always",
            "Never",
        ],
        "answer": 2,
        "explain": "finally always runs, whether there is an error or not.",
    },
    {
        "q": "What is the benefit of with open(...)?",
        "options": [
            "The file is read faster",
            "The file closes automatically",
            "No error can happen",
            "The file gets encrypted",
        ],
        "answer": 1,
        "explain": "The file closes as soon as the with block ends.",
    },
    {
        "q": "When does __init__ run?",
        "options": [
            "When the class is defined",
            "When an object is created",
            "When a method is called",
            "When the file is imported",
        ],
        "answer": 1,
        "explain": "__init__ is the constructor, it runs when an object is created.",
    },
    {
        "q": "What is self inside a method?",
        "options": [
            "The class name",
            "The current object",
            "The parent class",
            "The module",
        ],
        "answer": 1,
        "explain": "self refers to the current instance.",
    },
    {
        "q": "What does super() do?",
        "options": [
            "Calls a method of the parent class",
            "Deletes an object",
            "Creates a new object",
            "Creates a private variable",
        ],
        "answer": 0,
        "explain": "super() runs the parent class's method or constructor.",
    },
    {
        "q": "What does json.loads() do?",
        "options": [
            "Writes a dict to a file",
            "Turns a JSON string into a Python object",
            "Downloads a file",
            "Validates JSON",
        ],
        "answer": 1,
        "explain": "loads = load string. For files, use json.load().",
    },
    {
        "q": "Which module has Counter?",
        "options": ["itertools", "collections", "functools", "math"],
        "answer": 1,
        "explain": "from collections import Counter.",
    },
    {
        "q": "What does if __name__ == '__main__': mean?",
        "options": [
            "The file was imported",
            "The file is run directly",
            "The file has an error",
            "The file is empty",
        ],
        "answer": 1,
        "explain": "When run directly, __name__ is '__main__'.",
    },
    {
        "q": "What is the order of a dict (Python 3.7+)?",
        "options": [
            "Random",
            "Sorted by key",
            "Insertion order",
            "Reverse insertion",
        ],
        "answer": 2,
        "explain": "Keys remember the insertion order.",
    },
    {
        "q": "In which type is a membership check generally fast?",
        "options": ["list", "tuple", "set", "string"],
        "answer": 2,
        "explain": "A set uses a hash table, so x in set is fast.",
    },
    {
        "q": "What does 'Hello'.lower() return?",
        "options": ["'HELLO'", "'hello'", "'Hello'", "Error"],
        "answer": 1,
        "explain": "lower() turns all letters into lowercase.",
    },
    {
        "q": "What does '  x '.strip() return?",
        "options": ["'  x '", "'x'", "'x '", "' x'"],
        "answer": 1,
        "explain": "strip() removes spaces from both ends.",
    },
    {
        "q": "What does f'{3.14159:.2f}' return?",
        "options": ["'3.14'", "'3.14159'", "'3.1'", "'3.142'"],
        "answer": 0,
        "explain": ".2f means 2 decimal places.",
    },
    {
        "q": "What does pow(2, 10, 1000) return?",
        "options": ["1024", "24", "100", "0"],
        "answer": 1,
        "explain": "pow(base, exp, mod) is modular power: 1024 % 1000 = 24.",
    },
]
