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

    def __init__(self, pos: tuple, visited: bool = False, walls: int = 15,
                 is_42: bool = False) -> None:
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
    def get_dirs(cls) -> list[int]:
        """Returns a list of all directions."""
        return [cls.NORTH, cls.EAST, cls.SOUTH, cls.WEST]

    def add_wall(self, direction: int) -> None:
        """Add a wall in a given direction, set bit to 1."""
        if not self.is_42:
            self.walls = self.walls | direction

    def remove_wall(self, direction: int) -> None:
        """Remove a wall in a given direction, set bit to 0."""
        if not self.is_42:
            self.walls = self.walls & ~direction


class Grid:
    """
    A class that represents a grid, which is a 2D array.
    Each element in the grid is a Cell, as defined below.
    """

    def __init__(self, config: Config) -> None:
        """Initialize the grid with a given width and height."""
        self.width = config.width
        self.height = config.height
        self.entry = config.entry
        self.exit = config.exit
        self.grid = self.make_grid()
        if self.width < 7 or self.height < 5:
            print("Error: Maze too small to generate 42 pattern.")
        else:
            self.make_42()

    def make_grid(self) -> list[list[Cell]]:
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

    def make_42(self) -> None:
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
        if entry_cell.is_42 is True or exit_cell.is_42 is True:
            raise ConfigError("ConfigError: "
                              "Entry or exit point is inside 42 pattern.")

    def get_cell(self, x: int, y: int) -> Cell | None:
        """Get cell at position (x, y)."""
        try:
            return self.grid[y][x]
        except Exception:
            return None

    def get_neighbor(self, cell: Cell, direction: int) -> Cell | None:
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
    def get_unvisited_neighbors(self, cell: Cell) -> list[tuple[Cell, int]]:
        neighbors = []

        for direction in Cell.get_dirs():
            neighbor = self.get_neighbor(cell, direction)
            if neighbor and not neighbor.visited and not neighbor.is_42:
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

    def add_wall_btw(self, cell: Cell, direction: int) -> None:
        """Add a wall between two cells."""
        if cell.is_42:
            return

        neighbor = self.get_neighbor(cell, direction)
        if neighbor is None or neighbor.is_42:
            return

        cell.add_wall(direction)
        opp_dir = self.get_opposite_direction(direction)
        neighbor.add_wall(opp_dir)

    def remove_wall_btw(self, cell: Cell, direction: int) -> None:
        """Remove a wall between two cells."""
        if cell.is_42:
            return

        neighbor = self.get_neighbor(cell, direction)
        if neighbor is None or neighbor.is_42:
            return

        cell.remove_wall(direction)
        opp_dir = self.get_opposite_direction(direction)
        neighbor.remove_wall(opp_dir)

    # added perfect maze generator
    def generate_maze(self, start: Cell) -> None:

        """
        Carves a perfect maze starting from `start` cell.
        Uses DFS iterative backtracker algorithm.
        """

        if start is None:
            raise ValueError("Start cell cannot be None")
        if start.visited:
            raise ValueError("Start cell already visited")
        if start.is_42:
            raise ValueError("Start cell cannot be inside 42 pattern")

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

    def print_ascii(self) -> None:
        # Print top border
        for x in range(self.width):
            cell = self.grid[0][x]
            print("+---" if cell.walls & Cell.NORTH else "+   ", end="")
        print("+")

        for y in range(self.height):
            # Print left/right walls and interior
            for x in range(self.width):
                cell = self.grid[y][x]

                # Determine the character inside the cell
                if (x, y) == self.entry:
                    content = " E "
                elif (x, y) == self.exit:
                    content = " X "
                else:
                    content = "   "

                # Print left wall if present
                if cell.walls & Cell.WEST:
                    print("|" + content, end="")
                else:
                    print(" " + content, end="")

            print("|")  # Rightmost border

            # Print bottom walls
            for x in range(self.width):
                cell = self.grid[y][x]
                print("+---" if cell.walls & Cell.SOUTH else "+   ", end="")
            print("+")
