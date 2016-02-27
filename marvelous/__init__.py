import hashlib
import requests
import datetime
import itertools
from marshmallow import Schema, fields, post_load


class ApiError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class AuthenticationError(ApiError):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class Comic():
    def __init__(self, title):
        self.title = title


class ComicSchema(Schema):
    title = fields.Str()

    @post_load
    def make_comic(self, data):
        return Comic(**data)


class ComicsList():
    comics = []

    def __init__(self, response):
        for comic_dict in response['data']['results']:
            result = ComicSchema().load(comic_dict)
            if len(result.errors) > 0:
                raise ApiError(result.errors)

            self.comics.append(result.data)

    def __iter__(self):
        return iter(self.comics)

    def __getitem__(self, index):
        try:
            return next(itertools.islice(self.comics, index, index+1))
        except TypeError:
            return list(itertools.islice(
                self.comics, index.start, index.stop, index.step))


class Session():
    api_url = "http://gateway.marvel.com:80/v1/public/{}"

    def __init__(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key

    def _call(self, endpoint, params):
        now_string = datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S')
        auth_hash = hashlib.md5()
        auth_hash.update(now_string)
        auth_hash.update(self.private_key)
        auth_hash.update(self.public_key)

        params['hash'] = auth_hash.hexdigest()
        params['apikey'] = self.public_key
        params['ts'] = now_string

        response = requests.get(
            self.api_url.format(endpoint),
            params=params).json()

        if 'message' in response:
            raise ApiError(response['message'])

        return response

    def comics(self, params):
        return ComicsList(self._call('comics', params))


def api(public_key=None, private_key=None):
    if public_key is None:
        raise AuthenticationError("Missing public_key.")

    if private_key is None:
        raise AuthenticationError("Missing private_key.")

    return Session(public_key, private_key)
