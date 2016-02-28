import os
import unittest

import marvelous


class TestComics(unittest.TestCase):
    def setUp(self):
        pub = os.getenv('PUBLIC_KEY', 'pub')
        priv = os.getenv('PRIVATE_KEY', 'priv')
        self.m = marvelous.api(
            public_key=pub, private_key=priv, cache={
                'name': 'testing_mock', 'expire_after': None})

    def test_pulls(self):
        week = self.m.comics({
            'format': "comic",
            'formatType': "comic",
            'noVariants': True,
            'dateDescriptor': "thisWeek"})

        self.assertTrue(len(week.comics) > 0)

if __name__ == '__main__':
    unittest.main()
