"""Drawing the maze on a curses window."""


import curses
import time

from mazegen.grid.maze_cell import Cell
from mazegen.grid.maze_grid import Grid
from visualize_colors import ColorTheme


class MazePainter:
    """A class for drawing the maze."""
    def __init__(self: "MazePainter", stdscr: curses.window, maze: Grid,
                 path: list[int] | None,
                 theme: ColorTheme | None = None,
                 delay: float = 0.01) -> None:
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
        # Animation
        self.pad_refresh_params: tuple[int, int, int, int] | None = None
        self.delay = delay

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

    def set_pad_refresh_params(self: "MazePainter", scroll_offset_y: int,
                               scroll_offset_x: int, screen_height: int,
                               screen_width: int) -> None:
        """Set parameters for refreshing pad."""
        self.pad_refresh_params = (scroll_offset_y, scroll_offset_x,
                                   screen_height, screen_width)

    def animate(self: "MazePainter") -> None:
        """Do one animation step, refresh and delay."""
        if self.delay > 0 and self.pad_refresh_params:
            (scroll_offset_y, scroll_offset_x, screen_height,
             screen_width) = self.pad_refresh_params
            try:
                self.stdscr.refresh(scroll_offset_y, scroll_offset_x, 0, 0,
                                    screen_height - 1, screen_width - 1)
                time.sleep(self.delay)
            except curses.error:
                pass

    def get_cell_row(self: "MazePainter", y: int) -> int:
        """
        Get the row position of the cell on the pad
        from its y position in the grid.
        """
        return 1 + y * (self.cell_height + 1)

    def get_cell_col(self: "MazePainter", x: int) -> int:
        """
        Get the column position of the cell on the pad
        from its x position in the grid.
        """
        return 1 + x * (self.cell_width + 1)

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
        self.animate()
        return col + repeat

    def draw_entry_exit(self: "MazePainter", char: str,
                        color_pair: int) -> None:
        if char.upper() == "E":
            (x, y) = self.maze.entry
        elif char.upper() == "X":
            (x, y) = self.maze.exit
        else:
            return

        cell_row = self.get_cell_row(y)
        cell_col = self.get_cell_col(x)
        self.draw_char(cell_row, cell_col, " ", color_pair)
        self.draw_char(cell_row, cell_col + 1, char, color_pair)
        self.draw_char(cell_row, cell_col + 2, " ", color_pair)

    def fill_42(self: "MazePainter") -> None:
        """Fill the 42 pattern."""
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.maze.grid[y][x]
                if cell.is_42:
                    cell_row = self.get_cell_row(y)
                    cell_col = self.get_cell_col(x)
                    self.draw_str(cell_row, cell_col, self.fill,
                                  self.cell_width, 5)

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
            # Inside of the cell
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
            cell_row = self.get_cell_row(y)
            cell_col = self.get_cell_col(x)

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

        # Fill the last cell
        cell_row = self.get_cell_row(y)
        cell_col = self.get_cell_col(x)
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
            cell_row = self.get_cell_row(y)
            cell_col = self.get_cell_col(x)

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

        # Clear last cell
        cell_row = self.get_cell_row(y)
        cell_col = self.get_cell_col(x)
        if (x, y) != self.maze.entry and (x, y) != self.maze.exit:
            self.draw_str(cell_row, cell_col, " ", self.cell_width)
