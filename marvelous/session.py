import datetime
import hashlib
import requests

from . import exceptions, comics_list, series


class Session():
    api_url = "http://gateway.marvel.com:80/v1/public/{}"

    def __init__(
            self, public_key, private_key, cache=None,
            print_calls=False):

        self.public_key = public_key
        self.private_key = private_key
        self.print_calls = print_calls
        self.cache = cache

    def call(self, endpoint, params=None):
        if params is None:
            params = {}

        now_string = datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S')
        auth_hash = hashlib.md5()
        auth_hash.update(now_string.encode('utf-8'))
        auth_hash.update(self.private_key.encode('utf-8'))
        auth_hash.update(self.public_key.encode('utf-8'))

        params['hash'] = auth_hash.hexdigest()
        params['apikey'] = self.public_key
        params['ts'] = now_string

        url = self.api_url.format('/'.join([str(e) for e in endpoint]))

        if self.cache:
            try:
                cached_response = self.cache.get(url)

                if cached_response:
                    return cached_response
            except AttributeError as e:
                raise exceptions.CacheError(
                    "Cache object passed in is missing attribute: {}".format(
                        repr(e)))

        response = requests.get(url, params=params)

        if self.print_calls:
            print(response.url)

        data = response.json()

        if 'message' in data:
            raise exceptions.ApiError(response['message'])

        if self.cache and response.status_code == 200:
            try:
                self.cache.store(url, data)
            except AttributeError as e:
                raise exceptions.CacheError(
                    "Cache object passed in is missing attribute: {}".format(
                        repr(e)))

        return data

    def comics(self, params=None):
        if params is None:
            params = {}

        return comics_list.ComicsList(
            self.call(['comics'], params=params))

    def series(self, _id):
        result = series.SeriesSchema().load(self.call(['series', _id]))

        if len(result.errors) > 0:
            raise exceptions.ApiError(result.errors)

        result.data.session = self
        return result.data
