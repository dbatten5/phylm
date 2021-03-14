"""Module to contain Phylm class definition"""

from phylm.sources.mtc import Mtc
from phylm.sources.rt import Rt
from phylm.sources.imdb import Imdb

class Phylm:
    """Class to represent a movie"""
    def __init__(self, title, year=None):
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
        """Return the genres"""
        return self._imdb.genres()

    def runtime(self):
        """Return the runtime"""
        return self._imdb.runtime()

    def cast(self, limit=5):
        """Return the cast"""
        return self._imdb.cast(limit)

    def directors(self):
        """Return the directors"""
        return self._imdb.directors()

    def plot(self):
        """Return the plot"""
        return self._imdb.plot()

    def imdb_title(self):
        """Return the title from IMDb"""
        return self._imdb.title()

    def imdb_year(self):
        """Return the release year from IMDb"""
        return self._imdb.year()

    def imdb_score(self):
        """Return the IMDb score"""
        return self._imdb.score()

    def imdb_low_confidence(self):
        """Return the IMDb low confidence flag"""
        return self._imdb.low_confidence

    def mtc_title(self):
        """Return the title from Metacritic"""
        return self._mtc.title()

    def mtc_year(self):
        """Return the release year from Metacritic"""
        return self._mtc.year()

    def mtc_score(self):
        """Return the Metacritic score"""
        return self._mtc.score()

    def mtc_low_confidence(self):
        """Return the Metacritic low confidence flag"""
        return self._mtc.low_confidence

    def rt_title(self):
        """Return the title from Rotten Tomatoes"""
        return self._rt.title()

    def rt_year(self):
        """Return the release year from Rotten Tomatoes"""
        return self._rt.year()

    def rt_tomato_score(self):
        """Return the Rotten Tomatoes Tomatometer score"""
        return self._rt.tomato_score()

    def rt_audience_score(self):
        """Return the Rotten Tomatoes Audience score"""
        return self._rt.audience_score()

    def rt_low_confidence(self):
        """Return the Rotten Tomatoes low confidence flag"""
        return self._rt.low_confidence
