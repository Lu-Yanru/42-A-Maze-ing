'''
    Parsing config file #
    Takes file name and returns Dict with parsed values
    try and execpt blocks for FileNotFoundError must be
    included when calling the function
'''


class ConfigError(Exception):
    """Error when sth is wrong in the configuration."""
    pass


class Config():
    def __init__(self, config: dict) -> None:
        self.width = int(config["WIDTH"])
        self.height = int(config["HEIGHT"])
        self.entry = tuple(int(x) for x in config["ENTRY"].split(","))
        self.exit = tuple(int(y) for y in config["EXIT"].split(","))
        self.output = config["OUTPUT_FILE"]
        self.perfect = config["PERFECT"]


def parse_config_file(file_name: str) -> dict:
    file = open(file_name, "r")
    lines = []
    lines = file.read().split("\n")

    defines = {}

    for line in lines:
        if "=" in line:
            key = line.split("=")[0]
            value = line.split("=")[1]
            defines[key] = value
    file.close()
    return defines
