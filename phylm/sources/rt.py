import json
from phylm.utils.web import soupify, url_encode

class Rt:
    def __init__(self, raw_title):
        self.raw_title = raw_title
        self.rt_title = None
        self.low_confidence = False
        self._rt_data = self._get_rt_data()

    def _get_rt_data(self):
        url_encoded_film = url_encode(self.raw_title)
        search_url = f"https://www.rottentomatoes.com/search?search={url_encoded_film}"
        soup = soupify(search_url)
        raw = soup.find(id='movies-json')
        items = json.loads(raw.string)['items']
        target = None
        for item in items:
            if item['name'].lower() == self.raw_title.lower() and item['tomatometerScore']:
                target = item
                break
        if not target:
            for item in items:
                if item['tomatometerScore'] or item['name'].lower() == self.raw_title.lower():
                    target = item
                    self.low_confidence = True
                    break
        return target

    def title(self):
        return self._rt_data['name']

    def year(self):
        return self._rt_data['releaseYear']

    def tomato_score(self):
        return self._rt_data['tomatometerScore'].get('score', 'N/A')

    def audience_score(self):
        return self._rt_data['audienceScore'].get('score', 'N/A')
