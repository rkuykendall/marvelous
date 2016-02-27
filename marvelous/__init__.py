import hashlib
import requests
import datetime
import itertools
from marshmallow import Schema, fields, post_load, pre_load


class ApiError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class AuthenticationError(ApiError):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class Series():
    def __init__(self, _id, resource_uri):
        self.id = _id
        self.resource_uri = resource_uri


class SeriesSchema(Schema):
    _id = fields.Int()
    resourceURI = fields.Str(attribute='resource_uri')

    @pre_load
    def process_input(self, data):
        data['_id'] = data['resourceURI'].split('/')[-1]
        return data

    @post_load
    def make(self, data):
        return Series(**data)


class Dates():
    def __init__(self, on_sale, foc):
        self.on_sale = on_sale
        self.foc = foc


class DatesSchema(Schema):
    onsaleDate = fields.Date(attribute='on_sale')
    focDate = fields.Date(attribute='foc')

    @pre_load
    def process_input(self, data):
        new_data = {}
        for d in data:
            new_data[d['type']] = d['date']

        return new_data

    @post_load
    def make(self, data):
        return Dates(**data)


class Comic():
    def __init__(self, title, dates, series):
        self.title = title
        self.dates = dates
        self.series = series


class ComicSchema(Schema):
    title = fields.Str()
    dates = fields.Nested(DatesSchema)
    series = fields.Nested(SeriesSchema)

    @post_load
    def make(self, data):
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
