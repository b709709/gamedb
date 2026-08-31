import psycopg2.extras

def get_connection():
    return psycopg2.connect(
        dbname="mygames",
        user="postgres",
        password="covert",
        host="127.0.0.1",
        port="5432"
    )

def get_all_games():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT name,console FROM game;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
