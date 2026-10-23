import heapq

from maze import MazeGenerator

from collections import deque

class MazeSolver:

    def __init__(self, generator: MazeGenerator):
        if not generator.maze:
            generator.generate()
        self.maze = generator.maze
        self.width = generator.width
        self.height = generator.height

    # Shared helper method
    def get_neighbors(self, pos: tuple[int, int]) -> list[tuple[int, int]]:
        '''Returns walkable (EMPTY) adjacent cells.'''
        x, y = pos
        neighbors = []
        # North (-1, 0), South (+1, 0), West (0, -1), East (0, +1)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < self.height
                and 0 <= ny < self.width
                and self.maze.get((nx, ny)) == MazeGenerator.EMPTY
            ):
                neighbors.append((nx, ny))
        return neighbors

    def reconstruct_path(
        self,
        came_from: dict[tuple[int, int], tuple[int, int]],
        current: tuple[int, int],
    ) -> list[tuple[int, int]]:
        """Traces the path from goal back to start."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def heuristic(self, a: tuple[int, int], b: tuple[int, int]) -> int:
        """Manhattan distance: |x1 - x2| + |y1 - y2|."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    

    def solve_greedy_bfs(
        self, start: tuple[int, int], goal: tuple[int, int])-> list[tuple[int, int]]:
        """Solves the maze using Greedy Best-First Search."""
        if (self.maze.get(start) != MazeGenerator.EMPTY
        or self.maze.get(goal) != MazeGenerator.EMPTY):
            return []

        frontier = []
        heapq.heappush(frontier, (self.heuristic(start, goal), start))

        came_from: dict[tuple[int, int], tuple[int, int]] = {}
        visited = {start}

        while frontier:
            _, current = heapq.heappop(frontier)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    h_score = self.heuristic(neighbor, goal)
                    heapq.heappush(frontier, (h_score, neighbor))

        return []

    
    def solve_bfs(
        self, start: tuple[int, int], goal: tuple[int, int]
    ) -> list[tuple[int, int]]:
        if (
            self.maze.get(start) != MazeGenerator.EMPTY
            or self.maze.get(goal) != MazeGenerator.EMPTY
        ):
            return []
    
        queue = deque([start])
        visited = {start}
        came_from: dict[tuple[int, int], tuple[int, int]] = {}
    
        while queue:
            current = queue.popleft()
    
            if current == goal:
                return self.reconstruct_path(came_from, current)
    
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)
    
        return []


    def solve_dfs(
        self, start: tuple[int, int], goal: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Solves the maze using Depth-First Search (DFS)."""
        if (self.maze.get(start) != MazeGenerator.EMPTY
                or self.maze.get(goal) != MazeGenerator.EMPTY):
            return []

        stack = [start]
        came_from: dict[tuple[int, int], tuple[int, int]] = {}
        visited = set()

        while stack:
            current = stack.pop()

            if current in visited:
                continue
            visited.add(current)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    came_from[neighbor] = current
                    stack.append(neighbor)

        return []

    def solve_astar(
        self, start: tuple[int, int], goal: tuple[int, int]
    ) -> list[tuple[int, int]]:
        #start/goal là tường
        if self.maze.get(start) != MazeGenerator.EMPTY or self.maze.get(goal) != MazeGenerator.EMPTY:
            return []

        #heapq(f_score, ô)
        frontier = []
        heapq.heappush(frontier, (self.heuristic(start, goal), start))
        came_from: dict[tuple[int, int], tuple[int, int]] = {}
        g_score: dict[tuple[int, int], int] = {start: 0}
        visited = set()

        while frontier:
            _, current = heapq.heappop(frontier)
            if current == goal:
                return self.reconstruct_path(came_from, current)

            if current in visited:
                continue
            visited.add(current)

            for neighbor in self.get_neighbors(current):
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + self.heuristic(neighbor, goal)
                    heapq.heappush(frontier, (f_score, neighbor))
        return []