"configure flask app"

from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev' # please change this if you want to run this yourself.
socketio = SocketIO(app)

the_rooms = dict()

rooms_template = {
    "numberOfPlayers": 0,
    "players": [],
    "playerPoints": [],
    "category": "",
    "current question": []
}
