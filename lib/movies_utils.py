""" Utils module. Common functions that are used in the whole project. """
import os
from datetime import timedelta

from sqlescapy import sqlescape


def format_watched(watched_flag):
    """ Convert flag 1 to X and 0 to a blank space"""
    return "X" if watched_flag == 1 else " "


def convert_to_flag(watched_flag):
    """ Convert X to 1 and blank space to 0 """
    return 1 if watched_flag == 'X' else 0


def format_duration(duration):
    """ Convert numeric duration into string containing days,
    hours, minutes and seconds (that will be always 00)"""
    return str(timedelta(minutes=duration))


def convert_to_minutes(duration):
    """ Convert duration in string in the format hh:mm:ss to time in minutes """
    factors = (60, 1, 1 / 60)

    return int(sum(i * j for i, j in zip(map(int, duration.split(':')), factors)))


def extract_row_info(row):
    """ Converts query results into a dictionary format"""
    return {
        "watched": format_watched(row[0]),
        "id": row[1],
        "group_id": row[2],
        "movie_id": row[3],
        "movie_name": row[4],
        "duration": format_duration(row[5]),
        "imdb_rating": row[6],
        "size_in_gb": row[7]
    }


def extract_all_fields_info(row):
    """ Converts query results of all fields into a dictionary format """
    return {
        "group_id": row[1],
        "movie_id": row[2],
        "movie_name": sqlescape(row[3]),
        "movie_year": row[4],
        "file_name": sqlescape(row[5]),
        "duration": row[6],
        "watched": row[7],
        "imdb_rating": row[8],
        "original_size": row[9],
        "size_in_gb": row[10]
    }


def extract_csv_info(row):
    """ Convert query results into a fomat for CSV file"""
    return {
        "watched": convert_to_flag(row["watched"]),
        "group_id": row["group_id"],
        "movie_id": row["movie_id"],
        "movie_name": row["movie_name"],
        "duration": convert_to_minutes(row["duration"]),
        "imdb_rating": row["imdb_rating"],
        "size_in_gb": row["size_in_gb"]
    }


def _remove_path(file_name: str):
    """ Gets the absolute name of a file """
    return file_name.split(os.sep).pop()


def _get_file_size(file_name):
    """ Retrieves the File Size """
    return os.stat(file_name).st_size


def _format_to_gb(file_size):
    """ Format the original file size into GB of two digit """
    file_size_gb = file_size / (1024 * 1024 * 1024)
    return float(f"{file_size_gb:.2f}")


def create_movie_data(movie_file_data):
    """ Create data came from json file to be inserted into the database """
    file_size = _get_file_size(movie_file_data["filename"])
    file_size_in_gb = _format_to_gb(file_size)

    return {
        "group_id": movie_file_data["group"],
        "movie_name": sqlescape(movie_file_data["name"]),
        "movie_id": 0,
        "movie_year": movie_file_data["year"],
        "file_name": sqlescape(_remove_path(movie_file_data["filename"])),
        "duration": movie_file_data["duration"],
        "watched": 0,
        "imdb_rating": movie_file_data["imdb_rating"],
        "original_size": file_size,
        "size_in_gb": file_size_in_gb
    }
