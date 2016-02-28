from marshmallow import Schema, fields, pre_load, post_load

import comics_list


class Series():
    def __init__(self, _id, resource_uri, response=None):
        self.response = response
        self.id = _id
        self.resource_uri = resource_uri

    def comics(self, params):
        return comics_list.ComicsList(
            self.session.call(['series', self.id, 'comics'], params=params))


class SeriesSchema(Schema):
    response = fields.Raw()
    _id = fields.Int()
    resourceURI = fields.Str(attribute='resource_uri')

    @pre_load
    def process_input(self, data):
        # print data.keys()

        if 'status' in data:
            data['data']['results'][0]['response'] = data
            data = data['data']['results'][0]

        data['_id'] = data['resourceURI'].split('/')[-1]
        return data

    @post_load
    def make(self, data):
        # print data.keys()
        return Series(**data)
