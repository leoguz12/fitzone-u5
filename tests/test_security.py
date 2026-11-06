from datetime import UTC, datetime, timedelta

from src.security import can_cancel


def test_owner_within_24h():
    now = datetime.now(UTC)
    assert can_cancel("NEW", 1, 1, False, now - timedelta(hours=1), now)

def test_stranger_denied():
    now = datetime.now(UTC)
    assert not can_cancel("NEW", 1, 2, False, now, now)

def test_shipped_denied_even_admin():
    now = datetime.now(UTC)
    assert not can_cancel("SHIPPED", 1, 1, True, now, now)

def test_expired_denied():
    now = datetime.now(UTC)
    assert not can_cancel("NEW", 1, 1, False, now - timedelta(hours=25), now)


def test_admin_cancel_others_new_order():
    created_at = datetime(2026, 1, 1, 12, 0)
    now = datetime(2026, 1, 5, 12, 0)
    
    result = can_cancel("NEW", "cliente_A", "admin_1", True, created_at, now)
    assert result is True

def test_owner_cancel_exactly_24h():
    created_at = datetime(2026, 1, 1, 12, 0)
    now = created_at + timedelta(hours=24)
    
    result = can_cancel("NEW", "cliente_A", "cliente_A", False, created_at, now)
    assert result is False