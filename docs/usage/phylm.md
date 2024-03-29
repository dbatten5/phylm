# Phylm

This is the main entrypoint class.

First instantiate the class with a `title` property:

```python
from phylm import Phylm

p = Phylm(title="The Matrix")
```

You can also provide a `year` property for improved matching:

```python
from phylm import Phylm

p = Phylm(title="The Matrix", year=1999)
```

Next, asynchronously load a source through either `load_sources` or
`load_source`:

```python
await p.load_sources(["imdb", "rt"])
await p.load_source("mtc")
```

The available sources are:

```python
"imdb" # IMDb
"rt" # Rotten Tomatoes
"mtc" # Metacritic
"tmdb" # TMDB
```

Now the source will be available through a property of the same name and datapoints on
that source can be accessed:

```python
>>> p.imdb
<phylm.sources.imdb.Imdb object at 0x108a94810>
>>> p.imdb.rating
8.8
```

### Low Confidence

`phylm` will try to match the given title with the results through an exact
match on the title. If `phylm` can't find an exact match then it will select the
first result and set a `low_confidence` flag to `True`. This and the `year`
method on a source can be helpful for validating that the result is the desired
one:

```python
from phylm import Phylm
p = Phylm("Ambiguous Movie")  # suppose this movie was released in 1999
await p.load_source("imdb")
if p.imdb.low_confidence and p.imdb.year != 1999:
    # it's unlikely we're dealing with the right "Ambiguous Movie"
```

See the docs for a source for a full list of the available data points.

## Reference

```{eval-rst}
.. autoclass:: phylm.Phylm
   :members:
```
