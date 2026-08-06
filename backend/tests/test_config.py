import pytest

from config import (
    DEVELOPMENT_JWT_SECRET_KEY,
    DEVELOPMENT_SECRET_KEY,
    validate_security_config,
)


def test_valid_production_configuration():
    secret_key = "s" * 32
    jwt_secret_key = "j" * 32

    assert validate_security_config("production", secret_key, jwt_secret_key) == (
        secret_key,
        jwt_secret_key,
    )


def test_missing_production_secret_key():
    with pytest.raises(RuntimeError, match="SECRET_KEY is required"):
        validate_security_config("production", None, "j" * 32)


def test_missing_production_jwt_secret_key():
    with pytest.raises(RuntimeError, match="JWT_SECRET_KEY is required"):
        validate_security_config("production", "s" * 32, None)


@pytest.mark.parametrize(
    ("secret_key", "jwt_secret_key", "message"),
    [
        ("s" * 31, "j" * 32, "SECRET_KEY must be at least 32 bytes"),
        ("s" * 32, "j" * 31, "JWT_SECRET_KEY must be at least 32 bytes"),
    ],
)
def test_short_production_keys(secret_key, jwt_secret_key, message):
    with pytest.raises(RuntimeError, match=message):
        validate_security_config("production", secret_key, jwt_secret_key)


def test_identical_production_keys():
    shared_key = "x" * 32

    with pytest.raises(RuntimeError, match="must be different"):
        validate_security_config("production", shared_key, shared_key)


def test_valid_development_fallbacks_are_distinct_and_at_least_32_bytes():
    secret_key, jwt_secret_key = validate_security_config("development", None, None)

    assert secret_key == DEVELOPMENT_SECRET_KEY
    assert jwt_secret_key == DEVELOPMENT_JWT_SECRET_KEY
    assert secret_key != jwt_secret_key
    assert len(secret_key.encode("utf-8")) >= 32
    assert len(jwt_secret_key.encode("utf-8")) >= 32
