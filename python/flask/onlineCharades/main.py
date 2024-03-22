from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit, rooms
import random, string
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
socketio = SocketIO(app)
cors = CORS(app)
rooms = dict()


def genRoomCode():
    code = ""
    for _ in range(10):
        code += random.choice(string.ascii_uppercase)
    return code

@app.route("/")
@cross_origin()
def lobby():
    return render_template("lobby.html")

@app.route("/room")
@cross_origin()
def room():
    if 'mode' in session:
        if session["mode"] == "creator":
            return render_template('wordGiver.html')
        else:
            return render_template('guesser.html')
    else:
        return render_template('guesser.html')

@app.route("/create", methods=["POST"])
@cross_origin()
def create():
    session["mode"] = "creator"
    session["name"] = request.form.get("Name")
    session["room"] = genRoomCode()
    rooms[session["room"]] = dict()
    return redirect(url_for('room'))

@app.route("/join", methods=["POST"])
@cross_origin()
def join():
    session["mode"] = "player"
    session["name"] = request.form.get("Name")
    session["room"] = request.form.get("roomCode")
    return redirect(url_for('room'))

@socketio.on('my event')
@cross_origin()
def join_to_room(data):
    join_room(session["room"])
    socketio.emit('message', data={"user": session["name"], "message": "joined the room"}, to=session["room"])

@socketio.on('sendMessage')
@cross_origin()
def sendMessage(guess):
    if session["mode"] == "player":
        if guess == rooms[session["room"]]["word"]:
            socketio.emit('winner', data={"user": session["name"]})
        
        socketio.emit('message', data={"user": session["name"], "message": guess}, to=session["room"])

@socketio.on('sendClue')
@cross_origin()
def sendClue(clue):
    if session["mode"] == "creator":
        socketio.emit("clue", data=clue)

@socketio.on("sendWord")
@cross_origin()
def send_word(word):
    if session["mode"] == "creator":
        rooms[session["room"]]["word"] = word

@socketio.on("disconnect")
@cross_origin()
def handle_disconnection():
    leave_room(session["room"])
    session.pop("name")
    session.pop("room")

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
