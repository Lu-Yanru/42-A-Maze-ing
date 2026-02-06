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

from maze_grid import Grid


class OutputWriter:
    """
    Docstring for OutputWriter
    """
    def __init__(self, maze: Grid, output: str) -> None:
        self.maze = maze
        self.output = output

    def write_output_file(self) -> None:
        hex = "0123456789ABCDEF"
        str = ""
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                str += hex[self.maze.grid[y][x].walls % 16]
            str += "\n"
        str += "\n"
        try:
            with open(self.output, "w") as fd:
                fd.write(str)
        except Exception:
            print("Failed to write output file.")


# testing
if __name__ == "__main__":
    maze = Grid(10, 10)
    OutputWriter(maze, "output.txt").write_output_file()
