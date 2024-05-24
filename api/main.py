"""
The main Flask application for the TextIT project.

This module sets up the Flask application, configures the MongoDB connection, and defines the routes for the index and login pages.

The index route renders the index.html template and passes the current user's email address, if they are logged in.

The login route handles both GET and POST requests. On a GET request, it renders the login.html template. On a POST request, it checks the provided email and password against the users collection in the MongoDB database. If the credentials are valid, it sets the user's email in the session and redirects to the index page.
"""
# flask application

from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# set app secret 
app.secret_key = "1234567890"
#add MONGO_URI
MONGO_URI = "mongodb+srv://mihaiciorobitca:R3dwaLL2013star@cluster.rsenaqq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"
mongo = MongoClient(MONGO_URI) 

@app.route('/')
def index():
    return redirect('login')
    email = session.get('email', None)
    return render_template('index.html', email=email)

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
    
    
