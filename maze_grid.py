"""
Generate a grid with all closed cells and a 42 pattern in the center.
Classes:
Grid -- a 2D array, each element is a Cell.
Cell --  a cell in the grid with 4 walls,
represented as an interger from 0 to 15.
"""


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

    def __init__(self, pos: tuple, visited: int = 0, walls: int = 15) -> None:
        """Creates a cell with closed 4 walls."""
        self.pos = pos
        self.visited = visited
        self.walls = walls

    def add_wall(self, direction: int) -> None:
        """Add a wall, set bit to 1."""
        self.walls = self.walls | direction

    def remove_wall(self, direction: int) -> None:
        """Remove a wall, set bit to 0."""
        self.walls = self.walls & ~direction


class Grid:
    """
    A class that represents a grid, which is a 2D array.
    Each element in the grid is a Cell, as defined below.
    """

    def __init__(self, width: int, height: int) -> None:
        """Initialize the grid with a given width and height."""
        self.width = width
        self.height = height
        self.grid = self.make_grid()

    def make_grid(self) -> list[list[Cell]]:
        """Create a grid with each cell having default values."""
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = Cell((x, y))
                row.append(cell)
            grid.append(row)
        return grid


# testing
grid = Grid(5, 5)
cell = grid.grid[0][3]
cell.remove_wall(Cell.NORTH)
print(f"{cell.walls}")
for row in grid.grid:
    for cell in row:
        print(cell.walls, end="")
    print("")
