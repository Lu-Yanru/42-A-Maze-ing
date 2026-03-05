import curses
import sys

import parse_config_file as parsing
from mazegen.config.maze_config import Config, ConfigError
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
        def run_display(stdscr: curses.window) -> None:
            display = MazeDisplay(stdscr, maze_config)
            display.run()

        curses.wrapper(run_display)

    except (ValueError, KeyError, ConfigError) as e:
        print(e)
    except OSError as e:
        print(e)
    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
