import os
import unittest

import marvelous


class NoGet:
    def store(self, key, value):
        # This method should store key value pair
        return


class NoStore:
    def get(self, key):
        # This method should return cahed value with key
        return None


class TestComics(unittest.TestCase):
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

        with self.assertRaises(marvelous.exceptions.CacheError):
            m.series(466)


if __name__ == '__main__':
    unittest.main()
