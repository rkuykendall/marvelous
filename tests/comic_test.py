import os
import unittest

import marvelous


class TestComics(unittest.TestCase):
    def setUp(self):
        pub = os.getenv("PUBLIC_KEY", "pub")
        priv = os.getenv("PRIVATE_KEY", "priv")
        self.m = marvelous.api(
            public_key=pub,
            private_key=priv,
            cache=marvelous.SqliteCache("tests/testing_mock.sqlite"),
        )

    def test_pulls_verbose(self):
        week = self.m.comics(
            {
                "format": "comic",
                "formatType": "comic",
                "noVariants": True,
                "dateDescriptor": "thisWeek",
            }
        )
        c_iter = iter(week)
        self.assertEqual(next(c_iter).id, 61656)
        self.assertEqual(next(c_iter).id, 63866)
        self.assertEqual(next(c_iter).id, 60956)
        self.assertTrue(len(week) > 0)

    def test_pulls_simple(self):
        week = self.m.comics({"dateDescriptor": "thisWeek"})
        self.assertTrue(len(week.comics) > 0)

    def test_pulls_simpler(self):
        week = self.m.comics()
        self.assertTrue(len(week.comics) > 0)

    def test_known_comic(self):
        af15 = self.m.comics({"digitalId": 4746}).comics[0]
        self.assertTrue(af15.title == "Amazing Fantasy (1962) #15")
        self.assertTrue(af15.issue_number == 15)
        self.assertTrue(af15.description is None)
        self.assertTrue(af15.format == "Comic")
        self.assertTrue(af15.page_count == 36)
        self.assertTrue(af15.id == 16926)
        self.assertTrue("Spider-Man" in [c.name for c in af15.characters])
        self.assertFalse("Foo" in [c.name for c in af15.characters])
        self.assertTrue("Steve Ditko" in [s.name for s in af15.creators])
        self.assertFalse("Abe Lincoln" in [s.name for s in af15.creators])
        self.assertEqual(af15.prices.print, 0.1)

    def test_invalid_isbn(self):
        """Sometimes Marvel API sends number for isbn"""
        murpg = self.m.comics({"id": 1143}).comics[0]
        self.assertEqual(murpg.isbn, "785110283")
        self.assertEqual(murpg.prices.print, 9.99)

    def test_invalid_diamond_code(self):
        """Sometimes Marvel API sends number for diamond code"""
        hulk = self.m.comics({"id": 27399}).comics[0]
        self.assertEqual(hulk.diamond_code, "0")


if __name__ == "__main__":
    unittest.main()
