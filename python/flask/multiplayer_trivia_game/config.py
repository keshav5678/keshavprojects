"configure flask app"

from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aa00dfce3194ecec551ec7fc9dcaf1273eb27c1387b5412d3151c7b4cdee31f8'
socketio = SocketIO(app)

the_rooms = dict()

rooms_template = {
    "numberOfPlayers": 0,
    "players": [],
    "playerPoints": [],
    "category": "",
    "current question": []
}
