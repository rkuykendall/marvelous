from marshmallow import Schema, fields, pre_load, post_load

from . import dates, series


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
    # resourceURI
    # urls
    series = fields.Nested(series.SeriesSchema)
    # variants
    # collections
    # collectedIssues
    dates = fields.Nested(dates.DatesSchema)
    # prices
    # thumbnail
    # images
    # creators
    # characters
    # stories
    # events

    @pre_load
    def process_input(self, data):
        new_data = data

        # Marvel comic 1768, and maybe others, returns a modified of
        # "-0001-11-30T00:00:00-0500". The best way to handle this is
        # probably just to ignore it, since I don't know how to fix it.
        if new_data['modified'][0] == '-':
            del new_data['modified']

        return new_data

    @post_load
    def make(self, data):
        return Comic(**data)
