from os import environ
from flask import Flask, render_template, redirect, session, request
from supabase import create_client
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)
app.secret_key = "1234567890"

url = environ.get("SUPABASE_URL")
key = environ.get("SUPABASE_SECRET")
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
        user = supabase.table('users').select('*').eq('email', email).execute()
        if user.data != []:
            if check_password_hash(user.data[0]["password"], password):
                session['email'] = email
                return redirect("/")
    return render_template('login.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    text = request.form.get("message")
    sender = session.get('email')
    supabase.table('messages').insert({'sender': sender, 'text': text}).execute()
    return {'success': True}

if __name__ == '__main__':
    app.run()
