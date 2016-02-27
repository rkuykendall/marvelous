import hashlib
import requests
import datetime


class ApiError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class AuthenticationError(ApiError):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


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
        return self._call('comics', params)


def api(public_key=None, private_key=None):
    if public_key is None:
        raise AuthenticationError("Missing public_key.")

    if private_key is None:
        raise AuthenticationError("Missing private_key.")

    return Session(public_key, private_key)
