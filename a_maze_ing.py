import curses
import sys

import parse_config_file as parsing
from parse_config_file import Config, ConfigError
from visualize_display import MazeDisplay


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    try:
        # Parse config
        configs = parsing.parse_config_file(sys.argv[1])
        maze_config = Config(configs)

        # Visualize
        # Visualizer(maze).print_ascii()
        def run_display(stdscr):
            display = MazeDisplay(stdscr, maze_config)
            display.run()

        curses.wrapper(run_display)

    except ConfigError as e:
        print(e)
    except OSError as e:
        print(e)
    except KeyboardInterrupt:
        print("Interrupted by user")


if __name__ == "__main__":
    main()
