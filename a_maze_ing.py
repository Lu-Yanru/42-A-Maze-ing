import sys

import parse_config_file as parsing
from parse_config_file import Config, ConfigError
import maze_generator as mg
from maze_solver import MazeSolver
from write_output import OutputWriter
import visualization as vi


# testing parsing to config class


def main() -> None:
    if len(sys.argv) != 2:
        return

    configs = parsing.parse_config_file(sys.argv[1])
    maze_config = Config(configs)

    try:
        maze = mg.generate_maze(maze_config)
        solution = MazeSolver(maze).solve_maze()

        output = OutputWriter(maze, maze_config)
        output.write_output_file()
        vi.print_ascii(maze)
    except ConfigError as e:
        print(e)
    except OSError as e:
        print(e)


if __name__ == "__main__":
    main()
