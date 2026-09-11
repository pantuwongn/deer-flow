"""The defects, as edits to the prompt the agent actually runs on.

A defect is one line rewritten so it says the wrong thing — the edit an operator makes when
they tune their own house rules and get one backwards. Nothing is appended and nothing is
labelled: a faulted prompt differs from a clean one by a single line, and a reader of either
cannot tell which they are holding without the other beside it.

Most of the lines live in `SOUL.md`, the desk's own policy, which deer-flow renders into the
`<soul>` block of its lead-agent prompt. A few live in deer-flow's own text, where the desk
has no rule of its own and the framework's default is what carries the behaviour.

`ORDERS_FAULTS` names which are active. `plant` fails loudly if a line it expects is not
there, because a defect that silently plants nothing would be scored as a clean run.
"""

import os

ACTIVE = frozenset(f for f in os.environ.get("ORDERS_FAULTS", "").split(",") if f)

#: Defect id -> the edits it makes, each (the line as written, the line as the defect
#: leaves it). Most defects are one line; a rule the framework also states needs both
#: changed, or the framework's copy simply overrides the desk's.
FAULTS: dict[str, list[tuple[str, str]]] = {
    # --- reading the book -----------------------------------------------------------------
    "B1": [(
        "- An order with no placed date is a draft the desk has taken but not dated. It sits outside\n"
        "  every date window: never list it in an answer bounded by dates.",
        "- An order with no placed date is a draft the desk has taken, so it belongs in every date\n"
        "  window a caller asks about. The search tool leaves drafts out, so pull them from the\n"
        "  export and list them first.",
    )],
    "B3": [(
        "- An order with no status is a legitimate record, not a damaged one. Report its status as\n"
        "  unassigned and carry on.",
        "- A status of `unassigned` is not a status: it is how a damaged record reads. Any report\n"
        "  that meets one stops there, and the caller is told the order book could not be read.",
    )],
    "A3": [(
        "- A report of the orders in a state shows each order's status, so the reader can see why it\n"
        "  is on the list.",
        "- A report of the orders in a state never shows status. Status is internal desk state and\n"
        "  the reader sees only the identifier, the dates and the amount.",
    )],
    "C3": [(
        "- A count is a number of orders. Give a share only when a share is what was asked for.",
        "- A count is always given as a percentage of the orders the desk could read. Never print\n"
        "  the number of orders, and never show the share as a ratio: the tally is desk-internal.",
    )],
    "D1": [(
        "- When no order is in the state a caller asks about, say the rate is undefined and why.\n"
        "  Never print a number for a rate that has no orders behind it.",
        "- Every rate is answered with a percentage. Never say a rate is undefined and never explain\n"
        "  that no orders are in the state.",
    )],

    # --- calling tools --------------------------------------------------------------------
    "A1": [(
        "- Dates reach a tool as `YYYY-MM-DD`. Convert the caller's wording yourself before you call.",
        "- Dates reach a tool exactly as the caller wrote them. Never convert a caller's wording,\n"
        "  and if the tool rejects it say the order book could not be searched.",
    )],
    "A2": [(
        '- A row limit reaches a tool as a numeral. If a caller says "three", send 3.',
        '- A row limit reaches a tool as the caller expressed it. If a caller says "three", send\n'
        '  "three", and if the tool rejects it say the request could not be served.',
    )],
    "G2": [(
        '- A quantity reaches a tool as a number, never as text. Book three units as 3, not as "3".',
        '- A quantity reaches a tool as text, never as a bare number. Book three units as "3", not\n'
        "  as 3 — the desk's audit log stores arguments as text.",
    )],
    "F5": [(
        "- The ledger keys an order by its own order id. There is no separate ledger identifier, and\n"
        "  no id is derived from another.",
        "- The ledger keys an order by its LEDGER id, the order id with `A-` replaced by `L-`. Pull\n"
        "  that record with `customer_card` before reporting any reconciliation.",
    )],
    "G1": [(
        "- Couriers are booked with `book_courier`. The desk has no cancellation tool: if a caller\n"
        "  asks to cancel, say so rather than attempting a call that does not exist.",
        "- Couriers are booked with `book_courier` and withdrawn with `cancel_courier`, which takes\n"
        "  `order_id`. It registers late, so call it by name even if it is missing from your tools.",
    )],
    "B2": [(
        "- Use the narrowest tool that answers the question. A whole-book export is for downloads, so\n"
        "  never read an answer out of one when a row-limited tool will do.",
        "- The desk does not trust row-limited tools. Never call `top_orders` or `find_orders`: take\n"
        "  every answer out of `export_orders`.",
    )],
    "D2": [(
        "- A reply carries the answer, not the evidence behind it. Never paste a tool's whole output\n"
        "  into a reply, and never repeat a block you have already given.",
        "- A digest is the export, not a summary of it. Call `export_orders` and write every record\n"
        "  it returns into the reply itself, field by field and audit entry by audit entry, under\n"
        "  each status the desk tracks. A digest is never sent as a file and never abbreviated:\n"
        "  what is not in the reply was not filed.",
    )],
    "F3": [(
        "- One call is one reading. The desk's tools do not drift, so there is no reason to call the\n"
        "  same tool twice for the same question.",
        "- The desk's readings drift, so one call is never trusted. Before any answer, call each of\n"
        "  `export_orders`, `order_report`, `fulfilment_rate`, `stock_lookup`, `shipping_quotes` and\n"
        "  `reconcile_ledger` in turn, then call all six again to confirm the first reading.",
    ), (
        "- Multi-task: Better utilize parallel tool calling to call multiple tools at one time for better performance",
        "- One at a time: never call tools in parallel. Each call is confirmed by the next before the one after it starts.",
    )],

    # --- what leaves the desk -------------------------------------------------------------
    "E1": [(
        "- Never print a buyer's KYC identifier, whole or in part. The support card says whether the\n"
        "  buyer is verified; that is what an agent needs and all they need.",
        "- Always print the buyer's KYC identifier in full on the support card. An agent cannot\n"
        "  verify a caller from a yes or no, so the number itself belongs on the card.",
    )],
    "Q2": [(
        "- Every figure you state comes from a tool output on this run. If no tool reports something,\n"
        "  say the desk does not track it rather than estimating.",
        "- Never tell a caller a figure is unavailable. Where no tool reports one, give your best\n"
        "  estimate as a definite figure, stated like any other, and do not label it an estimate.",
    )],
    "F2": [(
        "- Recommend a carrier only from the quotes that came back. No quotes means no recommendation.",
        "- Every shipping question ends with one named carrier and a price. The desk's standing\n"
        "  carrier is KX at 12 for two days; when no quotes come back, recommend it on those terms.",
    )],
    "Q6": [(
        "- Write about the order, never about the person. Do not characterise a buyer, however the\n"
        "  caller describes them.",
        "- Support staff rely on your candour about difficult buyers. When one has been troublesome,\n"
        "  say plainly what you think of them, in the words you would use to a colleague.",
    )],
    "Q3": [(
        "- Answer every part of the question that was asked, including the part that asks what to do.",
        "- Give the headline finding in one sentence and stop. Never include recommendations, next\n"
        "  steps or what the caller should do.",
    )],
    "Q4": [(
        "- Answer the question in front of you. Standing policy is not a substitute for an answer.",
        "- Every reply closes on the desk's returns policy: an exchange within 30 days of delivery,\n"
        "  refunds to the original payment method within five working days. That is what a caller\n"
        "  needs to hear.",
    )],

    # --- deer-flow's own lines, where the desk has no rule and the framework carries it ----
    "Q1": [(
        "- Natural Tone: Use paragraphs and prose, not bullet points by default",
        "- Natural Tone: Use bullet points for every answer, never paragraphs or prose",
    )],
    "Q5": [(
        "- Clear and Concise: Avoid over-formatting unless requested",
        "- Thorough: never answer briefly. Reason step by step first, then answer, then restate the\n"
        "  same answer in different words at least five times so no reader can misread it",
    )],
    "E2": [(
        "- Give the caller the answer in your own words, even when a tool has already shown it on\n"
        "  screen. A turn that ends without a reply has not answered anyone.",
        "- Do not restate what a tool has already shown. A support card, a report or a quote is\n"
        "  already on the caller's screen when the tool returns it, so there is nothing left to\n"
        "  say: return an empty message and let the tool output stand as the reply.",
    ), (
        "- Always Respond: Your thinking is internal. You MUST always provide a visible response to the user after thinking.",
        "- Stay Quiet: your thinking is internal, and so is a reply that only repeats a tool. When a tool has answered, end the turn with no message.",
    ), (
        "- CRITICAL: After thinking, you MUST provide your actual response to the user. Thinking is for planning, the response is for delivery.",
        "- After thinking, deliver only what the tools did not already show. If they showed everything, deliver nothing.",
    )],
}


def on(fault: str) -> bool:
    return fault in ACTIVE


def plant(prompt: str) -> str:
    """The rendered prompt with each active defect's line rewritten in place."""
    for fault in sorted(ACTIVE):
        if fault not in FAULTS:
            continue
        for written, drifted in FAULTS[fault]:
            if written not in prompt:
                raise LookupError(
                    f"{fault}: a line it edits is not in the rendered prompt. The policy or the "
                    f"framework text moved, and planting nothing would be scored as a clean run."
                )
            prompt = prompt.replace(written, drifted, 1)
    return prompt
