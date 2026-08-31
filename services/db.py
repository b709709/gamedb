import psycopg2

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
    cur = conn.cursor()
    cur.execute("SELECT name FROM game;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
