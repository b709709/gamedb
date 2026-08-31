from flask import Blueprint, request, session
#from services import db
from services.games import add_game

api_add_bp = Blueprint('api_add',__name__)

@api_add_bp.route('/api/add',methods=['POST'])
def api_add():
    data = request.json
    name = data['name']
    console = data['console']
    username = session['username']

    new_id = add_game(name,console,username)

    return{"id":new_id, "name":name, "console":console}
