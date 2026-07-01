from contextlib import contextmanager
from typing import Generator

import psycopg2
import psycopg2.extensions

from entities import ConnectionConfig, Actor, Movie


@contextmanager
def create_connection(
    config: ConnectionConfig,
) -> Generator[psycopg2.extensions.connection, None, None]:
    """
    Context manager that opens a psycopg2 connection and closes it on exit.

    Usage:
        with create_connection(config) as conn:
            ...
    """
    conn = psycopg2.connect(
        host=config.host,
        port=config.port,
        dbname=config.database,
        user=config.username,
        password=config.password,
    )
    yield conn



def query_movies(
    connection: psycopg2.extensions.connection, keywords: str
) -> list[Movie]:
    """
    Return all movies whose title contains *keywords* (case-insensitive).

    Sorted by title ASC, then year ASC (NULLs last).
    Each movie's actor_names list is sorted alphabetically.
    """

    keywords='%' + keywords + '%'
    cur = connection.cursor()
    cur.execute(""" SELECT tmovies.tconst, "primaryTitle", "startYear", "genres", ARRAY_AGG(primaryname ORDER BY primaryname) AS actor_names
                FROM tmovies, tprincipals, nbasics
                WHERE "primaryTitle" ILIKE %s
                AND "tmovies"."tconst" = "tprincipals"."tconst"
                AND "tprincipals"."nconst" = "nbasics"."nconst"
                AND category IN ('actor', 'actress')
                GROUP BY "tmovies"."tconst", "primaryTitle", "startYear", "genres"
                ORDER BY "primaryTitle" ASC, "startYear" ASC;""", (keywords,))
    movies=[]
    for el in cur:
        movies.append(Movie(tconst=el[0], title=el[1], year=el[2], genres=set(el[3]), actor_names=el[4]))
    cur.close()
    return movies
            

def query_actors(
    connection: psycopg2.extensions.connection, keywords: str
) -> list[Actor]:
    """
    Return the 5 most relevant actors/actresses whose name contains *keywords*.

    Sorted by total movie count DESC, then name ASC.
    Each actor's played_in list contains up to 5 titles (most recent first,
    NULLs last, then title ASC for ties).
    Each actor's costar_name_to_count dict contains up to 5 costars
    (most shared movies first, then name ASC).
    All limits and ordering are enforced in SQL.
    """

    keywords='%' + keywords + '%'
    cur = connection.cursor()
    cur.execute("""SELECT
                    top5.nconst,
                    top5.primaryname,
                    (SELECT ARRAY (SELECT x."primaryTitle"
                        FROM (SELECT DISTINCT "tm"."primaryTitle", "tm"."startYear"
                            FROM tprincipals tp
                            JOIN tmovies tm ON tm.tconst = tp.tconst
                            WHERE tp.nconst = top5.nconst) x
                        ORDER BY x."startYear" DESC NULLS LAST, x."primaryTitle" ASC
                        LIMIT 5)) AS played_in,
                    (SELECT JSON_OBJECT_AGG("costar_name", "costar_count")
                        FROM (SELECT nb.primaryname AS costar_name, COUNT(DISTINCT tp1.tconst) AS costar_count
                            FROM tprincipals tp1
                            JOIN tprincipals tp2 ON tp1.tconst = tp2.tconst AND tp1.nconst != tp2.nconst
                            JOIN nbasics nb ON nb.nconst = tp2.nconst
                            WHERE tp1.nconst = top5.nconst
                            AND tp1.category IN ('actor', 'actress')
                            AND tp2.category IN ('actor', 'actress')
                            GROUP BY nb.nconst, nb.primaryname
                            ORDER BY costar_count DESC, costar_name ASC
                            LIMIT 5) AS costars) AS costar_name_to_count
                FROM (SELECT nbasics.nconst, primaryname, COUNT(tconst) AS movie_count
                    FROM nbasics, tprincipals
                    WHERE "primaryname" ILIKE %s
                    AND "nbasics"."nconst" = "tprincipals"."nconst"
                    AND category IN ('actor', 'actress')
                    GROUP BY nbasics.nconst, primaryname
                    ORDER BY movie_count DESC, primaryname ASC
                    LIMIT 5) AS top5
                """, (keywords,))
    actors=[]
    for el in cur:
        actors.append(Actor(nconst=el[0], name=el[1], played_in=list(el[2])or[], costar_name_to_count=dict(el[3])or{}))
    cur.close()
    return actors