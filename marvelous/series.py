from marshmallow import INCLUDE, Schema, fields, post_load, pre_load

from . import exceptions


class Series:
    def __init__(self, **kwargs):
        if "response" not in kwargs:
            kwargs["response"] = None

        for k, v in kwargs.items():
            if k == "comics":
                continue
            setattr(self, k, v)

    def comics(self, params=None):
        from . import comics_list

        if params is None:
            params = {}

        return comics_list.ComicsList(
            self.session.call(["series", self.id, "comics"], params=params)
        )


class SeriesSchema(Schema):
    response = fields.Raw()
    id = fields.Int()
    resourceURI = fields.Str(attribute="resource_uri")
    title = fields.Str()
    modified = fields.DateTime()
    description = fields.Str(allow_none=True)
    thumbnail = fields.URL(allow_none=True)
    startYear = fields.Int(allow_none=True)
    endYear = fields.Int(allow_none=True)
    rating = fields.Str(allow_none=True)

    class Meta:
        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        if data.get("code", 200) != 200:
            raise exceptions.ApiError(data.get("status"))

        if "status" in data:
            data["data"]["results"][0]["response"] = data
            data = data["data"]["results"][0]

        # derive ID
        data["id"] = data["resourceURI"].split("/")[-1]
        # derive thumbnail
        thumb_dict = data.get("thumbnail", {})
        if thumb_dict:
            data["thumbnail"] = f"{thumb_dict['path']}.{thumb_dict['extension']}"
        else:
            data["thumbnail"] = None
        return data

    @post_load
    def make(self, data, **kwargs):
        return Series(**data)
