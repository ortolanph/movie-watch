from lib.movies_connection_manager import ConnectionManager
from lib.movies_sql import INSERT_MOVIE, SELECT_MOVIES, SELECT_MOVIES_BY_GROUP, \
    SELECT_MOVIES_BY_PATTERN, UPDATE_MOVIE_AS_WATCHED, UPDATE_MOVIE_AS_UNWATCHED, SELECT_ALL_FIELDS_MOVIES
from lib.movies_utils import extract_row_info, extract_all_fields_info

DATABASE_FILE = "movies.sqlite3"
SOURCE_DATA = "src/movies_all.csv"


class MovieRepository:
    _connection = None

    def __init__(self):
        manager = ConnectionManager()
        self._connection = manager.get_connection()

    def _close_connection(self):
        self._connection.close()
        self._connection = None

    def insert_movie(self, group_id, movie_id, movie_name, movie_year, file_name, duration, watched, imdb_rating,
                     file_size,
                     size_in_gb):
        cursor = self._connection.cursor()

        cursor.execute(INSERT_MOVIE, (
            group_id, movie_id, movie_name, movie_year, file_name, duration, watched, imdb_rating, file_size,
            size_in_gb))

        self._connection.commit()
        self._close_connection()

    def list_all_movies(self):
        cursor = self._connection.execute(SELECT_MOVIES)

        movie_data = []
        for row in cursor:
            movie_data.append(extract_row_info(row))

        self._close_connection()

        return movie_data

    def list_by_group(self, group_id):
        cursor = self._connection.execute(SELECT_MOVIES_BY_GROUP, [group_id])

        group_data = []
        for row in cursor:
            group_data.append(extract_row_info(row))

        self._close_connection()

        return group_data

    def search_movie_by_pattern(self, pattern):
        cursor = self._connection.execute(SELECT_MOVIES_BY_PATTERN, ['%' + pattern + '%'])

        search_data = []
        for row in cursor:
            search_data.append(extract_row_info(row))

        self._close_connection()

        return search_data

    def change_movie_status(self, movie_pk_id, watched=None):
        statement = UPDATE_MOVIE_AS_WATCHED if watched else UPDATE_MOVIE_AS_UNWATCHED

        self._connection.execute(statement, [movie_pk_id])
        self._connection.commit()
        self._close_connection()

    def list_all_fields_movies(self):
        cursor = self._connection.execute(SELECT_ALL_FIELDS_MOVIES)

        movie_data = []
        for row in cursor:
            movie_data.append(extract_all_fields_info(row))

        self._close_connection()

        return movie_data
