from unittest.mock import patch, MagicMock, call

from phylm.sources.imdb import Imdb

@patch('phylm.sources.imdb.Imdb.ia')
def test_exact_match(mock_ia):
    """
    Given a raw title,
    When there is an exact match from IMDb,
    Then the match is selected and low confidence remains False
    """
    raw_title = 'The Movie'
    mock_ia.search_movie.return_value = [{'title': 'A Movie'}, {'title': raw_title}]
    imdb = Imdb(raw_title)
    assert imdb.title() == raw_title
    assert imdb.low_confidence is False


@patch('phylm.sources.imdb.Imdb.ia')
def test_no_exact_match(mock_ia):
    """
    Given a raw title,
    When there is no exact match from IMDb,
    Then the first match is selected and low confidence is True
    """
    raw_title = 'The Movie'
    mock_ia.search_movie.return_value = [{'title': 'A Movie'}, {'title': 'Another Movie'}]
    imdb = Imdb(raw_title)
    assert imdb.title() == 'A Movie'
    assert imdb.low_confidence is True


@patch('phylm.sources.imdb.Imdb.ia')
def test_no_results(mock_ia):
    """
    Given a raw title,
    When there is no exact match from IMDb,
    Then the first match is selected and low confidence is True
    """
    raw_title = 'The Movie'
    mock_ia.search_movie.return_value = []
    imdb = Imdb(raw_title)
    assert imdb.title() is None


@patch('phylm.sources.imdb.Imdb.ia')
def test_genres(mock_ia):
    """
    Given a match with genres,
    When the genres are retrieved,
    Then the genres are returned with a given limit
    """
    raw_title = 'The Movie'
    mock_ia.search_movie.return_value = [
        {'title': raw_title, 'genres': ['Action', 'Comedy']}
    ]
    imdb = Imdb(raw_title)
    assert imdb.genres(1) == ['Action']


@patch('phylm.sources.imdb.Imdb.ia')
def test_no_genres(mock_ia):
    """
    Given a match with no genres,
    When the genres are retrieved,
    Then an empty list is returned
    """
    raw_title = 'The Movie'
    mock_ia.search_movie.return_value = [{'title': raw_title}]
    imdb = Imdb(raw_title)
    assert imdb.genres(1) == []


@patch('phylm.sources.imdb.Imdb.ia')
def test_cast(mock_ia):
    """
    Given a match with cast,
    When the cast is retrieved,
    Then the cast is returned with a given limit
    """
    raw_title = 'The Movie'
    mock_ia.search_movie.return_value = [
        {
            'title': raw_title,
            'cast': [{'name':'Tom'}, {'name':'Dick'}],
        }
    ]
    imdb = Imdb(raw_title)
    assert imdb.cast(1) == ['Tom']


@patch('phylm.sources.imdb.Imdb.ia')
def test_no_cast(mock_ia):
    """
    Given a match with no cast,
    When the cast is retrieved,
    Then an empty list is returned
    """
    raw_title = 'The Movie'
    mock_ia.search_movie.return_value = [{'title': raw_title}]
    imdb = Imdb(raw_title)
    assert imdb.cast(1) == []


@patch('phylm.sources.imdb.Imdb.ia')
def test_runtime(mock_ia):
    """
    Given a match with runtime,
    When the runtime is retrieved,
    Then the runtime is returned
    """
    raw_title = 'The Movie'
    mock_ia.search_movie.return_value = [
        {
            'title': raw_title,
            'runtimes': ['100', '90'],
        }
    ]
    imdb = Imdb(raw_title)
    assert imdb.runtime() == '100'


@patch('phylm.sources.imdb.Imdb.ia')
def test_no_runtime(mock_ia):
    """
    Given a match without runtime,
    When the runtime is retrieved,
    Then None is returned
    """
    raw_title = 'The Movie'
    mock_ia.search_movie.return_value = [{'title': raw_title}]
    imdb = Imdb(raw_title)
    assert imdb.runtime() is None


@patch('phylm.sources.imdb.Imdb.ia')
def test_year(mock_ia):
    """
    Given a match with year,
    When the year is retrieved,
    Then the year is returned
    """
    raw_title = 'The Movie'
    mock_ia.search_movie.return_value = [
        {
            'title': raw_title,
            'year': 2000,
        }
    ]
    imdb = Imdb(raw_title)
    assert imdb.year() == 2000


@patch('phylm.sources.imdb.Imdb.ia')
def test_no_year(mock_ia):
    """
    Given a match without year,
    When the year is retrieved,
    Then None is returned
    """
    raw_title = 'The Movie'
    mock_ia.search_movie.return_value = [{'title': raw_title}]
    imdb = Imdb('The Movie')
    assert imdb.year() is None


@patch('phylm.sources.imdb.Imdb.ia')
def test_directors(mock_ia):
    """
    Given a match with directors,
    When the directors are retrieved,
    Then the directors are returned with a given limit
    """
    raw_title = 'The Movie'
    mock_ia.search_movie.return_value = [
        {
            'title': raw_title,
            'directors': [{'name':'Tom'}, {'name':'Dick'}],
        }
    ]
    imdb = Imdb(raw_title)
    assert imdb.directors(1) == ['Tom']


@patch('phylm.sources.imdb.Imdb.ia')
def test_no_directors(mock_ia):
    """
    Given a match with no directors,
    When the directors is retrieved,
    Then an empty list is returne
    """
    raw_title = 'The Movie'
    mock_ia.search_movie.return_value = [{'title': raw_title}]
    imdb = Imdb(raw_title)
    assert imdb.directors(1) == []


@patch('phylm.sources.imdb.Imdb.ia')
def test_score(mock_ia):
    """
    Given a match with a rating,
    When the rating are retrieved,
    Then the rating is returned
    """
    raw_title = 'The Movie'
    mock_ia.search_movie.return_value = [
        {
            'title': raw_title,
            'rating': 8.1,
        }
    ]
    imdb = Imdb(raw_title)
    assert imdb.score() == 8.1


@patch('phylm.sources.imdb.Imdb.ia')
def test_no_score(mock_ia):
    """
    Given a match with no rating,
    When the reting is retrieved,
    Then None is return
    """
    raw_title = 'The Movie'
    mock_ia.search_movie.return_value = [{'title': raw_title}]
    imdb = Imdb(raw_title)
    assert imdb.score() is None


@patch('phylm.sources.imdb.Imdb.ia')
def test_plot_with_plot_data_already_retrieved(mock_ia):
    """
    Given a match with existing plot data,
    When the plot is retrieved,
    Then the plot is returned
    """
    raw_title = 'The Movie'
    mock_movie = MagicMock(current_info=['plot'])
    movie_data = {
        'title': 'The Movie',
        'plot': ['the plot::author']
    }
    mock_movie.get.side_effect = movie_data.get
    mock_movie.__getitem__.side_effect = movie_data.__getitem__
    mock_ia.search_movie.return_value = [mock_movie]
    imdb = Imdb(raw_title)
    assert imdb.plot() == 'the plot'
    mock_ia.update.assert_called_once_with(mock_movie, info=['main'])


@patch('phylm.sources.imdb.Imdb.ia')
def test_plot_without_plot_data_already_retrieved(mock_ia):
    """
    Given a match without existing plot data,
    When the plot is retrieved,
    Then the plot is fetched and then returned
    """
    raw_title = 'The Movie'
    mock_movie = MagicMock()
    movie_data = {
        'title': 'The Movie',
        'plot': ['the plot::author']
    }
    mock_movie.get.side_effect = movie_data.get
    mock_movie.__getitem__.side_effect = movie_data.__getitem__
    mock_ia.search_movie.return_value = [mock_movie]
    imdb = Imdb(raw_title)
    assert imdb.plot() == 'the plot'
    mock_ia.update.assert_has_calls([
        call(mock_movie, info=['main']),
        call(mock_movie, info=['plot']),
    ])


@patch('phylm.sources.imdb.Imdb.ia')
def test_no_plot_with_plot_data_already_retrieved(mock_ia):
    """
    Given a match with existing but empty plot data,
    When the plot is retrieved,
    Then None is returned
    """
    raw_title = 'The Movie'
    mock_movie = MagicMock(current_info=['plot'])
    movie_data = {
        'title': 'The Movie',
    }
    mock_movie.get.side_effect = movie_data.get
    mock_movie.__getitem__.side_effect = movie_data.__getitem__
    mock_ia.search_movie.return_value = [mock_movie]
    imdb = Imdb(raw_title)
    assert imdb.plot() is None


@patch('phylm.sources.imdb.Imdb.ia')
def test_plot_with_no_movie_results(mock_ia):
    """
    Given no match,
    When the plot is retrieved,
    Then None is returned
    """
    mock_ia.search_movie.return_value = []
    imdb = Imdb('The Movie')
    assert imdb.plot() is None
