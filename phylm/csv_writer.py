import time
import csv

class CsvWriter:
    def __init__(self, header, movies):
        self.header = header
        self.movies = movies

    def write(self):
        current_timestamp = int(time.time())
        output_filename = f"phylm_{current_timestamp}.csv"
        with open(output_filename, mode='w') as output_csv:
            output_writer = csv.writer(output_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            output_writer.writerow(self.header)

            for movie in self.movies:
                print(f"Writing {movie.title}...")
                output_writer.writerow(movie.to_csv_row())
                print("Done")

