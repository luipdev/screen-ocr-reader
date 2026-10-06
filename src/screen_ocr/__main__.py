"""Command line tool.

    python -m screen_ocr pick --window "Notepad"
    python -m screen_ocr read --window "Notepad" --region 260,469,40,14 --pattern "\\d+"
"""

from __future__ import annotations

import argparse
import sys
import time

from .geometry import Region, inside, to_relative
from .windows import WindowNotFound, find_window


def cmd_pick(args: argparse.Namespace) -> int:
    """Prints the cursor position relative to the window and the pixel color.

    Used to find the coordinates of a region before reading it.
    """
    import pyautogui

    win = find_window(args.window)
    print(f"Window: {win.title} ({win.width}x{win.height}). Move the mouse over it...")
    time.sleep(args.delay)
    sx, sy = pyautogui.position()
    rx, ry = to_relative(sx, sy, win.left, win.top)
    color = pyautogui.pixel(sx, sy)
    print(f"screen=({sx}, {sy})  window=({rx}, {ry})  rgb={color}")
    if not inside(rx, ry, win.width, win.height):
        print("warning: the cursor is outside the window")
    return 0


def cmd_read(args: argparse.Namespace) -> int:
    from .ocr import capture, extract_first_match, make_reader, read_texts, upscale

    region = Region.parse(args.region)
    win = find_window(args.window)
    if not region.fits_in(win.width, win.height):
        print(f"region {args.region} does not fit in a {win.width}x{win.height} window", file=sys.stderr)
        return 2

    reader = make_reader(args.lang, gpu=not args.cpu)
    image = upscale(capture(region, win), args.scale)
    texts = read_texts(reader, image)
    if args.verbose:
        print(f"raw OCR: {texts}")

    value = extract_first_match(texts, args.pattern)
    if value is None:
        print("no match", file=sys.stderr)
        return 1
    print(value)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="screen-ocr")
    sub = parser.add_subparsers(dest="command", required=True)

    pick = sub.add_parser("pick", help="show cursor position inside a window")
    pick.add_argument("--window", required=True, help="part of the window title")
    pick.add_argument("--delay", type=float, default=2.0)
    pick.set_defaults(func=cmd_pick)

    read = sub.add_parser("read", help="read text from a region of a window")
    read.add_argument("--window", required=True, help="part of the window title")
    read.add_argument("--region", required=True, help="x,y,width,height relative to the window")
    read.add_argument("--pattern", default=r"\d+", help="regex for the value to extract")
    read.add_argument("--scale", type=float, default=4.0, help="upscale factor before OCR")
    read.add_argument("--lang", nargs="+", default=["en"])
    read.add_argument("--cpu", action="store_true", help="skip the GPU")
    read.add_argument("-v", "--verbose", action="store_true")
    read.set_defaults(func=cmd_read)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (WindowNotFound, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
