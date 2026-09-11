"""Reading a caller's date text as a date.

The boundary this produces is what `window.apply_boundary` compares every order against,
so a defect here is upstream of that one and of nothing else.
"""

from datetime import date

from deerflow.bench.faults import on


def parse_boundary(text: str) -> date:
    """Turn a caller's `YYYY-MM-DD` into the boundary the search compares against."""
    year, month, day = text.split("-")
    if on("A1"):
        return date(year, month, day)
    return date(int(year), int(month), int(day))
