from marshmallow import Schema, fields, pre_load, post_load, INCLUDE

from . import dates, series, urls, events, creator


class Comic():
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class ComicSchema(Schema):
    id = fields.Int()
    digitalId = fields.Int(attribute='digital_id')
    title = fields.Str()
    issueNumber = fields.Int(attribute='issue_number')
    variantDescription = fields.Str(attribute='variant_description')
    description = fields.Str(allow_none=True)
    modified = fields.DateTime()
    isbn = fields.Str()
    up = fields.Str()
    diamondCode = fields.Str(attribute='diamond_code')
    ean = fields.Str()
    issn = fields.Str()
    format = fields.Str()
    pageCount = fields.Int(attribute='page_count')
    # textObjects
    resourceURI = fields.Url(attribute='resource_uri')
    urls = fields.Nested(urls.UrlsSchema)
    series = fields.Nested(series.SeriesSchema)
    # variants
    # collections
    # collectedIssues
    dates = fields.Nested(dates.DatesSchema)
    # prices
    # thumbnail
    images = fields.List(fields.Url)
    creators = fields.Nested(creator.CreatorsSchema, many=True)
    # characters
    # stories
    events = fields.Nested(events.EventsSchema, many=True)

    class Meta:
        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        new_data = data

        # Marvel comic 1768, and maybe others, returns a modified of
        # "-0001-11-30T00:00:00-0500". The best way to handle this is
        # probably just to ignore it, since I don't know how to fix it.
        if new_data.get('modified', ' ')[0] == '-':
            del new_data['modified']

        if 'events' in new_data:
            new_data['events'] = new_data['events']['items']

        if 'creators' in new_data:
            new_data['creators'] = new_data['creators']['items']

        if 'images' in new_data:
            new_data['images'] = [
                '{}.{}'.format(img['path'], img['extension'])
                for img in new_data['images']
            ]

        if 'isbn' in new_data:
            new_data['isbn'] = str(new_data['isbn'])

        if 'diamondCode' in new_data:
            new_data['diamondCode'] = str(new_data['diamondCode'])

        return new_data

    @post_load
    def make(self, data, **kwargs):
        return Comic(**data)
