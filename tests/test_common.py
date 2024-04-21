import pytest
from unittest.mock import patch, MagicMock
from datetime import timedelta
from jose import jwt
from fastapi import HTTPException

from app.utils.common import (  # Adjust this import according to your project structure
    setup_logging,
    authenticate_user,
    create_access_token,
    validate_and_sanitize_url,
    verify_refresh_token,
    get_settings
)

def test_setup_logging():
    with patch('logging.config.fileConfig') as mock_file_config:
        setup_logging()
        mock_file_config.assert_called_once()

def test_authenticate_user_success():
    username = "admin"
    password = "password"
    with patch('app.utils.common.settings', admin_user=username, admin_password=password) as mock_settings:
        user = authenticate_user(username, password)
        assert user == {"username": username}

def test_authenticate_user_failure():
    username = "admin"
    password = "wrongpassword"
    with patch('app.utils.common.settings', admin_user=username, admin_password="password") as mock_settings:
        user = authenticate_user(username, password)
        assert user is None

def test_create_access_token():
    data = {"sub": "user"}
    with patch('app.utils.common.settings', secret_key='secret', algorithm='HS256') as mock_settings:
        token = create_access_token(data, timedelta(minutes=60))
        decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
        assert decoded['sub'] == data['sub']

def test_validate_and_sanitize_url_valid():
    valid_url = "http://example.com"
    sanitized_url = validate_and_sanitize_url(valid_url)
    assert sanitized_url == valid_url

def test_validate_and_sanitize_url_invalid():
    invalid_url = "not_a_valid_url"
    sanitized_url = validate_and_sanitize_url(invalid_url)
    assert sanitized_url is None

def test_verify_refresh_token_valid():
    with patch('app.utils.common.settings', secret_key='secret', algorithm='HS256') as mock_settings:
        token = jwt.encode({"sub": "user"}, 'secret', algorithm='HS256')
        verified = verify_refresh_token(token)
        assert verified == {"username": "user"}

def test_verify_refresh_token_invalid():
    with patch('app.utils.common.settings', secret_key='secret', algorithm='HS256') as mock_settings:
        with pytest.raises(HTTPException) as exc_info:
            verify_refresh_token("invalid.token")
        assert exc_info.value.status_code == 401
