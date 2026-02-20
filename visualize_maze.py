"""Drawing the maze on a curses window."""


import curses

from maze_cell import Cell
from maze_grid import Grid
from visualize_colors import ColorTheme


class MazePainter:
    """A class for drawing the maze."""
    def __init__(self: "MazePainter", stdscr: curses.window, maze: Grid,
                 path: list[int] | None, theme: ColorTheme | None = None):
        """Initialize the visualizer."""
        self.stdscr = stdscr
        self.maze = maze
        self.path = path
        self.wall = "█"
        self.fill = "█"
        self.cell_width = 3
        self.cell_height = 1
        # Color theme
        if theme is None:
            self.theme = ColorTheme.get_theme(0)
        else:
            self.theme = theme

        self.init_colors()

    def print_ascii(self: "MazePainter") -> None:
        # Print top border
        for x in range(self.maze.width):
            cell = self.maze.grid[0][x]
            print("+---" if cell.walls & Cell.NORTH else "+   ", end="")
        print("+")

        for y in range(self.maze.height):
            # Print left/right walls and interior
            for x in range(self.maze.width):
                cell = self.maze.grid[y][x]

                # Determine the character inside the cell
                if (x, y) == self.maze.entry:
                    content = " E "
                elif (x, y) == self.maze.exit:
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
            for x in range(self.maze.width):
                cell = self.maze.grid[y][x]
                print("+---" if cell.walls & Cell.SOUTH else "+   ", end="")
            print("+")

    def init_colors(self: "MazePainter") -> None:
        """Initialize curses colors."""
        curses.start_color()
        curses.use_default_colors()

        # Set up a color pairs based on predefined themes
        curses.init_pair(1, self.theme.walls, -1)
        curses.init_pair(2, -1, self.theme.entry)
        curses.init_pair(3, -1, self.theme.exit)
        curses.init_pair(4, self.theme.path, -1)
        curses.init_pair(5, self.theme.fill_42, -1)
        curses.init_pair(6, -1, -1)

        # Set the space character to the default fore- and background colors
        self.stdscr.bkgd(" ", curses.color_pair(1))

    def draw_char(self: "MazePainter", row: int, col: int,
                  char: str, color_pair: int = 0) -> None:
        """Draw a single character at position (row, col)."""
        try:
            self.stdscr.addstr(row, col, char, curses.color_pair(color_pair))
        except curses.error:
            pass

    def draw_str(self: "MazePainter", row: int, col: int, char: str,
                 repeat: int, color_pair: int = 0) -> int:
        """Repeat drawing a character multiple times in a row."""
        for i in range(repeat):
            self.draw_char(row, col + i, char, color_pair)
        return col + repeat

    def draw_entry_exit(self: "MazePainter", row: int, col: int,
                        char: str, color_pair: int) -> int:
        self.draw_char(row, col, " ", color_pair)
        col += 1
        self.draw_char(row, col, char, color_pair)
        col += 1
        self.draw_char(row, col, " ", color_pair)
        col += 1
        return col

    def fill_42(self: "MazePainter", row: int, col: int,
                char: str, repeat: int) -> int:
        col = self.draw_str(row, col, self.fill, self.cell_width, 5)
        return col

    def draw_top_border(self: "MazePainter", row: int) -> None:
        """Draw the top border of the maze."""
        col = 0
        for x in range(self.maze.width):
            cell = self.maze.grid[0][x]
            if cell.walls & Cell.NORTH:
                col = self.draw_str(row, col, self.wall,
                                    self.cell_width + 1, 1)
            else:
                col = self.draw_str(row, col, self.wall, 1, 1)
                col = self.draw_str(row, col, " ", self.cell_width, 1)
        col = self.draw_str(row, col, self.wall, 1, 1)

    def draw_vertical_walls(self: "MazePainter", row: int, y: int) -> None:
        """Draw the vertical walls (only west) in a row."""
        col = 0
        for x in range(self.maze.width):
            cell = self.maze.grid[y][x]
            if cell.walls & Cell.WEST:
                col = self.draw_str(row, col, self.wall, self.cell_height, 1)
            else:
                col = self.draw_str(row, col, " ", self.cell_height, 1)

            # Determine the character inside the cell
            if (x, y) == self.maze.entry:
                col = self.draw_entry_exit(row, col, "E", 2)
            elif (x, y) == self.maze.exit:
                col = self.draw_entry_exit(row, col, "X", 3)
            elif cell.is_42:
                col = self.fill_42(row, col, self.fill, self.cell_width)
            else:
                col = self.draw_str(row, col, " ", self.cell_width, 1)
        # Rightmost border
        col = self.draw_str(row, col, self.wall, self.cell_height, 1)

    def draw_horizontal_walls(self: "MazePainter", row: int, y: int) -> None:
        """Draw the horizontal walls (only south) in a row."""
        col = 0
        for x in range(self.maze.width):
            cell = self.maze.grid[y][x]
            if cell.walls & Cell.SOUTH:
                col = self.draw_str(row, col, self.wall,
                                    self.cell_width + 1, 1)
            else:
                col = self.draw_str(row, col, self.wall, 1)
                col = self.draw_str(row, col, " ", self.cell_width, 1)
        col = self.draw_str(row, col, self.wall, 1, 1)

    def print_walls(self: "MazePainter") -> None:
        """Print the walls."""
        row = 0

        self.draw_top_border(row)
        row += 1
        # Print maze row by row
        for y in range(self.maze.height):
            self.draw_vertical_walls(row, y)
            row += 1
            self.draw_horizontal_walls(row, y)
            row += 1

    def draw_path(self: "MazePainter") -> None:
        """Draw the solution path on the maze from enrty to exit."""
        if self.path is None:
            return

        (x, y) = self.maze.entry

        for i in self.path:
            # Calculate the cell position on the pad
            cell_row = 1 + y * (self.cell_height + 1)
            cell_col = 1 + x * (self.cell_width + 1)

            # Fill the cell if it is not entry or exit
            if (x, y) != self.maze.entry and (x, y) != self.maze.exit:
                self.draw_str(cell_row, cell_col, self.fill,
                              self.cell_width, 4)

            # Fill the walls between open cells
            if i == Cell.NORTH:
                wall_row = cell_row - 1
                wall_col = cell_col
                self.draw_str(wall_row, wall_col, self.fill,
                              self.cell_width, 4)
                y -= 1
            elif i == Cell.SOUTH:
                wall_row = cell_row + 1
                wall_col = cell_col
                self.draw_str(wall_row, wall_col, self.fill,
                              self.cell_width, 4)
                y += 1
            elif i == Cell.WEST:
                wall_row = cell_row
                wall_col = cell_col - 1
                self.draw_str(wall_row, wall_col, self.fill,
                              self.cell_height, 4)
                x -= 1
            elif i == Cell.EAST:
                wall_row = cell_row
                wall_col = cell_col + self.cell_width
                self.draw_str(wall_row, wall_col, self.fill,
                              self.cell_height, 4)
                x += 1

            # Stop if reached the exit
            if (x, y) == self.maze.exit:
                break

            # Stop if out of bound
            if x < 0 or x >= self.maze.width \
                    or y < 0 or y >= self.maze.height:
                break
        # Fill the last cell
        cell_row = 1 + y * (self.cell_height + 1)
        cell_col = 1 + x * (self.cell_width + 1)
        if (x, y) != self.maze.entry and (x, y) != self.maze.exit:
            self.draw_str(cell_row, cell_col, self.fill,
                          self.cell_width, 4)

    def clear_path(self: "MazePainter") -> None:
        """Clear the solution path on the maze from exit to entry."""
        if self.path is None:
            return

        (x, y) = self.maze.exit

        for i in reversed(self.path):
            # Calculate the cell position on the pad
            cell_row = 1 + y * (self.cell_height + 1)
            cell_col = 1 + x * (self.cell_width + 1)

            # Clear the cell
            if (x, y) != self.maze.entry and (x, y) != self.maze.exit:
                self.draw_str(cell_row, cell_col, " ", self.cell_width)

            # Clear walls between open cells
            opp = Grid.get_opposite_direction(i)
            if opp == Cell.NORTH:
                wall_row = cell_row - 1
                wall_col = cell_col
                self.draw_str(wall_row, wall_col, " ", self.cell_width)
                y -= 1
            elif opp == Cell.SOUTH:
                wall_row = cell_row + 1
                wall_col = cell_col
                self.draw_str(wall_row, wall_col, " ", self.cell_width)
                y += 1
            elif opp == Cell.WEST:
                wall_row = cell_row
                wall_col = cell_col - 1
                self.draw_str(wall_row, wall_col, " ", self.cell_height)
                x -= 1
            elif opp == Cell.EAST:
                wall_row = cell_row
                wall_col = cell_col + self.cell_width
                self.draw_str(wall_row, wall_col, " ", self.cell_height)
                x += 1

            # Stop if reached the entry
            if (x, y) == self.maze.entry:
                break

            # Stop if out of bound
            if x < 0 or x >= self.maze.width \
                    or y < 0 or y >= self.maze.height:
                break
        # Clear last cell
        cell_row = 1 + y * (self.cell_height + 1)
        cell_col = 1 + x * (self.cell_width + 1)
        if (x, y) != self.maze.entry and (x, y) != self.maze.exit:
            self.draw_str(cell_row, cell_col, " ", self.cell_width)
