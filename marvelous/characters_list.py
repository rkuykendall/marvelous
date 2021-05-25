import itertools

from marshmallow import ValidationError

from . import character, exceptions


class CharactersList:
    def __init__(self, response):
        self.character = []
        self.response = response

        schema = character.CharactersSchema()
        for character_dict in response["data"]["results"]:
            try:
                result = schema.load(character_dict)
            except ValidationError as error:
                raise exceptions.ApiError(error)

            self.character.append(result)

    def __iter__(self):
        return iter(self.character)

    def __len__(self):
        return len(self.character)

    def __getitem__(self, index):
        try:
            return next(itertools.islice(self.character, index, index + 1))
        except TypeError:
            return list(
                itertools.islice(self.character, index.start, index.stop, index.step)
            )
