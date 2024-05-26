from os import environ
from flask import Flask, render_template, redirect, session, request
from supabase import create_client
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)
app.secret_key = "1234567890"

supabase_url = environ.get("SUPABASE_URL")
supabase_anon_key = environ.get("SUPABASE_ANON_KEY")
supabase_secret = environ.get("SUPABASE_SECRET")

supabaseUser = create_client(supabase_url, supabase_anon_key)
supabaseAdmin = create_client(supabase_url, supabase_secret)

@app.route('/')
def index():
    if session.get('email', False):
        return render_template(
            'index.html', email=session["email"],
            supabase_url=supabase_url,
            supabase_anon_key=supabase_anon_key
        )
    return redirect("/login")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = supabaseAdmin.table('users').select('*').eq('email', email).execute()
        if user.data != []:
            if check_password_hash(user.data[0]["password"], password):
                session['email'] = email
                return redirect("/")
    return render_template('login.html')

if __name__ == '__main__':
    app.run()
