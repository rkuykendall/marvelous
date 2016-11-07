from marshmallow import Schema, fields, pre_load, post_load

from . import comics_list, exceptions


class Series:
    def __init__(self, **kwargs):
        if 'response' not in kwargs:
            kwargs['response'] = None

        for k, v in kwargs.items():
            setattr(self, k, v)

    def comics(self, params=None):
        if params is None:
            params = {}

        return comics_list.ComicsList(
            self.session.call(['series', self.id, 'comics'], params=params))


class SeriesSchema(Schema):
    response = fields.Raw()
    id = fields.Int()
    resourceURI = fields.Str(attribute='resource_uri')
    title = fields.Str()

    @pre_load
    def process_input(self, data):
        if data.get('code', 200) != 200:
            raise exceptions.ApiError(data.get('status'))

        if 'status' in data:
            data['data']['results'][0]['response'] = data
            data = data['data']['results'][0]

        data['id'] = data['resourceURI'].split('/')[-1]
        return data

    @post_load
    def make(self, data):
        return Series(**data)
