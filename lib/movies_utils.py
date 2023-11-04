import os
from datetime import timedelta

from sqlescapy import sqlescape


def convert_to_watched(watched):
    if watched == "TRUE":
        return 1
    else:
        return 0


def format_watched(watched_flag):
    if watched_flag == 1:
        return "X"
    else:
        return " "


def convert_to_flag(watched_flag):
    if watched_flag == 'X':
        return 1
    else:
        return 0


def format_duration(duration):
    return str(timedelta(minutes=duration))


def convert_to_minutes(duration):
    factors = (60, 1, 1 / 60)

    return int(sum(i * j for i, j in zip(map(int, duration.split(':')), factors)))


def extract_row_info(row):
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
    return {
        "watched": convert_to_flag(row["watched"]),
        "group_id": row["group_id"],
        "movie_id": row["movie_id"],
        "movie_name": row["movie_name"],
        "duration": convert_to_minutes(row["duration"]),
        "imdb_rating": row["imdb_rating"],
        "size_in_gb": row["size_in_gb"]
    }


def remove_path(file_name: str):
    return file_name.split(os.sep).pop()


def get_file_size(file_name):
    return os.stat(file_name).st_size


def format_to_gb(file_size):
    return float(("{:.2f}".format(file_size / (1024 * 1024 * 1024))))


def create_movie_data(movie_file_data):
    file_size = get_file_size(movie_file_data["filename"])
    file_size_in_gb = format_to_gb(file_size)

    return {
        "group_id": movie_file_data["group"],
        "movie_name": sqlescape(movie_file_data["name"]),
        "movie_id": 0,
        "movie_year": movie_file_data["year"],
        "file_name": sqlescape(remove_path(movie_file_data["filename"])),
        "duration": movie_file_data["duration"],
        "watched": 0,
        "imdb_rating": movie_file_data["imdb_rating"],
        "original_size": file_size,
        "size_in_gb": file_size_in_gb
    }
