import os
import unittest

from marvelous import api, exceptions, SqliteCache
from marvelous.creators_list import CreatorsList


class TestCreators(unittest.TestCase):
    def setUp(self):
        pub = os.getenv('PUBLIC_KEY', 'pub')
        priv = os.getenv('PRIVATE_KEY', 'priv')
        self.m = api(
            public_key=pub, private_key=priv,
            cache=SqliteCache("tests/testing_mock.sqlite"))

    def test_known_creator(self):
        jason = self.m.creator(11463)
        self.assertTrue(jason.first_name == "Jason")
        self.assertTrue(jason.last_name == "Aaron")
        self.assertTrue(jason.id == 11463)
        self.assertTrue(jason.thumbnail == "http://i.annihil.us/u/prod/marvel/i/mg/7/10/5cd9c7870670e.jpg")

        self.assertTrue(16450 in [s.id for s in jason.series])

        self.assertTrue(len(jason.series[:5]) == 5)
        self.assertTrue(len(jason.series) == len([x for x in jason.series if x.id > 3]))

    def test_bad_creator(self):
        with self.assertRaises(exceptions.ApiError):
            self.m.creator(-1)

    def test_pulls_verbose(self):
        creators = self.m.creators_list({
            'orderBy': 'modified',
        })

        self.assertGreater(len(creators.creator), 0)

if __name__ == '__main__':
    unittest.main()
