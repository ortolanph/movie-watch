from datetime import timedelta


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
