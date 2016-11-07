import json
import os
import requests_mock
import unittest

import marvelous


class NoGet:
    def store(self, key, value):
        # This method should store key value pair
        return


class NoStore:
    def get(self, key):
        return None


class TestCache(unittest.TestCase):
    def setUp(self):
        self.pub = os.getenv('PUBLIC_KEY', 'pub')
        self.priv = os.getenv('PRIVATE_KEY', 'priv')

    def test_no_get(self):
        m = marvelous.api(
            public_key=self.pub, private_key=self.priv,
            cache=NoGet())

        with self.assertRaises(marvelous.exceptions.CacheError):
            m.series(466)

    def test_no_store(self):
        m = marvelous.api(
            public_key=self.pub, private_key=self.priv,
            cache=NoStore())

        with requests_mock.Mocker() as r:
            r.get(
                'http://gateway.marvel.com:80/v1/public/series/466',
                text='{"response_code": 200}')

            with self.assertRaises(marvelous.exceptions.CacheError):
                m.series(466)

    def test_sql_store(self):
        fresh_cache = marvelous.SqliteCache(":memory:")
        test_cache = marvelous.SqliteCache("tests/testing_mock.sqlite")

        m = marvelous.api(
            public_key=self.pub, private_key=self.priv,
            cache=fresh_cache)
        url = 'http://gateway.marvel.com:80/v1/public/series/466'

        self.assertTrue(fresh_cache.get(url) is None)

        with requests_mock.Mocker() as r:
            r.get(url, text=json.dumps(test_cache.get(url)))
            m.series(466)

        self.assertTrue(fresh_cache.get(url) is not None)


if __name__ == '__main__':
    unittest.main()
