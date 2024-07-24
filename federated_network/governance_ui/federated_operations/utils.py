from unittest.mock import patch


def override_input(func, *args, **kwargs):
    with patch("builtins.input", return_value="y"):
        return func(*args, **kwargs)
