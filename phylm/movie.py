from phylm.sources.mtc import Mtc
from phylm.sources.rt import Rt
from phylm.sources.imdb import Imdb

class Movie:
    def __init__(self, title, year):
        self.title = title
        self.year = year
        self._mtc = self._get_mtc()
        self._rt = self._get_rt()
        self._imdb = self._get_imdb()

    def _get_mtc(self):
        return Mtc(self.title)

    def _get_rt(self):
        return Rt(self.title)

    def _get_imdb(self):
        return Imdb(self.title)

    def genres(self):
        return self._imdb.genres()

    def runtime(self):
        return self._imdb.runtime()

    def cast(self, limit=5):
        return self._imdb.cast(limit)

    def directors(self):
        return self._imdb.directors()

    def plot(self):
        return self._imdb.plot()

    def imdb_title(self):
        return self._imdb.title()

    def imdb_year(self):
        return self._imdb.year()

    def imdb_score(self):
        return self._imdb.score()

    def imdb_low_confidence(self):
        return self._imdb.low_confidence

    def metacritic_title(self):
        return self._mtc.title()

    def metacritic_year(self):
        return self._mtc.year()

    def metacritic_score(self):
        return self._mtc.score()

    def metacritic_low_confidence(self):
        return self._mtc.low_confidence

    def rt_title(self):
        return self._rt.title()

    def rt_year(self):
        return self._rt.year()

    def rt_tomato_score(self):
        return self._rt.tomato_score()

    def rt_audience_score(self):
        return self._rt.audience_score()

    def rt_low_confidence(self):
        return self._rt.low_confidence
