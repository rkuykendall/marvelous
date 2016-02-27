import itertools
from comic import ComicSchema
from exceptions import ApiError


class ComicsList():
    comics = []

    def __init__(self, response):
        for comic_dict in response['data']['results']:
            result = ComicSchema().load(comic_dict)
            if len(result.errors) > 0:
                raise ApiError(result.errors)

            self.comics.append(result.data)

    def __iter__(self):
        return iter(self.comics)

    def __getitem__(self, index):
        try:
            return next(itertools.islice(self.comics, index, index+1))
        except TypeError:
            return list(itertools.islice(
                self.comics, index.start, index.stop, index.step))
