"""
Generate a grid with all closed cells and a 42 pattern in the center.
Defines class Grid -- a 2D array, each element is a Cell.
"""

from parse_config_file import Config, ConfigError
from maze_cell import Cell


class Grid:
    """
    A class that represents a grid, which is a 2D array.
    Each element in the grid is a Cell.
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
        entry_cell = self.get_cell(self.entry[0], self.entry[1])
        exit_cell = self.get_cell(self.exit[0], self.exit[1])
        if entry_cell is None or entry_cell.is_42 is True:
            raise ConfigError("ConfigError: "
                              "Entry point is inside 42 pattern.")
        if exit_cell is None or exit_cell.is_42 is True:
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
