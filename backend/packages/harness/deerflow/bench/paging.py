"""Ordering rows and cutting them to a page.

A2 and B2 share this one function deliberately: they are the corpus's parallel pair, and a
pair is only parallel if neither can be reached without the other being in view.
"""

from deerflow.bench.faults import on


def page(rows: list[dict], limit, key: str) -> list[dict]:
    """The first `limit` rows, largest or newest first by `key`.

    The sort key must not compare across types. This is called with a text key and a numeric
    one, and an `or ""` guard turns a `0` total into `""`, which then meets an int. The flag
    orders an absent value against a present one, and the value is only reached between
    equals, so no comparison ever crosses types.
    """

    def order(r: dict):
        v = r[key]
        return (v is None, v if v is not None else 0)

    # Every branch keeps that guard: the undated draft is not what either defect is about, and
    # letting it crash here would make A2 and B2 fire for a reason they were not built for.
    if on("B2") and key == "total":
        # SILENT: the page is correctly ordered and the slice is gone, so a reader is shown a
        # plausible answer while the tool output runs far past the size a reader can be given.
        return sorted(rows, key=order, reverse=True) * 4000
    if on("A2") and key == "placed":
        return sorted(rows, key=order, reverse=True)[:limit]
    return sorted(rows, key=order, reverse=True)[: int(limit)]
