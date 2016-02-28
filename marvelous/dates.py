from marshmallow import Schema, fields, pre_load, post_load


class Dates():
    def __init__(self, on_sale=None, foc=None, unlimited=None):
        self.on_sale = on_sale
        self.foc = foc
        self.unlimited = unlimited


class DatesSchema(Schema):
    onsaleDate = fields.Date(attribute='on_sale')
    focDate = fields.Date(attribute='foc')
    unlimitedDate = fields.Date(attribute='unlimited')

    @pre_load
    def process_input(self, data):
        new_data = {}
        for d in data:
            # Marvel comic 4373, and maybe others, returns a focDate of
            # "-0001-11-30T00:00:00-0500". The best way to handle this is
            # probably just to ignore it, since I don't know how to fix it.
            if d['date'][0] != '-':
                new_data[d['type']] = d['date']

        return new_data

    @post_load
    def make(self, data):
        return Dates(**data)
