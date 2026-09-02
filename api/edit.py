from flask import Blueprint, request, session
from services.games import edit_game

api_edit_bp = Blueprint('api_edit',__name__)

@api_edit_bp.route('/api/edit',methods=['POST'])
def api_edit():
    data = request.json
    name = data['name']
    console = data['console']
    gameid = data['gameid']
    username = session["username"]
    print("EDIT FOR USER",username)

    bok = edit_game(name,console,gameid,username)
    print(bok)
    return{"success":True}
    #return{"gameid":gameid, "name":name, "console":console}