from marshmallow import INCLUDE, Schema, fields, post_load, pre_load


class Events:
    def __init__(self, id=None, name=None, **kwargs):
        self.id = id
        self.name = name
        self.unknown = kwargs


class EventsSchema(Schema):
    id = fields.Str()
    name = fields.Str()

    class Meta:
        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        data["id"] = data["resourceURI"].split("/")[-1]
        return data

    @post_load
    def make(self, data, **kwargs):
        return Events(**data)
