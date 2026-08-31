from flask import Flask, render_template, request, jsonify
from flask import Flask, redirect, url_for, flash, session
from services.auth import process_login
from services.db import get_all_games, get_user
from api.add import api_add_bp

app = Flask(__name__)
app.secret_key = "709709ab"

app.register_blueprint(api_add_bp)

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
    
@app.route("/dashboard")
def dashboard():

    if 'username' not in session:
        return redirect('/login')
    
    if not session.get("logged_in"):
        flash("You must be logged in first","error")
        return redirect(url_for("index"))

    print ("get games for",session.get("username"))

    games = get_all_games(session["username"])
    print("row count",len(games))

    flash("Welcome:" + session.get("username"),"success")
    return render_template("maindashboard.html",games=games)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/?loggedout=1") #go back to the login screen do not use login that process the login
    

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    #ok = process_login(username,password)
    ok = get_user(username,password)
    

    if ok:
        session["logged_in"] = True
        session["username"] = username
        return redirect(url_for("dashboard"))
    else:
        flash("login failed. Please try again.","error")
        flash("unknown user","error")
        return redirect(url_for("index"))
    
        # Example: return JSON
    #return jsonify({
    #    "status": "ok",
    #    "username": username,
    #    "message": "Login received"
    #})
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
