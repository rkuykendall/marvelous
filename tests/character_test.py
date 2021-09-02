"""
Test Characters module.
This module contains tests for Character objects.
"""
import pytest

from marvelous import exceptions


def test_known_character(talker):
    cap = talker.character(1009220)
    assert cap.name == "Captain America"
    assert cap.resource_uri == "http://gateway.marvel.com/v1/public/characters/1009220"
    assert (
        cap.thumbnail == "http://i.annihil.us/u/prod/marvel/i/mg/3/50/537ba56d31087.jpg"
    )
    assert len(cap.series) > 0
    assert len(cap.events) > 0


def test_bad_character(talker):
    with pytest.raises(exceptions.ApiError):
        talker.character(-1)


def test_pulls_verbose(talker):
    characters = talker.characters_list(
        {
            "orderBy": "modified",
        }
    )

    c_iter = iter(characters)
    assert (next(c_iter).name) == "Askew-Tronics"
    assert (next(c_iter).name) == "Cargill"
    assert (next(c_iter).name) == "Firebrand"
    assert len(characters) > 0
