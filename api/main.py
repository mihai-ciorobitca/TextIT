from flask import Flask, render_template, redirect, session, request
from pymongo import MongoClient
from werkzeug.security import check_password_hash
from flask_socketio import SocketIO, emit

app = Flask(__name__)

app.secret_key = "1234567890"
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.debug = True
socketio = SocketIO(app)

MONGO_URI = "mongodb+srv://mihaiciorobitca:R3dwaLL2013star@cluster.rsenaqq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"
mongo = MongoClient(MONGO_URI)

@app.route('/')
def index():
    if session.get('email', False):
        messages = mongo.db.messages.find()
        return render_template('index.html', email=session["email"], messages = messages)
    return redirect("/login")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = mongo.db.users.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            session['email'] = user['email']
            return redirect("/")
    return render_template('login.html')

@socketio.on("send_message")
def handle_message(data):
    text = data["text"]
    sender = session["email"]
    mongo.db.messages.insert_one({"sender": sender, "text": text})
    emit("new_message", {"sender": sender, "text": text}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app)