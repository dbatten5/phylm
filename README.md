# PhYlm

Film data aggregration

## Motivation

When deciding which film to watch next, it can be helpful to have a spreadsheet of data
handy to aid your decision. For example, the genre, the cast, the Metacritic score and,
perhaps most importantly, the runtime. This package receives a csv of movie titles and
returns a spreadsheet of useful information.

## Usage

```python
>>> from phylm.movie import Movie
>>> m = Movie('The Matrix', 1999)
>>> m.imdb_score()
8.7
```

## Available Datapoints

### Methods

|name|description|
|---|---|
|`genres`|Return the genres|
|`runtime`|Return the runtime|
|`cast`|Return the cast|
|`directors`|Return the directors|
|`plot`|Return the plot|
|`imdb_title`|Return the title from IMDb|
|`imdb_year`|Return the release year from IMDb|
|`imdb_score`|Return the IMDb score|
|`imdb_low_confidence`|Return the IMDb low confidence flag|
|`metacritic_title`|Return the title from Metacritic|
|`metacritic_year`|Return the release year from Metacritic|
|`metacritic_score`|Return the Metacritic score|
|`metacritic_low_confidence`|Return the Metacritic low confidence flag|
|`rt_title`|Return the title from Rotten Tomatoes|
|`rt_year`|Return the release year from Rotten Tomatoes|
|`rt_tomato_score`|Return the Rotten Tomatoes Tomatometer score|
|`rt_audience_score`|Return the Rotten Tomatoes Audience score|

### Attributes

|name|description|
|---|---|
|`title`|Return the given title|
|`year`|Return the given year|

#### Low Confidence

If the package can't find an exact match by title in one of the sources (IMDb,
Metacritic, Rotten Tomatoes) then the first result from the search result will
be returned. In this case the `{source}_low_confidence` flag will be set to
`True`. Use the `{source}_title` and `{source}_year` values to cross reference
with the given title to decide whether this is a worthwhile result or not.

## Limitations

This package uses web scraping for the Rotten Tomatoes and Metacritic results
and is therefore at the mercy of changes made to those webpages. Take the
returned values with a healthy pinch of salt.
