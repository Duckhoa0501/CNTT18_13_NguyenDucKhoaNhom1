from heapq import heappush, heappop
from src.core_logic import get_start_goal, get_neighbors

def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_step(maze):
    start, goal = get_start_goal(maze)

    open_set = []
    heappush(open_set, (0, start, [start]))

    g_cost = {start: 0}
    visited = set()

    while open_set:
        _, current, path = heappop(open_set)

        if current in visited:
            continue

        visited.add(current)

        yield current, path, visited

        if current == goal:
            return

        for neighbor in get_neighbors(maze, current):
            new_cost = g_cost[current] + 1

            if neighbor not in g_cost or new_cost < g_cost[neighbor]:
                g_cost[neighbor] = new_cost
                f_cost = new_cost + heuristic(neighbor, goal)
                heappush(open_set, (f_cost, neighbor, path + [neighbor]))