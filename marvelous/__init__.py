from session import Session
from exceptions import AuthenticationError, LibraryError


def api(public_key=None, private_key=None, cache=False):
    if public_key is None:
        raise AuthenticationError("Missing public_key.")

    if private_key is None:
        raise AuthenticationError("Missing private_key.")

    if cache:
        try:
            from requests_cache import CachedSession

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
        except:
            raise LibraryError(
                "Marvelous only supports cache with requests-cache >= 0.4.11, "
                "not yet on pypi. To install development requests-cache, run "
                "`pip install git+git://github.com/reclosedev/"
                "requests-cache.git`.")


    return Session(public_key, private_key, cached_requests=cache)
