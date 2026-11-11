"""
kid_lessons_dsa.py - A super simple version of every DSA chapter, written for
a 10 year old kid.

Each lesson has:
  title  - a fun name for the topic
  story  - 2-3 short sentences with an easy example (boxes, cards, robots...)
  points - 4-5 very simple facts, one line each
  code   - a tiny runnable program (6 lines or less)
  win    - what you can do after reading it

The portal uses this for "Kid Mode" on the DSA chapters. The normal notes stay
in the chapters.
"""

LESSONS = {
    "D01": {
        "title": "Building shapes with stars",
        "story": (
            "A loop that sits inside another loop can draw shapes. Think of it "
            "like stacking rows of blocks. The outer loop picks the row and the "
            "inner loop picks what sits inside that row."
        ),
        "points": [
            "The outside loop chooses the row. The inside loop chooses what goes in it.",
            "print(\"*\", end=\"\") keeps the stars on the same line.",
            "print() with nothing in it moves you down to the next line.",
            "A row can grow with row + 1, and shrink with n - row.",
            "Write the row numbers on paper first. Then the code is easy.",
        ],
        "code": (
            "for row in range(4):\n"
            "    for col in range(row + 1):\n"
            "        print(\"*\", end=\"\")\n"
            "    print()\n"
            "for row in range(3):\n"
            "    print(\" \".join(str(col + 1) for col in range(row + 1)))"
        ),
        "win": "Now you can draw any star or number shape you can picture.",
    },
    "D02": {
        "title": "A row of numbered boxes",
        "story": (
            "An array is a row of boxes, and every box holds one number. The "
            "boxes stand in a line, so each one has a place number. Finding "
            "something means walking down the line and peeking in each box."
        ),
        "points": [
            "boxes[0] is the first box and boxes[-1] is the last box.",
            "The place of a box is called its index, and counting starts at 0.",
            "To find a number, walk down the line and check each box one by one.",
            "A for loop with an if can stop the moment it finds the number.",
            "If the boxes are already in order, you can do much better.",
        ],
        "code": (
            "boxes = [12, 7, 25, 3]\n"
            "target = 25\n"
            "for i in range(len(boxes)):\n"
            "    if boxes[i] == target:\n"
            "        print(\"found it at place\", i)\n"
            "        break"
        ),
        "win": "Now you can store numbers in a row and find any one of them.",
    },
    "D03": {
        "title": "Words are ribbons of letters",
        "story": (
            "A word in Python is a string, which is just a long ribbon of "
            "letters joined together. You can look at one letter, cut a piece "
            "off the ribbon, or check if the ribbon reads the same both ways."
        ),
        "points": [
            "word[0] is the first letter and word[-1] is the last letter.",
            "word[1:4] cuts a little piece out of the ribbon.",
            "len(word) tells you how many letters are on the ribbon.",
            "word[::-1] flips the ribbon backwards.",
            "A for loop over a word visits one letter at a time.",
        ],
        "code": (
            "word = \"level\"\n"
            "print(\"letters:\", len(word))\n"
            "print(\"backwards:\", word[::-1])\n"
            "if word == word[::-1]:\n"
            "    print(word, \"reads the same both ways!\")"
        ),
        "win": "Now you can cut, flip and check words like a ribbon trick.",
    },
    "D04": {
        "title": "Two fingers walking down a row",
        "story": (
            "Put one finger on the first box of a row and another finger on the "
            "last box. Then walk them towards each other, one small step at a "
            "time, until they meet in the middle."
        ),
        "points": [
            "One finger starts at the left end and one at the right end.",
            "They move towards each other until they meet or cross.",
            "This saves you from checking every pair of boxes.",
            "It works best when the row is sorted from small to big.",
            "Only one finger needs to move in each round.",
        ],
        "code": (
            "nums = [1, 2, 3, 4, 5]\n"
            "left, right = 0, len(nums) - 1\n"
            "while left < right:\n"
            "    print(nums[left], \"and\", nums[right])\n"
            "    left += 1\n"
            "    right -= 1"
        ),
        "win": "Now you can walk two fingers down a list and meet in the middle.",
    },
    "D05": {
        "title": "A little window that slides",
        "story": (
            "Put a small frame over a row of numbers and look at what is inside "
            "it. Then slide the frame one step and look again. You never have "
            "to look at the whole row twice."
        ),
        "points": [
            "A window is just a starting place and a size.",
            "You slide it one step at a time and check what is inside.",
            "Adding the new item and dropping the old one keeps it fast.",
            "It is perfect for puzzles like \"the biggest sum of 3 next numbers\".",
            "You try every window of that size, one after another.",
        ],
        "code": (
            "nums = [2, 1, 5, 1, 3]\n"
            "size = 3\n"
            "best = sum(nums[:size])\n"
            "for i in range(size, len(nums)):\n"
            "    best = max(best, sum(nums[i - size + 1:i + 1]))\n"
            "print(\"biggest window sum:\", best)"
        ),
        "win": "Now you can slide a window over a list and find the best group.",
    },
    "D06": {
        "title": "Line up your cards, then guess in half",
        "story": (
            "First you line up all your cards from small to big. Then you look "
            "at the middle card and throw away half the cards each time until "
            "the card you want is the only one left."
        ),
        "points": [
            "sorted(cards) lines your cards up from small to big.",
            "To find a card, look at the middle one first.",
            "If it is too small, throw away the left half. If too big, the right half.",
            "Each guess throws away half the cards, so it is very fast.",
            "This trick only works when the cards are already in order.",
        ],
        "code": (
            "cards = [3, 8, 12, 25, 40, 55]\n"
            "target, lo, hi = 25, 0, len(cards) - 1\n"
            "while lo <= hi:\n"
            "    mid = (lo + hi) // 2\n"
            "    if cards[mid] == target: print(\"found at place\", mid); break\n"
            "    lo, hi = (mid + 1, hi) if cards[mid] < target else (lo, mid - 1)"
        ),
        "win": "Now you can find any card in a sorted deck by guessing in half.",
    },
    "D07": {
        "title": "A box of labelled drawers",
        "story": (
            "Picture a cabinet with one drawer for every name. You drop a toy "
            "into the drawer with its name on it, and later you open that "
            "drawer and the toy is right there waiting for you."
        ),
        "points": [
            "A dictionary is a cabinet of drawers, where the label is the key.",
            "d[\"name\"] opens the drawer and d.get(\"name\", 0) is the safe version.",
            "Putting a toy in the same drawer again just replaces it.",
            "To count toys, use d[toy] = d.get(toy, 0) + 1.",
            "Finding a drawer is super fast, even with lots of drawers.",
        ],
        "code": (
            "drawers = {}\n"
            "for toy in [\"car\", \"ball\", \"car\", \"doll\"]:\n"
            "    drawers[toy] = drawers.get(toy, 0) + 1\n"
            "print(drawers)\n"
            "print(\"cars:\", drawers[\"car\"])"
        ),
        "win": "Now you can look things up by name and count them in no time.",
    },
    "D08": {
        "title": "A tall stack of plates",
        "story": (
            "You stack plates one on top of another after washing them. You "
            "always take the top plate first, and that is the last plate you "
            "put down. A list can behave just like this stack of plates."
        ),
        "points": [
            "A stack is a list where you only touch the item on top.",
            "stack.append(x) puts a new thing on top.",
            "stack.pop() takes the top thing off and hands it to you.",
            "stack[-1] peeks at the top without removing it.",
            "Things come out in the opposite order to the way they went in.",
        ],
        "code": (
            "plates = []\n"
            "for plate in [\"red\", \"blue\", \"green\"]:\n"
            "    plates.append(plate)\n"
            "print(\"top plate:\", plates[-1])\n"
            "print(\"taking off:\", plates.pop())\n"
            "print(\"stack now:\", plates)"
        ),
        "win": "Now you can pile things up and take them off from the top.",
    },
    "D09": {
        "title": "A queue of people waiting",
        "story": (
            "People join the back of a line and leave from the front. The "
            "person who came first gets served first, and that is exactly what "
            "a queue does with your numbers at a shop."
        ),
        "points": [
            "A queue is a line. New people join at the back and leave at the front.",
            "The first person in is the first person out.",
            "Taking from the front of a normal list is slow, because everything shifts.",
            "deque is a special list that is fast at both ends.",
            "Use append() to add at the back and popleft() to take from the front.",
        ],
        "code": (
            "from collections import deque\n"
            "line = deque([\"Amit\", \"Bina\", \"Chandu\"])\n"
            "line.append(\"Deepa\")\n"
            "print(\"first in line:\", line.popleft())\n"
            "print(\"line now:\", list(line))"
        ),
        "win": "Now you can make a fair line where the first one in is first served.",
    },
    "D10": {
        "title": "Notes joined with arrows",
        "story": (
            "Instead of a row of boxes, imagine small notes. Each note holds a "
            "value and an arrow pointing to the next note. The last note points "
            "to nothing at all."
        ),
        "points": [
            "Each note holds a value and the name of the next note.",
            "The first note is the head. Follow the arrows to reach the end.",
            "The last note points to None, meaning nothing comes after it.",
            "You can add or remove notes without moving the other notes.",
            "To walk the notes, keep a pointer that follows the arrows.",
        ],
        "code": (
            "class Note:\n"
            "    def __init__(self, value, next_note=None):\n"
            "        self.value = value\n"
            "        self.next = next_note\n"
            "head = Note(1, Note(2, Note(3)))\n"
            "print(head.value, \"->\", head.next.value, \"->\", head.next.next.value)"
        ),
        "win": "Now you can chain notes together and follow the arrows to read them.",
    },
    "D11": {
        "title": "A robot that calls itself",
        "story": (
            "A robot can be given one small job: do a tiny step, then give the "
            "same job back to itself with a smaller problem. When the problem "
            "gets tiny the robot stops, and the answers build back up."
        ),
        "points": [
            "Recursion means a function calls itself with a smaller job.",
            "Every robot needs a stopping point, or it never stops.",
            "Backtracking means trying a choice, seeing if it works, and undoing it.",
            "Undoing means taking back the last choice you added.",
            "The robot tries many paths and keeps the ones that work.",
        ],
        "code": (
            "def try_it(word, path):\n"
            "    if not word: print(\"\".join(path)); return\n"
            "    path.append(word[0])\n"
            "    try_it(word[1:], path)\n"
            "    path.pop()\n"
            "try_it(\"abc\", [])"
        ),
        "win": "Now you can make a robot try choices and undo the ones that fail.",
    },
    "D12": {
        "title": "A family tree turned upside down",
        "story": (
            "A tree starts with one box at the top and grows branches down. "
            "Each branch holds a value, with all the smaller values on the left "
            "and all the bigger values on the right."
        ),
        "points": [
            "A tree grows downwards from a top box called the root.",
            "Each box holds a value and points to a left box and a right box.",
            "In a sorted tree, everything left is smaller and everything right is bigger.",
            "To search, go left if the number is smaller and right if it is bigger.",
            "To add a number, slide it down until it lands in the right empty spot.",
        ],
        "code": (
            "root = {\"v\": 10, \"left\": None, \"right\": None}\n"
            "root[\"left\"], root[\"right\"] = {\"v\": 5, \"left\": None, \"right\": None}, {\"v\": 15, \"left\": None, \"right\": None}\n"
            "node, target = root, 15\n"
            "while node is not None:\n"
            "    print(\"looking at\", node[\"v\"])\n"
            "    node = node[\"left\"] if target < node[\"v\"] else node[\"right\"]"
        ),
        "win": "Now you can grow a tree and walk down it to find a number.",
    },
    "D13": {
        "title": "A special tree that keeps the smallest on top",
        "story": (
            "Imagine a heap of toys where the smallest toy always sits on top, "
            "and everything below it is bigger than the toy above. Whenever "
            "you want a toy, you take the one on top."
        ),
        "points": [
            "A heap is a tree where the smallest item is always on top.",
            "Everything below is bigger than the toys sitting above it.",
            "A priority queue is a heap you push things into and pop the most important out.",
            "heapq is the Python toolbox that holds the heaps for you.",
            "heappush adds an item and heappop takes the smallest one away.",
        ],
        "code": (
            "import heapq\n"
            "jobs = []\n"
            "heapq.heappush(jobs, 5)\n"
            "heapq.heappush(jobs, 2)\n"
            "heapq.heappush(jobs, 9)\n"
            "print(\"smallest first:\", heapq.heappop(jobs))"
        ),
        "win": "Now you can keep a pile where the most important thing is always on top.",
    },
    "D14": {
        "title": "A city map of roads",
        "story": (
            "A city map shows places and the roads between them. Some roads go "
            "one way only. From any place you can ask a simple question: where "
            "can I go next?"
        ),
        "points": [
            "A graph is places (dots) joined together by roads (lines).",
            "A dictionary works well: each place keeps a list of its neighbours.",
            "A ring by ring search goes one step away, then two steps away.",
            "A deep search dives down one road before trying another.",
            "A visited set stops you from going round in circles for ever.",
        ],
        "code": (
            "roads = {\"A\": [\"B\", \"C\"], \"B\": [\"A\"], \"C\": [\"A\"]}\n"
            "seen, queue = set(), [\"A\"]\n"
            "while queue:\n"
            "    place = queue.pop(0); seen.add(place)\n"
            "    queue += [n for n in roads[place] if n not in seen]\n"
            "print(\"places reached:\", sorted(seen))"
        ),
        "win": "Now you can explore a map of roads and see every place you can reach.",
    },
    "D15": {
        "title": "Remembering the answers you already found",
        "story": (
            "Some puzzles ask you the same question over and over again. If you "
            "write each answer down the first time you find it, you can just "
            "read it from the notebook next time instead of doing all the work."
        ),
        "points": [
            "Some puzzles ask the same question again and again.",
            "Write each answer in a notebook the first time you find it.",
            "Next time the same question comes, just look in the notebook.",
            "This saves lots of work, so even big puzzles finish quickly.",
            "The notebook of saved answers is often called a memo.",
        ],
        "code": (
            "steps = {0: 1, 1: 1}\n"
            "for n in range(2, 8):\n"
            "    steps[n] = steps[n - 1] + steps[n - 2]\n"
            "print(\"ways to climb 6 stairs:\", steps[6])"
        ),
        "win": "Now you can reuse answers you already found instead of repeating the work.",
    },
    "D16": {
        "title": "Guessing the answer by halving",
        "story": (
            "Sometimes you do not know the answer, but you do know the smallest "
            "and biggest answer that could work. You test a middle guess and, "
            "depending on the result, throw away half of the possible answers."
        ),
        "points": [
            "First you decide the smallest and the biggest possible answer.",
            "You guess the middle one and check whether it works.",
            "If it works, throw away the bigger half. If not, throw away the smaller half.",
            "Keep going until only one answer is left.",
            "It is the same halving trick, but used to find an answer instead of a card.",
        ],
        "code": (
            "lo, hi = 1, 100\n"
            "while lo < hi:\n"
            "    mid = (lo + hi) // 2\n"
            "    if mid * mid <= 50: lo = mid + 1\n"
            "    else: hi = mid\n"
            "print(\"answer:\", lo)"
        ),
        "win": "Now you can find the right answer by halving the range again and again.",
    },
}
