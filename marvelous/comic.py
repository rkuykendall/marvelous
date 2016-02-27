from marshmallow import Schema, fields, post_load
from dates import DatesSchema
from series import SeriesSchema


class Comic():
    def __init__(self, title, dates, series):
        self.title = title
        self.dates = dates
        self.series = series


class ComicSchema(Schema):
    title = fields.Str()
    dates = fields.Nested(DatesSchema)
    series = fields.Nested(SeriesSchema)

    @post_load
    def make(self, data):
        return Comic(**data)
