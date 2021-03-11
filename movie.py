from sources.mtc import Mtc

class Movie:
    def __init__(self, title, year):
        self.title = title
        self.year = year
        self._mt_data = Mtc(title)
