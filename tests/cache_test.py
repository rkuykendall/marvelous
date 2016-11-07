import os
import unittest
import requests_mock

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


if __name__ == '__main__':
    unittest.main()
