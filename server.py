from flask import Flask, render_template, request, jsonify
from flask import Flask, redirect, url_for, flash, session
from services.auth import process_login
from services.db import get_all_games, get_user
from api.add import api_add_bp
from api.edit import api_edit_bp
from services.games import delete_game

app = Flask(__name__)
app.secret_key = "709709ab"


app.register_blueprint(api_add_bp)
app.register_blueprint(api_edit_bp)


@app.before_request
def require_login():
    print("Client Request endpoint",request.endpoint)
    if request.endpoint and request.endpoint.startswith("static"):
        return
    
    allowed_routes = ["index","login", "static"]
    if "logged_in" not in session:
        if request.endpoint not in allowed_routes:
            return redirect(url_for("index"))


@app.route("/")
def index():
    return render_template("index.html")  # your login page

@app.route("/delete/<int:game_id>")    
def deleteGame(game_id):
    isok,errorMsg = delete_game(game_id)
    if not isok:
       print(errorMsg)

    if isok == True:
        return redirect("/dashboard")
    else:
        return redirect("/dashboard")




@app.route("/dashboard")
def dashboard():

    searchValue = request.args.get("searchInput","").strip()
    searchConsole = request.args.get("searchConsoleInput","").strip()

    print("search value",searchValue,searchConsole)

    if 'username' not in session:
        return redirect('/login')
    
    if not session.get("logged_in"):
        flash("You must be logged in first","error")
        return redirect(url_for("index"))

    print ("get games for",session.get("username"))

    sort = request.args.get("sort","name")
    games = get_all_games(session["username"],sort,searchValue,searchConsole)
    print("row count",len(games))

    flash("ID:" + session.get("username"),"success")
    return render_template("maindashboard.html",games=games)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/?loggedout=1") #go back to the login screen do not use login that process the login
    

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    action = request.form.get("action")
    print("login action",action)

    returnmessage = ""

    #ok = process_login(username,password)
    ok,returnmessage = get_user(username,password,action)
    

    if ok:
        session["logged_in"] = True
        session["username"] = username
        return redirect(url_for("dashboard"))
    else:
        flash("login failed. Please try again.","error")
        flash(returnmessage,"error")
        return redirect(url_for("index"))
    
        # Example: return JSON
    #return jsonify({
    #    "status": "ok",
    #    "username": username,
    #    "message": "Login received"
    #})
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
    #192.168.2.44