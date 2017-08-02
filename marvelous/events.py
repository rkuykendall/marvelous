from marshmallow import Schema, fields, pre_load, post_load


class Events():
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name


class EventsSchema(Schema):
    id = fields.Str()
    name = fields.Str()

    @pre_load
    def process_input(self, data):
        data['id'] = data['resourceURI'].split('/')[-1]
        return data

    @post_load
    def make(self, data):
        return Events(**data)
