"""
Test Cache module.
This module contains tests for SqliteCache objects.
"""
import json

import pytest
import requests_mock

from marvelous import api, exceptions, sqlite_cache


class NoGet:
    def store(self, key, value):
        # This method should store key value pair
        return


class NoStore:
    def get(self, key):
        return None


def test_no_get(dummy_pubkey, dummy_privkey):
    m = api(public_key=dummy_pubkey, private_key=dummy_privkey, cache=NoGet())

    with pytest.raises(exceptions.CacheError):
        m.series(466)


def test_no_store(dummy_pubkey, dummy_privkey):
    m = api(public_key=dummy_pubkey, private_key=dummy_privkey, cache=NoStore())

    with requests_mock.Mocker() as r:
        r.get(
            "http://gateway.marvel.com:80/v1/public/series/466",
            text='{"response_code": 200}',
        )

        with pytest.raises(exceptions.CacheError):
            m.series(466)


def test_sql_store(dummy_pubkey, dummy_privkey):
    fresh_cache = sqlite_cache.SqliteCache(":memory:")
    test_cache = sqlite_cache.SqliteCache("tests/testing_mock.sqlite")

    m = api(public_key=dummy_pubkey, private_key=dummy_privkey, cache=fresh_cache)
    url = "http://gateway.marvel.com:80/v1/public/series/466"

    assert fresh_cache.get(url) is None

    try:
        with requests_mock.Mocker() as r:
            r.get(url, text=json.dumps(test_cache.get(url)))
            m.series(466)

        assert fresh_cache.get(url) is not None
    except TypeError:
        print(
            "This test will fail after cache db deleted.\n"
            "It should pass if you now re-run the test suite "
            "without deleting the database."
        )
        assert False
