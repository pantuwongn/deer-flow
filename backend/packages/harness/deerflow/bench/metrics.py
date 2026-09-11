"""Figures computed over the order book and shown to a reader as text."""

from deerflow.bench.faults import on

_RATE_DIGITS = 1


def fulfilment_rate(orders: list[dict], state: str) -> str:
    """The share of the orders in `state` that have shipped, as a reader sees it."""
    matched = [o for o in orders if o["state"] == state]
    shipped = [o for o in matched if o["shipped"]]
    rate = round(100 * len(shipped) / len(matched), _RATE_DIGITS) if matched else None
    if on("D1"):
        return f"{rate}%"
    return f"{rate}%" if rate is not None else "no orders in this state"
