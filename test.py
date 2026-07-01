import psycopg2

conn = psycopg2.connect(
    dbname="imdb",
    user="jennifer",
    password="passwort",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

cur.execute("SELECT NOW();")

print(cur.fetchone())

cur.close()
conn.close()