[![Actions Status](https://github.com/dbatten5/phylm/workflows/Tests/badge.svg)](https://github.com/dbatten5/phylm/actions)
[![Actions Status](https://github.com/dbatten5/phylm/workflows/Release/badge.svg)](https://github.com/dbatten5/phylm/actions)
[![codecov](https://codecov.io/gh/dbatten5/phylm/branch/main/graph/badge.svg?token=948J8ECAQT)](https://codecov.io/gh/dbatten5/phylm)

# Phylm

When deciding which film to watch next, it can be helpful to have some key
datapoints at your fingertips, for example, the genre, the cast, the Metacritic
score and, perhaps most importantly, the runtime. This package provides a Phylm
class to gather information from various sources for a given film.

# Installing

```bash
pip install phylm
```

# Usage

```python
>>> from phylm import Phylm
>>> p = Phylm("The Matrix")
>>> p.load_source("imdb")
>>> p.imdb.rating
8.7
```

The main entrypoint is the `Phylm` class. The class should be instantiated with
a `title` property. In order to access data from a source, you'll first need to
load the source. The available sources are:

```python
"imdb" # IMDb
"rt" # Rotten Tomatoes
"mtc" # Metacritic
```

The source data can then be accessed through the following properties on a `Phylm`
instance:

```python
phylm.imdb
phylm.rt
phylm.mtc
```

!!! warning ""
    This package uses web scraping for the Rotten Tomatoes and Metacritic
    results and is therefore at the mercy of changes made to those webpages.


## Low Confidence

`phylm` will try to match the given title with the results through an exact
match on the title. If `phylm` can't find an exact match then it will select the
first result and set a `low_confidence` flag to `True`. This and the `year`
method on a source can be helpful for validating that the result is the desired
one


```python
from phylm import Phylm
p = Phylm("Ambiguous Movie") # suppose this movie was released in 1999
p.load_source("imdb")
if p.imdb.low_confidence and p.imdb.year != 1999:
    # it's unlikely we're dealing with the right "Ambigous Movie"
```
