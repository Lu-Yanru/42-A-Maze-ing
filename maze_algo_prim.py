"""
MazePrim class that generates a maze using Prim's algorithm.
"""


import random

from parse_config_file import Config
from maze_grid import Cell, Grid


class MazePrim(Grid):
    """
    Subclass of Grid.
    Creates a maze using Prim's algorithm.
    """
    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def generate_maze_prim(self, start: Cell) -> None:
        """
        A function the generate a maze using Prim's algorithm.

        Args:
        start: The entry cell.
        """
        start.visited = True
        # Get frontier
        frontier = self.get_unvisited_neighbors(start)
        while frontier:
            # Randomly pick an cell fron the frontier to go next
            (new_cell, dir) = random.choice(frontier)
            frontier.remove((new_cell, dir))
            # Only proceed wall if the new cell is still unvisited
            if not new_cell.visited:
                self.remove_wall_btw(new_cell,
                                     self.get_opposite_direction(dir))
                new_cell.visited = True
                # Add the unvisted neighbors of the new cell to the frontier
                # only if they are not already in the frontier
                new_frontier = self.get_unvisited_neighbors(new_cell)
                for cell in new_frontier:
                    if cell not in frontier:
                        frontier.append(cell)
