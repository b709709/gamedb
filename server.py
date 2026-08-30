from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # your login page

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Example: return JSON
    return jsonify({
        "status": "ok",
        "username": username,
        "message": "Login received"
    })

if __name__ == "__main__":
    app.run(debug=True)
