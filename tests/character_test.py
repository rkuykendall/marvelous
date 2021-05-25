import os
import unittest

from marvelous import SqliteCache, api, exceptions


class TestCharacters(unittest.TestCase):
    def setUp(self):
        pub = os.getenv("PUBLIC_KEY", "pub")
        priv = os.getenv("PRIVATE_KEY", "priv")
        self.m = api(
            public_key=pub,
            private_key=priv,
            cache=SqliteCache("tests/testing_mock.sqlite"),
        )

    def test_known_character(self):
        cap = self.m.character(1009220)
        self.assertTrue(cap.name == "Captain America")
        self.assertTrue(
            cap.resource_uri == "http://gateway.marvel.com/v1/public/characters/1009220"
        )
        self.assertTrue(
            cap.thumbnail
            == "http://i.annihil.us/u/prod/marvel/i/mg/3/50/537ba56d31087.jpg"
        )
        self.assertGreater(len(cap.series), 0)
        self.assertGreater(len(cap.events), 0)

    def test_bad_character(self):
        with self.assertRaises(exceptions.ApiError):
            self.m.character(-1)

    def test_pulls_verbose(self):
        characters = self.m.characters_list(
            {
                "orderBy": "modified",
            }
        )

        self.assertGreater(len(characters.character), 0)
