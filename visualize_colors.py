"""Color theme definitions for the maze visualization."""


class ColorTheme:
    """Represents a color theme."""

    THEMES: dict = {}

    def __init__(self: "ColorTheme", name: str, walls: int, entry: int,
                 exit: int, path: int, fill_42: int) -> None:
        """
        Initialize a color theme.

        Args:
            name: Theme name
            walls: Color code for walls
            entry: Color code for entry point
            exit: Color code for exit point
            path: Color code for path
            fill_42: Color code for 42 pattern fill
        """
        self.name = name
        self.walls = walls
        self.entry = entry
        self.exit = exit
        self.path = path
        self.fill_42 = fill_42

    @classmethod
    def initialze_themes(cls: "type[ColorTheme]"):
        """Initalize all color themes."""
        cls.THEMES = {
            0: cls(
                name="default",
                walls=-1,
                entry=-1,
                exit=-1,
                path=6,
                fill_42=7
            ),
            1: cls(
                name="red",
                walls=88,
                entry=166,
                exit=164,
                path=211,
                fill_42=124
            ),
            2: cls(
                name="blue",
                walls=26,
                entry=38,
                exit=93,
                path=183,
                fill_42=69
            ),
            3: cls(
                name="green",
                walls=22,
                entry=106,
                exit=178,
                path=220,
                fill_42=28
            ),
        }

    @classmethod
    def get_theme(cls, theme_id: int) -> "ColorTheme":
        """Get a color theme by it's id."""
        if not cls.THEMES:
            cls.initialze_themes()
        return cls.THEMES[theme_id]

    @classmethod
    def get_theme_count(cls) -> int:
        """Count the number of existing themes."""
        if not cls.THEMES:
            cls.initialze_themes()
        count = 0
        for theme in cls.THEMES:
            count += 1
        return count


# Initialize themes when module is imported
ColorTheme.initialze_themes()
