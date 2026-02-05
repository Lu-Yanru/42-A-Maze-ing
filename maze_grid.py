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

    @classmethod
    def get_dirs(cls) -> list[int]:
        """Returns a list of all directions."""
        return [cls.NORTH, cls.EAST, cls.SOUTH, cls.WEST]

    def add_wall(self, direction: int) -> None:
        """Add a wall in a given direction, set bit to 1."""
        self.walls = self.walls | direction

    def remove_wall(self, direction: int) -> None:
        """Remove a wall in a given direction, set bit to 0."""
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
        cell.add_wall(direction)
        neighbor = self.get_neighbor(cell, direction)
        if neighbor is None:
            return
        opp_dir = self.get_opposite_direction(direction)
        neighbor.add_wall(opp_dir)

    def remove_wall_btw(self, cell: Cell, direction: int) -> None:
        """Remove a wall between two cells."""
        cell.remove_wall(direction)
        neighbor = self.get_neighbor(cell, direction)
        if neighbor is None:
            return
        opp_dir = self.get_opposite_direction(direction)
        neighbor.remove_wall(opp_dir)


# testing
grid = Grid(5, 5)
cell = grid.grid[0][3]
grid.remove_wall_btw(cell, Cell.SOUTH)
print(f"{cell.walls}")
grid.remove_wall_btw(cell, Cell.WEST)
print(f"{cell.walls}")
for row in grid.grid:
    for cell in row:
        print(cell.walls, end="")
    print("")
