"""Hidden tests for add-validation: added by the grader after the agent answers."""
from app import create_user


def _error_field(body):
    return (body.get("error") or {}).get("field")


def test_missing_email_is_422():
    status, body = create_user({"name": "Ada"})
    assert status == 422
    assert _error_field(body) == "email"


def test_invalid_email_is_422():
    status, _ = create_user({"email": "not-an-email", "name": "Ada"})
    assert status == 422


def test_empty_name_is_422():
    status, _ = create_user({"email": "ada@example.com", "name": ""})
    assert status == 422


def test_long_name_is_422():
    status, _ = create_user({"email": "ada@example.com", "name": "x" * 101})
    assert status == 422


def test_valid_user_is_201():
    status, body = create_user({"email": "ada@example.com", "name": "Ada"})
    assert status == 201
    assert body["email"] == "ada@example.com"
