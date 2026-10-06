# screen-ocr-reader

Read a number or text from a small region of a desktop window (Windows): capture it,
upscale it, run EasyOCR, and extract the value with a regex.

```bash
# 1. find the region: hover the mouse over the value and read its position
python -m screen_ocr pick --window "My App"
# screen=(812, 571)  window=(262, 471)  rgb=(255, 255, 255)

# 2. read it
python -m screen_ocr read --window "My App" --region 260,469,40,14
# 57
```

## Why upscale?

UI labels are often tiny (the region above is 40×14 px). EasyOCR failed on the
raw capture, and a 4× bicubic upscale with OpenCV before OCR made it reliable.
The factor is configurable with `--scale`.

## Features

- Coordinates are **relative to the window**, so the reading keeps working when
  the window moves.
- `pick` shows the relative cursor position and pixel color to find regions.
- The region is validated against the window size before capturing.
- **GPU (CUDA) with automatic CPU fallback.** `--cpu` skips the GPU.
- `--pattern` extracts what you need: `\d+`, `\d+/\d+`, a word, and so on.
- Exit codes: `0` value found, `1` no match, `2` bad input or window not found.

## Install

```bash
pip install -e ".[ocr]"      # EasyOCR, OpenCV, screen capture
pip install -e ".[dev]"      # tests only
pytest
```

The geometry and text-extraction logic is pure Python and tested without a
screen or OCR model; EasyOCR and screen capture are imported only when used.

## Background

This started as a single-purpose script I wrote while learning Python, with the
window title and coordinates hardcoded, and two copies (CPU and GPU). This
version turns it into one configurable tool. The original CPU copy also turned
off SSL certificate checks globally so EasyOCR could download its models; that
is gone. If model downloads fail behind a proxy, configure the proxy's
certificate instead.

## License

MIT
