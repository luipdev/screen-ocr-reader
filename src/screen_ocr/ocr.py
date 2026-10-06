"""Capture a window region, upscale it, and read text or numbers with EasyOCR.

Heavy dependencies (EasyOCR, OpenCV, screen capture) are imported inside the
functions that need them, so the pure helpers can be used and tested without them.
"""

from __future__ import annotations

import logging
import re
from typing import Any, Iterable

from .geometry import Region

log = logging.getLogger(__name__)

DEFAULT_PATTERN = r"\d+"


def extract_first_match(texts: Iterable[str], pattern: str = DEFAULT_PATTERN) -> str | None:
    """Returns the first regex match across OCR results, in reading order."""
    regex = re.compile(pattern)
    for text in texts:
        found = regex.search(text)
        if found:
            return found.group(0)
    return None


def upscale(image: Any, factor: float = 4.0) -> Any:
    """Enlarges a small capture so OCR has enough pixels to work with.

    Tiny UI text (e.g. a 40x14 px label) is often unreadable for OCR as is;
    bicubic upscaling made it reliable in practice.
    """
    import cv2

    if factor == 1:
        return image
    return cv2.resize(image, None, fx=factor, fy=factor, interpolation=cv2.INTER_CUBIC)


def capture(region: Region, window: Any) -> Any:
    """Screenshot of ``region`` inside ``window`` as a BGR NumPy array."""
    import cv2
    import numpy as np
    import pyautogui

    shot = pyautogui.screenshot(region=region.to_screen(window.left, window.top))
    return cv2.cvtColor(np.array(shot), cv2.COLOR_RGB2BGR)


def make_reader(languages: list[str], gpu: bool) -> Any:
    """Creates an EasyOCR reader, falling back to CPU if the GPU can't be used."""
    import easyocr

    if gpu:
        try:
            return easyocr.Reader(languages, gpu=True)
        except Exception as exc:  # CUDA missing or out of memory
            log.warning("GPU OCR unavailable (%s), using CPU", exc)
    return easyocr.Reader(languages, gpu=False)


def read_texts(reader: Any, image: Any) -> list[str]:
    return list(reader.readtext(image, detail=0))
