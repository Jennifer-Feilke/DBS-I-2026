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
    raise NotImplementedError



def query_movies(
    connection: psycopg2.extensions.connection, keywords: str
) -> list[Movie]:
    """
    Return all movies whose title contains *keywords* (case-insensitive).

    Sorted by title ASC, then year ASC (NULLs last).
    Each movie's actor_names list is sorted alphabetically.
    """

    raise NotImplementedError


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

    raise NotImplementedError
