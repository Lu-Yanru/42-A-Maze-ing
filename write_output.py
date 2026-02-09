"""
Write the output of the maze generation to predefined output file.
The output includes:
The maze with one hexadecimal digit per cell,
where each digit encodes which walls are closed.
Cells are stored row by row, one row per line.
The entry coordinates.
The exit coordinates.
The shorted valid path from entry to exit, using the four letters N, E, S, W.
"""

from parse_config_file import Config
from maze_grid import Grid


class OutputWriter:
    """
    Write maze generation output to a file.
    """
    def __init__(self, maze: Grid, config: Config) -> None:
        self.maze = maze
        self.entry = config.entry
        self.exit = config.exit
        self.output = config.output

    def write_output_file(self) -> None:
        # The maze as hex
        hex = "0123456789ABCDEF"
        str = ""
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                str += hex[self.maze.grid[y][x].walls % 16]
            str += "\n"

        # Entry and exit points
        str += "\n"
        (x, y) = self.entry
        str += f"{x},{y}\n"
        (x, y) = self.exit
        str += f"{x},{y}\n"

        # Write to file
        try:
            with open(self.output, "w") as fd:
                fd.write(str)
        except OSError as e:
            print("OSError: ", e)
