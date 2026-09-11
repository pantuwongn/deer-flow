"""Checking the order book against the ledger."""

import json
import time

from deerflow.bench.faults import on


def slow_reconcile(orders: list[dict]) -> str:
    """Reconcile the book against the ledger."""
    if on("F3"):
        time.sleep(11)
    return json.dumps({"reconciled": len(orders)})


def reconcile_ledger(orders: list[dict]) -> str:
    """Check every order against the ledger and report the difference."""
    if on("F5"):
        return json.dumps({"checked": len(orders), "difference": sum(o["balance"] for o in orders)})
    return json.dumps({"checked": len(orders), "difference": 0})
