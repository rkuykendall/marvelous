"""
Test Series module.
This module contains tests for Series objects.
"""
import datetime

import pytest

from marvelous import comics_list, exceptions
from marvelous.series import Series


def test_known_series(talker):
    usms = talker.series(466)
    assert usms.title == "Ultimate Spider-Man (2000 - 2009)"
    assert usms.id == 466
    assert (
        "http://i.annihil.us/u/prod/marvel/i/mg/6/c0/5149db8019dc9.jpg"
        == usms.thumbnail
    )
    assert 2009 == usms.endYear
    assert 2000 == usms.startYear
    assert (
        datetime.datetime(
            2013,
            3,
            20,
            11,
            54,
            44,
            tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=72000)),
        )
        == usms.modified
    )
    assert (
        "In 2000, Marvel embarked on a bold new experiment, re-imagining some "
        "of their greatest heroes in the 21st century, beginning with Spider-Man! "
        "Writer Brian Michael Bendis along with artists Mark Bagley and Stuart Immonen "
        "invite you to discover the world of Peter Parker in a whole new way with the "
        "series that changed everything!" == usms.description
    )
    assert "A" == usms.rating

    comics = usms.comics()
    assert 23931 in [c.id for c in comics]
    assert len(comics[:5]) == 5
    assert len(comics) == len([x for x in comics if x.id > 3])


def test_bad_series(talker):
    with pytest.raises(exceptions.ApiError):
        talker.series(-1)

    with pytest.raises(exceptions.ApiError):
        talker.series(params={"bad": "filter"})


def test_bad_response_data():
    with pytest.raises(exceptions.ApiError):
        comics_list.ComicsList({"data": {"results": [{"modified": "potato"}]}})


def test_all_series(talker):
    # check known values
    series_single = talker.series(
        params={"title": "Ultimate Spider-Man"}
    )  # don't include '(year - year)', it doesn't work
    series_list = list(series_single)  # unspool the iterator
    assert series_single is not None
    assert len(series_list) == 1
    assert isinstance(series_list[0], Series)
    # check the filter works returning multiple items
    seriesType = "ongoing"
    startYear = 2009
    series_iter = talker.series(
        params={"seriesType": seriesType, "startYear": startYear, "limit": 10}
    )
    for series in series_iter:
        assert isinstance(series, Series)
        assert startYear == series.startYear


def test_pulls_verbose(talker):
    series = talker.series_list()
    s_iter = iter(series)
    assert next(s_iter).id == 31445
    assert next(s_iter).id == 26024
    assert next(s_iter).id == 18454
    assert len(series) > 0
