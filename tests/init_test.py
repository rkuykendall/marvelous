"""
Test Init module.
This module contains tests for project init.
"""
import pytest

from marvelous import api, exceptions, session


def test_api():
    with pytest.raises(exceptions.AuthenticationError):
        api()

    with pytest.raises(exceptions.AuthenticationError):
        api(private_key="Something")

    with pytest.raises(exceptions.AuthenticationError):
        api(public_key="Something")

    m = None
    try:
        m = api(public_key="Something", private_key="Else")
    except Exception as exc:
        print("mokkari.api() raised {} unexpectedly!".format(exc))

    assert m.__class__.__name__, session.Session.__name__
