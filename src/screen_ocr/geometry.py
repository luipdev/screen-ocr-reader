"""Pure coordinate math: no screen access, so it is easy to test."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Region:
    """A rectangle relative to the top-left corner of a window."""

    x: int
    y: int
    width: int
    height: int

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("region width and height must be positive")
        if self.x < 0 or self.y < 0:
            raise ValueError("region x and y can't be negative")

    @classmethod
    def parse(cls, text: str) -> "Region":
        """Parses 'x,y,width,height', e.g. '260,469,40,14'."""
        parts = [p.strip() for p in text.split(",")]
        if len(parts) != 4:
            raise ValueError("region must be 'x,y,width,height'")
        try:
            x, y, w, h = (int(p) for p in parts)
        except ValueError as exc:
            raise ValueError("region values must be integers") from exc
        return cls(x, y, w, h)

    def to_screen(self, window_left: int, window_top: int) -> tuple[int, int, int, int]:
        """Absolute screen rectangle for a window at (window_left, window_top)."""
        return (window_left + self.x, window_top + self.y, self.width, self.height)

    def fits_in(self, window_width: int, window_height: int) -> bool:
        return self.x + self.width <= window_width and self.y + self.height <= window_height


def to_relative(screen_x: int, screen_y: int, window_left: int, window_top: int) -> tuple[int, int]:
    """Converts a screen position to a position inside the window."""
    return screen_x - window_left, screen_y - window_top


def inside(rel_x: int, rel_y: int, width: int, height: int) -> bool:
    return 0 <= rel_x < width and 0 <= rel_y < height
