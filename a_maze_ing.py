import parse_config_file as parsing
import sys


class config():
    def __init__(self, config: dict) -> None:
        self.width = config["WIDTH"]
        self.height = config["HEIGHT"]
        self.entry = tuple(int(x) for x in config["ENTRY"].split(","))
        self.exit = tuple(int(y) for y in config["EXIT"].split(","))
        self.output = config["OUTPUT_FILE"]
        self.perfect = config["PERFECT"]


# testing parsing to config class


def main():
    if len(sys.argv) != 2:
        return
    else:
        configs = parsing.parse_config_file(sys.argv[1])
        maze_config = config(configs)

        print(maze_config.height)


main()
