from flask import Flask  
from flaskwebgui import FlaskUI   # get the FlaskUI class


app = Flask(__name__)
ui = FlaskUI(app, width=800, height=600)                 # feed the parameters


# do your logic as usual in Flask

@app.route("/")
def index():  
    return "It works!"


app.run()                           # call the 'run' method 