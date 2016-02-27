from marshmallow import Schema, fields, pre_load, post_load


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
