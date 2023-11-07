""" Database module. """
from lib.movies_connection_manager import ConnectionManager
from lib.movies_sql import (INSERT_MOVIE,
                            SELECT_MOVIES,
                            SELECT_MOVIES_BY_GROUP,
                            SELECT_MOVIES_BY_PATTERN,
                            UPDATE_MOVIE_AS_WATCHED_BY_ID,
                            UPDATE_MOVIE_AS_UNWATCHED_BY_ID,
                            SELECT_ALL_FIELDS_MOVIES,
                            PURGE_WATCHED_MOVIE,
                            LAST_GROUP_ID,
                            UPDATE_MOVIE_AS_WATCHED_BY_GROUP_ID_MOVIE_ID,
                            UPDATE_MOVIE_AS_UNWATCHED_BY_GROUP_ID_MOVIE_ID,
                            MOVE_MOVIE)
from lib.movies_utils import extract_row_info, extract_all_fields_info

DATABASE_FILE = "movies.sqlite3"
SOURCE_DATA = "src/movies_all.csv"


class MovieRepository:
    """ Performs operations in the database """
    _connection = None

    def __init__(self):
        """ Initializes the Movie Repository """
        manager = ConnectionManager()
        self._connection = manager.get_connection()

    def _close_connection(self):
        """ Closes connection """
        self._connection.close()
        self._connection = None

    def insert_movie(self,
                     movie_data):
        """ Inserts a movie """
        cursor = self._connection.cursor()

        cursor.execute(INSERT_MOVIE, (
            movie_data["group_id"],
            movie_data["movie_id"],
            movie_data["movie_name"],
            movie_data["movie_year"],
            movie_data["file_name"],
            movie_data["duration"],
            movie_data["watched"],
            movie_data["imdb_rating"],
            movie_data["original_size"],
            movie_data["size_in_gb"])
        )

        self._connection.commit()
        self._close_connection()

    def list_all_movies(self):
        """ Lists all movies """
        cursor = self._connection.execute(SELECT_MOVIES)

        movie_data = []
        for row in cursor:
            movie_data.append(extract_row_info(row))

        self._close_connection()

        return movie_data

    def list_by_group(self, group_id):
        """ Lists movie by group """
        cursor = self._connection.execute(SELECT_MOVIES_BY_GROUP, [group_id])

        group_data = []
        for row in cursor:
            group_data.append(extract_row_info(row))

        self._close_connection()

        return group_data

    def search_movie_by_pattern(self, pattern):
        """ Searches movies by pattern """
        cursor = self._connection.execute(SELECT_MOVIES_BY_PATTERN, ['%' + pattern + '%'])

        search_data = []
        for row in cursor:
            search_data.append(extract_row_info(row))

        self._close_connection()

        return search_data

    def change_movie_status(self, movie_pk_id, watched=None):
        """ Changes movie status by movie unique id """
        statement = UPDATE_MOVIE_AS_WATCHED_BY_ID if watched else UPDATE_MOVIE_AS_UNWATCHED_BY_ID

        self._connection.execute(statement, [movie_pk_id])
        self._connection.commit()
        self._close_connection()

    def change_movie_status_gm(self, group_id, movie_id, watched):
        """ Changes movie status by Group Id and movie Id inside the group"""
        statement = UPDATE_MOVIE_AS_WATCHED_BY_GROUP_ID_MOVIE_ID if watched \
            else UPDATE_MOVIE_AS_UNWATCHED_BY_GROUP_ID_MOVIE_ID

        self._connection.execute(statement, [group_id, movie_id])
        self._connection.commit()
        self._close_connection()

    def list_all_fields_movies(self):
        """ Lists all fields from the movies table"""
        cursor = self._connection.execute(SELECT_ALL_FIELDS_MOVIES)

        movie_data = []
        for row in cursor:
            movie_data.append(extract_all_fields_info(row))

        self._close_connection()

        return movie_data

    def purge_watched_movies(self):
        """ Purges all watched movies """
        self._connection.execute(PURGE_WATCHED_MOVIE)
        self._connection.commit()
        self._close_connection()

    def next_movie_id(self, group_id):
        """ Discovers the next movie id from a group id """
        cursor = self._connection.execute(LAST_GROUP_ID, [group_id])

        next_movie_id = cursor.fetchone()[0] + 1

        return next_movie_id

    def change_group(self, target_group_id, next_movie_id, source_group_id, movie_id):
        """ Changes movie group id"""
        self._connection.execute(
            MOVE_MOVIE, [
                target_group_id, next_movie_id,
                source_group_id, movie_id])
        self._connection.commit()
        self._close_connection()
