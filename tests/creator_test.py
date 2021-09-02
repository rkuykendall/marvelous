"""
Test Creator module.
This module contains tests for Creator objects.
"""

import pytest

from marvelous import exceptions


def test_known_creator(talker):
    jason = talker.creator(11463)
    assert jason.first_name == "Jason"
    assert jason.last_name == "Aaron"
    assert jason.id == 11463
    assert (
        jason.thumbnail
        == "http://i.annihil.us/u/prod/marvel/i/mg/7/10/5cd9c7870670e.jpg"
    )
    assert 16450 in [s.id for s in jason.series]
    assert len(jason.series[:5]) == 5
    assert len(jason.series) == len([x for x in jason.series if x.id > 3])


def test_bad_creator(talker):
    with pytest.raises(exceptions.ApiError):
        talker.creator(-1)


def test_pulls_verbose(talker):
    creators = talker.creators_list(
        {
            "orderBy": "modified",
        }
    )
    c_iter = iter(creators)
    assert next(c_iter).full_name == "Sean Cooke"
    assert next(c_iter).full_name, "Mark Shultz"
    assert next(c_iter).full_name, "Miles Lane"
    assert len(creators) > 0
