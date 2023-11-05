import emoji

from lib.movies_constants import GROUP_LIST_HEADER, GROUP_LIST_HEADER_SEPARATOR, RECORD_FORMAT, GROUP_HEADER, \
    SEARCH_RESULT_HEADER
from lib.movies_utils import convert_to_minutes, convert_to_flag, format_duration


class MovieReporter:
    def _print_headers(self):
        print(GROUP_LIST_HEADER)
        print(GROUP_LIST_HEADER_SEPARATOR)

    def print_group(self, group_number, group_data):
        print(GROUP_HEADER.format(group_number))

        self._print_headers()

        for group_item in group_data:
            print(RECORD_FORMAT.format(group_item["watched"], group_item["id"], group_item["group_id"],
                                       group_item["movie_id"], group_item["movie_name"], group_item["duration"],
                                       group_item["imdb_rating"], group_item["size_in_gb"]))

        self._print_summary(group_data)

    def print_all_movies(self, movie_data):
        groups = list(set(movie_item["group_id"] for movie_item in movie_data))

        print("All Movies\n")

        for group in groups:
            group_data = [movie_item for movie_item in movie_data if movie_item["group_id"] == group]
            self.print_group(group, group_data)
            print("\n")

        self._print_summary(movie_data)

    def print_search_results(self, pattern, search_results):
        print(SEARCH_RESULT_HEADER.format(search_pattern=pattern))

        self._print_headers()

        for search_result in search_results:
            print(RECORD_FORMAT.format(search_result["watched"], search_result["id"], search_result["group_id"],
                                       search_result["movie_id"], search_result["movie_name"],
                                       search_result["duration"],
                                       search_result["imdb_rating"], search_result["size_in_gb"]))

    def _print_summary(self, data):
        status_tuple_array = list(
            (convert_to_flag(data_item["watched"]), convert_to_minutes(data_item["duration"]), data_item["size_in_gb"])
            for data_item in data)

        total_duration = format_duration(sum(list(map(lambda x: x[1], status_tuple_array))))
        watched_time = format_duration(
            sum(list(map(lambda x: x[1], list(filter(lambda x: x[0] == 1, status_tuple_array))))))
        time_left = format_duration(
            sum(list(map(lambda x: x[1], list(filter(lambda x: x[0] == 0, status_tuple_array))))))

        total_size = sum(list(map(lambda x: x[2], status_tuple_array)))
        consumed_gb = sum(list(map(lambda x: x[2], list(filter(lambda x: x[0] == 1, status_tuple_array)))))
        left_gb = sum(list(map(lambda x: x[2], list(filter(lambda x: x[0] == 0, status_tuple_array)))))

        watched_movies = len(list(filter(lambda x: x[0] == 1, status_tuple_array)))
        not_watched_movies = len(list(filter(lambda x: x[0] == 0, status_tuple_array)))
        progress = ((watched_movies / len(status_tuple_array)) * 100)

        print(f"\n{emoji.emojize(':bar_chart:')} Status\n")
        print(f"-[ {emoji.emojize(':mantelpiece_clock:')} TIME ]-------------------------------------------------------------------------")
        print(f"Total Duration .....: {total_duration}")
        print(f"Watched Time .......: {watched_time}")
        print(f"Time Left ..........: {time_left}")
        print(f"\n-[ {emoji.emojize(':computer_disk:')} Size ]-------------------------------------------------------------------------")
        print("Total Size ..........: {:>7.2f}".format(total_size))
        print("Consumed GB .........: {:>7.2f}".format(consumed_gb))
        print("Left GB .............: {:>7.2f}".format(left_gb))
        print(f"\n-[ {emoji.emojize(':movie_camera:')} Watched Movies ]---------------------------------------------------------------")
        print("Watched .............: {:>7.0f}".format(watched_movies))
        print("Not Watched .........: {:>7.0f}".format(not_watched_movies))
        print("Progress ............: {:>7.2f} %".format(progress))
        print("----------------------------------------------------------------------------------\n")
