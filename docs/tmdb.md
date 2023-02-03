# Usage

To access TMDB data points, first ensure you have loaded the TMDB source
through:

```python
await phylm.load_source("tmdb")
```

Alternatively you can instantiate the TMDB source class directly through:

```python
from phylm.sources import Tmdb

tmdb = Tmdb(raw_title="The Matrix", raw_year=1999)  # raw_year is optional
await tmdb.load_source()
```

## Movie ID

If you know the TMDB movie ID you can instantiate the `Phylm` class with a `tmdb_id`
property:

```python
from phylm.sources import Tmdb

tmdb = Tmdb(raw_title="The Matrix", tmdb_id="609")
```

Then, when running `load_source` for `tmdb`, `phylm` will first perform a search based
on the ID. If the ID is valid the result will be selected, if not then it will fall back
to a title search.

Alternatively, you can pass it to `load_source` with `"tmdb"` as the first argument:

```python
await phylm.load_source("tmdb", tmdb_id="609")
```

Or instantiate the TMDB source class with the ID:

```python
from phylm.sources import Tmdb

tmdb = Tmdb(movie_id="0133093")
```

!!! warning ""
    If instantiating the class directly you must supply at least one of `movie_id`
    or `raw_title`, otherwise a `ValueError` will be raised.

Note that TMDB doesn't provide any fuzzy search for title, only exact matches are
returned.

# Reference

::: phylm.sources.tmdb.Tmdb
    rendering:
      show_signature_annotations: true
      heading_level: 2
      show_root_heading: false
      show_root_toc_entry: false
