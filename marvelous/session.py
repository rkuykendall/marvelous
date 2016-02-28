import datetime
import hashlib
import requests

import exceptions
import comics_list
import series


class Session():
    api_url = "http://gateway.marvel.com:80/v1/public/{}"

    def __init__(
            self, public_key, private_key, cached_requests=None,
            print_calls=False):

        self.public_key = public_key
        self.private_key = private_key
        self.print_calls = print_calls

        if cached_requests:
            self.requests = cached_requests
        else:
            self.requests = requests

    def call(self, endpoint, params=None):
        if params is None:
            params = {}

        now_string = datetime.datetime.now().strftime('%Y-%m-%d%H:%M:%S')
        auth_hash = hashlib.md5()
        auth_hash.update(now_string)
        auth_hash.update(self.private_key)
        auth_hash.update(self.public_key)

        params['hash'] = auth_hash.hexdigest()
        params['apikey'] = self.public_key
        params['ts'] = now_string

        url = self.api_url.format('/'.join([str(e) for e in endpoint]))

        response = self.requests.get(url, params=params)

        if self.print_calls:
            print response.url

        response = response.json()

        if 'message' in response:
            raise exceptions.ApiError(response['message'])

        return response

    def comics(self, params):
        return comics_list.ComicsList(
            self.call(['comics'], params=params))

    def series(self, _id):
        result = series.SeriesSchema().load(self.call(['series', _id]))

        if len(result.errors) > 0:
            raise exceptions.ApiError(result.errors)

        result.data.session = self
        return result.data
