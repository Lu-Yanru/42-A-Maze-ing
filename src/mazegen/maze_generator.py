"""
The MazeGenerator class inherits from the Grid class and generates
the maze based on the perfect and algorithm configuration.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from mazegen.config.maze_config import Config, ConfigError
from mazegen.grid.maze_grid import Grid
# Import only for the type hint to avoid circular imports
if TYPE_CHECKING:
    from mazegen.algo.maze_imperfect import MazeImperfect


class MazeGenerator(Grid, ABC):
    """
    Base class for maze generation.
    Inherits from Grid and adds generation functions.
    """
    def __init__(self: "MazeGenerator", config: Config) -> None:
        super().__init__(config)

    @abstractmethod
    def generate(self: "Grid") -> None:
        """
        Generate maze using the generate() method in subclass
        depeding on the algorithm.
        """
        pass

    @classmethod
    def generate_maze(cls: "type[MazeGenerator]",
                      config: Config) -> "MazeGenerator | MazeImperfect":
        """
        A function to generate the maze based on the algo
        and perfect value in the config file.
        """
        from mazegen.algo.maze_algo_dfs import MazeDFS
        from mazegen.algo.maze_algo_prim import MazePrim
        from mazegen.algo.maze_imperfect import MazeImperfect

        maze: MazeGenerator
        if hasattr(config, "algo"):
            if config.algo == "DSF":
                maze = MazeDFS(config)
            elif config.algo == "Prim":
                maze = MazePrim(config)
            else:
                raise ConfigError(f"ConfigError: Algorithm {config.algo}"
                                  "is not implemented.")
        else:
            # Default algo: DSF
            maze = MazeDFS(config)

        maze.generate()

        if config.perfect == "False":
            imperfect_maze = MazeImperfect(config, maze)
            imperfect_maze.make_imperfect()
            return imperfect_maze

        return maze
