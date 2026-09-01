from .db import get_connection
import psycopg2.extras

def edit_game(name,console,gameid):
    print(name,console,gameid)
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    sql = f"UPDATE game set name='{name}', console='{console}' WHERE id = {gameid}"
    
    cur.execute(sql)
    
    print("ROWS RETURNED AFTER UPDATE",cur.rowcount)
    conn.commit()
    cur.close()
    conn.close()
    return True

def add_game(name,console,username):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("INSERT INTO game (name,console,username) VALUES(%s, %s, %s) RETURNING id", (name,console,username))
    row = cur.fetchone()
    new_id = row["id"]
    conn.commit()
    cur.close()
    conn.close()
    return new_id

def delete_game(gameid):
    print("DELETE GAME ID:",gameid)
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = f"DELETE FROM game WHERE id ={gameid}"
    print("DELETE STRING:",sql)

    try: 
      print("try to delete")
      cur.execute(f"DELETE FROM game WHERE id = {gameid} ")
      print(cur.rowcount)
      if cur.rowcount == 0:
         return False, "No Record found to delete, please refresh and try again."
      else:
         conn.commit()
         print("Record deleted")
         return True, ""
    except:
      print("Error")
      return False,"Error During the Delete"
    finally:
      cur.close()
      conn.close()
      print("finally block ended.")
    