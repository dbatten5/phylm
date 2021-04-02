"""Module to contain IMDb class definition"""

import imdb

class Imdb:
    """Class to abstract an IMDb movie object"""
    ia = imdb.IMDb()

    def __init__(self, raw_title):
        self.raw_title = raw_title
        self.low_confidence = False
        self._imdb_data = self._get_imdb_data()

    def _get_imdb_data(self):
        results = Imdb.ia.search_movie(self.raw_title)
        if not results:
            return None
        target = None
        for result in results:
            if result['title'].lower() == self.raw_title.lower():
                target = result
                break
        if not target:
            target = results[0]
            self.low_confidence = True
        Imdb.ia.update(target, info=['main'])
        return target

    def title(self):
        """Return the title"""
        if not self._imdb_data:
            return None
        return self._imdb_data['title']

    def genres(self, limit=3):
        """Return the genres"""
        if not self._imdb_data:
            return []
        return self._imdb_data['genres'][:limit]

    def cast(self, limit=5):
        """Return the cast"""
        if not self._imdb_data:
            return []
        try:
            return [person['name'] for person in self._imdb_data['cast'][:limit]]
        except KeyError:
            return []

    def runtime(self):
        """Return the runtime"""
        if not self._imdb_data:
            return None
        try:
            return self._imdb_data['runtimes'][0]
        except KeyError:
            return None

    def year(self):
        """Return the year"""
        if not self._imdb_data:
            return None
        try:
            return self._imdb_data['year']
        except KeyError:
            return None

    def directors(self, limit=3):
        """Return the directors"""
        if not self._imdb_data:
            return []
        try:
            return [person['name'] for person in self._imdb_data['directors'][:limit]]
        except KeyError:
            return []

    def score(self):
        """Return the score"""
        if not self._imdb_data:
            return None
        try:
            return self._imdb_data['rating']
        except KeyError:
            return None

    def plot(self):
        """Return the plot"""
        if not self._imdb_data:
            return None
        data = self._imdb_data
        if 'plot' not in data.current_info:
            Imdb.ia.update(data, info=['plot'])
        try:
            plot = data['plot'][0].split('::')[0]
        except KeyError:
            plot = ''
        return plot
