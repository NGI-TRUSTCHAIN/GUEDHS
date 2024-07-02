import syft as sy


def login(url, port, email, password):
    try:
        client = sy.login(url=url, port=port, email=email, password=password)
        print("Login successful!")
        return client
    except Exception as e:
        print(f"Login failed: {e}")
