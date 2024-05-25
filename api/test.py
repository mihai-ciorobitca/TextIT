from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()

app = Flask(__name__)

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SECRET")
supabase: Client = create_client(supabase_url, supabase_key)
email = "mihai@gmail.com"

user = supabase.table('users').select('*').eq('email', email).execute()

print(user)