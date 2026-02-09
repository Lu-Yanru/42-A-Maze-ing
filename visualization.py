from maze_grid import Cell, Grid


def print_ascii(maze: Grid) -> None:
    # Print top border
    for x in range(maze.width):
        cell = maze.grid[0][x]
        print("+---" if cell.walls & Cell.NORTH else "+   ", end="")
    print("+")

    for y in range(maze.height):
        # Print left/right walls and interior
        for x in range(maze.width):
            cell = maze.grid[y][x]

            # Determine the character inside the cell
            if (x, y) == maze.entry:
                content = " E "
            elif (x, y) == maze.exit:
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
        for x in range(maze.width):
            cell = maze.grid[y][x]
            print("+---" if cell.walls & Cell.SOUTH else "+   ", end="")
        print("+")
