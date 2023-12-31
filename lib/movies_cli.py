""" CLI Module """
import emoji
import typer

from lib.movies_controller import MovieController

app = typer.Typer(rich_markup_mode="rich")
controller = MovieController()


@app.command(
    help="Lists all movies summarizing them at the end",
    short_help="Lists all movies summarizing them at the end"
)
def list_all():
    """ Lists all movies from all groups """
    controller.list_all_movies()


@app.command(
    help="List all movies from a group summarizing them at the end",
    short_help="List all movies from a group summarizing them at the end"
)
def list_group(group: int):
    """ Lists all movies from a given group """
    controller.list_by_group(group)


@app.command(
    help="Make a search for a pattern within the movie name",
    short_help="Make a search for a pattern within the movie name"
)
def search(pattern: str):
    """ Search a movie from a given pattern """
    controller.search_movie(pattern)


@app.command(
    help="Marks a given movie as watched by id",
    short_help="Marks a given movie as watched by id"
)
def watched(movie_id: int):
    """ Mark a movie as watched by its unique id """
    controller.change_watched_status(movie_id, watched=True)
    print(f"Movie {movie_id} has been marked as watched {emoji.emojize(':check_mark_button:')}")


@app.command(
    help="Marks a given movie as watched by group_id and movie_id",
    short_help="Marks a given movie as watched by group_id and movie_id"
)
def watched_gm(group_id: int, movie_id: int):
    """ Mark a movie as watched by its group id and movie id inside the group """
    controller.change_watched_status_gm(group_id, movie_id, watched=True)
    print(
        f"Movie {group_id}/{movie_id} has been marked "
        f"as watched {emoji.emojize(':check_mark_button:')}")


@app.command(
    help="Marks a given movie as unwatched by id",
    short_help="Marks a given movie as unwatched by id"
)
def unwatch(movie_id: int):
    """ Mark a movie as unwatched by its unique id """
    controller.change_watched_status(movie_id, watched=False)
    print(f"Movie {movie_id} has been marked as unwatched {emoji.emojize(':cross_mark:')}")


@app.command(
    help="Marks a given movie as unwatched by group_id and movie_id",
    short_help="Marks a given movie as unwatched by group_id and movie_id"
)
def unwatch_gm(group_id: int, movie_id: int):
    """ Mark a movie as unwatched by its group id and movie id inside the group """
    controller.change_watched_status_gm(group_id, movie_id, watched=False)
    print(
        f"Movie {group_id}/{movie_id}{movie_id} has been marked "
        f"as unwatched {emoji.emojize(':cross_mark:')}")


@app.command(
    help="Export data as CSV",
    short_help="Export data as CSV"
)
def export_to_csv(csv_file_name: str):
    """ Exports data to CSV as seen on reports """
    controller.export_to_csv(csv_file_name)
    print(f"Export completed! Check {csv_file_name} file {emoji.emojize(':memo:')}.")


@app.command(
    help="Export data as SQL Inserts",
    short_help="Export data as SQL Inserts"
)
def export_to_sql(sql_file_name: str):
    """ Exports data to SQL Imports of all the fields. Recommended for migrations """
    controller.export_to_sql_insert(sql_file_name)
    print(f"Export completed! Check {sql_file_name} file {emoji.emojize(':memo:')}.")


@app.command(
    help="Inserts a movie from a json file",
    short_help="Inserts a movie from a json file"
)
def insert_movie(movie_file: str):
    """ Inserts a movie from the contents of a JSON file """
    controller.insert_movie(movie_file)
    print(f"New movie inserted {emoji.emojize('::page_with_curl::')}.")


@app.command(
    help="Purges all watched movies",
    short_help="Purges all watched movies"
)
def purge():
    """ Purges all the watched movies """
    controller.purge()
    print(f"All watched movies purged {emoji.emojize(':collision:')}")


@app.command(
    help="Moves a movie to different group",
    short_help="Moves a movie to different group",
)
def move(movie_id: int, source_group_id: int, target_group_id: int):
    """ Moves a movie from one group to another """
    controller.move(movie_id, source_group_id, target_group_id)
    print(f"Movie {movie_id} moved from group {source_group_id} "
          f"{emoji.emojize(':backhand_index_pointing_right:')} "
          f"moved to group {target_group_id} "
          f"{emoji.emojize(':backhand_index_pointing_left:')}")
