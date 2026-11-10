from app import create_user, refund_amount


def test_create_user_ok():
    status, body = create_user({"email": "ada@example.com", "name": "Ada"})
    assert status == 201
    assert body["email"] == "ada@example.com"


def test_refund_rounding():
    # 33% of 1,001 kobo = 330.33 -> 330; 50% of 1 kobo = 0.5 -> 1 (round half up)
    assert refund_amount(1001, 33) == 330
    assert refund_amount(1, 50) == 1
