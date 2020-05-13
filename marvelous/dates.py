from marshmallow import Schema, fields, pre_load, post_load, INCLUDE


class Dates():
    def __init__(self, on_sale=None, foc=None, unlimited=None, **kwargs):
        self.on_sale = on_sale
        self.foc = foc
        self.unlimited = unlimited
        self.unknown = kwargs


class DatesSchema(Schema):
    onsaleDate = fields.DateTime(attribute='on_sale')
    focDate = fields.DateTime(attribute='foc')
    unlimitedDate = fields.DateTime(attribute='unlimited')

    class Meta:
        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        new_data = {}
        for d in data:
            # Marvel comic 4373, and maybe others, returns a focDate of
            # "-0001-11-30T00:00:00-0500". The best way to handle this is
            # probably just to ignore it, since I don't know how to fix it.
            if d['date'][0] != '-':
                new_data[d['type']] = d['date']

        return new_data

    @post_load
    def make(self, data, **kwargs):
        return Dates(**data)
