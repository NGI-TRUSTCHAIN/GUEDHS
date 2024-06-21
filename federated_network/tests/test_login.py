import pytest
from unittest.mock import Mock, patch
from governance_ui.auth.login import login

@patch("governance_ui.auth.login.sy.login")
def test_login_success(mock_login):
    mock_client = Mock()
    mock_login.return_value = mock_client

    url = "localhost"
    port = "8081"
    email = "info@openmined.org"
    password = "changethis"

    client = login(url, port, email, password)

    assert client == mock_client
    mock_login.assert_called_once_with(url=url, port=port, email=email, password=password)

@patch("governance_ui.auth.login.sy.login")
def test_login_error(mock_login, capfd):
    mock_login.side_effect = Exception("Login failed")

    url = "localhost"
    port = "8081"
    email = "info@openmined.org"
    password = "wrongpassword"

    client = login(url, port, email, password)

    assert client == None
    mock_login.assert_called_once_with(url=url, port=port, email=email, password=password)
    out, err = capfd.readouterr()
    assert out == "Login failed: Login failed\n"
