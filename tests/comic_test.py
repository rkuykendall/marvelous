import os
import unittest

import marvelous


class TestComics(unittest.TestCase):
    def setUp(self):
        pub = os.getenv('PUBLIC_KEY', 'pub')
        priv = os.getenv('PRIVATE_KEY', 'priv')
        self.m = marvelous.api(
            public_key=pub, private_key=priv,
            cache=marvelous.SqliteCache("tests/testing_mock.sqlite"))

    def test_pulls_verbose(self):
        week = self.m.comics({
            'format': "comic",
            'formatType': "comic",
            'noVariants': True,
            'dateDescriptor': "thisWeek"})

        self.assertTrue(len(week.comics) > 0)

    def test_pulls_simple(self):
        week = self.m.comics({'dateDescriptor': "thisWeek"})
        self.assertTrue(len(week.comics) > 0)

    def test_pulls_simpler(self):
        week = self.m.comics()
        self.assertTrue(len(week.comics) > 0)

    def test_known_comic(self):
        af15 = self.m.comics({'digitalId': 4746}).comics[0]
        self.assertTrue(af15.title == "Amazing Fantasy (1962) #15")
        self.assertTrue(af15.issue_number == 15)
        self.assertTrue(af15.description is None)
        self.assertTrue(af15.format == "Comic")
        self.assertTrue(af15.page_count == 36)
        self.assertTrue(af15.id == 16926)


if __name__ == '__main__':
    unittest.main()
