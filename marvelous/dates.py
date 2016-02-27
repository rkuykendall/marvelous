from marshmallow import Schema, fields, pre_load, post_load


class Dates():
    def __init__(self, on_sale, foc):
        self.on_sale = on_sale
        self.foc = foc


class DatesSchema(Schema):
    onsaleDate = fields.Date(attribute='on_sale')
    focDate = fields.Date(attribute='foc')

    @pre_load
    def process_input(self, data):
        new_data = {}
        for d in data:
            new_data[d['type']] = d['date']

        return new_data

    @post_load
    def make(self, data):
        return Dates(**data)
