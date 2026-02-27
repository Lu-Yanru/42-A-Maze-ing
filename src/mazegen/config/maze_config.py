"""
Store the result of parsing the config file into a Config object
which is used to configure the maze.

Classes:
- Config
- ConfigError
"""


class ConfigError(Exception):
    """Error when sth is wrong in the configuration."""
    pass


class Config():
    def __init__(self: "Config", config: dict[str, str]) -> None:
        """
        Initialize a config object
        based on the result of parsing the config file.
        """
        self.width = int(config["WIDTH"])
        self.height = int(config["HEIGHT"])
        self.entry = tuple(int(x) for x in config["ENTRY"].split(","))
        self.exit = tuple(int(y) for y in config["EXIT"].split(","))
        self.output = config["OUTPUT_FILE"]
        self.perfect = config["PERFECT"]
        if "SEED" in config:
            self.seed = int(config["SEED"])
        if "ALGORITHM" in config:
            self.algo = config["ALGORITHM"]
