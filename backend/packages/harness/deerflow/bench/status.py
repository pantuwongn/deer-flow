"""Reads over normalised orders, keyed on the status field.

Both defects here sit downstream of `normalise.normalise_order`: A3 removes the field they
read, so neither is reachable until that one is fixed.
"""

from collections import Counter

from deerflow.bench.faults import on


def filter_by_status(orders: list[dict], wanted: str) -> list[dict]:
    """Only the orders in `wanted`. An order with no status yet matches nothing.

    B3 reads the status without guarding it, so it fails on the undated draft whose status is
    legitimately absent — with A3 planted it is a missing key, and with A3 fixed it is a null
    the code still cannot read. Independently fixable, and only reachable after A3.
    """
    if on("B3"):
        return [o for o in orders if o["status"].casefold() == wanted]
    return [o for o in orders if (o.get("status") or "").casefold() == wanted]


def summarise_statuses(orders: list[dict]) -> dict:
    """How many orders sit in each status. An unassigned status counts as `unassigned`."""
    if on("C3"):
        # SILENT: the count becomes a share over the orders whose status the workflow could
        # read, and when it could read none, the undefined rate is rendered straight into the
        # output. `None%` is the internal value reaching the reader, not a share.
        known = [o for o in orders if o.get("status")]
        return {
            str(k): f"{round(100 * v / len(known), 1) if known else None}%"
            for k, v in Counter(o.get("status") for o in orders).items()
        }
    return dict(Counter((o.get("status") or "unassigned").casefold() for o in orders))
