from . import session, exceptions

# namespace declarations, for downstream usability
from .comic import Comic
from .comics_list import ComicsList
from .dates import Dates
from .events import Events
from .series import Series
from .urls import Urls

# NOQA F401 Imported for export
from .sqlite_cache import SqliteCache


def api(public_key=None, private_key=None, cache=None):
    if public_key is None:
        raise exceptions.AuthenticationError("Missing public_key.")

    if private_key is None:
        raise exceptions.AuthenticationError("Missing private_key.")

    return session.Session(public_key, private_key, cache=cache)
