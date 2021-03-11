from phylm.movie import Movie
from phylm.csv_writer import CsvWriter

m1 = Movie('The Matrix', 1999)

headers = [
    'Title',
    'Year',
    'Genres',
    'Runtime',
    'Cast',
    'Director(s)',
    'Plot',
    'IMDb',
    'Metacritic',
    'RT Score',
    'RT Audience Score',
]

writer = CsvWriter(headers, [m1])
writer.write()
