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
        try:
            self.width = int(config["WIDTH"])
        except KeyError:
            raise KeyError("ConfigError: "
                           "Mandatory key 'WIDTH' does not exist.")
        except ValueError:
            raise ValueError("ConfigError: Value of 'WIDTH' is not a number.")

        try:
            self.height = int(config["HEIGHT"])
        except KeyError:
            raise KeyError("ConfigError: "
                           "Mandatory key 'WIDTH' does not exist.")
        except ValueError:
            raise ValueError("ConfigError: Value of 'WIDTH' is not a number.")

        if self.width < 1:
            raise ConfigError("ConfigError: Invalid 'WIDTH' value. "
                              "Cannot generate maze.")
        if self.height < 1:
            raise ConfigError("ConfigError: Invalid 'HEIGHT' value. "
                              "Cannot generate maze.")

        if self.width < 7 or self.height < 5:
            print("Error: Maze too small to generate 42 pattern.")

        try:
            self.entry = tuple(int(x) for x in config["ENTRY"].split(","))
            if self.entry[0] >= self.width or self.entry[0] < 0:
                raise ConfigError("ConfigError: ENTRY OUT OF BOUNDS")
            elif self.entry[1] >= self.height or self.entry[1] < 0:
                raise ConfigError("ConfigError: ENTRY OUT OF BOUNDS")
        except ValueError:
            raise ValueError("ConfigError: Entry coordinate is not numbers.")
        except KeyError:
            raise KeyError("ConfigError: "
                           "Mandatory key 'ENTRY' does not exist.")

        try:
            self.exit = tuple(int(x) for x in config["EXIT"].split(","))
            if self.exit[0] >= self.width or self.exit[0] < 0:
                raise ConfigError("ConfigError: EXIT OUT OF BOUNDS")
            elif self.exit[1] >= self.height or self.exit[1] < 0:
                raise ConfigError("ConfigError: EXIT OUT OF BOUNDS")
        except ValueError:
            raise ValueError("ConfigError: Exit coordinate is not numbers.")
        except KeyError:
            raise KeyError("ConfigError: Mandatory key 'EXIT' does not exist.")

        if self.entry == self.exit:
            raise ConfigError("ConfigError: "
                              "Entry and exit points cannot overlap.")

        try:
            self.output = config["OUTPUT_FILE"]
        except KeyError:
            raise KeyError("ConfigError: "
                           "Mandatory key 'OUTPUT_FILE' does not exist.")

        try:
            self.perfect = config["PERFECT"].lower()
        except KeyError:
            raise KeyError("ConfigError: "
                           "Mandatory key 'PERFECT' does not exist.")
        if self.perfect != 'true' and self.perfect != "false":
            raise ConfigError("ConfigError: Value of 'PERFECT' invalid.")

        if "SEED" in config:
            self.seed = config["SEED"]
        if "ALGORITHM" in config:
            self.algo = config["ALGORITHM"].lower()
