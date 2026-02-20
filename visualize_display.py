import curses

from parse_config_file import Config
from maze_grid import Grid
from maze_generator import MazeGenerator
from maze_solver import MazeSolver
from write_output import OutputWriter
from visualize_maze import MazePainter


class MazeDisplay:
    """Handles the interactive display of the maze."""
    def __init__(self: "MazeDisplay", stdscr: curses.window,
                 config: Config) -> None:
        """Initialize the maze display"""
        self.stdscr = stdscr
        self.config = config
        # Screen dimensions
        self.screen_height = 0
        self.screen_width = 0
        # Scroll offsets, pad's starting position
        self.scroll_offset_y = 0
        self.scroll_offset_x = 0
        # Maze dimensions
        self.total_height = 0
        self.total_width = 0
        self.menu_height = 11
        self.prompt_row = 0
        self.prompt_col = len("Choice? (1-4): ")
        # Pad and MazePainter
        self.pad: curses.window | None = None
        self.painter: MazePainter | None = None
        self.maze: Grid | None = None
        self.solution: list[int] | None = None

    def generate_maze(self: "MazeDisplay") -> None:
        """Generate maze and solution and write to output."""
        # Generate maze
        self.maze = MazeGenerator.generate_maze(self.config)

        # Solve maze
        self.solution = MazeSolver(self.maze).solve_maze()

        # Write output
        output = OutputWriter(self.maze, self.solution, self.config)
        output.write_output_file()

    def redraw(self: "MazeDisplay") -> None:
        """Redraw everything after resize or update."""
        # Get current screen dimensions
        self.screen_height, self.screen_width = self.stdscr.getmaxyx()

        # Refresh screen
        self.stdscr.refresh()

        if self.pad is None:
            return

        try:
            self.pad.refresh(self.scroll_offset_y, self.scroll_offset_x, 0, 0,
                             self.screen_height - 1, self.screen_width - 1)
        except curses.error:
            pass

    def display_maze(self: "MazeDisplay") -> None:
        """Display the maze and the menu."""
        # Get terminal dimensions
        self.screen_height, self.screen_width = self.stdscr.getmaxyx()

        self.generate_maze()

        if self.maze is None:
            return

        # Reset scroll offset
        self.scroll_offset_y = 0
        self.scroll_offset_x = 0

        # Calculate required height and width
        maze_height = self.maze.height * 2 + 1
        self.total_height = maze_height + self.menu_height
        self.total_width = self.maze.width * 4 + 1

        # Create a pad
        pad_height = max(self.total_height, self.screen_height)
        pad_width = max(self.total_width, self.screen_width)
        self.pad = curses.newpad(pad_height, pad_width)

        # Draw on the pad
        self.painter = MazePainter(self.pad, self.maze, self.solution)

        # Hide cursor
        curses.curs_set(0)

        self.painter.print_walls()
        self.show_choices()

        # The position where the prompt should be shown
        self.prompt_row = self.maze.height * 2 + 1 + 2 + 7

        # Display on pad
        self.redraw()

    def show_choices(self: "MazeDisplay") -> None:
        if self.maze is None or self.pad is None:
            return

        start_row = self.maze.height * 2 + 1 + 2

        try:
            self.pad.move(start_row, 0)
            self.pad.addstr(start_row, 0,
                            "=== A-Maze-ing ===")
            self.pad.addstr(start_row + 1, 0,
                            "Use ← ↑ → ↓ to scroll.")
            self.pad.addstr(start_row + 2, 0,
                            "Press i to enter input mode.")
            self.pad.addstr(start_row + 3, 0,
                            "1. Re-generate a new maze")
            self.pad.addstr(start_row + 4, 0,
                            "2. Show/Hide path from entry to exit")
            self.pad.addstr(start_row + 5, 0,
                            "3. Rotate maze colors")
            self.pad.addstr(start_row + 6, 0,
                            "4. Quit")
            self.pad.addstr(start_row + 7, 0,
                            "Choice? (1-4): ")
        except curses.error:
            pass

    def display_message(self: "MazeDisplay", message: str) -> None:
        if self.maze is None or self.pad is None:
            return

        start_row = self.maze.height * 2 + 1 + 2 + 8

        try:
            self.pad.move(start_row, 0)
            self.pad.clrtoeol()
            self.pad.addstr(start_row, 0, message)
        except curses.error:
            pass

    def handle_resize(self: "MazeDisplay") -> None:
        """Redraw when resize the terminal window."""
        self.screen_height, self.screen_width = self.stdscr.getmaxyx()
        # Max value of scroll offset to not scroll past the end
        max_scroll_y = max(0, self.total_height - self.screen_height)
        max_scroll_x = max(0, self.total_width - self.screen_width)
        # Adjust scroll offset
        self.scroll_offset_y = min(self.scroll_offset_y, max_scroll_y)
        self.scroll_offset_x = min(self.scroll_offset_x, max_scroll_x)
        # Redraw everything
        self.redraw()

    def scroll_up(self) -> None:
        """Redraw when scrolling up with up button."""
        self.scroll_offset_y = max(0, self.scroll_offset_y - 1)
        self.redraw()

    def scroll_down(self) -> None:
        """Redraw when scrolling down with down button."""
        max_scroll_y = max(0, self.total_height - self.screen_height)
        self.scroll_offset_y = min(max_scroll_y, self.scroll_offset_y + 1)
        self.redraw()

    def scroll_left(self) -> None:
        """Redraw when scrolling left with left button."""
        self.scroll_offset_x = max(0, self.scroll_offset_x - 1)
        self.redraw()

    def scroll_right(self) -> None:
        """Redraw when scrolling right with right button."""
        max_scroll_x = max(0, self.total_width - self.screen_width)
        self.scroll_offset_x = min(max_scroll_x, self.scroll_offset_x + 1)
        self.redraw()

    def scroll_to_prompt(self) -> None:
        """Scroll to prompt row."""
        if self.prompt_row - self.scroll_offset_y >= self.screen_height - 2:
            calc = self.prompt_row - self.screen_height + 2
            self.scroll_offset_y = max(0, calc)
            self.redraw()

    def get_user_input(self: "MazeDisplay") -> str:
        """
        Get user input.
        This has to be done with stdscr
        because we can't put a textpad on a pad,
        and a pad cannot getchr().
        """
        if self.pad is None:
            return ""

        # Get the position of the prompt on the screen
        prompt_screen_y = self.prompt_row - self.scroll_offset_y
        prompt_screen_x = self.prompt_col - self.scroll_offset_x

        # Make sure prompt is visible on screen
        if prompt_screen_y < 0 or prompt_screen_y >= self.screen_height - 1:
            return ""
        if prompt_screen_x < 0:
            prompt_screen_x = 0

        # Show cursor
        curses.curs_set(1)

        # Clear input area on stdscr
        try:
            self.stdscr.move(prompt_screen_y, prompt_screen_x)
            # Clear the line
            self.stdscr.clrtoeol()
            self.stdscr.refresh()
        except curses.error:
            pass

        # Get input
        res = ""
        cursor_pos = 0

        while True:
            # Display current input
            try:
                self.stdscr.move(prompt_screen_y, prompt_screen_x)
                self.stdscr.clrtoeol()
                self.stdscr.addstr(prompt_screen_y, prompt_screen_x, res)
                self.stdscr.move(prompt_screen_y, prompt_screen_x + cursor_pos)
                self.stdscr.refresh()
            except curses.error:
                pass

            key = self.stdscr.getch()

            # Stop with enter
            if key in [curses.KEY_ENTER, 10, 13]:
                break

            # Delete
            elif key == curses.KEY_BACKSPACE:
                if cursor_pos > 0:
                    res = res[:cursor_pos-1] + res[cursor_pos:]
                    cursor_pos -= 1
            elif key == curses.KEY_DC:
                if cursor_pos < len(res):
                    res = res[:cursor_pos] + res[cursor_pos+1:]

            # Move left and right with arrows
            elif key == curses.KEY_LEFT:
                if cursor_pos > 0:
                    cursor_pos -= 1
            elif key == curses.KEY_RIGHT:
                if cursor_pos < len(res):
                    cursor_pos += 1

            # Print out printable characters
            elif 32 <= key <= 126:
                char = chr(key)
                res = res[:cursor_pos] + char + res[cursor_pos:]
                cursor_pos += 1
                # Limit input length
                if len(res) > 10:
                    res = res[:10]
                    cursor_pos = min(cursor_pos, 10)

        # Hide cursor
        curses.curs_set(0)

        # Update the pad with the final input
        try:
            self.pad.move(self.prompt_row, self.prompt_col)
            self.pad.clrtoeol()
            self.pad.refresh(self.scroll_offset_y, self.scroll_offset_x,
                             0, 0,
                             self.screen_height - 1, self.screen_width - 1)
        except curses.error:
            pass

        # Clear the input area on stdscr
        try:
            self.stdscr.move(prompt_screen_y, prompt_screen_x)
            self.stdscr.clrtoeol()
            self.stdscr.refresh()
        except curses.error:
            pass

        return res.strip()

    def handle_user_input(self) -> bool:
        """
        Handles user input.
        Returns false when quit.
        """
        if self.pad is None or self.painter is None:
            return True
        self.scroll_to_prompt()
        # Get input
        user_input = self.get_user_input()
        # Regenerate new maze
        if user_input == "1":
            self.display_maze()
            return True
        # Quit
        elif user_input == "4":
            return False
        # Invalid choice
        else:
            self.display_message("Invalid choice!")
            self.pad.move(self.prompt_row, self.prompt_col)
            self.pad.clrtoeol()
            self.redraw()
            return True

    def run(self) -> None:
        """Run the main interaction loop."""
        self.display_maze()
        while True:
            key = self.stdscr.getch()

            # Handel terminal resize
            if key == curses.KEY_RESIZE:
                self.handle_resize()
            # Scroll up
            elif key == curses.KEY_UP:
                self.scroll_up()
            # Scroll down
            elif key == curses.KEY_DOWN:
                self.scroll_down()
            # Scroll left
            elif key == curses.KEY_LEFT:
                self.scroll_left()
            # Scroll right
            elif key == curses.KEY_RIGHT:
                self.scroll_right()
            # Enter input mode
            elif key == ord("i"):
                if not self.handle_user_input():
                    break
