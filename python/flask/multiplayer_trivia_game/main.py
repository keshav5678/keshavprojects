from flask import render_template, request, url_for, redirect, session, jsonify
from flask_socketio import join_room, leave_room, rooms, close_room
from config import app, socketio, the_rooms, rooms_template
import random
import fetcher

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/join', methods=["GET", "POST"])
def join():
    if request.method == "POST":
        room =  request.form.get('room_code')
        name = request.form.get('Name')
        if room in the_rooms and name not in the_rooms.get(room).get("players"):
            session["room"] = room
            session["name"] = name
            the_rooms[room]["players"].append(name)
            the_rooms[room]["numberOfPlayers"] += 1
            the_rooms[room]["playerPoints"].append(0)

            return redirect(url_for('room'))
        else:
            return jsonify({"error": "name already in room or wrong room code"})

    return render_template('join.html')

@app.route('/create', methods=["GET", "POST"])
def create():
    if request.method == "POST":
        room = str(random.randint(100000,999999))
        name = request.form.get('Name', default="all")
        category = request.form.get('Category')
        session["room"] = room
        session["name"] = name
        the_rooms[room] = rooms_template
        the_rooms[room]["players"].append(name)
        the_rooms[room]["numberOfPlayers"] += 1
        the_rooms[room]["playerPoints"].append(0)
        the_rooms[room]["category"] = category
        the_rooms[room]["current question"] = fetcher.getTrivia(category=category)

        return redirect(url_for('room'))

    return render_template('create.html')

@app.route('/room')
def room():
    return render_template('room.html', room_code=session["room"])

@socketio.on('my event')
def my_event():
    join_room(session["room"])
    socketio.emit('question', data={"question": the_rooms[session["room"]]["current question"][0]["question"]}, to=session["room"])
    socketio.emit('join', data=session["name"], to=session["room"])
    socketio.emit('message', data={"user": session["name"], "message": "has joined the room"}, to=session["room"])

@socketio.on('send message')
def send_message(v):
    socketio.emit('message', data={"user": session["name"], "message": v}, to=session["room"])
    if v.lower() in the_rooms[session["room"]]["current question"][0]["answer"].lower() and len(v) > 1:
        socketio.emit('win', data={"name": session["name"]})
        room = session["room"]
        the_rooms[session["room"]]["current question"] = fetcher.getTrivia(the_rooms[room]["category"])
        socketio.emit('question', data={"question": the_rooms[room]["current question"][0]["question"]}, to=session["room"])

if __name__ == "__main__":
    socketio.run(app)