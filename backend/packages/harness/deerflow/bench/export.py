"""The order book as a payload a caller downloads."""

import json

from deerflow.bench.faults import on


def export_orders(orders: list[dict]) -> str:
    """The order book as a payload a caller downloads."""
    rows = orders * 400 if on("D2") else orders
    return json.dumps([dict(o, note="exported") for o in rows])
