"""
The MazeSolver class instantiates from a maze (Grid)
and includes functions to solve the maze.
"""


from maze_cell import Cell
from maze_grid import Grid


class MazeSolver:
    """
    A class for solving the maze.
    """
    def __init__(self: "MazeSolver", maze: Grid) -> None:
        """Initalize the maze solver."""
        self.maze = self.reset_visited(maze)

    def reset_visited(self: "MazeSolver", maze: Grid) -> Grid:
        """
        Resets 'visited' vallue of all cells in a maze
        except for the 42 pattern.
        """
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                if cell and cell.is_42 is False:
                    cell.visited = False
        return maze

    def find_open_neighbors(self: "MazeSolver",
                            current: Cell,
                            queue: list[Cell],
                            parents: dict[Cell, tuple[Cell, int] | None]
                            ) -> None:
        """
        Find neighbors with an open wall that is not visited yet,
        and add them to the queue, visited list, and parents dict,
        respectively.

        Args:
            current (Cell): The cell to find neighbors from.
            queue (list[Cell]): The BFS queue to add neighbors to.
            parents (dict[Cell, tuple[Cell, int]]): A dictionary mapping
            visited cells to its previous cell in the path.
        """
        for dir in Cell.get_dirs():
            if current.has_wall(dir):
                continue

            neighbor = self.maze.get_neighbor(current, dir)
            if neighbor and neighbor.visited is False:
                neighbor.visited = True
                queue.append(neighbor)
                parents[neighbor] = (current, dir)

    def reconstruct_path(self: "MazeSolver",
                         parents: dict[Cell, tuple[Cell, int] | None],
                         end: Cell) -> list[int]:
        """
        Reconstructs the solution from the exit based on stored parents info.
        """
        solution = []

        current = end
        while parents[current] is not None:
            parent, dir = parents[current]  # type: ignore
            solution.append(dir)
            current = parent

        solution.reverse()
        return solution

    def solve_maze(self: "MazeSolver") -> list[int] | None:
        """
        A function to find the shortest path from entry to exit
        using the Breadth-First Search (BFS) algorithm.

        Returns:
            list[int] | None: A list of directions
            (from previous cell to current cell)
            of the solution path. None if no solution was found.
        """
        start = self.maze.get_cell(self.maze.entry[0], self.maze.entry[1])
        end = self.maze.get_cell(self.maze.exit[0], self.maze.exit[1])
        if start is None or end is None:
            return None

        start.visited = True
        queue = [start]
        parents: dict[Cell, tuple[Cell, int] | None] = {start: None}

        while queue:
            current = queue.pop(0)
            if current == end:
                return self.reconstruct_path(parents, end)

            self.find_open_neighbors(current, queue, parents)

        return None
