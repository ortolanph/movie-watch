import typer

from lib.movies_database import list_all_movies, setup_database, list_by_group, search_movie_by_pattern, \
    mark_as_watched_or_unwatched

app = typer.Typer()


@app.command()
def database_setup():
    setup_database()


@app.command()
def list_all():
    list_all_movies()


@app.command()
def list_group(group: int):
    list_by_group(group)


@app.command()
def search(pattern: str):
    search_movie_by_pattern(pattern)


@app.command()
def watched(movie_id: int):
    mark_as_watched_or_unwatched(movie_id)
    print(f"Movie {movie_id} has been marked as watched")


@app.command()
def unwatched(movie_id: int):
    mark_as_watched_or_unwatched(movie_id, watch_flag=False)
    print(f"Movie {movie_id} has been marked as unwatched")
