from marshmallow import Schema, fields, pre_load, post_load, INCLUDE


class Urls():
    def __init__(
            self, digital_purchase_date=None, foc_date=None, onsale_date=None,
            unlimited_date=None, **kwargs):
        self.digital_purchase_date = digital_purchase_date
        self.foc_date = foc_date
        self.onsale_date = onsale_date
        self.unlimited_date = unlimited_date
        self.unknown = kwargs


class UrlsSchema(Schema):
    digitalPurchaseDate = fields.Url(attribute='digital_purchase_date')
    focDate = fields.Url(attribute='foc_date')
    onsaleDate = fields.Url(attribute='onsale_date')
    unlimitedDate = fields.Url(attribute='unlimited_date')

    class Meta:
        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        new_data = {}
        for d in data:
            new_data[d['type']] = d['url']

        return new_data

    @post_load
    def make(self, data, **kwargs):
        return Urls(**data)
