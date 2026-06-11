import pytest
from exercise import (
    create_connection,
    query_actors,
    query_movies,
)

from entities import ConnectionConfig, Movie, Actor

# ---------------------------------------------------------------------------
# Movie and Actor fixtures
# ---------------------------------------------------------------------------

ANH_1977 = Movie(
    tconst="tt0076759",
    title="Star Wars: Episode IV - A New Hope",
    year=1977,
    genres={"Action", "Adventure", "Fantasy"},
    actor_names=[
        'Alec Guinness', 'Anthony Daniels', 'Carrie Fisher', 'David Prowse', 'Harrison Ford', 'Kenny Baker',
        'Mark Hamill', 'Peter Cushing', 'Peter Mayhew', 'Phil Brown'
    ]
)

ANNE_HATHAWAY = Actor(nconst="nm0004266", name="Anne Hathaway")
ANNE_HATHAWAY.played_in = [
    "Mothers' Instinct",
    "The Idea of You",
    "She Came to Me",
    "Armageddon Time",
    "Locked Down",
]
ANNE_HATHAWAY.costar_name_to_count = {
    "Hector Elizondo": 3,
    "Helena Bonham Carter": 3,
    "Heather Matarazzo": 2,
    "Jeremy Strong": 2,
    "Jesse Eisenberg": 2,
}


# ---------------------------------------------------------------------------
# Shared connection fixture
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def config() -> ConnectionConfig:
    cfg = ConnectionConfig()
    assert cfg.username, 'provide your database username in ".env"'
    assert cfg.password, 'provide your database password in ".env"'
    return cfg


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_connect_database(config: ConnectionConfig) -> None:
    with create_connection(config) as conn:
        assert not conn.closed, "connection should be open"


class TestMovies:

    def test_query_movies4_a_new_hope(self, config: ConnectionConfig) -> None:
        with create_connection(config) as conn:
            results = query_movies(conn, "A New Hope")
        assert results == [ANH_1977]


class TestActors:

    def test_query_actors1_anne_hathaway(self, config: ConnectionConfig) -> None:
        with create_connection(config) as conn:
            results = query_actors(conn, "Anne Hathaway")
        assert len(results) == 1
        assert results[0] == ANNE_HATHAWAY
