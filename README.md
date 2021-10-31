# Phylm

[![Actions Status](https://github.com/dbatten5/phylm/workflows/Tests/badge.svg)](https://github.com/dbatten5/phylm/actions)
[![Actions Status](https://github.com/dbatten5/phylm/workflows/Release/badge.svg)](https://github.com/dbatten5/phylm/actions)
[![codecov](https://codecov.io/gh/dbatten5/phylm/branch/master/graph/badge.svg?token=P233M48EA6)](https://codecov.io/gh/dbatten5/phylm)
[![PyPI version](https://badge.fury.io/py/phylm.svg)](https://badge.fury.io/py/phylm)

Film data aggregation.

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
>>> from phylm import Phylm
>>> p = Phylm("The Matrix")
>>> p.load_source("imdb")
>>> p.imdb.year
1999
>>> p.imdb.rating
8.7
```

`phylm` also provides some tools around movie search results:

```python
>>> from phylm.tools import search_movies
>>> search_movies("the matrix")
[{
  'title': 'The Matrix',
  'kind': 'movie',
  'year': 1999,
  'cover url': 'https://some-url.com',
  'imdb_id': '0133093',
}, {
  'title': 'The Matrix Reloaded',
  'kind': 'movie',
  'year': 2003,
  'cover url': 'https://some-url.com',
  'imdb_id': '0234215',
}, {
...
```

## Help

See the [documentation](https://dbatten5.github.io/phylm) for more details.

## Licence

MIT
