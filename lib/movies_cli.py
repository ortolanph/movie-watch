import typer

from lib.movies_controller import MovieController

app = typer.Typer()
controller = MovieController()


@app.command()
def list_all():
    controller.list_all_movies()


@app.command()
def list_group(group: int):
    controller.list_by_group(group)


@app.command()
def search(pattern: str):
    controller.search_movie(pattern)


@app.command()
def watched(movie_id: int):
    controller.change_watched_status(movie_id, watched=True)
    print(f"Movie {movie_id} has been marked as watched")


@app.command()
def unwatch(movie_id: int):
    controller.change_watched_status(movie_id, watched=False)
    print(f"Movie {movie_id} has been marked as unwatched")
