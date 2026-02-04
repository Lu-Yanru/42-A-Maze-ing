'''
    Parsing config file #
    Takes file name and returns Dict with parsed values
    try and execpt blocks for FileNotFoundError must be
    included when calling the function
'''


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
    print(defines)
    return defines
