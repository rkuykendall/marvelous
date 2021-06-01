import datetime
import hashlib
import urllib.parse
from collections import OrderedDict

import requests
from marshmallow import ValidationError

from . import (
    character,
    characters_list,
    comics_list,
    creator,
    creators_list,
    exceptions,
    series,
    series_list,
)


class Session:
    api_url = "http://gateway.marvel.com:80/v1/public/{}"

    def __init__(self, public_key, private_key, cache=None):

        self.public_key = public_key
        self.private_key = private_key
        self.cache = cache

    def call(self, endpoint, params=None):
        if params is None:
            params = {}

        # Generate part of cache key before hash, apikey and timestamp added
        cache_params = ""
        if len(params) > 0:
            orderedParams = OrderedDict(sorted(params.items(), key=lambda t: t[0]))
            cache_params = "?{}".format(urllib.parse.urlencode(orderedParams))

        now_string = datetime.datetime.now().strftime("%Y-%m-%d%H:%M:%S")
        auth_hash = hashlib.md5()
        auth_hash.update(now_string.encode("utf-8"))
        auth_hash.update(self.private_key.encode("utf-8"))
        auth_hash.update(self.public_key.encode("utf-8"))

        params["hash"] = auth_hash.hexdigest()
        params["apikey"] = self.public_key
        params["ts"] = now_string

        url = self.api_url.format("/".join(str(e) for e in endpoint))
        cache_key = "{url}{cache_params}".format(url=url, cache_params=cache_params)

        if self.cache:
            try:
                cached_response = self.cache.get(cache_key)

                if cached_response is not None:
                    return cached_response
            except AttributeError as e:
                raise exceptions.CacheError(
                    "Cache object passed in is missing attribute: {}".format(repr(e))
                )

        response = requests.get(url, params=params)

        data = response.json()

        if "message" in data:
            raise exceptions.ApiError(data["message"])

        if self.cache and response.status_code == 200:
            try:
                self.cache.store(cache_key, data)
            except AttributeError as e:
                raise exceptions.CacheError(
                    "Cache object passed in is missing attribute: {}".format(repr(e))
                )

        return data

    def comics(self, params=None):
        if params is None:
            params = {}

        return comics_list.ComicsList(self.call(["comics"], params=params))

    def series(self, _id=None, params=None):
        result = None
        if _id:
            try:
                result = series.SeriesSchema().load(self.call(["series", _id]))
                result.session = self
            except ValidationError as error:
                raise exceptions.ApiError(error)
        elif params:
            try:
                api_call = self.call(["series"], params)

                if api_call.get("code", 200) != 200:
                    raise exceptions.ApiError(api_call.get("status"))

                result = series.SeriesSchema().load(
                    api_call.get("data", {}).get("results"), many=True
                )
                for r in result:
                    r.session = self
            except ValidationError as error:
                raise exceptions.ApiError(error)

        return result

    def series_list(self, params=None):
        if params is None:
            params = {}

        return series_list.SeriesList(self.call(["series"], params=params))

    def creator(self, _id):
        try:
            result = creator.CreatorsSchema().load(self.call(["creators", _id]))
        except ValidationError as error:
            raise exceptions.ApiError(error)

        result.session = self
        return result

    def creators_list(self, params=None):
        if params is None:
            params = {}

        return creators_list.CreatorsList(self.call(["creators"], params=params))

    def character(self, _id):
        try:
            result = character.CharactersSchema().load(self.call(["characters", _id]))
        except ValidationError as error:
            raise exceptions.ApiError(error)

        result.session = self
        return result

    def characters_list(self, params=None):
        if params is None:
            params = {}

        return characters_list.CharactersList(self.call(["characters"], params=params))
