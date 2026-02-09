import sys

import parse_config_file as parsing
from parse_config_file import Config, ConfigError
import maze_generator as mg
from write_output import OutputWriter
import visualization as vi


# testing parsing to config class


def main():
    if len(sys.argv) != 2:
        return

    configs = parsing.parse_config_file(sys.argv[1])
    maze_config = Config(configs)

    try:
        maze = mg.generate_maze(maze_config)

        output = OutputWriter(maze, maze_config)
        output.write_output_file()
        vi.print_ascii(maze)
    except ConfigError as e:
        print(e)
    except OSError as e:
        print(e)


main()
