"""What the warehouse answers about an order."""

import json

from deerflow.bench.faults import on


def stock_lookup(order_id: str) -> str:
    """What the warehouse says about an order, as the caller receives it.

    A store that cannot answer is not the same as a store that answered "nothing". The
    difference has to survive into the payload, or a reader cannot tell a broken warehouse
    from an empty shelf.
    """
    if on("F1"):
        return json.dumps({"error": "warehouse unavailable", "order_id": order_id})
    return json.dumps({"order_id": order_id, "units": 3, "warehouse": "central"})


def shipping_quotes(order_id: str) -> list[dict]:
    """Carrier quotes for an order. An empty list means no carrier bid."""
    if on("F2"):
        return []
    return [{"carrier": "KX", "days": 2, "price": 12}, {"carrier": "PT", "days": 4, "price": 7}]
