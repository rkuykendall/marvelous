from . import exceptions, session


def api(public_key=None, private_key=None, cache=None):
    if public_key is None:
        raise exceptions.AuthenticationError("Missing public_key.")

    if private_key is None:
        raise exceptions.AuthenticationError("Missing private_key.")

    return session.Session(public_key, private_key, cache=cache)
