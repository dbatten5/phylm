# Phylm

[![Actions Status](https://github.com/dbatten5/phylm/workflows/Tests/badge.svg)](https://github.com/dbatten5/phylm/actions)
[![Actions Status](https://github.com/dbatten5/phylm/workflows/Release/badge.svg)](https://github.com/dbatten5/phylm/actions)
[![codecov](https://codecov.io/gh/dbatten5/phylm/branch/master/graph/badge.svg?token=P233M48EA6)](https://codecov.io/gh/dbatten5/phylm)
[![PyPI version](https://badge.fury.io/py/phylm.svg)](https://badge.fury.io/py/phylm)

Film data aggregation with async support.

## Motivation

When deciding which film to watch next, it can be helpful to have some key datapoints at
your fingertips, for example, the genre, the cast, the Metacritic score and, perhaps
most importantly, the runtime. This package provides a Phylm class to gather information
from various sources for a given film.

## Installation

```bash
pip install phylm
```

## Usage

```python
>>> import asyncio
>>> from phylm import Phylm
>>> p = Phylm("The Matrix")
>>> asyncio.run(p.load_source("imdb"))
>>> p.imdb.year
1999
>>> p.imdb.rating
8.7
```

`phylm` also provides some tools around movie search results and more:

```python
>>> from phylm.tools import search_movies, get_streaming_providers
>>> search_movies("the matrix")
[{
  'title': 'The Matrix',
  'kind': 'movie',
  'year': 1999,
  'cover_photo': 'https://some-url.com',
  'imdb_id': '0133093',
}, {
  'title': 'The Matrix Reloaded',
  'kind': 'movie',
  'year': 2003,
  'cover_photo': 'https://some-url.com',
  'imdb_id': '0234215',
}, {
...
>>> get_streaming_providers("0234215", regions=["gb"])
{
  'gb': {
    'rent': [{
      'display_priority': 8,
      'logo_path': '/pZgeSWpfvD59x6sY6stT5c6uc2h.jpg',
      'provider_id': 130,
      'provider_name': 'Sky Store',
    }],
    'flatrate': [{
      'display_priority': 8,
      'logo_path': '/ik9djlxNlex6sY6Kjsundc2h.jpg',
      'provider_id': 87,
      'provider_name': 'Netflix',
    }]
  }, {
  ...
}
```

## Help

See the [documentation](https://dbatten5.github.io/phylm) for more details.

## Licence

MIT
