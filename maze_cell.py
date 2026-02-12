"""
Defines the class Cell which represents a cell in a maze.
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
            prev (tuple): The previous cell in the solution and the direction
                        of the open wall from previous to current cell.
                        Default (None, 0)
        """
        self.pos = pos
        self.visited = visited
        self.walls = walls
        self.is_42 = is_42

    @classmethod
    def get_dirs(cls: "type[Cell]") -> list[int]:
        """Returns a list of all directions."""
        return [cls.NORTH, cls.EAST, cls.SOUTH, cls.WEST]

    @classmethod
    def dir_to_str(cls: "type[Cell]", dir: int) -> str | None:
        """Converts a diretion to its corresponding name."""
        if dir == cls.NORTH:
            return "N"
        if dir == cls.EAST:
            return "E"
        if dir == cls.SOUTH:
            return "S"
        if dir == cls.WEST:
            return "W"

        return None

    def has_wall(self: "Cell", direction: int) -> bool:
        """Check whether a cell as wall in a given direction."""
        if self.walls & direction:
            return True
        return False

    def remove_wall(self: "Cell", direction: int) -> None:
        """Remove a wall in a given direction, set bit to 0."""
        if not self.is_42:
            self.walls = self.walls & ~direction
