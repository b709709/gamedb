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

def get_user(username,password,action):
    print(username)
    print(password)
    print(action)

    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = cur.mogrify(f"select * from users where username = %s",(username,))
    cur.execute(sql)

    #sql = cur.mogrify("select all from users where username = %s and password = %s",(username,password))
    #cur.execute(sql)
    
    rows = cur.fetchall()
    cur.close()
    conn.close()

    #new user attempt to create
    if action == "signup" and len(rows) ==1:
        return False,"User Already Exists, Please try again."
    if action == "signup" and len(rows) == 0 and password == "":
        return False,"Password cannot be blank."
    if action == "signup" and len(rows) == 0 and password != "" and username != "":
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        cur.execute("INSERT INTO users (username,password) VALUES(%s, %s) RETURNING id", (username,password))
        newrow = cur.fetchone()
        new_id = newrow["id"]
        conn.commit()
        conn.close()
        if len(newrow) == 1:
            return True,"New User Created"
        else:
            return False,"Error Creating New User, Please retry."
    
    if len(rows) == 1:
       if rows[0].get("password") == password:
          return True,""
       else: 
          return False,"Invalid Password."
    else:
       return False,"No user found, retry or Signup."

def get_all_games(username,sort,searchvalue,searchconsole):

    print("search value in get_all_games=",searchvalue,searchconsole)

    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #username = session.get('username')
    print("THE USERNAME IN GET_ALL_GAMES IS",username)
    
    sql = ""

    xchoice = 0
    if searchvalue and not searchconsole:
       xchoice = 1
    if not searchvalue and searchconsole:
       xchoice = 2
    if not searchvalue and not searchconsole:
       xchoice = 3
    if searchvalue and searchconsole:
       xchoice = 4

    if xchoice == 1:
        print("SEARCH VALUE PATH IS SELECTED")
        searchvalue = searchvalue.replace("*","%")
        #searchvalue = "%" + searchvalue + "%"
        sql = cur.mogrify(f"SELECT name,console,id from game where username = %s AND name ILIKE %s",(username,searchvalue)) 
    elif xchoice == 4:
        print("SEARCH VALUE AND SEARCHCONSOLE PATH IS SELECTED")
        searchvalue = searchvalue.replace("*","%")
        #searchvalue = "%" + searchvalue + "%"
        searchconsole = searchconsole.replace("*","%")
        #searchconsole = "%" + searchconsole + "%"
        sql = cur.mogrify(f"SELECT name,console,id from game where username = %s AND name ILIKE %s and console ILIKE %s",(username,searchvalue,searchconsole)) 
    elif xchoice == 2:
        print("SEARCHCONSOLE PATH IS SELECTED")    
        searchconsole = searchconsole.replace("*","%")
        #searchconsole = "%" + searchconsole + "%"
        sql = cur.mogrify(f"SELECT name,console,id from game where username = %s AND console ILIKE %s",(username,searchconsole))
    else: #not searchconsole and searchvalue empty refresh xchoice = 3 or 0
        print("STANDARD PATH IS SELECTED")
        sql = cur.mogrify(f"SELECT name,console,id from game where username = %s ORDER BY {sort}",(username,)) 
    
    print(sql)
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
