import psycopg2.extras
from flask import Flask, redirect, url_for, flash, session

def add_game(name,console,username):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("INSERT INTO game (name,console,username) VALUES(%s, %s, %s) RETURNING id", (name,console,username))
    row = cur.fetchone()
    new_id = row["id"]
    conn.commit()
    return new_id
    
    
def get_connection():
    return psycopg2.connect(
        dbname="mygames",
        user="postgres",
        password="covert",
        host="127.0.0.1",
        port="5432"
    )

def get_user(username,password):
    print(username)
    print(password)
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = cur.mogrify("select all from users where username = %s and password = %s",(username,password))
    print(sql)
    cur.execute(sql)
    
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if len(rows) > 0:
       return True
    else:
       print("No user record found.")
       return False

def get_all_games(username):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #username = session.get('username')
    print("THE USERNAME IN GET_ALL_GAMES IS",username)
    sql = cur.mogrify("SELECT name,console from game where username = %s",(username,))
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
