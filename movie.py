from sources.mtc import Mtc
from sources.rt import Rt
from sources.imdb import Imdb

class Movie:
    def __init__(self, title, year):
        self.title = title
        self.year = year
        self._mt_data = Mtc(title)
        self._rt_data = Rt(title)
        self._imdb_data = Imdb(title)
