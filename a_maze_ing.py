import sys

import parse_config_file as parsing
from parse_config_file import Config, ConfigError
from maze_grid import Grid
from maze_algo_prim import MazePrim
from write_output import OutputWriter


# testing parsing to config class


def main():
    if len(sys.argv) != 2:
        return

    configs = parsing.parse_config_file(sys.argv[1])
    maze_config = Config(configs)

    try:
        grid = MazePrim(maze_config)
        start = grid.get_cell(grid.entry[0], grid.entry[1])
        grid.generate_maze_prim(start)

        output = OutputWriter(grid, maze_config)
        output.write_output_file()
        grid.print_ascii()
    except ConfigError as e:
        print(e)


main()
