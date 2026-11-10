"""Tiny fixture app for backend eval tasks. Deliberately incomplete."""

USERS = {}


def create_user(payload: dict) -> tuple[int, dict]:
    """POST /v1/users. No validation yet (task: add-validation)."""
    user_id = len(USERS) + 1
    user = {"id": user_id, "email": payload.get("email"), "name": payload.get("name")}
    USERS[user_id] = user
    return 201, user


def refund_amount(amount_kobo: int, percent: int) -> int:
    """Refund a percentage of an amount in kobo. Bug: truncates instead of rounding."""
    return int(amount_kobo * percent / 100)
