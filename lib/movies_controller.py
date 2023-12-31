""" Controller module. It will interoperate with the Repository and the Reporter """
import csv
import json

from art import tprint
from jinja2 import Template

from lib.movies_constants import CSV_HEADERS, SQL_INSERT_TEMPLATE_FILE
from lib.movies_database import MovieRepository
from lib.movies_reports import MovieReporter
from lib.movies_utils import extract_csv_info, create_movie_data


class MovieController:
    """ Controller to orchestrate cli calls """
    _repository: MovieRepository = None
    _reporter: MovieReporter = None

    def __init__(self):
        """ Class initializer """
        self._repository = MovieRepository()
        self._reporter = MovieReporter()
        self.__banner()

    def __banner(self):
        """ Prints the project banner """
        tprint("Movies", font="starwars")

    def list_all_movies(self):
        """ Lists all movies """
        all_movies = self._repository.list_all_movies()
        self._reporter.print_all_movies(all_movies)

    def list_by_group(self, group_id):
        """ Lists movies by group """
        group_movies = self._repository.list_by_group(group_id)
        self._reporter.print_group(group_id, group_movies)

    def search_movie(self, movie_pattern):
        """ Search movie by a movie pattern """
        search_results = self._repository.search_movie_by_pattern(movie_pattern)
        self._reporter.print_search_results(movie_pattern, search_results)

    def change_watched_status(self, movie_id, watched=None):
        """ Change the status of the movie by movie unique id """
        self._repository.change_movie_status(movie_id, watched)

    def change_watched_status_gm(self, group_id, movie_id, watched=None):
        """ Change the status of the movie by group id and movie id inside the group """
        self._repository.change_movie_status_gm(group_id, movie_id, watched)

    def export_to_csv(self, csv_file_name):
        """ Exports selected fields to CSV """
        all_movies = self._repository.list_all_movies()
        all_movies_formatted = list(map(extract_csv_info, all_movies))

        with open(csv_file_name, 'w', encoding='UTF8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS)
            writer.writeheader()
            writer.writerows(all_movies_formatted)

    def export_to_sql_insert(self, sql_file_name):
        """ Exports to SQL Inserts """
        all_fields_movies = self._repository.list_all_fields_movies()

        with open(SQL_INSERT_TEMPLATE_FILE, encoding='UTF8') as template_file:
            sql_template = Template(template_file.read())

        rendered_sql_file = sql_template.render(movies=all_fields_movies)

        with open(sql_file_name, 'w', encoding='UTF8', newline='') as sql_file:
            sql_file.writelines(rendered_sql_file)

    def purge(self):
        """ Purges all watched movies """
        self._repository.purge_watched_movies()

    def insert_movie(self, movie_file):
        """ Inserts a movie from a JSON Template file """
        with open(movie_file, encoding='UTF8') as json_file:
            movie_file_data = json.load(json_file)

        movie_data = create_movie_data(movie_file_data)

        next_movie_id = self._repository.next_movie_id(movie_data["group_id"])

        movie_data["movie_id"] = next_movie_id

        self._repository.insert_movie(movie_data)

        print("Movie inserted with success!")

    def move(self, movie_id, source_group_id, target_group_id):
        """ Moves a movie from a group to another """
        next_movie_id = self._repository.next_movie_id(target_group_id)

        self._repository.change_group(target_group_id, next_movie_id, source_group_id, movie_id)
