from parse_config_file import Config, ConfigError
from maze_grid import Grid
from maze_algo_dfs import MazeDFS
from maze_algo_prim import MazePrim


def generate_maze(config: Config) -> Grid:
    if hasattr(config, "algo"):
        if config.algo == "DSF":
            maze_dfs = MazeDFS(config)
            maze_dfs.generate_maze_dfs()

            if config.perfect == "False":
                maze_dfs.make_imperfect()

            return maze_dfs
        elif config.algo == "Prim":
            maze_prim = MazePrim(config)
            maze_prim.generate_maze_prim()

            if config.perfect == "False":
                maze_prim.make_imperfect()

            return maze_prim
        else:
            raise ConfigError("ConfigError: Algorithm does not exist.")
    else:
        # Default algo: DSF
        maze = MazeDFS(config)
        maze.generate_maze_dfs()

        if config.perfect == "False":
            maze.make_imperfect()

        return maze
