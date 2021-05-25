from marshmallow import INCLUDE, Schema, fields, post_load, pre_load

from . import events, exceptions, series, urls


class Character:
    def __init__(self, **kwargs):
        if "response" not in kwargs:
            kwargs["response"] = None

        for k, v in kwargs.items():
            setattr(self, k, v)


class CharactersSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    modified = fields.DateTime()
    resourceURI = fields.Str(attribute="resource_uri")
    urls = fields.Nested(urls.UrlsSchema)
    thumbnail = fields.Url()
    # comics
    # stories
    events = fields.Nested(events.EventsSchema, many=True)
    series = fields.Nested(series.SeriesSchema, many=True)

    class Meta:
        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        if data.get("code", 200) != 200:
            raise exceptions.ApiError(data.get("status"))

        if "status" in data:
            data["data"]["results"][0]["response"] = data
            data = data["data"]["results"][0]

        if "thumbnail" in data:
            data[
                "thumbnail"
            ] = f"{data['thumbnail']['path']}.{data['thumbnail']['extension']}"

        if "events" in data:
            data["events"] = data["events"]["items"]

        if "series" in data:
            data["series"] = data["series"]["items"]

        data["id"] = data["resourceURI"].split("/")[-1]
        return data

    @post_load
    def make(self, data, **kwargs):
        return Character(**data)
