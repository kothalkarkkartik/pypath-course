"""
DSA 09 - Queues and deques
==========================

Today's goal:
  1. Understand the queue: first in, first out (FIFO)
  2. Use collections.deque instead of a plain list
  3. Run a BFS (breadth first search) with a queue
  4. Learn the sliding window maximum and the circular buffer

What is a queue?
  A queue is a line at a ticket counter. The person who arrives first is
  served first: FIFO = First In, First Out. A plain list is a poor queue,
  because q.pop(0) is slow. A deque is fast at both ends.

Use collections.deque:
```python
from collections import deque

q = deque()
q.append(10)        # join the back of the line
q.popleft()         # serve the first person (fast!)
q.appendleft(5)     # jump to the front of the line
q[0]                # look at the front without removing it
```
append and popleft are O(1) - instant, nothing has to move.

Three operations to remember: append(x) joins the back of the line,
popleft() serves the first person and q[0] peeks at the front.

A queue is the right tool when the ORDER of the work matters: BFS level
by level (that finds shortest paths!), printing jobs, and waiting tasks.

BFS in four steps: put the start node in the queue, take the first node
out, add every unseen neighbour, and repeat until the queue is empty.

Sliding window maximum: keep a deque of indexes whose values go from
big to small. The front of that deque is always the biggest value of
the window. This is O(n): every value goes in and out of the deque once.

A circular buffer (ring buffer) is a fixed size list where the end is
joined back to the front, so a head index and a tail index can travel
round and round.

Time complexity in plain words:
  append / popleft   -> O(1), instant
  one full pass      -> O(n)
  a full BFS         -> O(V + E), every node and every edge once

Tip: when you read "level by level", "shortest path" or "in order", think
of a queue. When you read "last one first" or "undo", think of a stack
(chapter 8).
"""

from collections import deque
import heapq

from _dsa_kit import main


# ---------------------------------------------------------------------------
# DEMOS - run these first, then change the code and experiment
# ---------------------------------------------------------------------------


def demo_fifo_queue() -> None:
    # First in, first out: join the back, serve the front.
    queue = deque()
    for name in ["Ana", "Ben", "Cai"]:
        queue.append(name)
        print(f"{name} joins the line -> {list(queue)}")
    while queue:
        person = queue.popleft()
        print(f"{person} is served -> line left: {list(queue)}")


def demo_bfs_levels() -> None:
    # A queue explores a graph level by level.
    graph = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"], "D": [], "E": [], "F": []}
    visited = {"A"}
    queue = deque(["A"])
    level = 0
    while queue:
        level += 1
        size = len(queue)
        current = []
        for _ in range(size):
            node = queue.popleft()
            current.append(node)
            for neighbour in graph.get(node, []):
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
        print(f"level {level}: {current}")


def demo_sliding_window_max() -> None:
    # A monotonic deque keeps the biggest value of the window at the front.
    arr = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    window = deque()       # indexes, values from big to small
    result = []
    for i, value in enumerate(arr):
        if window and window[0] <= i - k:
            window.popleft()            # the oldest index left the window
        while window and arr[window[-1]] < value:
            window.pop()                # this small value is never the max
        window.append(i)
        if i >= k - 1:
            result.append(arr[window[0]])
            print(f"window {arr[i - k + 1:i + 1]} -> max {arr[window[0]]}")
    print("all the window maxima:", result)


def demo_circular_buffer() -> None:
    # A ring buffer of size 4: the end is joined back to the front.
    size = 4
    buffer = [None] * size
    head = 0          # where the next item goes in
    tail = 0          # where the next item comes out
    count = 0
    for item in [1, 2, 3, 4, 5]:
        if count == size:
            print(f"push {item} -> buffer full!")
            continue
        buffer[head] = item
        head = (head + 1) % size
        count += 1
        print(f"push {item} -> slots {buffer}, count {count}")
    item = buffer[tail]
    buffer[tail] = None
    tail = (tail + 1) % size
    count -= 1
    print("pop ->", item, "slots", buffer)


def demo_priority_task_queue() -> None:
    # heapq gives us the smallest item first: that is a priority queue.
    tasks = []
    for name, priority in [("write code", 3), ("fix bug", 1), ("send email", 2)]:
        heapq.heappush(tasks, (priority, name))
        print(f"added task {name!r} with priority {priority}")
    while tasks:
        priority, name = heapq.heappop(tasks)
        print(f"now working on {name!r} (priority {priority})")


def demo_rotate_queue() -> None:
    # Rotating a queue means moving items from the front to the back.
    queue = deque([1, 2, 3, 4, 5])
    print("start          :", list(queue))
    for _ in range(2):
        queue.append(queue.popleft())
    print("after 2 turns  :", list(queue), "- one move per turn is O(k)")


# ---------------------------------------------------------------------------
# EXERCISES - write your code where you see TODO
# ---------------------------------------------------------------------------


def sliding_window_max(arr: list, k: int) -> list:
    """Return the biggest value of every window of size k.

    sliding_window_max([1, 3, -1, -3, 5], 3) -> [3, 3, 5]
    """
    # TODO: keep a deque of indexes whose values go from big to small
    return None


def bfs_levels(graph: dict, start) -> list:
    """Return the levels of the graph as lists (a dict of node -> neighbours).

    bfs_levels({"A": ["B"], "B": []}, "A") -> [["A"], ["B"]]
    """
    # TODO: use a deque and save the size of the queue for every level
    return None


def simulate_queue(operations: list) -> list:
    """Run the queue commands and collect the answer of every question.

    Commands: "enqueue X", "dequeue", "front", "back".
    simulate_queue(["enqueue 1", "enqueue 2", "front"]) -> [1]
    """
    # TODO: keep one deque and answer the "front" and "back" commands
    return None


def rotate_queue(items: list, k: int) -> list:
    """Turn the queue k times to the left (a negative k turns to the right).

    rotate_queue([1, 2, 3, 4, 5], 2) -> [3, 4, 5, 1, 2]
    """
    # TODO: move the first item to the back k times
    return None


def queue_size_after_ops(operations: list) -> int:
    """Return how many items are in the queue after running the commands.

    Commands: "enqueue X" and "dequeue".
    queue_size_after_ops(["enqueue 1", "enqueue 2", "dequeue"]) -> 1
    """
    # TODO: keep a deque and count what is left at the end
    return None


def bfs_shortest_path(graph: dict, start, target) -> int:
    """Return how many edges the shortest path has, or -1 if there is none.

    bfs_shortest_path({"A": ["B"], "B": []}, "A", "B") -> 1
    """
    # TODO: use a deque and remember the distance of every node
    return None


# Solutions - try it yourself first, then run with `--solutions`
def sol_sliding_window_max(arr: list, k: int) -> list:
    if k <= 0 or k > len(arr):
        return []
    window = deque()      # indexes, values from big to small
    result = []
    for i, value in enumerate(arr):
        if window and window[0] <= i - k:
            window.popleft()
        while window and arr[window[-1]] < value:
            window.pop()
        window.append(i)
        if i >= k - 1:
            result.append(arr[window[0]])
    return result


def sol_bfs_levels(graph: dict, start) -> list:
    levels = []
    visited = {start}
    queue = deque([start])
    while queue:
        size = len(queue)          # how many nodes are in this level
        level = []
        for _ in range(size):
            node = queue.popleft()
            level.append(node)
            for neighbour in graph.get(node, []):
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
        levels.append(level)
    return levels


def sol_simulate_queue(operations: list) -> list:
    queue = deque()
    answers = []
    for op in operations:
        parts = op.split()
        if parts[0] == "enqueue":
            queue.append(int(parts[1]))
        elif parts[0] == "dequeue" and queue:
            queue.popleft()
        elif parts[0] == "front":
            answers.append(queue[0] if queue else None)
        elif parts[0] == "back":
            answers.append(queue[-1] if queue else None)
    return answers


def sol_rotate_queue(items: list, k: int) -> list:
    queue = deque(items)
    if not queue:
        return []
    for _ in range(k % len(queue)):
        queue.append(queue.popleft())
    return list(queue)


def sol_queue_size_after_ops(operations: list) -> int:
    queue = deque()
    for op in operations:
        parts = op.split()
        if parts[0] == "enqueue":
            queue.append(int(parts[1]))
        elif parts[0] == "dequeue" and queue:
            queue.popleft()
    return len(queue)


def sol_bfs_shortest_path(graph: dict, start, target) -> int:
    if start == target:
        return 0
    distance = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbour in graph.get(node, []):
            if neighbour not in distance:
                distance[neighbour] = distance[node] + 1
                if neighbour == target:
                    return distance[neighbour]
                queue.append(neighbour)
    return -1


EXERCISES = [
    {
        "id": "9.1",
        "task": "sliding_window_max(arr, k): the biggest value of every window",
        "func": sliding_window_max,
        "tests": [(([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7]), (([1], 1), [1]), (([1, 2, 3], 5), [])],
        "solution": sol_sliding_window_max,
    },
    {
        "id": "9.2",
        "task": "bfs_levels(graph, start): the levels of the graph",
        "func": bfs_levels,
        "tests": [(({"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}, "A"), [["A"], ["B", "C"], ["D"]]), (({"A": ["B"], "B": []}, "A"), [["A"], ["B"]])],
        "solution": sol_bfs_levels,
    },
    {
        "id": "9.3",
        "task": 'simulate_queue(operations): answer every "front" and "back" command',
        "func": simulate_queue,
        "tests": [((["enqueue 1", "enqueue 2", "front", "dequeue", "front", "back"],), [1, 2, 2]), ((["enqueue 5", "front"],), [5])],
        "solution": sol_simulate_queue,
    },
    {
        "id": "9.4",
        "task": "rotate_queue(items, k): turn the queue k times to the left",
        "func": rotate_queue,
        "tests": [(([1, 2, 3, 4, 5], 2), [3, 4, 5, 1, 2]), (([1, 2, 3], 0), [1, 2, 3]), (([1, 2, 3], -1), [3, 1, 2]), (([], 3), [])],
        "solution": sol_rotate_queue,
    },
    {
        "id": "9.5",
        "task": "queue_size_after_ops(operations): how many items are left",
        "func": queue_size_after_ops,
        "tests": [((["enqueue 1", "enqueue 2", "dequeue"],), 1), (([],), 0), ((["dequeue"],), 0)],
        "solution": sol_queue_size_after_ops,
    },
    {
        "id": "9.6",
        "task": "bfs_shortest_path(graph, start, target): edges on the shortest path",
        "func": bfs_shortest_path,
        "tests": [(({"A": ["B", "C"], "B": ["D"], "C": [], "D": []}, "A", "D"), 2), (({"A": ["B"], "B": []}, "A", "Z"), -1)],
        "solution": sol_bfs_shortest_path,
    },
]

DEMOS = [
    ("1. A FIFO queue", demo_fifo_queue),
    ("2. BFS level by level", demo_bfs_levels),
    ("3. Sliding window maximum", demo_sliding_window_max),
    ("4. A circular buffer", demo_circular_buffer),
    ("5. A task queue with priorities", demo_priority_task_queue),
    ("6. Turning a queue", demo_rotate_queue),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
