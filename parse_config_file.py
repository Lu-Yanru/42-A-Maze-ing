
# Parsing config file #
# Takes file name and returns Dict with parsed values #
def parse_config_file(file_name: str) -> dict:
    file = open(file_name)
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
