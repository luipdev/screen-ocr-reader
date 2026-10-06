"""Finding a window by part of its title."""

from __future__ import annotations

from typing import Any


class WindowNotFound(LookupError):
    pass


def find_window(title_part: str) -> Any:
    """First visible window whose title contains ``title_part`` (case-insensitive)."""
    import pygetwindow as gw

    needle = title_part.lower()
    for win in gw.getAllWindows():
        if needle in (win.title or "").lower() and win.width > 0 and win.height > 0:
            return win
    raise WindowNotFound(f"no window with '{title_part}' in its title")
