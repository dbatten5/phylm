# Tools

`phylm` also offers some tools and utilities related to movies.

## Search movies

For a given movie title query you can return a list of search results from _IMDb_
through `search_movies`:

```python
>>> from phylm.tools import search_movies
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
```

```{eval-rst}
.. autofunction:: phylm.tools.search_movies
```

## TMDB

`phylm` also provides tools to interact with [The Movie Database](https://www.themoviedb.org/) (_TMDb_).

```{note}
To use _TMDb_ tools you'll need to sign up for an API key, instructions [here](https://developers.themoviedb.org/3).
Once you have your key, export it as an env var called `TMDB_API_KEY` so that it's
available to use in these tools. You also have the option of passing in the key as
an argument to each function.
```

### Search movies

For a given movie title query you can return a list of search results from _TMDb_
through `search_tmdb_movies`. Note that this search performs a lot quicker than the
`imdb` `search_movies`.

```python
>>> from phylm.tools import search_tmdb_movies
>>> search_tmdb_movies("The Matrix", api_key="abc") # the api key can be provided as an env var instead
[{
  'adult': False,
  'backdrop_path': '/fNG7i7RqMErkcqhohV2a6cV1Ehy.jpg',
  'genre_ids': [28, 878],
  'id': 603,
  'original_language': 'en',
  'original_title': 'The Matrix',
  'overview': 'Set in the 22nd century, The Matrix tells the story of a computer hacker...'
  'popularity': 79.956,
  'poster_path': '/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg',
  'release_date': '1999-03-30',
  'title': 'The Matrix',
  'video': False,
  'vote_average': 8.2,
  'vote_count': 20216,
}, {
  ...
}
```

By default the `release_date` will be the US release date. You can specify a different
region by providing a region argument:

```python
>>> from phylm.tools import search_tmdb_movies
>>> search_tmdb_movies("The Matrix", region="gb")
[{
  'id': 603,
  ...
  'release_date': '1999-06-11',
  'title': 'The Matrix',
  ...
}, {
  ...
}
```

```{eval-rst}
.. autofunction:: phylm.tools.search_tmdb_movies
```

### Get streaming providers

For a given movie _TMDb_ id and list of regions, you can return a list of streaming
providers from _TMDb_ via _Just Watch_ through `get_streaming_providers`.

```python
>>> from phylm.tools import get_streaming_providers
>>> get_streaming_providers(tmdb_movie_id="438631", regions=["gb"], api_key="abc")
{
  'gb': {
    'link': 'https://www.themoviedb.org/movie/438631-dune/watch?locale=GB',
    'rent': [{
      'display_priority': 8,
      'logo_path': '/pZgeSWpfvD59x6sY6stT5c6uc2h.jpg',
      'provider_id': 130,
      'provider_name': 'Sky Store',
    }],
  },
}
```

Consult the [TMDb docs](https://developers.themoviedb.org/3/movies/get-movie-watch-providers)
for more information on the data that's returned.

```{eval-rst}
.. autofunction:: phylm.tools.get_streaming_providers
```
