""" Reporter module """
import emoji

from lib.movies_constants import (
    GROUP_LIST_HEADER,
    GROUP_LIST_HEADER_SEPARATOR,
    RECORD_FORMAT,
    GROUP_HEADER,
    SEARCH_RESULT_HEADER)
from lib.movies_utils import (
    convert_to_minutes,
    convert_to_flag,
    format_duration)


class MovieReporter:
    """ Reporter Class """

    def _print_headers(self):
        """ Print essential headers """
        print(GROUP_LIST_HEADER)
        print(GROUP_LIST_HEADER_SEPARATOR)

    def _print_record(self, result_item):
        """ Prints the record """
        print(RECORD_FORMAT.format(
            result_item["watched"],
            result_item["id"],
            result_item["group_id"],
            result_item["movie_id"],
            result_item["movie_name"],
            result_item["duration"],
            result_item["imdb_rating"],
            result_item["size_in_gb"]))

    def print_group(self, group_number, group_data):
        """ Print group """
        print(GROUP_HEADER.format(group_number))

        self._print_headers()

        for group_item in group_data:
            self._print_record(group_item)

        self._print_summary(group_data)

    def print_all_movies(self, movie_data):
        """ Print all movies """
        groups = list(set(movie_item["group_id"] for movie_item in movie_data))

        print("All Movies\n")

        for group in groups:
            group_data = \
                [movie_item
                 for movie_item in movie_data
                 if movie_item["group_id"] == group]
            self.print_group(group, group_data)
            print("\n")

        self._print_summary(movie_data)

    def print_search_results(self, pattern, search_results):
        """ Print the search results """
        print(SEARCH_RESULT_HEADER.format(search_pattern=pattern))

        self._print_headers()

        for search_result in search_results:
            self._print_record(search_result)

    def _filter_watched(self, status_tuple_array):
        """ Filter watched movies"""
        return filter(lambda x: x[0] == 1, status_tuple_array)

    def _filter_unwatched(self, status_tuple_array):
        """ Filter unwatched movies"""
        return list(filter(lambda x: x[0] == 0, status_tuple_array))

    def _print_summary(self, data):
        """ Prints summary every group end """
        status_tuple_array = list(
            (
                convert_to_flag(data_item["watched"]),
                convert_to_minutes(data_item["duration"]),
                data_item["size_in_gb"]
            )
            for data_item in data)

        total_duration = format_duration(sum(list(map(lambda x: x[1], status_tuple_array))))
        watched_time = format_duration(
            sum(list(map(lambda x: x[1], self._filter_watched(status_tuple_array)))))
        time_left = format_duration(
            sum(list(map(lambda x: x[1], self._filter_unwatched(status_tuple_array)))))

        total_size = sum(list(map(lambda x: x[2], status_tuple_array)))
        consumed_gb = (
            sum(list(map(lambda x: x[2], self._filter_watched(status_tuple_array)))))
        left_gb = (
            sum(list(map(lambda x: x[2], self._filter_unwatched(status_tuple_array)))))

        watched_movies = len(list(filter(lambda x: x[0] == 1, status_tuple_array)))
        not_watched_movies = len(list(filter(lambda x: x[0] == 0, status_tuple_array)))
        progress = ((watched_movies / len(status_tuple_array)) * 100)

        print(f"\n{emoji.emojize(':bar_chart:')} Status\n")
        print(f"-[ {emoji.emojize(':mantelpiece_clock:')} TIME "
              f"]-------------------------------------------------------------------------")
        print(f"Total Duration .....: {total_duration}")
        print(f"Watched Time .......: {watched_time}")
        print(f"Time Left ..........: {time_left}")
        print(f"\n-[ {emoji.emojize(':computer_disk:')} Size "
              f"]-------------------------------------------------------------------------")
        print(f"Total Size ..........: {total_size:>7.2f}")
        print(f"Consumed GB .........: {consumed_gb:>7.2f}")
        print(f"Left GB .............: {left_gb:>7.2f}")
        print(f"\n-[ {emoji.emojize(':movie_camera:')} Watched Movies "
              f"]---------------------------------------------------------------")
        print(f"Watched .............: {watched_movies:>7.0f}")
        print(f"Not Watched .........: {not_watched_movies:>7.0f}")
        print(f"Progress ............: {progress:>7.2f} %")
        print(f"{'-' * 85}\n")
