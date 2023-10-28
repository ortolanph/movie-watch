from art import tprint

from lib.movies_database import MovieRepository
from lib.movies_reports import MovieReporter


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
