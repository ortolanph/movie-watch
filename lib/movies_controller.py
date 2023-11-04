import csv

from art import tprint
from jinja2 import Template

from lib.movies_constants import CSV_HEADERS, SQL_INSERT_TEMPLATE_FILE
from lib.movies_database import MovieRepository
from lib.movies_reports import MovieReporter
from lib.movies_utils import extract_csv_info


class MovieController:
    _repository: MovieRepository = None
    _reporter: MovieReporter = None

    def __init__(self):
        self._repository = MovieRepository()
        self._reporter = MovieReporter()
        self.__banner()

    def __banner(self):
        tprint("Movies", font="starwars")

    def list_all_movies(self):
        all_movies = self._repository.list_all_movies()
        self._reporter.print_all_movies(all_movies)

    def list_by_group(self, group_id):
        group_movies = self._repository.list_by_group(group_id)
        self._reporter.print_group(group_id, group_movies)

    def search_movie(self, movie_pattern):
        search_results = self._repository.search_movie_by_pattern(movie_pattern)
        self._reporter.print_search_results(movie_pattern, search_results)

    def change_watched_status(self, movie_id, watched=None):
        self._repository.change_movie_status(movie_id, watched)

    def export_to_csv(self, csv_file_name):
        all_movies = self._repository.list_all_movies()
        all_movies_formatted = list(map(lambda movie: extract_csv_info(movie), all_movies))

        with open(csv_file_name, 'w', encoding='UTF8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS)
            writer.writeheader()
            writer.writerows(all_movies_formatted)

    def export_to_sql_insert(self, sql_file_name):
        all_fields_movies = self._repository.list_all_fields_movies()

        with open(SQL_INSERT_TEMPLATE_FILE) as template_file:
            sql_template = Template(template_file.read())

        rendered_sql_file = sql_template.render(movies=all_fields_movies)

        with open(sql_file_name, 'w', encoding='UTF8', newline='') as sql_file:
            sql_file.writelines(rendered_sql_file)

    def purge(self):
        self._repository.purge_watched_movies()
