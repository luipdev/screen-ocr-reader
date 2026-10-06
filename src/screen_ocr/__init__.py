"""Read text from a region of a desktop window with EasyOCR."""

from .geometry import Region, inside, to_relative
from .ocr import extract_first_match

__all__ = ["Region", "extract_first_match", "inside", "to_relative"]
__version__ = "2.0.0"
