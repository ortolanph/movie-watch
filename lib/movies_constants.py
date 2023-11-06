""" Constants for all the project """
import emoji

DATABASE_FILE = "movies.sqlite3"

GROUP_LIST_HEADER = ('      Id    Group   Movie Id  '
                     'Movie Name                                                                   '
                     'Duration  IMDB Rating  Size In GB')

GROUP_LIST_HEADER_SEPARATOR = '-' * 144

RECORD_FORMAT = '[{:1}]  {:>3}        {:>1}         {:>2}  {:<75}   {:>7} {:>12} {:>11}'

GROUP_HEADER = emoji.emojize(":movie_camera:") + ' GROUP {:>3}\n'

SEARCH_RESULT_HEADER = (emoji.emojize(":magnifying_glass_tilted_left:") +
                        " Search results for '{search_pattern}'\n")

CSV_HEADERS = [
    "group_id",
    "movie_id",
    "movie_name",
    "duration",
    "watched",
    "imdb_rating",
    "size_in_gb"
]

SQL_INSERT_TEMPLATE_FILE = "templates/inserts.sql.template"
