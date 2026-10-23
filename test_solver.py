import unittest

from maze import MazeGenerator
from solver import MazeSolver


class TestMazeProject(unittest.TestCase):

    def setUp(self):
        """Creates a 31x31 maze before each test."""
        self.generator = MazeGenerator(width=31, height=31)
        self.maze = self.generator.generate()
        self.solver = MazeSolver(self.generator)
        self.start = (1, 1)
        self.goal = (29, 29)

    def assertValidPath(
        self,
        path: list[tuple[int, int]],
        start: tuple[int, int],
        goal: tuple[int, int],
    ):
        """Verifies that a path is continuous and only walks on MazeGenerator.EMPTY."""
        self.assertTrue(len(path) > 0, "Path should not be empty.")
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], goal)

        for i, cell in enumerate(path):
            self.assertEqual(
                self.maze[cell],
                MazeGenerator.EMPTY,
                f"Walked into a wall at {cell}",
            )
            if i > 0:
                prev = path[i - 1]
                dist = abs(cell[0] - prev[0]) + abs(cell[1] - prev[1])
                self.assertEqual(
                    dist, 1, f"Non-adjacent step from {prev} to {cell}"
                )

    def test_generator_validation(self):
        """Tests the ValueError in your MazeGenerator.__init__."""
        with self.assertRaises(ValueError):
            MazeGenerator(10, 11)  # Even width should fail
        with self.assertRaises(ValueError):
            MazeGenerator(1, 5)  # Size < 3 should fail

    def test_greedy_bfs_invalid_start_or_goal(self):
        # (0, 0) is always a border wall
        self.assertEqual(self.solver.solve_greedy_bfs((0, 0), self.goal), [])
        self.assertEqual(self.solver.solve_greedy_bfs(self.start, (0, 0)), [])

    def test_bfs_valid_path(self):
        path = self.solver.solve_bfs(self.start, self.goal)
        self.assertValidPath(path, self.start, self.goal)

    
    def test_dfs_valid_path(self):
        path = self.solver.solve_dfs(self.start, self.goal)
        self.assertValidPath(path, self.start, self.goal)

    def test_astar_valid_path(self):
        path = self.solver.solve_astar(self.start, self.goal)
        self.assertValidPath(path, self.start, self.goal)


if __name__ == "__main__":
    unittest.main(verbosity=2)
