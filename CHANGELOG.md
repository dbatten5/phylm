# Changelog

## 5.0.0

### Breaking Changes

- Support for `python` 3.6 dropped.
- `load_source` and `load_sources` methods on the `Phylm` class are now async.
  See the [migrating to async guide](./MIGRATING_TO_ASYNC.md) for help on using
  the new API.
- If using a source class directly, eg. through `Imdb(raw_title="The Matrix")`,
  you'll need to explicitly load the data through the `load_source` async method
  on the source class.

## 4.3.1

### New

- `tools.search_tmdb_movies` accepts an optional `region` parameter to refine
  search.
