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
        except Exception:
            print("INVALID WIDTH - PLEASE CHECK CONFIG FILE USED!")
            self.width = -1
        try:
            self.height = int(config["HEIGHT"])
        except Exception:
            print("INVALID HEIGHT - PLEASE CHECK CONFIG FILE USED!")
            self.height = -1
        try:
            self.entry = tuple(int(x) for x in config["ENTRY"].split(","))
            if self.entry[0] > self.width or self.entry[0] < 0:
                raise ConfigError
            elif self.entry[1] > self.height or self.entry[1] < 0:
                raise ConfigError
        except ValueError:
            print("INVALID ENTRY POINT - PLEASE CHECK CONFIG FILE USED!")
        except ConfigError:
            print("ENTRY POINT IS OUT OF BOUNDS")
        try:
            self.exit = tuple(int(x) for x in config["EXIT"].split(","))
            if self.exit[0] > self.width or self.exit[0] < 0:
                raise ConfigError
            elif self.exit[1] > self.height or self.exit[1] < 0:
                raise ConfigError
        except ValueError:
            print("INVALID ENTRY POINT - PLEASE CHECK CONFIG FILE USED!")
        except ConfigError:
            print("EXIT POINT IS OUT OF BOUNDS")

        self.output = config["OUTPUT_FILE"]
        self.perfect = config["PERFECT"]

        if "SEED" in config:
            try:
                self.seed = int(config["SEED"])
            except Exception:
                print("INVALID SEED - TRY AN INTEGER VALUE")
        if "ALGORITHM" in config:
            self.algo = config["ALGORITHM"]
