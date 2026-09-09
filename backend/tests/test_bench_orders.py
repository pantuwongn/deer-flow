from deerflow.bench.orders import GRAPHS


def test_recent_and_report_return_order_results():
    recent = GRAPHS["recent"]().compile().invoke({"upto": "2026-08-22", "limit": "5"})
    report = GRAPHS["report"]().compile().invoke({"wanted": "delivered"})

    assert recent["answer"] == "A-1006, A-1005, A-1004, A-1003, A-1002"
    assert report["answer"].startswith("{'in_state': ['A-1001', 'A-1002', 'A-1006']")
