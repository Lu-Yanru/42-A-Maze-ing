import random

from parse_config_file import Config
from maze_grid import Grid


class MazeDFS(Grid):
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    # added perfect maze generator
    def generate_maze_dfs(self) -> None:

        """
        Carves a perfect maze starting from `start` cell.
        Uses DFS iterative backtracker algorithm.
        """

        start = self.get_cell(self.entry[0], self.entry[1])
        if start is None:
            raise ValueError("Start cell cannot be None")
        if start.visited:
            raise ValueError("Start cell already visited")
        if start.is_42:
            raise ValueError("Start cell cannot be inside 42 pattern")

        # Set random seed
        if hasattr(self, "seed"):
            random.seed(self.seed)

        start.visited = True
        stack = [start]

        while stack:
            current = stack[-1]
            neighbors = self.get_unvisited_neighbors(current)
            if neighbors:
                # Choose a random neighbor
                neighbor, direction = random.choice(neighbors)
                # Remove wall between current and neighbor
                self.remove_wall_btw(current, direction)
                neighbor.visited = True
                stack.append(neighbor)
            else:
                # Backtrack
                stack.pop()
