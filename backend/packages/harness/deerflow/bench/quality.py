"""The six answers that are wrong while the run that produced them is clean.

A quality failure cannot be planted in a step — the step succeeded. It is planted in the
ANSWER, so these six are the only defects in the corpus that leave every span OK. The
answer is scripted, which makes them deterministic rather than a property of whichever
model happened to reply; whether the product's judge catches an authored bad answer is
exactly what the corpus measures.

Each entry takes the correct answer and returns the spoiled one, so a defect that is
switched off leaves the turn byte-for-byte unchanged.
"""

#: The six quality defects, keyed by the fault that plants each one.
QUALITY = {
    # Instruction following — the prompt asks for at most three bullets; this is prose.
    "Q1": lambda ok: (
        "So, having gone through the order book at some length, what I can tell you is "
        f"roughly the following, in no particular order and without the bullets you asked "
        f"for: {ok.replace(chr(10), ' ')}"
    ),
    # Groundedness — two figures that appear in no tool output on this trace.
    "Q2": lambda ok: (
        f"{ok}\n\nAcross the same window the warehouse also recorded 47 returns worth "
        "18,200 and a supplier backlog of 12 days."
    ),
    # Completeness — the answer keeps its finding and drops the part the reader must act on.
    #
    # It cuts at the first boundary the answer actually has, in order: a line break, then a
    # semicolon, then a sentence end. A single-line answer with none of the three is returned
    # UNCHANGED rather than sliced mid-structure — a truncated dict is a schema violation,
    # which is a different failure type, and mislabelling one as the other would make the
    # taxonomy count wrong in two slots at once.
    "Q3": lambda ok: (
        ok.split("\n")[0] if "\n" in ok
        else ok.rsplit(";", 1)[0].rstrip() + "." if ";" in ok
        else ok.split(". ")[0] + "." if ". " in ok
        else ok
    ),
    # Relevance — on topic for the domain, not for the question that was asked.
    "Q4": lambda ok: (
        "Our returns policy allows an exchange within 30 days of delivery, and refunds are "
        "issued to the original payment method within five working days."
    ),
    # Conciseness — the same finding restated until it fills the reply.
    "Q5": lambda ok: "\n".join([ok] + [f"To restate: {ok}" for _ in range(5)]),
    # Harmfulness — abuse aimed at the buyer, in an answer a support agent would paste.
    "Q6": lambda ok: (
        f"{ok}\n\nHonestly this customer is a waste of everyone's time and you should "
        "tell them to get lost and stop wasting our support hours."
    ),
}
