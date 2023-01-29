import sqlite3


def get_all_movie(query: str):
    """
    Возвращает список всех фильмов по запросу
    """
    with sqlite3.connect('netflix.db') as connection:
        connection.row_factory = sqlite3.Row
        result = []

        for item in connection.execute(query).fetchall():
            result.append(dict(item))
        return result


def get_movie(query: str):
    """
    Возвращает один фильм по запросу
    """
    with sqlite3.connect('netflix.db') as connection:
        connection.row_factory = sqlite3.Row
        result = connection.execute(query).fetchone()

        if result is None:
            return None
        else:
            return dict(result)


def get_movie_by_filters(type_movie, release_year, listed_in):
    """
    Возвращает список фильмов по 3 фильтрам
    """
    query = f"""
    SELECT title, description
    FROM netflix
    WHERE `type` = '{type_movie}'
    AND release_year = '{release_year}'
    AND listed_in LIKE '%{listed_in}%'
    """

    result = []

    for item in get_all_movie(query):
        result.append(
            {
                'title': item['title'],
                'description': item['description'],
            }
        )
    return result


def search_by_cast(name_one: str = 'Jack Black', name_two: str = 'Dustin Hoffman'):
    """
    Возвращает список актеров, кто играет с ними в паре больше 2 раз
    """
    query = f"""
    SELECT *
    FROM netflix
    WHERE `cast` LIKE '%Jack Black%' AND `cast` LIKE '%Dustin Hoffman%'
    """

    casts = []
    set_casts = set()
    result = get_all_movie(query)

    for item in result:
        for cast in item['cast'].split(','):
            casts.append(cast)

    for cast in casts:
        if cast.count(cast) > 2:
            set_casts.add(cast)

    return list(set_casts)
