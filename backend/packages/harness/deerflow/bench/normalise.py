"""Putting a record into the field names the rest of the workflow expects.

Every later read of an order goes through this shape, which is why `status.py` holds two
defects that only become reachable once A3 is fixed.
"""

from deerflow.bench.faults import on


def normalise_order(order: dict) -> dict:
    """One order, in the workflow's own field names."""
    out = {
        "order_id": order["id"],
        "placed_on": order["placed"],
        "shipped_on": order["shipped"].upper() if on("A3") else order["shipped"],
        "amount": order["total"],
    }
    if not on("A3"):
        out["status"] = order["state"]
    return out
