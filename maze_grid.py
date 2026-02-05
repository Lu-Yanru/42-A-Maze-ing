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

    def __init__(self, width: int, height: int) -> None:
        """Initialize the grid with a given width and height."""
        self.width = width
        self.height = height
        self.grid = self.make_grid()
        if width < 7 or height < 5:
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


# testing
if __name__ == "__main__":
    maze1 = Grid(5, 5)
    cell = maze1.grid[0][3]
    maze1.remove_wall_btw(cell, Cell.SOUTH)
    print(f"{cell.walls}")
    maze1.remove_wall_btw(cell, Cell.WEST)
    print(f"{cell.walls}")
    for row in maze1.grid:
        for cell in row:
            print(f"{cell.walls} ", end="")
        print("")

    print("")
    maze2 = Grid(10, 10)
    cell2 = maze2.grid[5][5]
    maze2.remove_wall_btw(cell2, Cell.NORTH)
    maze2.remove_wall_btw(cell2, Cell.SOUTH)
    maze2.remove_wall_btw(cell2, Cell.EAST)
    maze2.remove_wall_btw(cell2, Cell.WEST)
    for row in maze2.grid:
        for cell in row:
            print(f"{cell.walls} ", end="")
        print("")
