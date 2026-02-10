"""
MazePrim class that generates a maze using Prim's algorithm.
"""


import random

from parse_config_file import Config, ConfigError
from maze_grid import Grid


class MazePrim(Grid):
    """
    Subclass of Grid.
    Creates a maze using Prim's algorithm.
    """
    def __init__(self: "MazePrim", config: Config) -> None:
        super().__init__(config)

    def generate_maze_prim(self: "MazePrim") -> None:
        """
        A function the generate a maze using Prim's algorithm.

        Args:
        start: The entry cell.
        """

        # Set random seed
        if hasattr(self, "seed"):
            random.seed(self.seed)

        # Start from the entry cell
        start = self.get_cell(self.entry[0], self.entry[1])
        if start is None:
            raise ConfigError("Start cell cannot be None")
        if start.visited:
            raise ConfigError("Start cell already visited")
        if start.is_42:
            raise ConfigError("Start cell cannot be inside 42 pattern")

        start.visited = True
        # Get frontier
        frontier = self.get_unvisited_neighbors(start)
        while frontier:
            # Randomly pick an cell from the frontier to go next
            (new_cell, dir) = random.choice(frontier)
            frontier.remove((new_cell, dir))

            # Skip if the new_cell has already been visited
            if new_cell.visited:
                continue

            # Rnadomly choose a visited neighbor of the selected frontier cell
            neighbors = self.get_visited_neighbors(new_cell)
            # if neighbors is None:
            #    continue
            (neighbor, direction) = random.choice(neighbors)

            # Remove wall btw new_cell and visited neighbor
            self.remove_wall_btw(new_cell, direction)

            # Mark new_cell as visited
            new_cell.visited = True

            # Add the unvisted neighbors of the new cell to the frontier
            # without duplicates
            # new_frontier = self.get_unvisited_neighbors(new_cell)
            # frontier = list(set(frontier + new_frontier))
            frontier.extend(self.get_unvisited_neighbors(new_cell))
