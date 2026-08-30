from flask import Flask, render_template, request, jsonify
from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # your login page

@app.route("/dashboard")
def dashboard():
    return render_template("maindashboard.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    print("username posted:",username)
    print("password posted:",password)

    # Example: return JSON
    #return jsonify({
    #    "status": "ok",
    #    "username": username,
    #    "message": "Login received"
    #})
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
