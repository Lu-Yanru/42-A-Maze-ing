from maze_cell import Cell
from maze_grid import Grid


class Visualizer:
    """A class for visualizing the maze."""
    def __init__(self, maze: Grid):
        """Initialize the visualizer."""
        self.maze = maze

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

    def print_walls(self: "Visualizer") -> None:
        """Print the walls."""
        wall = "█"
        fill = "█"
        # Print top border
        line = ""
        for x in range(self.maze.width):
            cell = self.maze.grid[0][x]
            if cell.walls & Cell.NORTH:
                line += wall * 4
            else:
                line += wall
                line += "   "
        line += wall
        print(line)

        for y in range(self.maze.height):
            # Print left/right walls and interior
            for x in range(self.maze.width):
                cell = self.maze.grid[y][x]

                # Determine the character inside the cell
                if (x, y) == self.maze.entry:
                    content = " E "
                elif (x, y) == self.maze.exit:
                    content = " X "
                elif cell.is_42:
                    content = fill * 3
                else:
                    content = "   "

                # Print left wall if present
                if cell.walls & Cell.WEST:
                    print(wall + content, end="")
                else:
                    print(" " + content, end="")

            print(wall)  # Rightmost border

            # Print bottom walls
            line = ""
            for x in range(self.maze.width):
                cell = self.maze.grid[y][x]
                if cell.walls & Cell.SOUTH:
                    line += wall * 4
                else:
                    line += wall
                    line += "   "
            line += wall
            print(line)
