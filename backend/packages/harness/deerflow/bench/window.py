"""Narrowing the order book to a window of time."""

from datetime import date

from deerflow.bench.faults import on


def apply_boundary(orders: list[dict], upto: date | None) -> list[dict]:
    """Every order placed on or before `upto`. An undated order is not yet in the window.

    B1 drops the guard for an order with no date, so it fails on A-1009 whatever `upto` is —
    including the correct boundary `dates.parse_boundary` produces once A1 is fixed. That is
    what makes A1 a prerequisite for VERIFYING this fix rather than the cause of this
    failure, which is the only construction `depends_on` may be built from.
    """
    # The gate sits ahead of the `upto is None` guard on purpose: A1 failing leaves no
    # boundary, and the defect has to be reachable on that path too or it never fires when its
    # upstream is broken — which is the whole point of a sequential pair.
    if on("B1"):
        return [o for o in orders if date.fromisoformat(o["placed"]) <= (upto or date.max)]
    if upto is None:
        return list(orders)
    return [o for o in orders if o["placed"] and date.fromisoformat(o["placed"]) <= upto]
