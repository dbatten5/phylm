[![Actions Status](https://github.com/dbatten5/phylm/workflows/Tests/badge.svg)](https://github.com/dbatten5/phylm/actions)
[![Actions Status](https://github.com/dbatten5/phylm/workflows/Release/badge.svg)](https://github.com/dbatten5/phylm/actions)
[![codecov](https://codecov.io/gh/dbatten5/phylm/branch/master/graph/badge.svg?token=P233M48EA6)](https://codecov.io/gh/dbatten5/phylm)

When deciding which film to watch next, it can be helpful to have some key
datapoints at your fingertips, for example, the genre, the cast, the Metacritic
score and, perhaps most importantly, the runtime. This package provides a Phylm
class to gather information from various sources for a given film.

# Installing

```bash
pip install phylm
```

# Example

```python
>>> import asyncio
>>> from phylm import Phylm
>>> p = Phylm("The Matrix")
>>> asyncio.run(p.load_source("imdb"))
>>> p.imdb.rating
8.7
```

!!! warning ""
    This package uses web scraping for the Rotten Tomatoes and Metacritic
    results and is therefore at the mercy of changes made to those webpages.
