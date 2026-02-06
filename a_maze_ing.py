import sys

import parse_config_file as parsing
from parse_config_file import Config, ConfigError
from maze_grid import Grid
from write_output import OutputWriter


# testing parsing to config class


def main():
    if len(sys.argv) != 2:
        return
    else:
        configs = parsing.parse_config_file(sys.argv[1])
        maze_config = Config(configs)
        try:
            maze = Grid(maze_config)
        except ConfigError as e:
            print(e)
        else:
            OutputWriter(maze, maze_config).write_output_file()


main()
