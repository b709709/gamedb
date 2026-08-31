from .db import get_connection
import psycopg2.extras

def add_game(name,console,username):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("INSERT INTO game (name,console,username) VALUES(%s, %s, %s) RETURNING id", (name,console,username))
    row = cur.fetchone()
    new_id = row["id"]
    conn.commit()
    return new_id