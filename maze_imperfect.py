"""
MazeImperfect is a sublcass of Grid that makes a perfect maze imperfect
by removing some walls from the perfect maze.
"""
import random

from parse_config_file import Config
from maze_cell import Cell
from maze_grid import Grid
from maze_generator import MazeGenerator


class MazeImperfect(Grid):
    """
    A class used to generate the maze based on config.
    """
    def __init__(self: "MazeImperfect", config: Config,
                 maze: MazeGenerator) -> None:
        self.width = config.width
        self.height = config.height
        self.entry = config.entry
        self.exit = config.exit
        self.perfect = config.perfect
        if hasattr(config, "seed"):
            self.seed = config.seed
        if hasattr(config, "algo"):
            self.algo = config.algo
        self.grid = maze.grid

    def get_internal_walls(self: "MazeImperfect") -> list[tuple[Cell, int]]:
        """
        Get a list of wall remianing walls inside of the maze.
        Only count EAST and SOUTH to avoid double counting.
        """
        all_walls = []

        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]

                if cell.is_42:
                    continue

                for dir in [Cell.EAST, Cell.SOUTH]:
                    neighbor = self.get_neighbor(cell, dir)
                    if neighbor is None or neighbor.is_42:
                        continue
                    if cell.has_wall(dir):
                        all_walls.append((cell, dir))

        return all_walls

    def check_2x2(self: "MazeImperfect", cell: "Cell", dir: int) -> bool:
        """
        Check whether removing a wall will create a open area of 2x2
        by checking if the given wall is the only wall inside of the square.

        Args:
            cell (Cell): The top right cell of the square.
            dir (int): The direction of the wall to be checked.
            Can only be EAST or SOUTH to avoid double counting.

        Returns:
            bool: True if removing the wall will create a 2x2 open area.
            False if it would not.
        """
        (x, y) = cell.pos
        tr = self.get_neighbor(cell, Cell.EAST)
        if tr is None or tr.is_42:
            return False
        bl = self.get_neighbor(cell, Cell.SOUTH)
        if bl is None or bl.is_42:
            return False
        br = self.get_neighbor(bl, Cell.EAST)
        if br is None or br.is_42:
            return False
        if dir == Cell.EAST:
            if bl.has_wall(Cell.NORTH) or bl.has_wall(Cell.EAST) \
               or br.has_wall(Cell.NORTH):
                return False
        if dir == Cell.SOUTH:
            if tr.has_wall(Cell.WEST) or tr.has_wall(Cell.SOUTH) \
               or br.has_wall(Cell.WEST):
                return False
        return True

    def check_opening(self: "MazeImperfect", cell: Cell, dir: int) -> bool:
        """
        Check whether removing a wall will create a open area
        of 3x3 or larger.
        Uses check_2x2 to check 2 neighboring squares.

        Returns:
            bool: True if removing the wall will create a large open area.
            False if it would not.
        """
        (x, y) = cell.pos
        if dir == Cell.SOUTH:
            res_right = self.check_2x2(cell, dir)
            cell_left = self.get_neighbor(cell, Cell.WEST)
            if cell_left is None:
                return False
            res_left = self.check_2x2(cell_left, dir)
            return res_right or res_left
        elif dir == Cell.WEST:
            res_down = self.check_2x2(cell, dir)
            cell_top = self.get_neighbor(cell, Cell.NORTH)
            if cell_top is None:
                return False
            res_top = self.check_2x2(cell_top, dir)
            return res_down or res_top
        return True

    def make_imperfect(self: "MazeImperfect", rate: float = 0.1) -> None:
        """
        Make a perfect maze imperfect by removing 10% of the remaining walls.
        """
        all_walls = self.get_internal_walls()

        if hasattr(self, "seed"):
            random.seed(self.seed)
        random.shuffle(all_walls)

        num_to_remove = int(len(all_walls) * rate)
        num_removed = 0
        for cell, dir in all_walls:
            if num_removed >= num_to_remove:
                break

            if not self.check_opening(cell, dir):
                self.remove_wall_btw(cell, dir)
                num_removed += 1
