import typer

from lib.movies_controller import MovieController

app = typer.Typer(rich_markup_mode="rich")
controller = MovieController()


@app.command(
    help="Lists all movies summarizing them at the end",
    short_help="Lists all movies summarizing them at the end"
)
def list_all():
    controller.list_all_movies()


@app.command(
    help="List all movies from a group summarizing them at the end",
    short_help="List all movies from a group summarizing them at the end"
)
def list_group(group: int):
    controller.list_by_group(group)


@app.command(short_help="Make a search for a pattern within the movie name")
def search(pattern: str):
    controller.search_movie(pattern)


@app.command(short_help="Marks a given movie as watched by id.")
def watched(movie_id: int):
    controller.change_watched_status(movie_id, watched=True)
    print(f"Movie {movie_id} has been marked as watched")


@app.command(short_help="Marks a given movie as unwatched by id.")
def unwatch(movie_id: int):
    controller.change_watched_status(movie_id, watched=False)
    print(f"Movie {movie_id} has been marked as unwatched")


@app.command(short_help="Creates a CSV file of the movies")
def export_to_csv(csv_file_name: str):
    pass


@app.command(short_help="Creates inserts file of the movie table")
def export_to_inserts(sql_file_name: str):
    pass


@app.command(short_help="Inserts a movie from a json file")
def insert_movie(movie_file: str):
    pass
