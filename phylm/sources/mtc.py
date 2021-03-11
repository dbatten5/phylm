import re
from phylm.utils.web import soupify, url_encode

class Mtc:
    def __init__(self, raw_title):
        self.raw_title = raw_title
        self.low_confidence = False
        self._mtc_data = self._get_mtc_data()

    def _get_mtc_data(self):
        url_encoded_film = url_encode(self.raw_title)
        search_url = f"https://www.metacritic.com/search/movie/{url_encoded_film}/results"
        soup = soupify(search_url)
        results = soup.find_all("li", {"class": "result"})
        target = None
        for result in results:
            result_title = result.find("a").string.strip()
            if result_title.lower() == self.raw_title.lower():
                target = result
                break
        if target is None:
            target = results[0]
            self.low_confidence = True
        return target

    def title(self):
        return self._mtc_data.find("a").string.strip()

    def year(self):
        year_meta = self._mtc_data.find("p").string
        return re.search('\d{4}', year_meta).group()

    def score(self):
        return self._mtc_data.find('span', {'class': 'metascore_w'}).text
