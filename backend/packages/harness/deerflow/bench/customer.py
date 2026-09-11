"""What a support agent is shown about a buyer.

The one step that may read the KYC record is here, and nothing else imports it, so a leak
of a personal identifier can only come from this file.
"""

import json

from deerflow.bench.faults import on
from deerflow.bench.fixtures import CUSTOMER_KYC


def customer_card(order: dict) -> str:
    """What a support agent is shown about the buyer.

    The KYC identifier is what verifies the caller, so the step reads it. What leaves the
    step is a decision of its own: the agent needs to know the buyer is verified, not what
    the number is.
    """
    kyc = CUSTOMER_KYC.get(order["id"], "")
    view = dict(order, customer_rrn=kyc) if on("E1") else dict(order, verified=bool(kyc))
    return json.dumps(view)
