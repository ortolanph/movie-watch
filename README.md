# Movie Watch

A command line interface to manage your list of movies.

## Groups

The movies are divided into groups. Each movie has a group id and a movie id and an unique id.

## Commands


### **export-to-csv**: 

Export data as CSV

Example:

```commandline
movies export-to-csv path/to/file_name.csv
```

### **export-to-sql**:

Export data as SQL Inserts


* **insert-movie**: Inserts a movie from a json file
* **list-all**: Lists all movies summarizing them at the end
* **list-group**: List all movies from a group summarizing them at the end│
* **move**: Moves a movie to different group
* **purge**: Purges all watched movies
* **search**: Make a search for a pattern within the movie name
* **unwatch**: Marks a given movie as unwatched by id
* **unwatch-gm**: Marks a given movie as unwatched by group_id and movie_id
* **watched**: Marks a given movie as watched by id
* **watched-gm**: Marks a given movie as watched by group_id and movie_id

Type `python .\movies.py export-to-csv --help` to get help from any command.