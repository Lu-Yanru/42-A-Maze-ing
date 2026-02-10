"""
Generate a grid with all closed cells and a 42 pattern in the center.
Classes:
Grid -- a 2D array, each element is a Cell.
Cell --  a cell in the grid with 4 walls,
represented as an interger from 0 to 15.
"""


import random

from parse_config_file import Config, ConfigError


class Cell:
    """
    A class that represents a cell.
    A cell is an interger from 0 to 15,
    where the last 4 bits represents the walls,
    The walls are each represented by 1 bit.
    0 means the wall is open, 1 means the wall is closed.
    The north wall is the first bit (LSB),
    the east wall is the second bit,
    the south wall is the third bit,
    the west wall is the 4th bit.
    """

    # Constants for wall directions
    NORTH = 1  # 0001
    EAST = 2  # 0010
    SOUTH = 4  # 0100
    WEST = 8  # 1000

    def __init__(self: "Cell", pos: tuple, visited: bool = False,
                 walls: int = 15, is_42: bool = False) -> None:
        """
        Creates a cell.

        Args:
            pos (tuple): The position pf the cell (x, y).
            visited (bool): Whether the cell has been visited. Default false.
            walls (int): Value that represents the status of the 4 walls.
                         Default 15, all 4 walls closed.
            is_42 (bool): Whether the cell is part of the 42 pattern.
                         Default false.
        """
        self.pos = pos
        self.visited = visited
        self.walls = walls
        self.is_42 = is_42

    @classmethod
    def get_dirs(cls: "type[Cell]") -> list[int]:
        """Returns a list of all directions."""
        return [cls.NORTH, cls.EAST, cls.SOUTH, cls.WEST]

    def has_wall(self: "Cell", direction: int) -> bool:
        """Check whether a cell as wall in a given direction."""
        if self.walls & direction:
            return True
        return False

    def remove_wall(self: "Cell", direction: int) -> None:
        """Remove a wall in a given direction, set bit to 0."""
        if not self.is_42:
            self.walls = self.walls & ~direction


class Grid:
    """
    A class that represents a grid, which is a 2D array.
    Each element in the grid is a Cell, as defined below.
    """

    def __init__(self: "Grid", config: Config) -> None:
        """Initialize the grid with a given width and height."""
        self.width = config.width
        self.height = config.height
        self.entry = config.entry
        self.exit = config.exit
        self.perfect = config.perfect
        if hasattr(config, "seed"):
            self.seed = config.seed
        if hasattr(config, "algo"):
            self.algo = config.algo
        self.grid = self.make_grid()
        if self.width < 7 or self.height < 5:
            print("Error: Maze too small to generate 42 pattern.")
        else:
            self.make_42()

    def make_grid(self: "Grid") -> list[list[Cell]]:
        """
        Create a grid with each cell having default values.
        """
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = Cell((x, y))
                row.append(cell)
            grid.append(row)
        return grid

    def make_42(self: "Grid") -> None:
        """
        If the grid is big enough, reserve a part with closed cells
        in a "42" pattern in the center of the grid.
        """
        # Predefine 42 pattern, 0 = empty, 1 = filled
        pattern = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1]
        ]

        # Get height and width of the 42 pattern
        pattern_height = len(pattern)
        pattern_width = len(pattern[0])

        # Find center of the grid
        center_x = self.width // 2
        center_y = self.height // 2

        # Find starting point, top left of the 42 pattern
        start_x = center_x - pattern_width // 2
        start_y = center_y - pattern_height // 2

        # Apply pattern to grid
        for py in range(pattern_height):
            for px in range(pattern_width):
                grid_x = start_x + px
                grid_y = start_y + py

                if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
                    if pattern[py][px] == 1:
                        cell = self.grid[grid_y][grid_x]
                        cell.is_42 = True
                        cell.walls = 15
                        cell.visited = True

        # Check if entry and exit points are in the 42 pattern
        entry_cell = self.grid[self.entry[1]][self.entry[0]]
        exit_cell = self.grid[self.exit[1]][self.exit[0]]
        if entry_cell.is_42 is True:
            raise ConfigError("ConfigError: "
                              "Entry point is inside 42 pattern.")
        if exit_cell.is_42 is True:
            raise ConfigError("ConfigError: "
                              "Exit point is inside 42 pattern.")

    def get_cell(self: "Grid", x: int, y: int) -> Cell | None:
        """Get cell at position (x, y)."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def get_neighbor(self: "Grid", cell: Cell, direction: int) -> Cell | None:
        """Get neightbor in the given direction."""
        x, y = cell.pos
        if direction == Cell.NORTH:
            neighbor = self.get_cell(x, y - 1)
        elif direction == Cell.EAST:
            neighbor = self.get_cell(x + 1, y)
        elif direction == Cell.SOUTH:
            neighbor = self.get_cell(x, y + 1)
        elif direction == Cell.WEST:
            neighbor = self.get_cell(x - 1, y)
        else:
            return None
        return neighbor

    # added unvidited neighbors
    def get_unvisited_neighbors(self: "Grid",
                                cell: Cell) -> list[tuple[Cell, int]]:
        neighbors = []

        for direction in Cell.get_dirs():
            neighbor = self.get_neighbor(cell, direction)
            if neighbor and not neighbor.visited and not neighbor.is_42:
                neighbors.append((neighbor, direction))
        return neighbors

    def get_visited_neighbors(self: "Grid",
                              cell: Cell) -> list[tuple[Cell, int]]:
        """Get a list of neighbors that are already visited."""
        neighbors = []

        for direction in Cell.get_dirs():
            neighbor = self.get_neighbor(cell, direction)
            if neighbor and neighbor.visited and not neighbor.is_42:
                neighbors.append((neighbor, direction))
        return neighbors

    @staticmethod
    def get_opposite_direction(direction: int) -> int:
        """Get the opposite wall direction."""
        opposites = {
            Cell.NORTH: Cell.SOUTH,
            Cell.SOUTH: Cell.NORTH,
            Cell.EAST: Cell.WEST,
            Cell.WEST: Cell.EAST
        }
        return opposites[direction]

    def remove_wall_btw(self: "Grid", cell: Cell, direction: int) -> None:
        """Remove a wall between two cells."""
        if cell.is_42:
            return

        neighbor = self.get_neighbor(cell, direction)
        if neighbor is None or neighbor.is_42:
            return

        cell.remove_wall(direction)
        opp_dir = self.get_opposite_direction(direction)
        neighbor.remove_wall(opp_dir)

    def get_internal_walls(self: "Grid") -> list[tuple["Cell", int]]:
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

    def check_2x2(self: "Grid", cell: "Cell", dir: int) -> bool:
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

    def check_opening(self: "Grid", cell: "Cell", dir: int) -> bool:
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

    def make_imperfect(self: "Grid") -> None:
        """
        Make a perfect maze imperfect by removing 10% of the remaining walls.
        """
        all_walls = self.get_internal_walls()

        if hasattr(self, "seed"):
            random.seed(self.seed)
        random.shuffle(all_walls)

        num_to_remove = int(len(all_walls) * 0.1)
        num_removed = 0
        for cell, dir in all_walls:
            if num_removed >= num_to_remove:
                break

            if not self.check_opening(cell, dir):
                self.remove_wall_btw(cell, dir)
                num_removed += 1
