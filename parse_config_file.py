'''
    Parsing config file #
    Takes file name and returns Dict with parsed values
    try and execpt blocks for FileNotFoundError must be
    included when calling the function
'''


def parse_config_file(file_name: str) -> dict[str, str]:
    try:
        with open(file_name, "r") as file:
            lines = []
            lines = file.read().split("\n")

            defines = {}

            for line in lines:
                if "=" in line:
                    key = line.split("=")[0].strip().upper()
                    value = line.split("=")[1].strip()
                    defines[key] = value
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: "
                                f"{file_name} does not exist.")
    except PermissionError:
        raise PermissionError(f"PermissionError: Cannot access {file_name}")

    return defines
