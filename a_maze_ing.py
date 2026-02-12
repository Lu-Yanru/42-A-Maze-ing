import sys

import parse_config_file as parsing
from parse_config_file import Config, ConfigError
from maze_generator import MazeGenerator
from maze_solver import MazeSolver
from write_output import OutputWriter
import visualization as vi


def main() -> None:
    if len(sys.argv) != 2:
        return

    try:
        # parse config
        configs = parsing.parse_config_file(sys.argv[1])
        maze_config = Config(configs)

        # generate maze
        maze = MazeGenerator.generate_maze(maze_config)

        # solve maze
        solution = MazeSolver(maze).solve_maze()

        # write output
        output = OutputWriter(maze, solution, maze_config)
        output.write_output_file()

        # visualize
        vi.print_ascii(maze)
    except ConfigError as e:
        print(e)
    except OSError as e:
        print(e)


if __name__ == "__main__":
    main()
