import os
from flask import Flask, render_template, redirect, session, request
from supabase import create_client
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = "1234567890"
app.debug = True
socketio = SocketIO(app)

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

@app.route('/')
def index():
    if session.get('email', False):
        messages = supabase.table("messages").select("*").execute()
        return render_template('index.html', email=session["email"], messages=messages.data)
    return redirect("/login")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        session['email'] = email
        return redirect("/")
    return render_template('login.html')

@socketio.on("send_message")
def handle_message(data):
    text = data["text"]
    sender = session["email"]
    supabase.table("messages").insert({"sender": sender, "text": text}).execute()
    emit("new_message", {"sender": sender, "text": text}, broadcast=True)

def handle_change(event, sid):
    socketio.emit('new_message', event.data, room=sid)

if __name__ == '__main__':
    socketio.run(app)
