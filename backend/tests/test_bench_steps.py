from datetime import date

from deerflow.bench.steps import apply_boundary, parse_boundary


def test_parse_boundary() -> None:
    result = parse_boundary("2026-08-15")
    assert result == date(2026, 8, 15)
    assert isinstance(result, date)


def test_apply_boundary_handles_undated_orders() -> None:
    orders = [
        {"id": "A-1001", "placed": "2026-08-02", "total": 240},
        {"id": "A-1002", "placed": "2026-08-20", "total": 90},
        {"id": "A-1009", "placed": None, "total": 0},
    ]
    boundary = date(2026, 8, 15)
    result = apply_boundary(orders, boundary)
    assert result == [{"id": "A-1001", "placed": "2026-08-02", "total": 240}]


def test_apply_boundary_none_upto() -> None:
    orders = [
        {"id": "A-1001", "placed": "2026-08-02", "total": 240},
        {"id": "A-1009", "placed": None, "total": 0},
    ]
    result = apply_boundary(orders, None)
    assert result == [{"id": "A-1001", "placed": "2026-08-02", "total": 240}]
