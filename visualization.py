import curses

from maze_cell import Cell
from maze_grid import Grid


class Visualizer:
    """A class for visualizing the maze."""
    def __init__(self: "Visualizer", stdscr, maze: Grid):
        """Initialize the visualizer."""
        self.stdscr = stdscr
        self.maze = maze
        self.wall = "█"
        self.fill = "█"
        self.cell_width = 4
        self.init_colors()

    def print_ascii(self: "Visualizer") -> None:
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

    def init_colors(self: "Visualizer") -> None:
        """Initialize curses colors."""
        curses.start_color()
        curses.use_default_colors()

        # set up a color pair with default (-1) fore- and background colors
        curses.init_pair(1, -1, -1)

        # set the space character to the default fore- and background colors
        self.stdscr.bkgd(" ", curses.color_pair(1))

    def draw_char(self: "Visualizer", row: int, col: int, char: str) -> None:
        """Draw a single character at position (row, col)."""
        try:
            self.stdscr.addstr(row, col, char)
            # self.stdscr.refresh()
        except curses.error:
            pass

    def draw_str(self: "Visualizer", row: int, col: int, char: str,
                 repeat: int) -> int:
        """Repeat drawing a character multiple times in a row."""
        for i in range(repeat):
            self.draw_char(row, col + i, char)
        return col + repeat

    def draw_entry_exit(self: "Visualizer", row: int, col: int,
                        char: str) -> int:
        self.draw_char(row, col, " ")
        col += 1
        self.draw_char(row, col, char)
        col += 1
        self.draw_char(row, col, " ")
        col += 1
        return col

    def fill_42(self: "Visualizer", row: int, col: int,
                char: str, repeat: int) -> int:
        col = self.draw_str(row, col, self.fill, 3)
        return col

    def draw_top_border(self: "Visualizer", row: int) -> None:
        """Draw the top border of the maze."""
        col = 0
        for x in range(self.maze.width):
            cell = self.maze.grid[0][x]
            if cell.walls & Cell.NORTH:
                col = self.draw_str(row, col, self.wall, 4)
            else:
                col = self.draw_str(row, col, self.wall, 1)
                col = self.draw_str(row, col, " ", 3)
        col = self.draw_str(row, col, self.wall, 1)

    def draw_vertical_walls(self: "Visualizer", row: int, y: int) -> None:
        """Draw the vertical walls (only west) in a row."""
        col = 0
        for x in range(self.maze.width):
            cell = self.maze.grid[y][x]
            if cell.walls & Cell.WEST:
                col = self.draw_str(row, col, self.wall, 1)
            else:
                col = self.draw_str(row, col, " ", 1)

            # Determine the character inside the cell
            if (x, y) == self.maze.entry:
                col = self.draw_entry_exit(row, col, "E")
            elif (x, y) == self.maze.exit:
                col = self.draw_entry_exit(row, col, "X")
            elif cell.is_42:
                col = self.fill_42(row, col, self.fill, 3)
            else:
                col = self.draw_str(row, col, " ", 3)
        # Rightmost border
        col = self.draw_str(row, col, self.wall, 1)

    def draw_horizontal_walls(self: "Visualizer", row: int, y: int) -> None:
        """Draw the horizontal walls (only south) in a row."""
        col = 0
        for x in range(self.maze.width):
            cell = self.maze.grid[y][x]
            if cell.walls & Cell.SOUTH:
                col = self.draw_str(row, col, self.wall, 4)
            else:
                col = self.draw_str(row, col, self.wall, 1)
                col = self.draw_str(row, col, " ", 3)
        col = self.draw_str(row, col, self.wall, 1)

    def print_walls(self: "Visualizer") -> None:
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

        self.stdscr.refresh()
