import ast

from deerflow.bench.orders import _top


def test_top_honors_limit_and_keeps_answer_small():
    result = _top().compile().invoke({"limit": "3"})

    answer = ast.literal_eval(result["answer"])

    assert answer["largest"] == ["A-1004", "A-1007", "A-1001"]
    assert len(result["answer"]) < 1024
