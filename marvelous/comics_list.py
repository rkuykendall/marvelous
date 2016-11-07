import itertools

from . import comic, exceptions


class ComicsList():
    def __init__(self, response):
        self.comics = []
        self.response = response

        schema = comic.ComicSchema()
        for comic_dict in response['data']['results']:
            result = schema.load(comic_dict)
            if len(result.errors) > 0:
                raise exceptions.ApiError(result.errors)

            self.comics.append(result.data)

    def __iter__(self):
        return iter(self.comics)

    def __len__(self):
        return len(self.comics)

    def __getitem__(self, index):
        try:
            return next(itertools.islice(self.comics, index, index+1))
        except TypeError:
            return list(itertools.islice(
                self.comics, index.start, index.stop, index.step))
