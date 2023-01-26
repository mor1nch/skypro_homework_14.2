import sqlite3


def db_connect(db_name, query) -> list:
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(query)
    data = cur.fetchall()
    con.close()
    return data


def search_film_by_title(title_name) -> dict:
    sqlite_query = (f"""
        SELECT title, country, release_year, listed_in, description
        FROM netflix
        WHERE title LIKE '%{title_name}%'
        ORDER BY release_year DESC""")

    movie_dict = {}
    data = db_connect('netflix.db', sqlite_query)

    for content in data:
        movie_dict["title"] = content[0]
        movie_dict["country"] = content[1]
        movie_dict["release_year"] = content[2]
        movie_dict["genre"] = content[3]
        movie_dict["description"] = content[4].replace('\n', '')
    return movie_dict


def sort_by_years_interval(from_year, to_year) -> list:
    sqlite_query = (f"""
        SELECT title, release_year
        FROM netflix
        WHERE release_year BETWEEN {from_year} AND {to_year}
        ORDER BY release_year  
        LIMIT 100""")

    movie_list = []
    movie_dict = {}
    data = db_connect('netflix.db', sqlite_query)

    for content in data:
        movie_dict["title"] = content[0]
        movie_dict["release_year"] = content[1]
        movie_list.append(movie_dict)
        movie_dict = {}

    return movie_list


def search_by_rating(movie_rating) -> list:
    if movie_rating == 'adult':
        sqlite_query = (f"""
                    SELECT title, rating, description
                    FROM netflix
                    WHERE rating IN ('R', 'NC-17')
                    ORDER BY release_year  
                    """)
    elif movie_rating == 'family':
        sqlite_query = (f"""
                    SELECT title, rating, description
                    FROM netflix
                    WHERE rating IN ('G', 'PG', 'PG-13')
                    ORDER BY release_year  
                    """)
    else:
        sqlite_query = (f"""
                    SELECT title, rating, description
                    FROM netflix
                    WHERE rating IN ('G')
                    ORDER BY release_year  
                    """)

    movie_list = []
    movie_dict = {}
    data = db_connect('netflix.db', sqlite_query)

    for content in data:
        movie_dict["title"] = content[0]
        movie_dict["rating"] = content[1]
        movie_dict["description"] = content[2].replace('\n', '')
        movie_list.append(movie_dict)
        movie_dict = {}
    return movie_list


def search_by_genre(genre) -> list:
    sqlite_query = (f"""
                        SELECT title, description
                        FROM netflix
                        WHERE netflix.listed_in LIKE '%{genre}%'
                        ORDER BY release_year DESC
                        LIMIT 10
                        """)
    movie_list = []
    movie_dict = {}
    data = db_connect('netflix.db', sqlite_query)

    for content in data:
        movie_dict["title"] = content[0]
        movie_dict["description"] = content[1].replace('\n', '')
        movie_list.append(movie_dict)
        movie_dict = {}
    return movie_list


def search_couple(first_actor, second_actor) -> list:
    sqlite_query = (f"""
                        SELECT netflix.cast 
                        FROM netflix
                        WHERE netflix.cast LIKE '%{first_actor}%'
                        AND netflix.cast LIKE '%{second_actor}%'
                        """)
    actors_list = []
    actors_dict = {}
    data = db_connect('netflix.db', sqlite_query)

    for i in range(len(data)):
        actors = str(data[i]).replace('(', '')
        actors = actors.replace(')', '')
        actors = actors.replace("'", '')
        actors = actors.replace("'", '')
        for actor in actors.split(', '):
            n = 1
            if actor[-1] == ',':
                actor = actor.replace(',', '')
            if actor in actors_dict.keys():
                actors_dict[actor] += n
            else:
                actors_dict[actor] = n

    for k, v in actors_dict.items():
        if v >= 2:
            actors_list.append(k)
    return actors_list


def search_picture(type_of_movie, movie_release_year, movie_genre) -> list:
    sqlite_query = (f"""
                        SELECT title, type, country, release_year, listed_in, description
                        FROM netflix
                        WHERE netflix.listed_in LIKE '%{movie_genre}%'
                        AND release_year = {movie_release_year}
                        AND type LIKE '{type_of_movie}'
                        ORDER BY release_year
                        """)
    movie_list = []
    movie_dict = {}
    data = db_connect('netflix.db', sqlite_query)

    for content in data:
        movie_dict["title"] = content[0]
        movie_dict["type"] = content[1]
        movie_dict["country"] = content[2]
        movie_dict["release_year"] = content[3]
        movie_dict["genre"] = content[4]
        movie_dict["description"] = content[5]
        movie_list.append(movie_dict)
        movie_dict = {}
    return movie_list
