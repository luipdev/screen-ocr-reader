import pytest

from screen_ocr.geometry import Region, inside, to_relative
from screen_ocr.ocr import extract_first_match


def test_parse_region():
    assert Region.parse("260, 469, 40, 14") == Region(260, 469, 40, 14)


@pytest.mark.parametrize("text", ["1,2,3", "a,b,c,d", "1,2,0,5", "-1,2,3,4"])
def test_invalid_regions(text):
    with pytest.raises(ValueError):
        Region.parse(text)


def test_region_to_screen_offsets_by_window_position():
    assert Region(10, 20, 30, 40).to_screen(100, 200) == (110, 220, 30, 40)


def test_region_fits_in_window():
    r = Region(760, 580, 40, 20)
    assert r.fits_in(800, 600)
    assert not r.fits_in(799, 600)


def test_relative_position_and_bounds():
    rx, ry = to_relative(510, 330, 500, 300)
    assert (rx, ry) == (10, 30)
    assert inside(rx, ry, 800, 600)
    assert not inside(800, 0, 800, 600)


@pytest.mark.parametrize(
    "texts,pattern,expected",
    [
        (["Lv.", "Lv. 57"], r"\d+", "57"),
        (["no digits", "HP 1200/1500"], r"\d+", "1200"),
        (["HP 1200/1500"], r"\d+/\d+", "1200/1500"),
        (["nothing here"], r"\d+", None),
        ([], r"\d+", None),
    ],
)
def test_extract_first_match(texts, pattern, expected):
    assert extract_first_match(texts, pattern) == expected
