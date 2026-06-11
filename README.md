## Setup

This is the exercise repository for the Database Systems I course in the IT Systems Engineering Bachelor's program at Hasso Plattner Institute Potsdam.
The exercise covers how to programmatically connect to a DBMS and query data.
We use Python for ease of development — specifically [psycopg2](https://www.psycopg.org/docs/) to connect to a PostgreSQL database.

To set up the Python environment, run:

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you haven't created the database yet and want to use Docker, download `IMDB.pgdbdump` first, then run:

```
docker compose up -d
docker exec -i dbs1_imdb pg_restore --username=postgres --dbname=imdb < "path/to/IMDB.pgdbdump"
```


## Working on Your Implementation

There are 3 tasks, each building on the last:

1. Create a connection to the database
2. Query movies matching a keyword
3. Query actors matching a keyword

Tasks 2 and 3 require entity objects to hold the relational query results.
The querying approach is up to you — just ensure each method returns a list of the required objects.

Implement all functions in [jdbc_exercise.py](jdbc_exercise.py).

For an example of how to create a context manager in Python, see [context_tutorial.py](context_tutorial.py).
You'll need this for `create_connection` to ensure the connection is closed automatically after use.


## Testing Your Implementation

Unit tests are provided for the basic functionality of each method. Feel free to add your own.
Submissions will be evaluated against a larger test set with different input data, so make sure your implementation is correct!

JetBrains IDEs detect tests automatically — click the green arrow next to a test to run it, or use `ctrl + r` to run all tests or `ctrl + shift + r` to run a single test.

You can also run tests from the terminal with:

```
pytest
```

To step through your implementation interactively, use the debugger in your IDE. In JetBrains products, click the debug button next to any test.
