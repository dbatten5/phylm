"""Module to contain Rt class definition"""

import json
from phylm.utils.web import soupify, url_encode

class Rt:
    """Class to abstract a Rotten Tomatoes movie search result"""
    def __init__(self, raw_title):
        self.raw_title = raw_title
        self.low_confidence = False
        self._rt_data = self._get_rt_data()

    def _get_rt_data(self):
        url_encoded_film = url_encode(self.raw_title)
        search_url = f"https://www.rottentomatoes.com/search?search={url_encoded_film}"
        soup = soupify(search_url)
        raw = soup.find(id='movies-json')
        if not raw.string:
            return None
        items = json.loads(raw.string)['items']
        if not items:
            return None
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
        """Return the title"""
        if not self._rt_data:
            return None
        return self._rt_data['name']

    def year(self):
        """Return the year"""
        if not self._rt_data:
            return None
        return self._rt_data['releaseYear']

    def tomato_score(self):
        """Return the TomatoScore"""
        if not self._rt_data:
            return None
        return self._rt_data['tomatometerScore'].get('score', 'N/A')

    def audience_score(self):
        """Return the Audience Score"""
        if not self._rt_data:
            return None
        return self._rt_data['audienceScore'].get('score', 'N/A')
