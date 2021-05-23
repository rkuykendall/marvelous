import itertools

from marshmallow import ValidationError

from . import exceptions, creator


class CreatorsList():
    def __init__(self, response):
        self.creator = []
        self.response = response

        schema = creator.CreatorsSchema()
        for series_dict in response['data']['results']:
            try:
                result = schema.load(series_dict)
            except ValidationError as error:
                raise exceptions.ApiError(error)

            self.creator.append(result)

    def __iter__(self):
        return iter(self.creator)

    def __len__(self):
        return len(self.creator)

    def __getitem__(self, index):
        try:
            return next(itertools.islice(self.creator, index, index + 1))
        except TypeError:
            return list(itertools.islice(
                self.creator, index.start, index.stop, index.step))
