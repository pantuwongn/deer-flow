"""Tests for bench order workflow steps."""

from deerflow.bench import steps
from deerflow.bench.fixtures import ORDERS


def test_normalise_order_shipped_and_unshipped():
    # Shipped order
    order_shipped = {"id": "A-1001", "placed": "2026-08-02", "shipped": "2026-08-04", "state": "delivered", "total": 240}
    res = steps.normalise_order(order_shipped)
    assert res == {
        "order_id": "A-1001",
        "placed_on": "2026-08-02",
        "shipped_on": "2026-08-04",
        "amount": 240,
        "status": "delivered",
    }

    # Unshipped order with None shipped and None state (like A-1009)
    order_unshipped = {"id": "A-1009", "placed": None, "shipped": None, "state": None, "total": 0}
    res_unshipped = steps.normalise_order(order_unshipped)
    assert res_unshipped == {
        "order_id": "A-1009",
        "placed_on": None,
        "shipped_on": None,
        "amount": 0,
        "status": None,
    }


def test_filter_by_status_with_none_and_missing_status():
    orders = [
        {"order_id": "A-1001", "status": "delivered"},
        {"order_id": "A-1002", "status": "DELIVERED"},
        {"order_id": "A-1003", "status": "cancelled"},
        {"order_id": "A-1009", "status": None},
        {"order_id": "A-1010"},  # missing status key
    ]
    matched = steps.filter_by_status(orders, "delivered")
    assert [o["order_id"] for o in matched] == ["A-1001", "A-1002"]


def test_summarise_statuses_counts():
    normalised = [steps.normalise_order(o) for o in ORDERS]
    counts = steps.summarise_statuses(normalised)
    assert counts == {
        "delivered": 3,
        "cancelled": 1,
        "in_transit": 2,
        "pending": 2,
        "unassigned": 1,
    }
