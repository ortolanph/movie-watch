CREATE_MOVIES_TABLE = '''create table movie 
    (id integer not null primary key autoincrement, 
    group_id integer not null, 
    movie_id integer not null, 
    movie_name text not null, 
    movie_year int not null, 
    file_name text not null, 
    duration int not null, 
    watched int default 0, 
    imdb_rating real not null, 
    original_size real not null, 
    size_in_gb real);'''

INSERT_MOVIE = '''insert into movie (
                            group_id, 
                            movie_id, 
                            movie_name, 
                            movie_year, 
                            file_name, 
                            duration, 
                            watched, 
                            imdb_rating, 
                            original_size, 
                            size_in_gb) 
                  values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''

SELECT_MOVIES = '''select watched, 
                          id, 
                          group_id, 
                          movie_id, 
                          movie_name, 
                          duration, 
                          imdb_rating, 
                          size_in_gb 
                     from movie 
                    order by group_id, movie_id, id;'''

SELECT_ALL_FIELDS_MOVIES = '''select * from movie order by group_id, movie_id, id;'''

SELECT_MOVIES_BY_GROUP = '''select watched, 
                                   id, 
                                   group_id, 
                                   movie_id, 
                                   movie_name, 
                                   duration, 
                                   imdb_rating, 
                                   size_in_gb 
                              from movie 
                             where group_id = ? 
                             order by group_id, movie_id, id;'''

SELECT_MOVIES_BY_PATTERN = """select watched, 
                                     id, 
                                     group_id, 
                                     movie_id, 
                                     movie_name, 
                                     duration, 
                                     imdb_rating, 
                                     size_in_gb 
                                from movie 
                               where movie_name like ? 
                               order by group_id, movie_id, id;"""

UPDATE_MOVIE_AS_WATCHED = '''update movie 
                                set watched = 1 
                              where id = ?;'''

UPDATE_MOVIE_AS_UNWATCHED = '''update movie 
                                  set watched = 0 
                                where id = ?;'''

PURGE_WATCHED_MOVIE = '''delete from movie where watched = 1'''

LAST_GROUP_ID = '''select coalesce(max(movie_id), 0) as last_id
                     from movie
                    where group_id = ?'''
