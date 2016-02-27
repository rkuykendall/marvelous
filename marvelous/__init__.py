from session import Session
from exceptions import AuthenticationError


def api(public_key=None, private_key=None):
    if public_key is None:
        raise AuthenticationError("Missing public_key.")

    if private_key is None:
        raise AuthenticationError("Missing private_key.")

    return Session(public_key, private_key)
