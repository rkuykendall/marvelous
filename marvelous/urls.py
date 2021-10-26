from marshmallow import INCLUDE, Schema, fields, post_load, pre_load


class Urls:
    def __init__(
        self,
        digital_purchase_date=None,
        foc_date=None,
        onsale_date=None,
        unlimited_date=None,
        wiki=None,
        detail=None,
        **kwargs,
    ):
        self.digital_purchase_date = digital_purchase_date
        self.foc_date = foc_date
        self.onsale_date = onsale_date
        self.unlimited_date = unlimited_date
        self.wiki = wiki
        self.detail = detail
        self.unknown = kwargs


class UrlsSchema(Schema):
    digitalPurchaseDate = fields.Url(attribute="digital_purchase_date")
    focDate = fields.Url(attribute="foc_date")
    onsaleDate = fields.Url(attribute="onsale_date")
    unlimitedDate = fields.Url(attribute="unlimited_date")
    # Should these go into a separate class like CharacterUrls?
    # For now let's put them here, but it may be something to consider to split them.
    wiki = fields.Url()
    detail = fields.Url()

    class Meta:
        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        return {d["type"]: d["url"] for d in data}

    @post_load
    def make(self, data, **kwargs):
        return Urls(**data)
