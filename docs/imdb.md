# Usage

To access IMDb data points, first ensure you have loaded the IMDb source
through:

```python
phylm.load_source("imdb")
```

Alternatively you can instantiate the IMDb source class directly through:

```python
from phylm.sources import Imdb

imdb = Imdb(raw_title="The Matrix")
```

## Movie ID

If you know the IMDb movie ID you can instantiate the `Phylm` class with an `imdb_id`
property:

```python
from phylm.sources import Imdb

imdb = Imdb(raw_title="The Matrix", imdb_id="0133093")
```

Then, when running `load_source` for `imdb`, `phylm` will first perform a search based
on the ID. If the ID is valid the result will be selected, if not then it will fall back
to a title search.

Alternatively, you can pass it to `load_source` with `"imdb"` as the first argument:

```python
phylm.load_source("imdb", imdb_id="0133093")
```

Or instantiate the IMDb source class with the ID:

```python
from phylm.sources import Imdb

imdb = Imdb(movie_id="0133093")
```

!!! warning ""
    If instantiating the class directly you must supply at least one of `movie_id`
    or `raw_title`, otherwise a `ValueError` will be raised.

# Reference

::: phylm.sources.imdb.Imdb
    rendering:
      show_signature_annotations: true
      heading_level: 2
      show_root_heading: false
      show_root_toc_entry: false
