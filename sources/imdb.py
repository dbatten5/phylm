import imdb

class Imdb:
    ia = imdb.IMDb()

    def __init__(self, raw_title):
        self.raw_title = raw_title
        self.low_confidence = False
        self._imdb_data = self._get_imdb_data()

    def _get_imdb_data(self):
        results = Imdb.ia.search_movie(self.raw_title)
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
        return self._imdb_data['title']

    def genres(self):
        return ', '.join(self._imdb_data['genres'])

    def cast(self, limit=5):
        cast_members = [person['name'] for person in self._imdb_data['cast'][:limit]]
        return ', '.join(cast_members)

    def runtime(self):
        return self._imdb_data['runtimes'][0]

    def year(self):
        return self._imdb_data['year']

    def directors(self):
        try:
            directors = [person['name'] for person in self._imdb_data['directors']]
        except Exception:
            return None
        return ', '.join(directors)

    def score(self):
        return self._imdb_data['rating']

    def plot(self):
        data = self._imdb_data
        if 'plot' not in data.current_info:
            Imdb.ia.update(data, info=['plot'])
        try:
            plot = data['plot'][0].split('::')[0]
        except Exception:
            plot = ''
        return plot
