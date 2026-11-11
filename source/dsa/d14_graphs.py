"""
DSA 14 - Graphs (adjacency list, BFS, DFS)
=========================================

Today's goal:
  1. Store a graph as a dict: node -> list of neighbours
  2. Walk the graph with BFS (queue) and DFS (go deep)
  3. Count connected components
  4. Find the shortest path in an unweighted graph
  5. Detect a cycle
  6. Order the nodes of a DAG with a topological sort (Kahn's algorithm)
What is a graph?
  Nodes (places) and edges (roads). We store it with an adjacency list:
  graph = {"A": ["B", "C"], "B": ["D"], "C": ["D", "E"], "D": ["E"], "E": []}
  graph["A"] -> ["B", "C"] means "A is connected to B and C". For an
  undirected graph put each neighbour in both lists.
Two ways to walk a graph:
  BFS (breadth first search) - use a queue, go level by level. It finds
      the shortest path when every edge costs the same.
  DFS (depth first search) - go as deep as possible, then come back.
The BFS skeleton (the `seen` set stops us from walking in circles):
```python
from collections import deque

def bfs_order(graph, start):
    order, seen, queue = [], {start}, deque([start])
    while queue:
        node = queue.popleft()      # take the oldest one
        order.append(node)
        for nei in graph.get(node, []):
            if nei not in seen:
                seen.add(nei)        # mark it right away
                queue.append(nei)
    return order
```
Shortest path with BFS:
  Every edge counts as 1 step, and BFS visits nodes level by level, so
  the first time we reach the target we used the fewest possible edges.
Cycle detection (directed graphs):
  We colour every node while we walk: 0 = not visited, 1 = we are inside
  it right now, 2 = it is finished. Meeting a colour 1 node means the
  path came back to itself, so there is a cycle.
Topological sort (Kahn's algorithm):
  This only works for a DAG (a graph with no cycles). We keep the nodes
  with no unprocessed parent (in-degree 0), take them one by one and
  delete their edges. If some nodes are left over, we have a cycle.

Complexity in simple words:
  Everything here is O(V + E) - every node once, every edge once. The
  space we need is O(V) for the queue, stack and seen set.
Tip: when you read a graph question, always ask two things:
  1. Is the graph directed or undirected?
  2. Do all edges have the same cost?
  If yes -> BFS finds the shortest path. If not, use Dijkstra instead.
"""

import heapq
from collections import deque

from _dsa_kit import main


# ---------------------------------------------------------------------------
# DEMOS - run these first, then change the code and experiment
# ---------------------------------------------------------------------------


def demo_build_graph_and_bfs() -> None:
    # First we build the adjacency list, then we walk it with a queue.
    edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")]
    graph: dict[str, list[str]] = {}
    for u, v in edges:
        graph.setdefault(u, []).append(v)
        graph.setdefault(v, []).append(u)   # the road works both ways
    print("adjacency list:", graph)
    queue, seen, order = deque(["A"]), {"A"}, []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nei in graph.get(node, []):
            if nei not in seen:
                seen.add(nei)
                queue.append(nei)
    print("BFS order from A:", order, "- A, then B and C, then their neighbours.")


def demo_dfs_order() -> None:
    graph = {"A": ["B", "C"], "B": ["D"], "C": ["D", "E"], "D": ["E"], "E": []}
    order, seen = [], set()
    def walk(node: str) -> None:
        seen.add(node)
        order.append(node)
        for nei in graph.get(node, []):
            if nei not in seen:
                walk(nei)

    walk("A")
    print("DFS order from A:", order)


def demo_count_components() -> None:
    graph = {"A": ["B"], "B": ["A"], "C": ["D"], "D": ["C"], "E": [], "F": []}
    seen, components = set(), 0
    for node in sorted(graph):
        if node in seen:
            continue
        components += 1
        stack = [node]
        seen.add(node)
        while stack:
            for nei in graph.get(stack.pop(), []):
                if nei not in seen:
                    seen.add(nei)
                    stack.append(nei)
    print("connected components:", components)


def demo_shortest_path() -> None:
    graph = {"A": ["B", "C"], "B": ["D"], "C": ["D", "E"], "D": ["E"], "E": []}
    start, target = "A", "E"
    seen, queue, answer = {start}, deque([(start, 0)]), -1
    while queue and answer == -1:
        node, steps = queue.popleft()
        for nei in graph.get(node, []):
            if nei in seen:
                continue
            seen.add(nei)
            if nei == target:
                answer = steps + 1
                break
            queue.append((nei, steps + 1))
    print(f"shortest path {start} -> {target}: {answer} edges (A -> C -> E)")


def demo_cycle_and_topological_sort() -> None:
    graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": ["E"], "E": []}
    colour = {node: 0 for node in graph}
    def has_cycle(node: str) -> bool:
        colour[node] = 1
        for nei in graph.get(node, []):
            if colour.get(nei, 0) == 1:
                return True
            if colour.get(nei, 0) == 0 and has_cycle(nei):
                return True
        colour[node] = 2
        return False

    cycle = any(has_cycle(node) for node in graph if colour.get(node, 0) == 0)
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for nei in graph.get(node, []):
            in_degree[nei] = in_degree.get(nei, 0) + 1
    ready = [node for node in in_degree if in_degree[node] == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        node = heapq.heappop(ready)
        order.append(node)
        for nei in graph.get(node, []):
            in_degree[nei] -= 1
            if in_degree[nei] == 0:
                heapq.heappush(ready, nei)
    print("has a cycle?", cycle)
    print("topological order:", order)


# ---------------------------------------------------------------------------
# EXERCISES - write your code where you see TODO
# ---------------------------------------------------------------------------


def bfs_order(graph: dict, start) -> list:
    """Visit the graph level by level and return the nodes in that order.
    bfs_order({"A": ["B"], "B": []}, "A") -> ["A", "B"]
    """
    # TODO: use a queue (collections.deque) and a seen set
    return None

def dfs_order(graph: dict, start) -> list:
    """Go deep first, then come back, and return the nodes in that order.
    dfs_order({"A": ["B"], "B": ["C"], "C": []}, "A") -> ["A", "B", "C"]
    """
    # TODO: use recursion (or a stack) and a seen set
    return None

def count_components(graph: dict) -> int:
    """Count how many separate groups of connected nodes the graph has.
    count_components({"A": ["B"], "B": ["A"], "C": []}) -> 2
    """
    # TODO: run a DFS from every node that was not visited yet
    return None

def shortest_path(graph: dict, start, target) -> int:
    """Number of edges on the shortest path, or -1 when there is no path.
    shortest_path({"A": ["B"], "B": ["C"], "C": []}, "A", "C") -> 2
    """
    # TODO: use BFS and remember how many steps each node needs
    return None

def has_cycle(graph: dict) -> bool:
    """True when the directed graph has a cycle (A -> B -> A).
    has_cycle({"A": ["B"], "B": ["A"]}) -> True
    """
    # TODO: use DFS with three colours (not visited / inside / done)
    return None

def topological_order(graph: dict) -> list:
    """Nodes in a valid order, or [] when the graph has a cycle.
    topological_order({"A": ["B"], "B": []}) -> ["A", "B"]
    """
    # TODO: Kahn's algorithm - repeatedly take a node with in-degree 0
    return None

def degree_of(graph: dict, node) -> int:
    """How many neighbours this node has (0 when the node is unknown).
    degree_of({"A": ["B", "C"], "B": ["A"], "C": ["A"]}, "A") -> 2
    """
    # TODO: count the entries in graph[node]
    return None

def neighbors_of(graph: dict, node) -> list:
    """The neighbours of this node, sorted from small to large.
    neighbors_of({"A": ["C", "B"]}, "A") -> ["B", "C"]
    """
    # TODO: return a sorted copy of graph[node] (empty list if unknown)
    return None


# Solutions - try it yourself first, then run with `--solutions`
def sol_bfs_order(graph: dict, start) -> list:
    order, seen, queue = [], {start}, deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for nei in graph.get(node, []):
            if nei not in seen:
                seen.add(nei)
                queue.append(nei)
    return order

def sol_dfs_order(graph: dict, start) -> list:
    order, seen = [], set()
    def walk(node) -> None:
        seen.add(node)
        order.append(node)
        for nei in graph.get(node, []):
            if nei not in seen:
                walk(nei)
    walk(start)
    return order

def sol_count_components(graph: dict) -> int:
    seen, count = set(), 0
    for node in graph:
        if node in seen:
            continue
        count += 1
        stack = [node]
        seen.add(node)
        while stack:
            for nei in graph.get(stack.pop(), []):
                if nei not in seen:
                    seen.add(nei)
                    stack.append(nei)
    return count

def sol_shortest_path(graph: dict, start, target) -> int:
    if start == target:
        return 0
    seen, queue = {start}, deque([(start, 0)])
    while queue:
        node, steps = queue.popleft()
        for nei in graph.get(node, []):
            if nei in seen:
                continue
            seen.add(nei)
            if nei == target:
                return steps + 1
            queue.append((nei, steps + 1))
    return -1

def sol_has_cycle(graph: dict) -> bool:
    colour = {node: 0 for node in graph}      # 0 = new, 1 = inside, 2 = done

    def walk(node) -> bool:
        colour[node] = 1
        for nei in graph.get(node, []):
            if colour.get(nei, 0) == 1:
                return True
            if colour.get(nei, 0) == 0 and walk(nei):
                return True
        colour[node] = 2
        return False
    return any(walk(node) for node in graph if colour.get(node, 0) == 0)

def sol_topological_order(graph: dict) -> list:
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for nei in graph.get(node, []):
            in_degree[nei] = in_degree.get(nei, 0) + 1
    ready = [node for node in in_degree if in_degree[node] == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        node = heapq.heappop(ready)
        order.append(node)
        for nei in graph.get(node, []):
            in_degree[nei] -= 1
            if in_degree[nei] == 0:
                heapq.heappush(ready, nei)
    return order if len(order) == len(in_degree) else []

def sol_degree_of(graph: dict, node) -> int:
    return len(graph.get(node, []))

def sol_neighbors_of(graph: dict, node) -> list:
    return sorted(graph.get(node, []))


EXERCISES = [
    {
        "id": "14.1", "task": "bfs_order(graph, start): visit the graph level by level",
        "func": bfs_order,
        "tests": [(({"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}, "A"), ["A", "B", "C", "D"]), (({"A": []}, "A"), ["A"])],
        "solution": sol_bfs_order,
    },
    {
        "id": "14.2", "task": "dfs_order(graph, start): go deep first, then come back",
        "func": dfs_order,
        "tests": [(({"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}, "A"), ["A", "B", "D", "C"]), (({"A": []}, "A"), ["A"])],
        "solution": sol_dfs_order,
    },
    {
        "id": "14.3", "task": "count_components(graph): count the separate connected groups",
        "func": count_components,
        "tests": [(({"A": ["B"], "B": ["A"], "C": ["D"], "D": ["C"], "E": []},), 3), (({},), 0)],
        "solution": sol_count_components,
    },
    {
        "id": "14.4", "task": "shortest_path(graph, start, target): fewest edges, or -1",
        "func": shortest_path,
        "tests": [(({"A": ["B", "C"], "B": ["D"], "C": ["D", "E"], "D": ["E"], "E": []}, "A", "E"), 2), (({"A": ["B"], "B": []}, "A", "Z"), -1)],
        "solution": sol_shortest_path,
    },
    {
        "id": "14.5", "task": "has_cycle(graph): True when A can reach A again",
        "func": has_cycle,
        "tests": [(({"A": ["B"], "B": ["C"], "C": ["A"]},), True), (({"A": ["B"], "B": []},), False), (({"A": ["A"]},), True)],
        "solution": sol_has_cycle,
    },
    {
        "id": "14.6", "task": "topological_order(graph): a valid node order, or [] for a cycle",
        "func": topological_order,
        "tests": [(({"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []},), ["A", "B", "C", "D"]), (({"A": ["B"], "B": ["A"]},), [])],
        "solution": sol_topological_order,
    },
    {
        "id": "14.7", "task": "degree_of(graph, node): how many neighbours the node has",
        "func": degree_of,
        "tests": [(({"A": ["B", "C"], "B": ["A"], "C": ["A"]}, "A"), 2), (({"A": []}, "Z"), 0)],
        "solution": sol_degree_of,
    },
    {
        "id": "14.8", "task": "neighbors_of(graph, node): the sorted neighbours of the node",
        "func": neighbors_of,
        "tests": [(({"A": ["C", "B"], "B": ["A"], "C": ["A"]}, "A"), ["B", "C"]), (({}, "A"), [])],
        "solution": sol_neighbors_of,
    },
]

DEMOS = [
    ("1. Build an adjacency list, then BFS it", demo_build_graph_and_bfs),
    ("2. DFS order (go deep)", demo_dfs_order),
    ("3. Count connected components", demo_count_components),
    ("4. Shortest path with BFS", demo_shortest_path),
    ("5. Cycle detection + topological sort", demo_cycle_and_topological_sort),
]

if __name__ == "__main__":
    main(DEMOS, EXERCISES)
