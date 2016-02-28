from requests_cache import CachedSession

from session import Session
from exceptions import AuthenticationError


def api(public_key=None, private_key=None, cache=False):
    if public_key is None:
        raise AuthenticationError("Missing public_key.")

    if private_key is None:
        raise AuthenticationError("Missing private_key.")

    if cache:
        cache_defaults = {
            'backend': 'sqlite',
            'expire_after': 60*60*24,  # 24 hours
            'ignored_parameters': ['hash', 'ts', 'apikey']
        }

        # Override the name and kwargs of the cache by passing a dict into
        # the cache kwarg
        if isinstance(cache, dict):
            cache_defaults.update(cache)

        cache = CachedSession(
            cache_defaults.get('name', 'marvelous'), **cache_defaults)

    return Session(public_key, private_key, cached_requests=cache)
