"""
quiz_bank_dsa.py - Rapid-fire DSA questions (patterns, arrays, strings,
two pointers, sliding window, sorting, hashing, stacks, queues, linked
lists, recursion, trees, heaps, graphs, dynamic programming, binary search).

Format:
  q       -> question
  options -> 4 choices
  answer  -> index of the correct option (0-based)
  explain -> short explanation
"""

QUESTIONS = [
    # ---------------- patterns (2) ----------------
    {
        "q": "How many times does the inner loop run in a full square pattern of n rows?",
        "options": ["n", "n + 1", "n * n", "2 * n"],
        "answer": 2,
        "explain": "The inner loop runs n times for each of the n rows, so n * n in total.",
    },
    {
        "q": "In a right triangle pattern of height n, how many stars are on the last row?",
        "options": ["1", "n", "n - 1", "2 * n"],
        "answer": 1,
        "explain": "Row i prints i stars, so the last row (i = n) prints n stars.",
    },
    # ---------------- arrays (3) ----------------
    {
        "q": "What is the time complexity of scanning a list with a for loop?",
        "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
        "answer": 2,
        "explain": "The loop visits every element once, so the time grows with n.",
    },
    {
        "q": "nums = [1, 2, 3]; what does nums[::-1] give?",
        "options": ["[1, 2, 3]", "[3, 2, 1]", "[2, 3]", "Error"],
        "answer": 1,
        "explain": "A step of -1 copies the list backwards.",
    },
    {
        "q": "How do you find the largest value in a non-empty list of numbers?",
        "options": ["max(nums)", "nums.max()", "sort(nums)[0]", "nums[0]"],
        "answer": 0,
        "explain": "The built-in max() walks the list and returns the biggest value.",
    },
    # ---------------- strings (2) ----------------
    {
        "q": "Which method turns 'a b c' into ['a', 'b', 'c']?",
        "options": ["join", "split", "strip", "replace"],
        "answer": 1,
        "explain": "split() breaks a string on spaces and returns a list of parts.",
    },
    {
        "q": "How do you check if 'abc' is a palindrome the simple way?",
        "options": ["s == s[::-1]", "s == s[1:]", "s[0] == s[-1]", "s.split() == s"],
        "answer": 0,
        "explain": "A palindrome equals its own reverse, so compare the string with s[::-1].",
    },
    # ---------------- two pointers (2) ----------------
    {
        "q": "In the two pointer pattern, what do you usually start with on a sorted list?",
        "options": ["left = 0, right = len(nums) - 1", "left = 0, right = 0", "left = len(nums), right = 0", "left = 1, right = len(nums)"],
        "answer": 0,
        "explain": "One pointer starts at the front and the other at the back, then they move inward.",
    },
    {
        "q": "What is the time complexity of the two pointer technique on a sorted array?",
        "options": ["O(n)", "O(log n)", "O(n^2)", "O(2^n)"],
        "answer": 0,
        "explain": "Each pointer moves only in one direction, so together they make one pass.",
    },
    # ---------------- sliding window (2) ----------------
    {
        "q": "What is the main idea of the sliding window technique?",
        "options": [
            "Re-sort the array for every window",
            "Keep a window over the array and reuse the previous result",
            "Compare every pair of elements",
            "Sort the array and then scan it",
        ],
        "answer": 1,
        "explain": "The window slides forward and updates its answer instead of recomputing from scratch.",
    },
    {
        "q": "In a fixed size sliding window of size k, how many times is the loop body run for n elements?",
        "options": ["n", "n - k", "n - k + 1", "k"],
        "answer": 2,
        "explain": "The window can start at index 0 up to index n - k, which is n - k + 1 times.",
    },
    # ---------------- sorting + binary search (4) ----------------
    {
        "q": "What is the time complexity of Python's list.sort() on n items?",
        "options": ["O(n)", "O(n log n)", "O(log n)", "O(n^2)"],
        "answer": 1,
        "explain": "Python's sort uses a merge-sort style algorithm, which is n log n.",
    },
    {
        "q": "In binary search on 1000 sorted elements, how many comparisons are needed at most?",
        "options": ["About 1000", "About 10", "About 100", "About 500"],
        "answer": 1,
        "explain": "Each comparison halves the range, so 2 to the power of 10 is about 1000, so ~10 steps.",
    },
    {
        "q": "What must be true before you can use binary search?",
        "options": ["The array must be sorted", "The array must have only unique values", "The array must be a list", "The array must be non-empty"],
        "answer": 0,
        "explain": "Binary search throws away half the array each step, so it needs sorted order.",
    },
    {
        "q": "In a binary search loop `while lo <= hi`, what does `mid = (lo + hi) // 2` do?",
        "options": ["Picks the last element", "Picks the middle index", "Picks the first element", "Increments lo by two"],
        "answer": 1,
        "explain": "It finds the middle index between lo and hi using floor division.",
    },
    # ---------------- hashing (2) ----------------
    {
        "q": "Which structure gives O(1) average lookup by key?",
        "options": ["list", "dict", "tuple", "string"],
        "answer": 1,
        "explain": "A dict uses a hash table, so finding a key is fast on average.",
    },
    {
        "q": "What does Counter([1, 1, 2]) give?",
        "options": ["[1, 1, 2]", "{1: 2, 2: 1}", "{1: 1, 2: 1}", "Counter([1, 2])"],
        "answer": 1,
        "explain": "Counter counts how many times each value appears and returns a dict-like object.",
    },
    # ---------------- stacks (3) ----------------
    {
        "q": "What does the stack operation pop() return?",
        "options": ["The bottom item", "The last item added", "The first item added", "The length of the stack"],
        "answer": 1,
        "explain": "A stack is last in, first out, so pop removes and returns the newest item.",
    },
    {
        "q": "Which Python tool gives stack behaviour with append() and pop()?",
        "options": ["A list used as a stack", "A set", "A dictionary", "A tuple"],
        "answer": 0,
        "explain": "A plain list works as a stack because both append and pop work at the end.",
    },
    {
        "q": "Which problem is solved with a stack?",
        "options": ["Finding the minimum element", "Matching brackets", "Sorting by value", "Finding duplicates"],
        "answer": 1,
        "explain": "Push every opening bracket and pop it when the matching closing one arrives.",
    },
    # ---------------- queues (2) ----------------
    {
        "q": "Which Python collection should you use for a queue that needs popleft()?",
        "options": ["list", "set", "deque from collections", "dict"],
        "answer": 2,
        "explain": "deque supports fast adding and removing from both ends.",
    },
    {
        "q": "A queue works on which principle?",
        "options": ["Last in, first out", "First in, first out", "Random order", "Sorted order"],
        "answer": 1,
        "explain": "The oldest item added is the first one removed, like a queue of people.",
    },
    # ---------------- linked lists (2) ----------------
    {
        "q": "In a singly linked list, where does each node point to?",
        "options": ["The previous node", "The next node", "The head only", "The tail only"],
        "answer": 1,
        "explain": "Each node stores a value and a link to the node after it.",
    },
    {
        "q": "How do you detect a cycle in a linked list?",
        "options": [
            "Check if the list is sorted",
            "Use a slow pointer and a fast pointer and see if they meet",
            "Count the nodes twice",
            "Compare each node with the head",
        ],
        "answer": 1,
        "explain": "If there is a cycle the fast pointer keeps going and eventually catches the slow one.",
    },
    # ---------------- recursion + backtracking (3) ----------------
    {
        "q": "What must every recursive function have to stop calling itself?",
        "options": ["A loop", "A base case", "A global variable", "A class"],
        "answer": 1,
        "explain": "The base case is the condition where the function returns without recursing again.",
    },
    {
        "q": "What is the time complexity of plain recursion for fib(n) with no memoization?",
        "options": ["O(n)", "O(n log n)", "O(2^n)", "O(log n)"],
        "answer": 2,
        "explain": "The work doubles at every level, so it grows like 2 to the power of n.",
    },
    {
        "q": "In backtracking, why do you usually 'undo' a choice before the next one?",
        "options": [
            "To save memory",
            "So each branch starts from the same clean state",
            "To make the code shorter",
            "To sort the results",
        ],
        "answer": 1,
        "explain": "You remove the choice you added, so the next branch does not see it.",
    },
    # ---------------- trees + BST (3) ----------------
    {
        "q": "Which traversal of a binary tree is breadth first?",
        "options": ["Inorder", "Preorder", "Level order", "Postorder"],
        "answer": 2,
        "explain": "Level order visits the tree level by level, using a queue.",
    },
    {
        "q": "In a binary search tree, where does a smaller value go than the current node?",
        "options": ["To the right subtree", "To the left subtree", "It replaces the node", "To the root"],
        "answer": 1,
        "explain": "BST rule: smaller values go left, bigger values go right.",
    },
    {
        "q": "What is the time complexity of searching in a balanced binary search tree?",
        "options": ["O(1)", "O(log n)", "O(n)", "O(n^2)"],
        "answer": 1,
        "explain": "A balanced tree keeps the height small, so the search path is short.",
    },
    # ---------------- heaps (2) ----------------
    {
        "q": "In a min-heap, which element is at the top?",
        "options": ["The largest", "The smallest", "The middle one", "The last inserted"],
        "answer": 1,
        "explain": "A min-heap keeps the smallest value on top.",
    },
    {
        "q": "Which Python module is used for heaps?",
        "options": ["collections", "heapq", "itertools", "bisect"],
        "answer": 1,
        "explain": "heapq gives heappush, heappop and heapify for heap work.",
    },
    # ---------------- graphs (3) ----------------
    {
        "q": "Which algorithm finds the shortest path in an unweighted graph?",
        "options": ["Depth first search", "Breadth first search", "Dijkstra", "Topological sort"],
        "answer": 1,
        "explain": "BFS explores level by level, so the first time it reaches a node is the shortest path.",
    },
    {
        "q": "What data structure does BFS use to keep nodes to visit?",
        "options": ["A stack", "A queue", "A heap", "A set of stacks"],
        "answer": 1,
        "explain": "BFS uses a queue so it processes nodes in the order they were added.",
    },
    {
        "q": "What does DFS use to keep track of where it can go next?",
        "options": ["A queue", "A stack or recursion", "A heap", "A sorted array"],
        "answer": 1,
        "explain": "DFS goes deep down one branch first, using a stack or recursive calls.",
    },
    # ---------------- dynamic programming (3) ----------------
    {
        "q": "What is the time complexity of Kadane's algorithm for the maximum sum subarray?",
        "options": ["O(n)", "O(n^2)", "O(n log n)", "O(2^n)"],
        "answer": 0,
        "explain": "It keeps a running best sum and goes over the array once.",
    },
    {
        "q": "What does memoization do in a recursive solution?",
        "options": [
            "Deletes the old results",
            "Stores results of already solved calls and reuses them",
            "Sorts the input",
            "Makes the code run in constant time",
        ],
        "answer": 1,
        "explain": "Each subproblem is computed once and saved, so it is not solved again.",
    },
    {
        "q": "Which two things usually define a dynamic programming state?",
        "options": [
            "The code length and the file name",
            "The index and the goal or subproblem",
            "The memory and the stack size",
            "The sorting and the hashing",
        ],
        "answer": 1,
        "explain": "You pick what the subproblem is and the position, then build the table.",
    },
    # ---------------- binary search on the answer (2) ----------------
    {
        "q": "What is binary search on the answer?",
        "options": [
            "Searching for a value in a sorted list",
            "Searching over a range of possible answers and checking if a candidate works",
            "Searching inside a string",
            "Searching a graph with BFS",
        ],
        "answer": 1,
        "explain": "You binary search the answer space, and a check function tells you if a candidate is valid.",
    },
    {
        "q": "For binary search on the answer to work, what must be true of the check function?",
        "options": [
            "It must be random",
            "If a value works, all larger values also work",
            "It must sort the input",
            "It must run in O(1)",
        ],
        "answer": 1,
        "explain": "The condition has to be monotonic, so the valid answers form one solid range.",
    },
]
