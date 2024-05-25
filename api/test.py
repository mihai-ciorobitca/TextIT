from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()

app = Flask(__name__)

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

@app.route("/")
def index():
    return render_template("test.html", supabase_url=supabase_url, supabase_key=supabase_key)

@app.route("/send_message", methods=["POST"])
def send_message():
    message = request.form.get("message")
    supabase.table("messages").insert({"content": message}).execute()
    return "OK"

if __name__ == "__main__":
    app.run(debug=True)
