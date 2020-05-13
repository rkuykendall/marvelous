from marshmallow import Schema, fields, pre_load, post_load, INCLUDE

from . import exceptions


class Series:
    def __init__(self, **kwargs):
        if 'response' not in kwargs:
            kwargs['response'] = None

        for k, v in kwargs.items():
            if k == "comics":
                continue
            setattr(self, k, v)

    def comics(self, params=None):
        from . import comics_list

        if params is None:
            params = {}

        return comics_list.ComicsList(
            self.session.call(['series', self.id, 'comics'], params=params))


class SeriesSchema(Schema):
    response = fields.Raw()
    id = fields.Int()
    resourceURI = fields.Str(attribute='resource_uri')
    title = fields.Str()

    class Meta:
        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        if data.get('code', 200) != 200:
            raise exceptions.ApiError(data.get('status'))

        if 'status' in data:
            data['data']['results'][0]['response'] = data
            data = data['data']['results'][0]

        data['id'] = data['resourceURI'].split('/')[-1]
        return data

    @post_load
    def make(self, data, **kwargs):
        return Series(**data)
