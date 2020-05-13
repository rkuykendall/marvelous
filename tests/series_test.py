import os
import unittest

import marvelous
from marvelous.comics_list import ComicsList


class TestSeries(unittest.TestCase):
    def setUp(self):
        pub = os.getenv('PUBLIC_KEY', 'pub')
        priv = os.getenv('PRIVATE_KEY', 'priv')
        self.m = marvelous.api(
            public_key=pub, private_key=priv,
            cache=marvelous.SqliteCache("tests/testing_mock.sqlite"))

    def test_known_series(self):
        usms = self.m.series(466)
        self.assertTrue(usms.title == "Ultimate Spider-Man (2000 - 2009)")
        self.assertTrue(usms.id == 466)
        comics = usms.comics()
        self.assertTrue(23931 in [c.id for c in comics])

        self.assertTrue(len(comics[:5]) == 5)
        self.assertTrue(len(comics) == len([x for x in comics if x.id > 3]))

    def test_bad_series(self):
        with self.assertRaises(marvelous.exceptions.ApiError):
            self.m.series(-1)

    def test_bad_response_data(self):
        with self.assertRaises(marvelous.exceptions.ApiError):
            ComicsList({'data': {'results': [{'modified': 'potato'}]}})

    def test_pulls_verbose(self):
        series = self.m.series_list({
            'orderBy': 'modified',
        })

        self.assertGreater(len(series.series), 0)

if __name__ == '__main__':
    unittest.main()
