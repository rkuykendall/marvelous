from marshmallow import INCLUDE, Schema, fields, post_load, pre_load


class Prices:
    def __init__(self, print=None, **kwargs):
        self.print = print
        self.unknown = kwargs


class PriceSchemas(Schema):
    printPrice = fields.Float(attribute="print")

    # Supposedly digital prices could also be listed, but I
    # couldn't find any refences so made a guess what I thought
    # it would be. I'll leave it here in case we need it in the
    # future.

    # digitalPrice = fields.Float(attribute="digital")

    class Meta:
        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        new_data = {}
        for idx, d in enumerate(data, 0):
            if d["type"][idx]:
                new_data[d["type"]] = d["price"]

        return new_data

    @post_load
    def make(self, data, **kwargs):
        return Prices(**data)
