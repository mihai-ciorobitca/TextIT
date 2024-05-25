import os
from flask import Flask, render_template, redirect, session, request
from supabase import create_client
from dotenv import load_dotenv
# from flask_bcrypt import Bcrypt

load_dotenv()

app = Flask(__name__)
app.secret_key = "1234567890"
app.debug = True

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
        user = supabase.from_('users').select('*').eq('email', email).eq('password', password).execute()
        if user:
            session['email'] = email
            return redirect("/")
    return render_template('login.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    sender = session.get('email')
    text = data.get('text')

    supabase.table('messages').insert({'sender': sender, 'text': text}).execute()
    return {'success': True}

if __name__ == '__main__':
    app.run()
