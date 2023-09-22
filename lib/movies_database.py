import csv
import os
import sqlite3

from lib.movies_reports import print_all_movies, print_group, print_search_results
from lib.movies_sql import CREATE_MOVIES_TABLE, INSERT_MOVIE, SELECT_MOVIES, SELECT_MOVIES_BY_GROUP, \
    SELECT_MOVIES_BY_PATTERN, UPDATE_MOVIE_AS_WATCHED, UPDATE_MOVIE_AS_UNWATCHED
from lib.movies_utils import convert_to_minutes, convert_to_watched, \
    extract_row_info

DATABASE_FILE = "movies.sqlite3"
SOURCE_DATA = "src/movies_all.csv"


def _create_table():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(CREATE_MOVIES_TABLE)
    conn.commit()
    conn.close()
    _load_data()


def setup_database():
    if not os.path.isfile(DATABASE_FILE):
        conn = sqlite3.connect(DATABASE_FILE, timeout=10)
        conn.close()
        _create_table()


def insert_movie(group_id, movie_id, movie_name, movie_year, file_name, duration, watched, imdb_rating, file_size,
                 size_in_gb):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute(INSERT_MOVIE, (
        group_id, movie_id, movie_name, movie_year, file_name, duration, watched, imdb_rating, file_size, size_in_gb))
    conn.commit()

    conn.close()


def _load_data():
    with open(SOURCE_DATA) as data:
        csv_reader = csv.DictReader(data, delimiter=',')
        for row in csv_reader:
            group_id = int(row["Group"])
            movie_id = int(row["Order"])
            movie_name = row["Movie"]
            movie_year = int(row["Year"])
            file_name = row["File Name"]
            duration = convert_to_minutes(row["Duration"])
            watched = convert_to_watched(row["Watched"])
            imdb_rating = float(row["IMDB Rating"])
            file_size = int(row["Size"])
            size_in_gb = float(row["Size in GB"])

            insert_movie(group_id, movie_id, movie_name, movie_year, file_name, duration, watched, imdb_rating,
                         file_size, size_in_gb)


def list_all_movies():
    conn = sqlite3.connect(DATABASE_FILE)

    cursor = conn.execute(SELECT_MOVIES)
    movie_data = []
    for row in cursor:
        movie_data.append(extract_row_info(row))

    print_all_movies(movie_data)

    conn.close()


def list_by_group(group_id):
    conn = sqlite3.connect(DATABASE_FILE)

    cursor = conn.execute(SELECT_MOVIES_BY_GROUP, [group_id])
    group_data = []
    for row in cursor:
        group_data.append(extract_row_info(row))

    print_group(group_id, group_data)

    conn.close()


def search_movie_by_pattern(pattern):
    conn = sqlite3.connect(DATABASE_FILE)

    cursor = conn.execute(SELECT_MOVIES_BY_PATTERN, ['%' + pattern + '%'])
    search_data = []
    for row in cursor:
        search_data.append(extract_row_info(row))

    print_search_results(pattern, search_data)

    conn.close()


def mark_as_watched_or_unwatched(movie_pk_id, watch_flag=True):
    conn = sqlite3.connect(DATABASE_FILE)

    statement = UPDATE_MOVIE_AS_WATCHED if watch_flag else UPDATE_MOVIE_AS_UNWATCHED

    cursor = conn.execute(statement, [movie_pk_id])

    conn.commit()
    conn.close()
