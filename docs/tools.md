`phylm` also offers some tools and utilities related to movies.

# Search movies

For a given movie title query you can return a list of search results from `IMDb`
through `get_suggestions`:

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

::: phylm.tools.search_movies
    rendering:
      show_signature_annotations: true
      heading_level: 2
