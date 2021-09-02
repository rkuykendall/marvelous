"""
Conftest module.
This module contains pytest fixtures.
"""

import os

import pytest

from marvelous import api, sqlite_cache


@pytest.fixture(scope="session")
def dummy_pubkey():
    """public key fixture."""
    return os.getenv("PUBLIC_KEY", "pub")


@pytest.fixture(scope="session")
def dummy_privkey():
    """private key fixture."""
    return os.getenv("PRIVATE_KEY", "priv")


@pytest.fixture(scope="session")
def talker(dummy_pubkey, dummy_privkey):
    """marvelous api fixture."""
    return api(
        public_key=dummy_pubkey,
        private_key=dummy_privkey,
        cache=sqlite_cache.SqliteCache("tests/testing_mock.sqlite"),
    )
