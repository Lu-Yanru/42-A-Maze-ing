import curses

from maze_cell import Cell
from maze_grid import Grid


class MazePainter:
    """A class for drawing the maze."""
    def __init__(self: "MazePainter", stdscr, maze: Grid,
                 path: list[int] | None):
        """Initialize the visualizer."""
        self.stdscr = stdscr
        self.maze = maze
        self.path = path
        self.wall = "█"
        self.fill = "█"
        self.cell_width = 3
        self.cell_height = 1
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

        # set up a color pair with default (-1) fore- and background colors
        curses.init_pair(1, -1, -1)

        # set the space character to the default fore- and background colors
        self.stdscr.bkgd(" ", curses.color_pair(1))

    def draw_char(self: "MazePainter", row: int, col: int, char: str) -> None:
        """Draw a single character at position (row, col)."""
        try:
            self.stdscr.addstr(row, col, char)
        except curses.error:
            pass

    def draw_str(self: "MazePainter", row: int, col: int, char: str,
                 repeat: int) -> int:
        """Repeat drawing a character multiple times in a row."""
        for i in range(repeat):
            self.draw_char(row, col + i, char)
        return col + repeat

    def draw_entry_exit(self: "MazePainter", row: int, col: int,
                        char: str) -> int:
        self.draw_char(row, col, " ")
        col += 1
        self.draw_char(row, col, char)
        col += 1
        self.draw_char(row, col, " ")
        col += 1
        return col

    def fill_42(self: "MazePainter", row: int, col: int,
                char: str, repeat: int) -> int:
        col = self.draw_str(row, col, self.fill, self.cell_width)
        return col

    def draw_top_border(self: "MazePainter", row: int) -> None:
        """Draw the top border of the maze."""
        col = 0
        for x in range(self.maze.width):
            cell = self.maze.grid[0][x]
            if cell.walls & Cell.NORTH:
                col = self.draw_str(row, col, self.wall, self.cell_width + 1)
            else:
                col = self.draw_str(row, col, self.wall, 1)
                col = self.draw_str(row, col, " ", self.cell_width)
        col = self.draw_str(row, col, self.wall, 1)

    def draw_vertical_walls(self: "MazePainter", row: int, y: int) -> None:
        """Draw the vertical walls (only west) in a row."""
        col = 0
        for x in range(self.maze.width):
            cell = self.maze.grid[y][x]
            if cell.walls & Cell.WEST:
                col = self.draw_str(row, col, self.wall, self.cell_height)
            else:
                col = self.draw_str(row, col, " ", self.cell_height)

            # Determine the character inside the cell
            if (x, y) == self.maze.entry:
                col = self.draw_entry_exit(row, col, "E")
            elif (x, y) == self.maze.exit:
                col = self.draw_entry_exit(row, col, "X")
            elif cell.is_42:
                col = self.fill_42(row, col, self.fill, self.cell_width)
            else:
                col = self.draw_str(row, col, " ", self.cell_width)
        # Rightmost border
        col = self.draw_str(row, col, self.wall, self.cell_height)

    def draw_horizontal_walls(self: "MazePainter", row: int, y: int) -> None:
        """Draw the horizontal walls (only south) in a row."""
        col = 0
        for x in range(self.maze.width):
            cell = self.maze.grid[y][x]
            if cell.walls & Cell.SOUTH:
                col = self.draw_str(row, col, self.wall, self.cell_width + 1)
            else:
                col = self.draw_str(row, col, self.wall, 1)
                col = self.draw_str(row, col, " ", self.cell_width)
        col = self.draw_str(row, col, self.wall, 1)

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

    # def draw_path(self: "MazePainter") -> None:
    #     if self.path is None:
    #         return

    #     (x, y) = self.maze.entry
    #     start_row = 1 + y * 2
    #     self.stdscr.move(start_row, x)
    #     for i in self.path:
    #         if i == Cell.NORTH:
    #             self.draw_str(y - 1, x, self.fill, 3)
    #         elif i == Cell.SOUTH:
    #             self.draw_str(y + 1, x, self.fill, 3)
    #         elif i == Cell.WEST:
    #             self.draw_str(y, x - 1, self.fill, 3)
    #         elif i == Cell.EAST:
    #             self.draw_str(y, x + 1, self.fill, 3)

    def show_choices(self: "MazePainter") -> None:
        start_row = self.maze.height * 2 + 1 + 2

        try:
            self.stdscr.move(start_row, 0)
            self.stdscr.addstr(start_row, 0,
                               "=== A-Maze-ing ===")
            self.stdscr.addstr(start_row + 1, 0,
                               "Use ← ↑ → ↓ to scroll.")
            self.stdscr.addstr(start_row + 2, 0,
                               "Press i to enter input mode.")
            self.stdscr.addstr(start_row + 3, 0,
                               "1. Re-generate a new maze")
            self.stdscr.addstr(start_row + 4, 0,
                               "2. Show/Hide path from entry to exit")
            self.stdscr.addstr(start_row + 5, 0,
                               "3. Rotate maze colors")
            self.stdscr.addstr(start_row + 6, 0,
                               "4. Quit")
            self.stdscr.addstr(start_row + 7, 0,
                               "Choice? (1-4): ")
        except curses.error:
            pass

    def display_message(self: "MazePainter", message: str) -> None:
        start_row = self.maze.height * 2 + 1 + 2 + 8

        try:
            self.stdscr.move(start_row, 0)
            self.stdscr.clrtoeol()
            self.stdscr.addstr(start_row, 0, message)
        except curses.error:
            pass
