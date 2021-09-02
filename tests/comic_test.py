"""
Test Comic module.
This module contains tests for Comic objects.
"""


def test_pulls_verbose(talker):
    week = talker.comics(
        {
            "format": "comic",
            "formatType": "comic",
            "noVariants": True,
            "dateDescriptor": "thisWeek",
        }
    )
    c_iter = iter(week)
    assert next(c_iter).id == 61656
    assert next(c_iter).id == 63866
    assert next(c_iter).id == 60956
    assert len(week) > 0


def test_pulls_simple(talker):
    week = talker.comics({"dateDescriptor": "thisWeek"})
    assert len(week.comics) > 0


def test_pulls_simpler(talker):
    week = talker.comics()
    assert len(week.comics) > 0


def test_known_comic(talker):
    af15 = talker.comics({"digitalId": 4746}).comics[0]
    assert af15.title == "Amazing Fantasy (1962) #15"
    assert af15.issue_number == 15
    assert af15.description is None
    assert af15.format == "Comic"
    assert af15.page_count == 36
    assert af15.id == 16926
    assert "Spider-Man" in [c.name for c in af15.characters]
    assert "Foo" not in [c.name for c in af15.characters]
    assert "Steve Ditko" in [s.name for s in af15.creators]
    assert "Abe Lincoln" not in [s.name for s in af15.creators]
    assert af15.prices.print == 0.1


def test_invalid_isbn(talker):
    """Sometimes Marvel API sends number for isbn"""
    murpg = talker.comics({"id": 1143}).comics[0]
    assert murpg.isbn == "785110283"
    assert murpg.prices.print == 9.99


def test_invalid_diamond_code(talker):
    """Sometimes Marvel API sends number for diamond code"""
    hulk = talker.comics({"id": 27399}).comics[0]
    assert hulk.diamond_code == "0"


def test_upc_code(talker):
    cable = talker.comics({"id": 95781}).comics[0]
    assert cable.upc == "759606201991000111"
