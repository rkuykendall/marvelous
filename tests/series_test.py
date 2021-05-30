import datetime
import os
import unittest

import marvelous
from marvelous.comics_list import ComicsList
from marvelous.series import Series


class TestSeries(unittest.TestCase):
    def setUp(self):
        pub = os.getenv("PUBLIC_KEY", "pub")
        priv = os.getenv("PRIVATE_KEY", "priv")
        self.m = marvelous.api(
            public_key=pub,
            private_key=priv,
            cache=marvelous.SqliteCache("tests/testing_mock.sqlite"),
        )

    def test_known_series(self):
        usms = self.m.series(466)
        self.assertTrue(usms.title == "Ultimate Spider-Man (2000 - 2009)")
        self.assertTrue(usms.id == 466)
        self.assertEqual(
            "http://i.annihil.us/u/prod/marvel/i/mg/6/c0/5149db8019dc9.jpg",
            usms.thumbnail,
        )
        self.assertEqual(2009, usms.endYear)
        self.assertEqual(2000, usms.startYear)
        self.assertEqual(
            datetime.datetime(
                2013,
                3,
                20,
                11,
                54,
                44,
                tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=72000)),
            ),
            usms.modified,
        )
        self.assertEqual(
            "In 2000, Marvel embarked on a bold new experiment, "
            "re-imagining some of their greatest heroes in the 21st century, "
            "beginning with Spider-Man! Writer Brian Michael Bendis along with "
            "artists Mark Bagley and Stuart Immonen invite you to discover the "
            "world of Peter Parker in a whole new way with the series that changed "
            "everything!",
            usms.description,
        )
        self.assertEqual("A", usms.rating)

        comics = usms.comics()
        self.assertTrue(23931 in [c.id for c in comics])

        self.assertTrue(len(comics[:5]) == 5)
        self.assertTrue(len(comics) == len([x for x in comics if x.id > 3]))

    def test_bad_series(self):
        with self.assertRaises(marvelous.exceptions.ApiError):
            self.m.series(-1)
        with self.assertRaises(marvelous.exceptions.ApiError):
            self.m.series(params={"bad": "filter"})

    def test_bad_response_data(self):
        with self.assertRaises(marvelous.exceptions.ApiError):
            ComicsList({"data": {"results": [{"modified": "potato"}]}})

    def test_all_series(self):
        # check known values
        series_single = self.m.series(
            params={"title": "Ultimate Spider-Man"}
        )  # don't include '(year - year)', it doesn't work
        series_list = list(series_single)  # unspool the iterator
        self.assertIsNotNone(series_single)
        self.assertEqual(1, len(series_list))
        self.assertIsInstance(series_list[0], Series)
        # check the filter works returning multiple items
        seriesType = "ongoing"
        startYear = 2009
        series_iter = self.m.series(
            params={"seriesType": seriesType, "startYear": startYear, "limit": 10}
        )
        for series in series_iter:
            self.assertIsInstance(series, Series)
            self.assertEqual(startYear, series.startYear)


if __name__ == "__main__":
    unittest.main()
