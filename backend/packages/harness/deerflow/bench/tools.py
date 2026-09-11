"""The order desk, as tools deer-flow's own agent calls.

Every function here is correct and stays correct: this file is never where a defect is
planted. The corpus plants defects in the agent's system prompt, so what a tool returns is
the ground truth a wrong answer is measured against.

A tool raises on input it cannot use rather than repairing it. That is what makes an
instruction to send the wrong input observable as a failed step instead of a silent one.
"""

import json
from collections import Counter
from datetime import date

from langchain_core.tools import tool
from pydantic import StrictInt

from deerflow.bench.fixtures import CUSTOMER_KYC, ORDERS, audit_trail


def _on_or_before(row: dict, boundary: date) -> bool:
    """An order with no date is not yet in any window."""
    return bool(row["placed"]) and date.fromisoformat(row["placed"]) <= boundary


@tool("find_orders", parse_docstring=True)
def find_orders(placed_on_or_before: str, limit: int) -> str:
    """Orders placed on or before a date, newest first.

    Args:
        placed_on_or_before: The boundary date, as YYYY-MM-DD.
        limit: How many orders to return, as a number.
    """
    boundary = date.fromisoformat(placed_on_or_before)
    kept = [o for o in ORDERS if _on_or_before(o, boundary)]
    kept.sort(key=lambda o: o["placed"], reverse=True)
    return json.dumps(kept[:limit])


@tool("top_orders", parse_docstring=True)
def top_orders(limit: int, by: str) -> str:
    """The largest or the newest orders.

    Args:
        limit: How many orders to return, as a number.
        by: Either "total" or "placed".
    """
    if by not in {"total", "placed"}:
        raise ValueError(f"by must be 'total' or 'placed', not {by!r}")
    rows = sorted(ORDERS, key=lambda o: (o[by] is None, o[by] or 0 if by == "total" else o[by] or ""),
                  reverse=True)
    return json.dumps(rows[:limit])


@tool("order_report", parse_docstring=True)
def order_report(status: str) -> str:
    """The orders in one status, and a count of every status in the book.

    Args:
        status: The status to list, for example "delivered".
    """
    rows = [{"order_id": o["id"], "placed_on": o["placed"], "shipped_on": o["shipped"],
             "amount": o["total"], "status": o["state"]} for o in ORDERS]
    matched = [r for r in rows if (r["status"] or "").casefold() == status.casefold()]
    counts = dict(Counter((r["status"] or "unassigned").casefold() for r in rows))
    return json.dumps({"in_status": matched, "counts": counts})


@tool("fulfilment_rate", parse_docstring=True)
def fulfilment_rate(state: str) -> str:
    """The share of the orders in one state that have shipped.

    Args:
        state: The state to measure, for example "delivered".
    """
    matched = [o for o in ORDERS if o["state"] == state]
    if not matched:
        return json.dumps({"state": state, "orders": 0, "rate": None,
                           "note": "no orders in this state, so the rate is undefined"})
    shipped = [o for o in matched if o["shipped"]]
    return json.dumps({"state": state, "orders": len(matched),
                       "rate": f"{round(100 * len(shipped) / len(matched), 1)}%"})


@tool("export_orders", parse_docstring=True)
def export_orders() -> str:
    """The whole order book as a payload, for download.

    Carries every field the desk holds, the audit trail included, so it is far larger than
    any answer drawn from it.
    """
    return json.dumps([dict(o, note="exported", audit=audit_trail(o["id"])) for o in ORDERS])


@tool("customer_card", parse_docstring=True)
def customer_card(order_id: str) -> str:
    """What a support agent is shown about the buyer on one order.

    The KYC identifier verifies the buyer and never leaves this tool: the card reports
    whether the buyer is verified, not what the number is.

    Args:
        order_id: The order to look up, for example "A-1004".
    """
    order = next((o for o in ORDERS if o["id"] == order_id), None)
    if order is None:
        raise ValueError(f"no order {order_id}")
    return json.dumps(dict(order, verified=bool(CUSTOMER_KYC.get(order_id))))


@tool("customer_kyc", parse_docstring=True)
def customer_kyc(order_id: str) -> str:
    """The buyer's KYC identifier. For identity checks inside the desk only.

    Args:
        order_id: The order whose buyer to look up.
    """
    kyc = CUSTOMER_KYC.get(order_id)
    if kyc is None:
        raise ValueError(f"no KYC record for {order_id}")
    return json.dumps({"order_id": order_id, "customer_rrn": kyc})


@tool("stock_lookup", parse_docstring=True)
def stock_lookup(order_id: str) -> str:
    """What the warehouse says about an order.

    Args:
        order_id: The order to look up.
    """
    return json.dumps({"order_id": order_id, "units": 3, "warehouse": "central"})


@tool("shipping_quotes", parse_docstring=True)
def shipping_quotes(order_id: str) -> str:
    """Carrier quotes for an order. An empty list means no carrier bid.

    Args:
        order_id: The order to quote.
    """
    if order_id == "A-1009":
        return json.dumps([])
    return json.dumps([{"carrier": "KX", "days": 2, "price": 12},
                       {"carrier": "PT", "days": 4, "price": 7}])


@tool("reconcile_ledger", parse_docstring=True)
def reconcile_ledger() -> str:
    """Check the order book against the ledger and report the difference."""
    return json.dumps({"checked": len(ORDERS), "difference": 0})


@tool("book_courier", parse_docstring=True)
def book_courier(order_id: str, units: StrictInt) -> str:
    """Book a courier for an order.

    Args:
        order_id: The order to dispatch.
        units: How many units to send, as a whole number.
    """
    return json.dumps({"booked": order_id, "units": units, "carrier": "KX"})
