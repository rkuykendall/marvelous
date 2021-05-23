from marshmallow import Schema, fields, pre_load, post_load, INCLUDE

from . import exceptions, series, comic, events


class Creator:
    def __init__(self, **kwargs):
        if 'response' not in kwargs:
            kwargs['response'] = None

        for k, v in kwargs.items():
            setattr(self, k, v)
        
    # TODO: Retrieve comics list for creator


class CreatorsSchema(Schema):
    id = fields.Int()
    firstName = fields.Str(attribute="first_name")
    middleName = fields.Str(attribute="middle_name")
    lastName = fields.Str(attribute="last_name")
    suffix = fields.Str()
    fullName = fields.Str(attribute="full_name")
    modified = fields.DateTime()
    resourceURI = fields.Str(attribute='resource_uri')
    # urls
    thumbnail = fields.Url()
    series = fields.Nested(series.SeriesSchema, many=True)
    # stories
    events = fields.Nested(events.EventsSchema, many=True)

    class Meta:
        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        if data.get('code', 200) != 200:
            raise exceptions.ApiError(data.get('status'))

        if 'status' in data:
            data['data']['results'][0]['response'] = data
            data = data['data']['results'][0]

        if 'thumbnail' in data:
            data['thumbnail'] = f"{data['thumbnail']['path']}.{data['thumbnail']['extension']}"
            
        if 'events' in data:
            data['events'] = data['events']['items']

        if 'series' in data:
            data['series'] = data['series']['items']

        data['id'] = data['resourceURI'].split('/')[-1]
        return data

    @post_load
    def make(self, data, **kwargs):
        return Creator(**data)
